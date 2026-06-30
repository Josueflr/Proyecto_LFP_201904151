
class ParseError(Exception):
    """
    Se lanza cuando la secuencia de tokens no cumple la gramática.

    Atributos:
        received  - Token que se encontró (None si es EOF).
        expected  - Descripción de lo que se esperaba.
        fila      - Fila del error.
        col       - Columna del error.
    """
    def __init__(self, received, expected, fila=0, col=0):
        self.received = received
        self.expected = expected
        self.fila     = fila
        self.col      = col
        tok_str = (f"'{received.lexema}' ({received.token_type})"
                   if received else 'EOF')
        super().__init__(
            f"Error sintáctico [fila {fila}, col {col}]: "
            f"se recibió {tok_str}, se esperaba {expected}"
        )


class Parser:
    """
    Analizador sintáctico de descenso recursivo para LigaBot.

    Uso:
        ast = Parser(tokens).parse()

    Retorna un diccionario con la clave 'cmd' y los parámetros del comando.
    Lanza ParseError si la secuencia de tokens es inválida.
    """

    def __init__(self, tokens):
        self.tokens = tokens
        self.pos    = 0

    # -- Primitivas --------

    def _current(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def _consume(self, *expected_types):
        """Consume el token actual si coincide con alguno de los tipos esperados."""
        tok = self._current()
        if tok is None:
            raise ParseError(None, ' | '.join(expected_types), 0, 0)
        if tok.token_type not in expected_types:
            raise ParseError(tok, ' | '.join(expected_types),
                             tok.fila, tok.columna)
        self.pos += 1
        return tok

    def _match(self, *types):
        """True si el token actual es uno de los tipos dados (sin consumirlo)."""
        tok = self._current()
        return tok is not None and tok.token_type in types

    def _expect_end(self):
        """Verifica que no queden tokens sin consumir."""
        tok = self._current()
        if tok is not None:
            raise ParseError(tok, 'fin de comando',
                             tok.fila, tok.columna)

    # -- Sub-reglas comunes ---------

    def _parse_temporada_val(self):
        """Produce: MENOR TEMPORADA_VAL MAYOR  ->  devuelve la cadena 'AAAA-AAAA'."""
        self._consume('MENOR')
        tv = self._consume('TEMPORADA_VAL')
        self._consume('MAYOR')
        return tv.lexema

    def _parse_cadena(self):
        """Consume un token CADENA y devuelve el texto sin comillas."""
        tok = self._consume('CADENA')
        return tok.lexema[1:-1]   # strip " "

    def _parse_flags(self, allowed=('BANDERA_F', 'BANDERA_JI', 'BANDERA_JF', 'BANDERA_N')):
        """
        Consume flags opcionales en cualquier orden.
        Retorna dict con claves 'nombre', 'ji', 'jf', 'n' según corresponda.
        """
        flags = {'nombre': None, 'ji': None, 'jf': None, 'n': None}
        seen  = set()
        while self._match(*allowed):
            tt = self._current().token_type
            if tt in seen:
                break             # flag duplicada -> la tratará _expect_end
            seen.add(tt)
            self._consume(tt)
            if tt == 'BANDERA_F':
                flags['nombre'] = self._parse_cadena()
            elif tt == 'BANDERA_N':
                flags['n'] = int(self._consume('NUMERO').lexema)
            elif tt == 'BANDERA_JI':
                flags['ji'] = int(self._consume('NUMERO').lexema)
            elif tt == 'BANDERA_JF':
                flags['jf'] = int(self._consume('NUMERO').lexema)
        return flags

    # -- Producciones de comandos --------

    def _parse_resultado(self):
        self._consume('RESULTADO')
        local     = self._parse_cadena()
        self._consume('VS')
        visitante = self._parse_cadena()
        self._consume('TEMPORADA')
        temporada = self._parse_temporada_val()
        self._expect_end()
        return {'cmd': 'RESULTADO', 'local': local,
                'visitante': visitante, 'temporada': temporada}

    def _parse_jornada(self):
        self._consume('JORNADA')
        num       = int(self._consume('NUMERO').lexema)
        self._consume('TEMPORADA')
        temporada = self._parse_temporada_val()
        flags     = self._parse_flags(('BANDERA_F',))
        self._expect_end()
        return {'cmd': 'JORNADA', 'jornada': num,
                'temporada': temporada, 'nombre': flags['nombre']}

    def _parse_goles(self):
        self._consume('GOLES')
        tipo_tok  = self._consume('LOCAL', 'VISITANTE', 'TOTAL')
        equipo    = self._parse_cadena()
        self._consume('TEMPORADA')
        temporada = self._parse_temporada_val()
        self._expect_end()
        return {'cmd': 'GOLES', 'tipo': tipo_tok.token_type,
                'equipo': equipo, 'temporada': temporada}

    def _parse_tabla(self):
        self._consume('TABLA')
        self._consume('TEMPORADA')
        temporada = self._parse_temporada_val()
        flags     = self._parse_flags(('BANDERA_F',))
        self._expect_end()
        return {'cmd': 'TABLA', 'temporada': temporada,
                'nombre': flags['nombre']}

    def _parse_partidos(self):
        self._consume('PARTIDOS')
        equipo    = self._parse_cadena()
        self._consume('TEMPORADA')
        temporada = self._parse_temporada_val()
        flags     = self._parse_flags(('BANDERA_F', 'BANDERA_JI', 'BANDERA_JF'))
        self._expect_end()
        return {'cmd': 'PARTIDOS', 'equipo': equipo, 'temporada': temporada,
                'nombre': flags['nombre'], 'ji': flags['ji'], 'jf': flags['jf']}

    def _parse_top(self):
        self._consume('TOP')
        tipo_tok  = self._consume('SUPERIOR', 'INFERIOR')
        self._consume('TEMPORADA')
        temporada = self._parse_temporada_val()
        flags     = self._parse_flags(('BANDERA_N',))
        self._expect_end()
        return {'cmd': 'TOP', 'tipo': tipo_tok.token_type,
                'temporada': temporada, 'n': flags['n'] or 5}

    def _parse_adios(self):
        self._consume('ADIOS')
        self._expect_end()
        return {'cmd': 'ADIOS'}

    # -- Punto de entrada --------

    def parse(self):
        """
        Analiza la lista de tokens y retorna el AST como diccionario.
        Lanza ParseError ante cualquier error sintáctico.
        """
        if not self.tokens:
            raise ParseError(None,
                             'RESULTADO | JORNADA | GOLES | TABLA | PARTIDOS | TOP | ADIOS',
                             1, 1)

        tok = self._current()
        dispatch = {
            'RESULTADO': self._parse_resultado,
            'JORNADA':   self._parse_jornada,
            'GOLES':     self._parse_goles,
            'TABLA':     self._parse_tabla,
            'PARTIDOS':  self._parse_partidos,
            'TOP':       self._parse_top,
            'ADIOS':     self._parse_adios,
        }
        fn = dispatch.get(tok.token_type)
        if fn is None:
            raise ParseError(tok,
                             'RESULTADO | JORNADA | GOLES | TABLA | PARTIDOS | TOP | ADIOS',
                             tok.fila, tok.columna)
        return fn()
