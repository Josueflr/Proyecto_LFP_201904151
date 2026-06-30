"""
Generador de manuales HTML (usuario y técnico) para LigaBot.
"""
import os
from .reporter import REPORTES_DIR, _ensure_dir, _base_html


def generate_manual_usuario():
    _ensure_dir()
    path = os.path.join(REPORTES_DIR, 'Manual_Usuario.html')

    body = """
<h2>Manual de Usuario - LigaBot Fase 2</h2>
<p class="meta">Analizador Léxico y Sintáctico con Chatbot de consultas de La Liga</p>

<h3 style="color:#0d3b2e;margin:20px 0 8px">¿Qué es LigaBot?</h3>
<p>LigaBot es un chatbot académico que recibe comandos escritos, los analiza léxica y
sintácticamente, y responde con datos reales de partidos de La Liga española (temporadas
1979-1980 a 2019-2020) consultados desde el archivo <code>LaLigaBot-LFP.csv</code>.</p>

<h3 style="color:#0d3b2e;margin:20px 0 8px">Cómo usar la interfaz</h3>
<table>
<thead><tr><th>Elemento</th><th>Función</th></tr></thead>
<tbody>
<tr><td><b>Campo de texto</b> (inferior)</td>
    <td>Escriba el comando completo y presione <b>Enviar</b> o la tecla <b>Enter</b>.</td></tr>
<tr><td><b>Botón Enviar</b></td>
    <td>Ejecuta el pipeline léxico -> sintáctico -> consulta CSV -> respuesta.</td></tr>
<tr><td><b>Área de conversación</b></td>
    <td>Muestra el historial completo: sus comandos y las respuestas de LigaBot.</td></tr>
<tr><td><b>Reporte de Tokens</b></td>
    <td>HTML con todos los tokens reconocidos en la sesión.</td></tr>
<tr><td><b>Reporte Errores Léxicos</b></td>
    <td>HTML con errores de caracteres o lexemas inválidos.</td></tr>
<tr><td><b>Reporte Errores Sintácticos</b></td>
    <td>HTML con errores de estructura de comandos.</td></tr>
<tr><td><b>Limpiar Tokens</b></td>
    <td>Borra los tokens y errores léxicos acumulados.</td></tr>
<tr><td><b>Limpiar Errores</b></td>
    <td>Borra los errores sintácticos acumulados.</td></tr>
</tbody>
</table>

<h3 style="color:#0d3b2e;margin:20px 0 8px">Comandos disponibles</h3>
<table>
<thead><tr><th>Comando</th><th>Sintaxis completa</th><th>Descripción</th></tr></thead>
<tbody>
<tr><td><b>RESULTADO</b></td>
    <td><code>RESULTADO "Local" VS "Visitante" TEMPORADA &lt;AAAA-AAAA&gt;</code></td>
    <td>Muestra el marcador exacto del partido.</td></tr>
<tr><td><b>JORNADA</b></td>
    <td><code>JORNADA N TEMPORADA &lt;AAAA-AAAA&gt; [-f "nombre"]</code></td>
    <td>Genera un reporte HTML con todos los partidos de la jornada.</td></tr>
<tr><td><b>GOLES LOCAL</b></td>
    <td><code>GOLES LOCAL "Equipo" TEMPORADA &lt;AAAA-AAAA&gt;</code></td>
    <td>Total de goles anotados como local.</td></tr>
<tr><td><b>GOLES VISITANTE</b></td>
    <td><code>GOLES VISITANTE "Equipo" TEMPORADA &lt;AAAA-AAAA&gt;</code></td>
    <td>Total de goles anotados como visitante.</td></tr>
<tr><td><b>GOLES TOTAL</b></td>
    <td><code>GOLES TOTAL "Equipo" TEMPORADA &lt;AAAA-AAAA&gt;</code></td>
    <td>Total de goles (local + visitante).</td></tr>
<tr><td><b>TABLA</b></td>
    <td><code>TABLA TEMPORADA &lt;AAAA-AAAA&gt; [-f "nombre"]</code></td>
    <td>Genera tabla de clasificación ordenada por puntos.</td></tr>
<tr><td><b>PARTIDOS</b></td>
    <td><code>PARTIDOS "Equipo" TEMPORADA &lt;AAAA-AAAA&gt; [-f "nombre"] [-ji N] [-jf N]</code></td>
    <td>Genera reporte de partidos del equipo con filtro opcional por jornada.</td></tr>
<tr><td><b>TOP SUPERIOR</b></td>
    <td><code>TOP SUPERIOR TEMPORADA &lt;AAAA-AAAA&gt; [-n N]</code></td>
    <td>Muestra los N primeros equipos (defecto 5).</td></tr>
<tr><td><b>TOP INFERIOR</b></td>
    <td><code>TOP INFERIOR TEMPORADA &lt;AAAA-AAAA&gt; [-n N]</code></td>
    <td>Muestra los N últimos equipos (defecto 5).</td></tr>
<tr><td><b>ADIOS</b></td>
    <td><code>ADIOS</code></td>
    <td>Finaliza la sesión del chatbot.</td></tr>
</tbody>
</table>

<h3 style="color:#0d3b2e;margin:20px 0 8px">Ejemplos de comandos y respuestas esperadas</h3>
<table>
<thead><tr><th>Comando ingresado</th><th>Respuesta esperada</th></tr></thead>
<tbody>
<tr><td><code>RESULTADO "Betis" VS "Rayo Vallecano" TEMPORADA &lt;1979-1980&gt;</code></td>
    <td>LigaBot: El resultado de este partido fue: Betis 1 - 2 Rayo Vallecano.</td></tr>
<tr><td><code>GOLES LOCAL "Betis" TEMPORADA &lt;1979-1980&gt;</code></td>
    <td>LigaBot: Los goles anotados por el Betis en local en la temporada 1979-1980 fueron 26.</td></tr>
<tr><td><code>GOLES TOTAL "Betis" TEMPORADA &lt;1979-1980&gt;</code></td>
    <td>LigaBot: Los goles anotados por el Betis en total en la temporada 1979-1980 fueron 39.</td></tr>
<tr><td><code>TOP SUPERIOR TEMPORADA &lt;1979-1980&gt; -n 3</code></td>
    <td>LigaBot: El top superior... 1. Real Madrid  2. Real Sociedad  3. Sporting de Gijón</td></tr>
<tr><td><code>TOP INFERIOR TEMPORADA &lt;1979-1980&gt; -n 3</code></td>
    <td>LigaBot: El top inferior... 1. Burgos  2. CD Málaga  3. Rayo Vallecano</td></tr>
<tr><td><code>JORNADA 1 TEMPORADA &lt;1979-1980&gt; -f "jornada_1"</code></td>
    <td>LigaBot: Generando archivo de resultados... (abre reporte HTML)</td></tr>
<tr><td><code>TABLA TEMPORADA &lt;1979-1980&gt;</code></td>
    <td>LigaBot: Generando tabla de posiciones... (abre reporte HTML)</td></tr>
<tr><td><code>PARTIDOS "Betis" TEMPORADA &lt;1979-1980&gt; -ji 1 -jf 5</code></td>
    <td>LigaBot: Generando reporte de partidos... (abre reporte HTML)</td></tr>
<tr><td><code>ADIOS</code></td>
    <td>LigaBot: ADIOS</td></tr>
<tr><td><code>resultado$ "equipo"</code></td>
    <td>2 tokens (RESULTADO + CADENA), 1 error ($)</td></tr>
</tbody>
</table>

<h3 style="color:#0d3b2e;margin:20px 0 8px">Banderas opcionales</h3>
<table>
<thead><tr><th>Bandera</th><th>Argumento</th><th>Aplica en</th><th>Efecto</th></tr></thead>
<tbody>
<tr><td><code>-f</code></td><td><code>"nombre"</code></td>
    <td>JORNADA, TABLA, PARTIDOS</td>
    <td>Nombre del archivo HTML generado (sin extensión).</td></tr>
<tr><td><code>-n</code></td><td><code>N</code></td>
    <td>TOP SUPERIOR / INFERIOR</td>
    <td>Cantidad de equipos a mostrar (defecto 5).</td></tr>
<tr><td><code>-ji</code></td><td><code>N</code></td>
    <td>PARTIDOS</td>
    <td>Jornada inicial del filtro (inclusivo).</td></tr>
<tr><td><code>-jf</code></td><td><code>N</code></td>
    <td>PARTIDOS</td>
    <td>Jornada final del filtro (inclusivo).</td></tr>
</tbody>
</table>

<hr style="margin:30px 0;border-color:#cde3d4">
<h2 style="color:#0d3b2e">Vista previa de los reportes generados</h2>
<p style="color:#555;font-size:.9rem;margin-bottom:18px">
Los reportes HTML se abren automáticamente en el navegador después de ejecutar el comando
correspondiente. A continuación se muestran ejemplos con datos reales de la temporada
1979-1980.</p>

<h3 style="color:#0d3b2e;margin:20px 0 8px">Reporte de Jornada</h3>
<p style="color:#666;font-size:.88rem">
  Comando: <code>JORNADA 1 TEMPORADA &lt;1979-1980&gt;</code></p>
<div style="margin:10px 0 28px;text-align:center">
  <img src="../assets/jornada_f2.png" alt="Reporte Jornada"
       style="max-width:100%;border-radius:8px;box-shadow:0 2px 12px rgba(0,0,0,.12);
              border:1px solid #cde3d4">
</div>

<h3 style="color:#0d3b2e;margin:20px 0 8px">Tabla de Posiciones</h3>
<p style="color:#666;font-size:.88rem">
  Comando: <code>TABLA TEMPORADA &lt;1979-1980&gt;</code></p>
<div style="margin:10px 0 28px;text-align:center">
  <img src="../assets/tabla_posiciones_f2.png" alt="Tabla de Posiciones"
       style="max-width:100%;border-radius:8px;box-shadow:0 2px 12px rgba(0,0,0,.12);
              border:1px solid #cde3d4">
</div>

<h3 style="color:#0d3b2e;margin:20px 0 8px">Partidos por Equipo</h3>
<p style="color:#666;font-size:.88rem">
  Comando: <code>PARTIDOS "Betis" TEMPORADA &lt;1979-1980&gt; -ji 1 -jf 10</code></p>
<div style="margin:10px 0 28px;text-align:center">
  <img src="../assets/partidos_f2.png" alt="Partidos por Equipo"
       style="max-width:100%;border-radius:8px;box-shadow:0 2px 12px rgba(0,0,0,.12);
              border:1px solid #cde3d4">
</div>

<h3 style="color:#0d3b2e;margin:20px 0 8px">Reporte de Errores Sintácticos</h3>
<p style="color:#666;font-size:.88rem">
  Botón: <b>Reporte Errores Sintácticos</b> - se genera cuando hay comandos con errores de estructura.</p>
<div style="margin:10px 0 16px;text-align:center">
  <img src="../assets/errores_sintacticos_f2.png" alt="Errores Sintácticos"
       style="max-width:100%;border-radius:8px;box-shadow:0 2px 12px rgba(0,0,0,.12);
              border:1px solid #f5c6cb">
</div>
"""
    with open(path, 'w', encoding='utf-8') as f:
        f.write(_base_html('Manual de Usuario - LigaBot', body))
    return path


def generate_manual_tecnico():
    _ensure_dir()
    path = os.path.join(REPORTES_DIR, 'Manual_Tecnico.html')

    body = """
<h2>Manual Tecnico - LigaBot Fase 1</h2>
<p class="meta">Descripción técnica del analizador léxico</p>

<h3 style="color:#0d3b2e;margin:20px 0 8px">Requisitos del sistema</h3>
<ul style="margin-left:20px;line-height:2">
  <li>Python 3.8 o superior</li>
  <li>Módulo <code>tkinter</code> (incluido en la instalación estándar de Python)</li>
  <li>Sistema operativo: Windows, Linux o macOS</li>
  <li>Navegador web para visualizar los reportes HTML</li>
</ul>

<h3 style="color:#0d3b2e;margin:20px 0 8px">Instrucciones de ejecución</h3>
<pre style="background:#1e1e1e;color:#d4d4d4;padding:16px;border-radius:8px;font-size:.88rem">
# Desde la carpeta del proyecto:
python main.py
</pre>

<h3 style="color:#0d3b2e;margin:20px 0 8px">Estructura de archivos</h3>
<table>
<thead><tr><th>Archivo</th><th>Responsabilidad</th></tr></thead>
<tbody>
<tr><td><code>main.py</code></td>
    <td>Punto de entrada. Crea la ventana Tkinter y lanza la GUI.</td></tr>
<tr><td><code>lexer.py</code></td>
    <td>Analizador léxico manual. Clases: <code>Lexer</code>, <code>Token</code>,
    <code>LexicalError</code>, <code>TokenType</code>.</td></tr>
<tr><td><code>reporter.py</code></td>
    <td>Generador de reportes HTML para tokens y errores léxicos.</td></tr>
<tr><td><code>metodo_arbol.py</code></td>
    <td>Genera el HTML con el desarrollo formal del método del árbol.</td></tr>
<tr><td><code>manual_generator.py</code></td>
    <td>Genera los manuales HTML de usuario y técnico.</td></tr>
<tr><td><code>gui.py</code></td>
    <td>Interfaz gráfica con Tkinter.</td></tr>
<tr><td><code>reportes/</code></td>
    <td>Directorio de salida para todos los archivos HTML generados.</td></tr>
</tbody>
</table>

<h3 style="color:#0d3b2e;margin:20px 0 8px">Diseño del Lexer (<code>lexer.py</code>)</h3>
<p>El lexer implementa un <strong>autómata finito determinista (AFD) de 22 estados
(q0-q21)</strong> mediante un único bucle <code>while</code> en el método
<code>analyze()</code>. La variable <code>state</code> almacena el estado actual;
en cada iteración se evalúa el par (estado, carácter) y se avanza al estado siguiente.</p>
<table>
<thead><tr><th>Método</th><th>Descripción</th></tr></thead>
<tbody>
<tr><td><code>analyze()</code></td>
    <td>Bucle principal del AFD. Evalúa cada par (estado, carácter) y ejecuta la
    transición correspondiente. Retorna <code>(lista[Token], lista[LexicalError])</code>.</td></tr>
<tr><td><code>_char()</code></td>
    <td>Retorna el carácter actual <em>sin consumirlo</em> (lookahead de 1 carácter).
    Retorna <code>None</code> al llegar al EOF.</td></tr>
<tr><td><code>_advance()</code></td>
    <td>Consume el carácter actual, actualiza <code>fila</code>/<code>columna</code>
    y lo retorna. Incrementa fila si el carácter es <code>\\n</code>.</td></tr>
<tr><td><code>_emit(lexema, tipo, fila, col)</code></td>
    <td>Añade un <code>Token</code> a la lista de tokens reconocidos.</td></tr>
<tr><td><code>_emit_error(lexema, desc, fila, col)</code></td>
    <td>Añade un <code>LexicalError</code> a la lista de errores (recuperación en
    modo pánico: se descarta el lexema y el AFD regresa a q0).</td></tr>
</tbody>
</table>

<h3 style="color:#0d3b2e;margin:20px 0 8px">Estados del AFD</h3>
<table>
<thead><tr><th>Estados</th><th>Función</th></tr></thead>
<tbody>
<tr><td><code>q0</code></td><td>Estado inicial. Decide el tipo de token por el primer carácter.</td></tr>
<tr><td><code>q1</code></td><td>Acumula letras; emite KEYWORD o error al encontrar un no-letra.</td></tr>
<tr><td><code>q2, q3</code></td><td>Acumulan 1 y 2 dígitos; emiten NUMERO al salir del patrón.</td></tr>
<tr><td><code>q4-q10</code></td><td>Detectan el patrón <code>DDDD-DDDD</code> para TEMPORADA_VAL.</td></tr>
<tr><td><code>q11, q12</code></td><td>Reconocen cadenas entre comillas dobles.</td></tr>
<tr><td><code>q13-q18</code></td><td>Reconocen las cuatro banderas (-f, -n, -ji, -jf).</td></tr>
<tr><td><code>q19, q20</code></td><td>Emiten MENOR y MAYOR (tokens de un solo carácter).</td></tr>
<tr><td><code>q21</code></td><td>Estado de error por desbordamiento (&gt;4 dígitos consecutivos).</td></tr>
</tbody>
</table>

<h3 style="color:#0d3b2e;margin:20px 0 8px">Registro de posición</h3>
<p>El lexer mantiene las variables <code>self.fila</code> y <code>self.columna</code>.
Cada llamada a <code>_advance()</code> actualiza ambas: si el carácter consumido es
<code>\\n</code>, la fila incrementa y la columna se reinicia a 1; en otro caso solo
la columna incrementa.</p>

<h3 style="color:#0d3b2e;margin:20px 0 8px">Flujo de datos</h3>
<pre style="background:#1e1e1e;color:#d4d4d4;padding:16px;border-radius:8px;font-size:.88rem">
Texto de entrada
      |
      ▼
  Lexer.analyze()
      |
      ├--> Lista de Token(lexema, tipo, fila, col)
      |
      └--> Lista de LexicalError(lexema, desc, fila, col)
                |                          |
                ▼                          ▼
      Reporte_Token.html       Reporte_Errores.html
</pre>

<h3 style="color:#0d3b2e;margin:20px 0 8px">Restricciones cumplidas</h3>
<ul style="margin-left:20px;line-height:2">
  <li>No se utiliza ninguna librería de análisis léxico (PLY, ANTLR, <code>re.compile</code> para tokenizar, etc.)</li>
  <li>La lectura es estrictamente carácter por carácter (<code>_advance()</code> consume uno a la vez)</li>
  <li>No se usa backtracking; el lookahead de un carácter (<code>_char()</code>) es suficiente para decidir cada transición</li>
</ul>

<hr style="margin:30px 0;border-color:#cde3d4">
<h2 style="color:#0d3b2e">Fase 2 - Analizador Sintactico y Chatbot</h2>

<h3 style="color:#0d3b2e;margin:20px 0 8px">Nuevos archivos</h3>
<table>
<thead><tr><th>Archivo</th><th>Responsabilidad</th></tr></thead>
<tbody>
<tr><td><code>parser.py</code></td>
    <td>Analizador sintáctico de descenso recursivo. Valida la lista de tokens contra la
    gramática de los 8 comandos y retorna un AST (diccionario).</td></tr>
<tr><td><code>data_source.py</code></td>
    <td>Carga <code>LaLigaBot-LFP.csv</code> (encoding latin-1) y expone métodos de consulta:
    resultado, goles, jornada, tabla, partidos, top.</td></tr>
<tr><td><code>chatbot.py</code></td>
    <td>Integra Lexer -> Parser -> DataSource -> Reporter.
    Retorna <code>(response, lex_errors, parse_error, report_path)</code>.</td></tr>
</tbody>
</table>

<h3 style="color:#0d3b2e;margin:20px 0 8px">Gramática del lenguaje</h3>
<pre style="background:#1e1e1e;color:#d4d4d4;padding:16px;border-radius:8px;font-size:.85rem">
programa       -> comando

comando        -> resultado_cmd | jornada_cmd | goles_cmd | tabla_cmd
               | partidos_cmd | top_cmd | adios_cmd

resultado_cmd  -> RESULTADO CADENA VS CADENA TEMPORADA &lt;tv&gt;
jornada_cmd    -> JORNADA NUMERO TEMPORADA &lt;tv&gt; [-f CADENA]
goles_cmd      -> GOLES (LOCAL|VISITANTE|TOTAL) CADENA TEMPORADA &lt;tv&gt;
tabla_cmd      -> TABLA TEMPORADA &lt;tv&gt; [-f CADENA]
partidos_cmd   -> PARTIDOS CADENA TEMPORADA &lt;tv&gt; [-f CADENA] [-ji NUMERO] [-jf NUMERO]
top_cmd        -> TOP (SUPERIOR|INFERIOR) TEMPORADA &lt;tv&gt; [-n NUMERO]
adios_cmd      -> ADIOS

&lt;tv&gt;           -> MENOR TEMPORADA_VAL MAYOR    (ej: &lt;1979-1980&gt;)
Las banderas son opcionales y pueden aparecer en cualquier orden.
</pre>

<h3 style="color:#0d3b2e;margin:20px 0 8px">Diseño del Parser (<code>parser.py</code>)</h3>
<table>
<thead><tr><th>Método</th><th>Descripción</th></tr></thead>
<tbody>
<tr><td><code>parse()</code></td>
    <td>Punto de entrada. Despacha al método correspondiente según el primer token.</td></tr>
<tr><td><code>_consume(*types)</code></td>
    <td>Consume el token actual si su tipo coincide; lanza <code>ParseError</code> en caso contrario.</td></tr>
<tr><td><code>_parse_flags()</code></td>
    <td>Consume banderas opcionales en cualquier orden usando un bucle while.</td></tr>
<tr><td><code>_expect_end()</code></td>
    <td>Verifica que no queden tokens sin consumir al final del comando.</td></tr>
<tr><td><code>ParseError</code></td>
    <td>Excepción con: <code>received</code> (token encontrado), <code>expected</code> (descripción),
    <code>fila</code>, <code>col</code>.</td></tr>
</tbody>
</table>

<h3 style="color:#0d3b2e;margin:20px 0 8px">Fuente de datos (<code>data_source.py</code>)</h3>
<table>
<thead><tr><th>Método</th><th>Descripción</th></tr></thead>
<tbody>
<tr><td><code>get_resultado(local, vis, tmp)</code></td>
    <td>Busca partido exacto; comparación case-insensitive con normalización de acentos.</td></tr>
<tr><td><code>get_goles_local/visitante/total()</code></td>
    <td>Suma de goles del equipo según rol (Equipo1=local, Equipo2=visitante).</td></tr>
<tr><td><code>get_jornada(jornada, tmp)</code></td>
    <td>Lista de partidos de la jornada indicada.</td></tr>
<tr><td><code>get_tabla(tmp)</code></td>
    <td>Clasificación calculada: Victoria=3pts, Empate=1pt, Derrota=0pts. Ordenada por puntos,
    diferencia de goles y goles a favor.</td></tr>
<tr><td><code>get_partidos(equipo, tmp, ji, jf)</code></td>
    <td>Partidos del equipo con filtro de jornada. Incluye resultado (Victoria/Derrota/Empate)
    desde la perspectiva del equipo consultado.</td></tr>
<tr><td><code>get_top_superior/inferior(tmp, n)</code></td>
    <td>Primeros o últimos N equipos de la tabla.</td></tr>
</tbody>
</table>

<h3 style="color:#0d3b2e;margin:20px 0 8px">Pipeline completo (Fase 2)</h3>
<pre style="background:#1e1e1e;color:#d4d4d4;padding:16px;border-radius:8px;font-size:.88rem">
Texto ingresado por el usuario
      |
      ▼
  Lexer.analyze()
      ├--> tokens          --> Parser.parse()  --> AST
      └--> lex_errors           |
                                ├--> ParseError  --> Reporte_Errores_S.html
                                └--> AST cmd
                                          |
                                          ▼
                                    DataSource (CSV)
                                          |
                              ┌-----------┴--------------┐
                              ▼                          ▼
                         Respuesta texto          Reporte HTML
                         (RESULTADO, GOLES,       (JORNADA, TABLA,
                          TOP, ADIOS)              PARTIDOS)
</pre>

<h3 style="color:#0d3b2e;margin:20px 0 8px">Reportes generados en Fase 2</h3>
<table>
<thead><tr><th>Reporte</th><th>Archivo</th><th>Contenido</th></tr></thead>
<tbody>
<tr><td>Errores sintácticos</td><td><code>Reporte_Errores_S.html</code></td>
    <td>Token recibido, token esperado, fila y columna.</td></tr>
<tr><td>Jornada</td><td><code>{nombre}.html</code></td>
    <td>Partidos de la jornada con equipos, goles y ganador.</td></tr>
<tr><td>Tabla de posiciones</td><td><code>{nombre}.html</code></td>
    <td>Clasificación: PJ, G, E, P, GF, GC, DG, Pts.</td></tr>
<tr><td>Partidos por equipo</td><td><code>{nombre}.html</code></td>
    <td>Jornada, rival, marcador y resultado para el equipo.</td></tr>
</tbody>
</table>

<h3 style="color:#0d3b2e;margin:28px 0 8px">Vista previa de las tablas generadas</h3>
<p style="color:#555;font-size:.9rem;margin-bottom:18px">
Las siguientes imágenes muestran el formato real de cada reporte generado por LigaBot Fase 2
usando datos de la temporada 1979-1980.</p>

<p style="color:#0d3b2e;font-weight:600;margin:16px 0 6px">1. Reporte de Jornada</p>
<div style="margin:0 0 24px;text-align:center">
  <img src="../assets/jornada_f2.png" alt="Reporte de Jornada"
       style="max-width:100%;border-radius:8px;box-shadow:0 2px 12px rgba(0,0,0,.12);
              border:1px solid #cde3d4">
  <p style="color:#888;font-size:.82rem;margin-top:6px">
    Comando: <code>JORNADA 1 TEMPORADA &lt;1979-1980&gt;</code>
    - verde = victoria local, rojo = victoria visitante, amarillo = empate</p>
</div>

<p style="color:#0d3b2e;font-weight:600;margin:16px 0 6px">2. Tabla de Posiciones</p>
<div style="margin:0 0 24px;text-align:center">
  <img src="../assets/tabla_posiciones_f2.png" alt="Tabla de Posiciones"
       style="max-width:100%;border-radius:8px;box-shadow:0 2px 12px rgba(0,0,0,.12);
              border:1px solid #cde3d4">
  <p style="color:#888;font-size:.82rem;margin-top:6px">
    Comando: <code>TABLA TEMPORADA &lt;1979-1980&gt;</code>
    - verde = top 3, azul = top 6, Pts en negrita</p>
</div>

<p style="color:#0d3b2e;font-weight:600;margin:16px 0 6px">3. Partidos por Equipo</p>
<div style="margin:0 0 24px;text-align:center">
  <img src="../assets/partidos_f2.png" alt="Partidos por Equipo"
       style="max-width:100%;border-radius:8px;box-shadow:0 2px 12px rgba(0,0,0,.12);
              border:1px solid #cde3d4">
  <p style="color:#888;font-size:.82rem;margin-top:6px">
    Comando: <code>PARTIDOS "Betis" TEMPORADA &lt;1979-1980&gt; -ji 1 -jf 10</code>
    - resultado desde la perspectiva del equipo consultado</p>
</div>

<p style="color:#0d3b2e;font-weight:600;margin:16px 0 6px">4. Reporte de Errores Sintacticos</p>
<div style="margin:0 0 16px;text-align:center">
  <img src="../assets/errores_sintacticos_f2.png" alt="Errores Sintacticos"
       style="max-width:100%;border-radius:8px;box-shadow:0 2px 12px rgba(0,0,0,.12);
              border:1px solid #f5c6cb">
  <p style="color:#888;font-size:.82rem;margin-top:6px">
    Boton "Reporte Errores Sintacticos" - token recibido, token esperado, fila y columna</p>
</div>
"""
    with open(path, 'w', encoding='utf-8') as f:
        f.write(_base_html('Manual Técnico - LigaBot', body))
    return path
