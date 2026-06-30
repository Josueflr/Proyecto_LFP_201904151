# chatbot.py - Procesador de comandos LigaBot  (Fase 2)
# Integra: Lexer -> Parser -> DataSource -> Reporter
# Expone la clase Chatbot que recibe texto, lo analiza lexica y sintacticamente,
# consulta el CSV y retorna (texto_respuesta, ruta_reporte_o_None).

from .lexer   import Lexer
from .parser  import Parser, ParseError
from .reporter import (generate_jornada_report, generate_tabla_report,
                       generate_partidos_report)


class Chatbot:
    """
    Motor del chatbot de LigaBot.

    Uso:
        bot = Chatbot(data_source)
        response, lex_errors, parse_error, report_path = bot.process(text)

    Retorno:
        response    - Cadena de texto con la respuesta del bot.
        lex_errors  - Lista de LexicalError del lexico (puede estar vacia).
        parse_error - ParseError si hubo error sintactico, o None.
        report_path - Ruta al HTML generado (None si el comando no genera reporte).
    """

    def __init__(self, data_source):
        self.ds = data_source

    def process(self, text):
        # -- 1. Análisis léxico -------
        lexer = Lexer(text)
        tokens, lex_errors = lexer.analyze()

        # Si hay errores léxicos no seguimos al parser
        if lex_errors:
            msg = (f"LigaBot: Se encontraron {len(lex_errors)} error(es) léxico(s). "
                   f"Corrija el comando e intente de nuevo.")
            return msg, lex_errors, None, None

        if not tokens:
            return "LigaBot: Comando vacío.", [], None, None

        # -- 2. Análisis sintáctico -------
        try:
            ast = Parser(tokens).parse()
        except ParseError as pe:
            msg = (f"LigaBot: Error sintáctico - {pe}")
            return msg, [], pe, None

        # -- 3. Ejecución del comando --------
        cmd = ast['cmd']

        if not self.ds.loaded:
            if cmd != 'ADIOS':
                return ("LigaBot: No se pudo cargar el archivo CSV. "
                        "Verifique que LaLigaBot-LFP.csv esté en la carpeta del proyecto."),\
                        [], None, None

        dispatch = {
            'RESULTADO': self._cmd_resultado,
            'JORNADA':   self._cmd_jornada,
            'GOLES':     self._cmd_goles,
            'TABLA':     self._cmd_tabla,
            'PARTIDOS':  self._cmd_partidos,
            'TOP':       self._cmd_top,
            'ADIOS':     self._cmd_adios,
        }
        response, report_path = dispatch[cmd](ast)
        return response, [], None, report_path

    # -- Handlers por comando -----------

    def _cmd_resultado(self, ast):
        local     = ast['local']
        visitante = ast['visitante']
        temporada = ast['temporada']

        if not self.ds.exists_temporada(temporada):
            return (f"LigaBot: La temporada {temporada} no existe en los datos.",
                    None)

        r = self.ds.get_resultado(local, visitante, temporada)
        if r is None:
            return (f"LigaBot: No se encontró el partido "
                    f"{local} vs {visitante} en la temporada {temporada}.",
                    None)
        return (f"LigaBot: El resultado de este partido fue: "
                f"{r['Equipo1']} {r['Goles1']} - {r['Goles2']} {r['Equipo2']}.",
                None)

    def _cmd_goles(self, ast):
        tipo      = ast['tipo']
        equipo    = ast['equipo']
        temporada = ast['temporada']

        if not self.ds.exists_temporada(temporada):
            return (f"LigaBot: La temporada {temporada} no existe en los datos.", None)
        if not self.ds.exists_equipo(equipo, temporada):
            return (f"LigaBot: El equipo '{equipo}' no se encontró en la temporada {temporada}.", None)

        if tipo == 'LOCAL':
            goles = self.ds.get_goles_local(equipo, temporada)
            return (f"LigaBot: Los goles anotados por el {equipo} en local "
                    f"en la temporada {temporada} fueron {goles}.", None)
        elif tipo == 'VISITANTE':
            goles = self.ds.get_goles_visitante(equipo, temporada)
            return (f"LigaBot: Los goles anotados por el {equipo} en visitante "
                    f"en la temporada {temporada} fueron {goles}.", None)
        else:
            goles = self.ds.get_goles_total(equipo, temporada)
            return (f"LigaBot: Los goles anotados por el {equipo} en total "
                    f"en la temporada {temporada} fueron {goles}.", None)

    def _cmd_jornada(self, ast):
        jornada   = ast['jornada']
        temporada = ast['temporada']

        if not self.ds.exists_temporada(temporada):
            return (f"LigaBot: La temporada {temporada} no existe en los datos.", None)

        partidos = self.ds.get_jornada(jornada, temporada)
        if not partidos:
            return (f"LigaBot: No se encontraron partidos para la jornada {jornada} "
                    f"de la temporada {temporada}.", None)

        nombre = ast.get('nombre') or f'jornada_{jornada}_{temporada.replace("-","_")}'
        path   = generate_jornada_report(partidos, jornada, temporada, nombre)
        return (f"LigaBot: Generando archivo de resultados jornada {jornada} "
                f"temporada {temporada}", path)

    def _cmd_tabla(self, ast):
        temporada = ast['temporada']

        if not self.ds.exists_temporada(temporada):
            return (f"LigaBot: La temporada {temporada} no existe en los datos.", None)

        tabla = self.ds.get_tabla(temporada)
        nombre = ast.get('nombre') or f'tabla_{temporada.replace("-","_")}'
        path   = generate_tabla_report(tabla, temporada, nombre)
        return (f"LigaBot: Generando tabla de posiciones temporada {temporada}", path)

    def _cmd_partidos(self, ast):
        equipo    = ast['equipo']
        temporada = ast['temporada']

        if not self.ds.exists_temporada(temporada):
            return (f"LigaBot: La temporada {temporada} no existe en los datos.", None)
        if not self.ds.exists_equipo(equipo, temporada):
            return (f"LigaBot: El equipo '{equipo}' no se encontró en la temporada {temporada}.", None)

        partidos = self.ds.get_partidos(equipo, temporada, ast.get('ji'), ast.get('jf'))
        nombre   = ast.get('nombre') or f'partidos_{equipo.lower().replace(" ","_")}'
        path     = generate_partidos_report(partidos, equipo, temporada, nombre)
        return (f"LigaBot: Generando reporte de partidos de {equipo} "
                f"temporada {temporada}", path)

    def _cmd_top(self, ast):
        tipo      = ast['tipo']
        temporada = ast['temporada']
        n         = ast['n']

        if not self.ds.exists_temporada(temporada):
            return (f"LigaBot: La temporada {temporada} no existe en los datos.", None)

        if tipo == 'SUPERIOR':
            top   = self.ds.get_top_superior(temporada, n)
            names = '\n'.join(f"  {i+1}. {t['equipo']} ({t['pts']} pts)"
                              for i, t in enumerate(top))
            return (f"LigaBot: El top superior de la temporada {temporada} fue:\n{names}",
                    None)
        else:
            top   = self.ds.get_top_inferior(temporada, n)
            names = '\n'.join(f"  {i+1}. {t['equipo']} ({t['pts']} pts)"
                              for i, t in enumerate(top))
            return (f"LigaBot: El top inferior de la temporada {temporada} fue:\n{names}",
                    None)

    def _cmd_adios(self, ast):
        return ("LigaBot: ADIOS", None)
