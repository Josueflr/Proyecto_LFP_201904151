
RESERVED_WORDS = {
    'RESULTADO', 'VS', 'TEMPORADA', 'JORNADA', 'GOLES',
    'LOCAL', 'VISITANTE', 'TOTAL', 'TABLA', 'PARTIDOS',
    'TOP', 'SUPERIOR', 'INFERIOR', 'ADIOS'
}


Q0  = 0
Q1  = 1
Q2  = 2
Q3  = 3
Q4  = 4
Q5  = 5
Q6  = 6
Q7  = 7
Q8  = 8
Q9  = 9
Q10 = 10
Q11 = 11
Q12 = 12
Q13 = 13
Q14 = 14
Q15 = 15
Q16 = 16
Q17 = 17
Q18 = 18
Q19 = 19
Q20 = 20
Q21 = 21


class TokenType:
    RESULTADO     = "RESULTADO"
    VS            = "VS"
    TEMPORADA     = "TEMPORADA"
    JORNADA       = "JORNADA"
    GOLES         = "GOLES"
    LOCAL         = "LOCAL"
    VISITANTE     = "VISITANTE"
    TOTAL         = "TOTAL"
    TABLA         = "TABLA"
    PARTIDOS      = "PARTIDOS"
    TOP           = "TOP"
    SUPERIOR      = "SUPERIOR"
    INFERIOR      = "INFERIOR"
    ADIOS         = "ADIOS"
    BANDERA_F     = "BANDERA_F"
    BANDERA_N     = "BANDERA_N"
    BANDERA_JI    = "BANDERA_JI"
    BANDERA_JF    = "BANDERA_JF"
    CADENA        = "CADENA"
    TEMPORADA_VAL = "TEMPORADA_VAL"
    NUMERO        = "NUMERO"
    MENOR         = "MENOR"
    MAYOR         = "MAYOR"


class Token:
    def __init__(self, lexema, token_type, fila, columna):
        self.lexema     = lexema
        self.token_type = token_type
        self.fila       = fila
        self.columna    = columna

    def __repr__(self):
        return (f"Token({self.lexema!r}, {self.token_type}, "
                f"f={self.fila}, c={self.columna})")


class LexicalError:
    def __init__(self, lexema, descripcion, fila, columna):
        self.lexema      = lexema
        self.descripcion = descripcion
        self.fila        = fila
        self.columna     = columna


class Lexer:
    """
    Analizador léxico LigaBot - AFD de 22 estados (q0-q21).

    La función de transición es explícita: para cada estado se evalúan
    las posibles clases del carácter actual y se avanza al estado siguiente.
    No se utilizan expresiones regulares ni bibliotecas de apoyo.
    """

    def __init__(self, text: str):
        self.text    = text
        self.pos     = 0
        self.fila    = 1
        self.columna = 1
        self.tokens  = []
        self.errors  = []

    # -- Primitivas de acceso al flujo de entrada -----
    def _char(self):
        """Retorna el carácter actual sin avanzar; None si se llegó al EOF."""
        return self.text[self.pos] if self.pos < len(self.text) else None

    def _advance(self):
        """Consume el carácter actual, actualiza fila/columna y lo retorna."""
        ch = self.text[self.pos]
        self.pos += 1
        if ch == '\n':
            self.fila   += 1
            self.columna = 1
        else:
            self.columna += 1
        return ch

    # -- Emisores de token y error ---------

    def _emit(self, lexema, tok_type, fila, col):
        self.tokens.append(Token(lexema, tok_type, fila, col))

    def _emit_error(self, lexema, desc, fila, col):
        self.errors.append(LexicalError(lexema, desc, fila, col))

    # -- Ciclo principal del AFD -----

    def analyze(self):
        """
        Recorre el texto carácter a carácter siguiendo las transiciones del AFD.
        Retorna (lista[Token], lista[LexicalError]).
        """
        state  = Q0   # estado actual
        lexeme = ''   # lexema en construcción
        t_row  = 1    # fila de inicio del lexema actual
        t_col  = 1    # columna de inicio del lexema actual

        while True:
            ch = self._char()   # None == EOF
            if state == Q0:
                if ch is None:
                    break      

                t_row, t_col = self.fila, self.columna
                lexeme = ''

                if ch in ' \t\r\n':
                    self._advance()      

                elif ch == '"':
                    lexeme = self._advance()
                    state  = Q11        

                elif ch == '<':
                    lexeme = self._advance()
                    state  = Q19        

                elif ch == '>':
                    lexeme = self._advance()
                    state  = Q20       

                elif ch == '-':
                    lexeme = self._advance()
                    state  = Q13       

                elif ch.isdigit():
                    lexeme = self._advance()
                    state  = Q2       

                elif ch.isalpha():
                    lexeme = self._advance()
                    state  = Q1       

                else:
                    self._emit_error(
                        ch,
                        f"Carácter no reconocido: '{ch}'",
                        t_row, t_col
                    )
                    self._advance()

            elif state == Q1:
                if ch is not None and ch.isalpha():
                    lexeme += self._advance()           # seguir acumulando -> q1
                else:
                    # Fin natural de la palabra (sin consumir el delimitador)
                    upper = lexeme.upper()
                    if upper in RESERVED_WORDS:
                        self._emit(lexeme, upper, t_row, t_col)
                    else:
                        self._emit_error(
                            lexeme,
                            f"Palabra no reconocida: '{lexeme}'",
                            t_row, t_col
                        )
                    state = Q0
            elif state == Q2:
                if ch is not None and ch.isdigit():
                    lexeme += self._advance()
                    state   = Q3
                else:
                    self._emit(lexeme, TokenType.NUMERO, t_row, t_col)
                    state = Q0
            elif state == Q3:
                if ch is not None and ch.isdigit():
                    lexeme += self._advance()
                    state   = Q4
                else:
                    self._emit(lexeme, TokenType.NUMERO, t_row, t_col)
                    state = Q0
            elif state == Q4:
                if ch is not None and ch.isdigit():
                    lexeme += self._advance()
                    state   = Q5
                else:
                    self._emit_error(
                        lexeme,
                        f"Número inválido '{lexeme}': se esperan 1-2 dígitos "
                        "o el formato AAAA-AAAA",
                        t_row, t_col
                    )
                    state = Q0
            elif state == Q5:
                if ch == '-':
                    lexeme += self._advance()
                    state   = Q6
                elif ch is not None and ch.isdigit():
                    lexeme += self._advance()
                    state   = Q21                       # desbordamiento
                else:
                    self._emit_error(
                        lexeme,
                        f"Número inválido '{lexeme}': se esperan 1-2 dígitos "
                        "o el formato AAAA-AAAA",
                        t_row, t_col
                    )
                    state = Q0
            elif state == Q6:
                if ch is not None and ch.isdigit():
                    lexeme += self._advance()
                    state   = Q7
                else:
                    self._emit_error(
                        lexeme,
                        f"Temporada inválida '{lexeme}': "
                        "se esperan 4 dígitos después del guion",
                        t_row, t_col
                    )
                    state = Q0
            elif state == Q7:
                if ch is not None and ch.isdigit():
                    lexeme += self._advance()
                    state   = Q8
                else:
                    self._emit_error(
                        lexeme,
                        f"Temporada inválida '{lexeme}': faltan 3 dígitos",
                        t_row, t_col
                    )
                    state = Q0
            elif state == Q8:
                if ch is not None and ch.isdigit():
                    lexeme += self._advance()
                    state   = Q9
                else:
                    self._emit_error(
                        lexeme,
                        f"Temporada inválida '{lexeme}': faltan 2 dígitos",
                        t_row, t_col
                    )
                    state = Q0
            elif state == Q9:
                if ch is not None and ch.isdigit():
                    lexeme += self._advance()
                    state   = Q10         
                else:
                    self._emit_error(
                        lexeme,
                        f"Temporada inválida '{lexeme}': falta 1 dígito",
                        t_row, t_col
                    )
                    state = Q0
            elif state == Q10:
                self._emit(lexeme, TokenType.TEMPORADA_VAL, t_row, t_col)
                state = Q0
            elif state == Q11:
                if ch is None or ch == '\n':
                    self._emit_error(
                        lexeme,
                        f"Cadena no cerrada: {lexeme!r}",
                        t_row, t_col
                    )
                    state = Q0      
                elif ch == '"':
                    lexeme += self._advance()
                    state   = Q12      
                else:
                    lexeme += self._advance()     
            elif state == Q12:
                self._emit(lexeme, TokenType.CADENA, t_row, t_col)
                state = Q0
            elif state == Q13:
                if ch in ('f', 'F'):
                    lexeme += self._advance()
                    state   = Q14
                elif ch in ('n', 'N'):
                    lexeme += self._advance()
                    state   = Q15
                elif ch in ('j', 'J'):
                    lexeme += self._advance()
                    state   = Q16
                elif ch is not None:
                    lexeme += self._advance()
                    self._emit_error(
                        lexeme,
                        f"Bandera no reconocida: '{lexeme}' "
                        "(se esperaba -f, -n, -ji o -jf)",
                        t_row, t_col
                    )
                    state = Q0
                else:    
                    self._emit_error(
                        lexeme,
                        f"Bandera incompleta al final del texto: '{lexeme}'",
                        t_row, t_col
                    )
                    state = Q0
            elif state == Q14:
                self._emit(lexeme, TokenType.BANDERA_F, t_row, t_col)
                state = Q0
            elif state == Q15:
                self._emit(lexeme, TokenType.BANDERA_N, t_row, t_col)
                state = Q0
            elif state == Q16:
                if ch in ('i', 'I'):
                    lexeme += self._advance()
                    state   = Q17
                elif ch in ('f', 'F'):
                    lexeme += self._advance()
                    state   = Q18
                elif ch is not None:
                    lexeme += self._advance()
                    self._emit_error(
                        lexeme,
                        f"Bandera no reconocida: '{lexeme}' "
                        "(se esperaba -ji o -jf)",
                        t_row, t_col
                    )
                    state = Q0
                else:
                    self._emit_error(
                        lexeme,
                        f"Bandera incompleta al final del texto: '{lexeme}'",
                        t_row, t_col
                    )
                    state = Q0
            elif state == Q17:
                self._emit(lexeme, TokenType.BANDERA_JI, t_row, t_col)
                state = Q0
            elif state == Q18:
                self._emit(lexeme, TokenType.BANDERA_JF, t_row, t_col)
                state = Q0
            elif state == Q19:
                self._emit(lexeme, TokenType.MENOR, t_row, t_col)
                state = Q0
            elif state == Q20:
                self._emit(lexeme, TokenType.MAYOR, t_row, t_col)
                state = Q0
            elif state == Q21:
                if ch is not None and ch.isdigit():
                    lexeme += self._advance()           # consumir dígito extra
                else:
                    self._emit_error(
                        lexeme,
                        f"Número inválido '{lexeme}': demasiados dígitos "
                        "(máximo 2 dígitos o formato AAAA-AAAA)",
                        t_row, t_col
                    )
                    state = Q0

        return self.tokens, self.errors
