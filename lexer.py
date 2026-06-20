RESERVED_WORDS = {
    'RESULTADO', 'VS', 'TEMPORADA', 'JORNADA', 'GOLES',
    'LOCAL', 'VISITANTE', 'TOTAL', 'TABLA', 'PARTIDOS',
    'TOP', 'SUPERIOR', 'INFERIOR', 'ADIOS'
}


class TokenType:
    RESULTADO    = "RESULTADO"
    VS           = "VS"
    TEMPORADA    = "TEMPORADA"
    JORNADA      = "JORNADA"
    GOLES        = "GOLES"
    LOCAL        = "LOCAL"
    VISITANTE    = "VISITANTE"
    TOTAL        = "TOTAL"
    TABLA        = "TABLA"
    PARTIDOS     = "PARTIDOS"
    TOP          = "TOP"
    SUPERIOR     = "SUPERIOR"
    INFERIOR     = "INFERIOR"
    ADIOS        = "ADIOS"
    BANDERA_F    = "BANDERA_F"
    BANDERA_N    = "BANDERA_N"
    BANDERA_JI   = "BANDERA_JI"
    BANDERA_JF   = "BANDERA_JF"
    CADENA       = "CADENA"
    TEMPORADA_VAL = "TEMPORADA_VAL"
    NUMERO       = "NUMERO"
    MENOR        = "MENOR"
    MAYOR        = "MAYOR"


class Token:
    def __init__(self, lexema, token_type, fila, columna):
        self.lexema = lexema
        self.token_type = token_type
        self.fila = fila
        self.columna = columna

    def __repr__(self):
        return f"Token({self.lexema!r}, {self.token_type}, f={self.fila}, c={self.columna})"


class LexicalError:
    def __init__(self, lexema, descripcion, fila, columna):
        self.lexema = lexema
        self.descripcion = descripcion
        self.fila = fila
        self.columna = columna


class Lexer:
    """
    Analizador léxico manual para el lenguaje de comandos LigaBot.
    Lee caracter por caracter y reconoce los tokens definidos.
    """

    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.fila = 1
        self.columna = 1
        self.tokens = []
        self.errors = []


    # Helpers de lectura  


    def _char(self):
        """Retorna el carácter actual sin avanzar, o None si llegó al final."""
        return self.text[self.pos] if self.pos < len(self.text) else None

    def _advance(self):
        """Consume el carácter actual y actualiza fila/columna."""
        ch = self.text[self.pos]
        self.pos += 1
        if ch == '\n':
            self.fila += 1
            self.columna = 1
        else:
            self.columna += 1
        return ch


    # Punto de entrada   


    def analyze(self):
        """
        Ejecuta el análisis léxico sobre el texto completo.
        Retorna (lista_tokens, lista_errores).
        """
        while self.pos < len(self.text):
            ch = self._char()

            if ch in ' \t\r\n':
                self._advance()

            elif ch == '"':
                self._lex_string()

            elif ch == '<':
                r, c = self.fila, self.columna
                self._advance()
                self.tokens.append(Token('<', TokenType.MENOR, r, c))

            elif ch == '>':
                r, c = self.fila, self.columna
                self._advance()
                self.tokens.append(Token('>', TokenType.MAYOR, r, c))

            elif ch == '-':
                self._lex_flag()

            elif ch.isdigit():
                self._lex_number_or_season()

            elif ch.isalpha():
                self._lex_word()

            else:
                r, c = self.fila, self.columna
                self.errors.append(LexicalError(
                    ch,
                    f"Carácter no reconocido: '{ch}'",
                    r, c
                ))
                self._advance()

        return self.tokens, self.errors

    # Reconocedores individuales    

    def _lex_string(self):
        """Estado: dentro de una cadena entre comillas dobles."""
        r, c = self.fila, self.columna
        self._advance()   
        content = ''

        while self.pos < len(self.text):
            ch = self._char()
            if ch == '"':
                self._advance() 
                self.tokens.append(Token(f'"{content}"', TokenType.CADENA, r, c))
                return
            if ch == '\n':
                break
            content += self._advance()

        self.errors.append(LexicalError(
            f'"{content}',
            f"Cadena no cerrada: '\"{content}'",
            r, c
        ))

    def _lex_flag(self):
        """Estado: después de leer '-', intenta reconocer una bandera."""
        r, c = self.fila, self.columna
        self._advance()    
        ch = self._char()

        if ch is None:
            self.errors.append(LexicalError('-', "Bandera incompleta al final del texto", r, c))
            return

        if ch in ('f', 'F'):
            self._advance()
            self.tokens.append(Token('-f', TokenType.BANDERA_F, r, c))

        elif ch in ('n', 'N'):
            self._advance()
            self.tokens.append(Token('-n', TokenType.BANDERA_N, r, c))

        elif ch in ('j', 'J'):
            self._advance()
            ch2 = self._char()
            if ch2 in ('i', 'I'):
                self._advance()
                self.tokens.append(Token('-ji', TokenType.BANDERA_JI, r, c))
            elif ch2 in ('f', 'F'):
                self._advance()
                self.tokens.append(Token('-jf', TokenType.BANDERA_JF, r, c))
            else:
                bad = f'-j{ch2 or ""}'
                self.errors.append(LexicalError(
                    bad,
                    f"Bandera no reconocida: '{bad}'",
                    r, c
                ))
                if ch2:
                    self._advance()

        else:
            bad = f'-{ch}'
            self.errors.append(LexicalError(
                bad,
                f"Bandera no reconocida: '{bad}'",
                r, c
            ))
            self._advance()

    def _lex_number_or_season(self):
        """
        Estado: primer carácter es dígito.
        Reconoce NUMERO (1-2 dígitos) o TEMPORADA_VAL (AAAA-AAAA).
        """
        r, c = self.fila, self.columna
        digits = ''
        while self._char() is not None and self._char().isdigit():
            digits += self._advance()

        if len(digits) == 4 and self._char() == '-':
            save_pos  = self.pos
            save_fila = self.fila
            save_col  = self.columna
            self._advance()   
            digits2 = ''
            while self._char() is not None and self._char().isdigit():
                digits2 += self._advance()

            if len(digits2) == 4:
                self.tokens.append(Token(f'{digits}-{digits2}', TokenType.TEMPORADA_VAL, r, c))
                return
            else:
                self.pos     = save_pos
                self.fila    = save_fila
                self.columna = save_col
                self.errors.append(LexicalError(
                    digits,
                    f"Se esperaba temporada AAAA-AAAA pero se encontró '{digits}' seguido de '-' sin 4 dígitos",
                    r, c
                ))
                return

        if len(digits) in (1, 2):
            self.tokens.append(Token(digits, TokenType.NUMERO, r, c))
        else:
            self.errors.append(LexicalError(
                digits,
                f"Número inválido '{digits}': se esperan 1-2 dígitos o el formato AAAA-AAAA",
                r, c
            ))

    def _lex_word(self):
        """Estado: primer carácter es letra. Reconoce palabras reservadas."""
        r, c = self.fila, self.columna
        word = ''
        while self._char() is not None and self._char().isalpha():
            word += self._advance()

        upper = word.upper()
        if upper in RESERVED_WORDS:
            self.tokens.append(Token(word, upper, r, c))
        else:
            self.errors.append(LexicalError(
                word,
                f"Palabra no reconocida: '{word}' (¿olvidó comillas o hay un error de escritura?)",
                r, c
            ))
