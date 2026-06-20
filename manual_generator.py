"""
Generador de manuales HTML (usuario y técnico) para LigaBot Fase 1.
"""
import os
from reporter import REPORTES_DIR, _ensure_dir, _base_html


def generate_manual_usuario():
    _ensure_dir()
    path = os.path.join(REPORTES_DIR, 'Manual_Usuario.html')

    body = """
<h2>Manual de Usuario — LigaBot Fase 1</h2>
<p class="meta">Analizador Léxico del Lenguaje de Comandos LigaBot</p>

<h3 style="color:#0d3b2e;margin:20px 0 8px">¿Qué es LigaBot?</h3>
<p>LigaBot es un analizador léxico interactivo que reconoce los tokens del lenguaje de
comandos LigaBot — un lenguaje diseñado para consultar estadísticas históricas de La Liga
española. En la Fase 1 solo se evalúa el análisis léxico.</p>

<h3 style="color:#0d3b2e;margin:20px 0 8px">Cómo usar la interfaz</h3>
<table>
<thead><tr><th>Elemento</th><th>Función</th></tr></thead>
<tbody>
<tr><td><b>Campo de texto</b> (inferior)</td>
    <td>Escriba cualquier cadena de texto o un comando de LigaBot y presione <b>Analizar</b>
    o la tecla <b>Enter</b>.</td></tr>
<tr><td><b>Botón Analizar</b></td>
    <td>Ejecuta el analizador léxico sobre el texto ingresado.</td></tr>
<tr><td><b>Área de resultado</b></td>
    <td>Muestra cuántos tokens se reconocieron y los errores léxicos encontrados.</td></tr>
<tr><td><b>Reporte de Tokens</b></td>
    <td>Abre en el navegador la tabla completa de tokens reconocidos (todos los análisis
    acumulados).</td></tr>
<tr><td><b>Reporte de Errores</b></td>
    <td>Abre en el navegador el listado de errores léxicos encontrados.</td></tr>
<tr><td><b>Limpiar Tokens</b></td>
    <td>Borra la lista interna de tokens (el próximo reporte empezará vacío).</td></tr>
<tr><td><b>Limpiar Errores</b></td>
    <td>Borra la lista interna de errores léxicos.</td></tr>
<tr><td><b>Método del Árbol</b></td>
    <td>Abre la documentación formal del proceso de construcción del analizador léxico.</td></tr>
<tr><td><b>Manual de Usuario</b></td>
    <td>Este documento.</td></tr>
<tr><td><b>Manual Técnico</b></td>
    <td>Descripción técnica de la implementación.</td></tr>
</tbody>
</table>

<h3 style="color:#0d3b2e;margin:20px 0 8px">Tokens reconocidos</h3>
<table>
<thead><tr><th>Categoría</th><th>Ejemplo(s)</th><th>Token asignado</th></tr></thead>
<tbody>
<tr><td>Palabras reservadas</td>
    <td><code>RESULTADO, VS, TEMPORADA, JORNADA, GOLES, LOCAL,<br>
    VISITANTE, TOTAL, TABLA, PARTIDOS, TOP, SUPERIOR, INFERIOR, ADIOS</code></td>
    <td>El nombre de la palabra en mayúsculas</td></tr>
<tr><td>Banderas</td>
    <td><code>-f &nbsp; -n &nbsp; -ji &nbsp; -jf</code></td>
    <td>BANDERA_F, BANDERA_N, BANDERA_JI, BANDERA_JF</td></tr>
<tr><td>Cadenas</td>
    <td><code>"Real Madrid"</code>, <code>"Betis"</code></td>
    <td>CADENA</td></tr>
<tr><td>Temporada</td>
    <td><code>1979-1980</code>, <code>2023-2024</code></td>
    <td>TEMPORADA_VAL</td></tr>
<tr><td>Número</td>
    <td><code>1</code>, <code>38</code></td>
    <td>NUMERO (máx. 2 dígitos)</td></tr>
<tr><td>Símbolo menor</td>
    <td><code>&lt;</code></td>
    <td>MENOR</td></tr>
<tr><td>Símbolo mayor</td>
    <td><code>&gt;</code></td>
    <td>MAYOR</td></tr>
</tbody>
</table>

<h3 style="color:#0d3b2e;margin:20px 0 8px">Ejemplos de análisis</h3>
<table>
<thead><tr><th>Texto ingresado</th><th>Resultado esperado</th></tr></thead>
<tbody>
<tr><td><code>RESULTADO "Betis" VS "Rayo Vallecano" TEMPORADA &lt;1979-1980&gt;</code></td>
    <td>8 tokens, 0 errores</td></tr>
<tr><td><code>GOLES LOCAL "Barcelona" TEMPORADA &lt;2023-2024&gt;</code></td>
    <td>6 tokens, 0 errores</td></tr>
<tr><td><code>TOP SUPERIOR TEMPORADA &lt;1979-1980&gt; -n 3</code></td>
    <td>7 tokens, 0 errores</td></tr>
<tr><td><code>PARTIDOS "Betis" TEMPORADA &lt;1979-1980&gt; -ji 1 -jf 5 -f "partidos_betis"</code></td>
    <td>11 tokens, 0 errores</td></tr>
<tr><td><code>ADIOS</code></td>
    <td>1 token, 0 errores</td></tr>
<tr><td><code>resultado$ "equipo"</code></td>
    <td>1 token (resultado→RESULTADO), 1 error ($)</td></tr>
</tbody>
</table>

<h3 style="color:#0d3b2e;margin:20px 0 8px">Tipos de errores léxicos detectados</h3>
<ul style="margin-left:20px;line-height:2.2">
  <li>Carácter no reconocido (ej: <code>$</code>, <code>@</code>, <code>!</code>)</li>
  <li>Cadena no cerrada (falta la comilla de cierre <code>"</code>)</li>
  <li>Bandera no reconocida (ej: <code>-x</code>, <code>-jk</code>)</li>
  <li>Número inválido (más de 2 dígitos sin formato de temporada)</li>
  <li>Palabra no reconocida (no es keyword ni está entre comillas)</li>
</ul>
"""
    with open(path, 'w', encoding='utf-8') as f:
        f.write(_base_html('Manual de Usuario — LigaBot', body))
    return path


def generate_manual_tecnico():
    _ensure_dir()
    path = os.path.join(REPORTES_DIR, 'Manual_Tecnico.html')

    body = """
<h2>Manual Técnico — LigaBot Fase 1</h2>
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
<p>El lexer implementa un <strong>autómata de estados finito manual</strong> que lee el
texto de entrada carácter por carácter. El método principal es <code>analyze()</code>.</p>
<table>
<thead><tr><th>Método</th><th>Descripción</th></tr></thead>
<tbody>
<tr><td><code>analyze()</code></td>
    <td>Ciclo principal. Despacha al método correcto según el primer carácter.</td></tr>
<tr><td><code>_lex_string()</code></td>
    <td>Reconoce cadenas entre comillas dobles. Error si no se cierra.</td></tr>
<tr><td><code>_lex_flag()</code></td>
    <td>Reconoce banderas: <code>-f</code>, <code>-n</code>, <code>-ji</code>,
    <code>-jf</code>. Error para banderas no definidas.</td></tr>
<tr><td><code>_lex_number_or_season()</code></td>
    <td>Lee dígitos; decide si es NUMERO (1-2 d.) o TEMPORADA_VAL (AAAA-AAAA).
    Backtracking simple si los 4 dígitos no van seguidos de 4 más.</td></tr>
<tr><td><code>_lex_word()</code></td>
    <td>Lee letras consecutivas y verifica si forman una palabra reservada
    (insensible a mayúsculas). Error si no coincide con ningún keyword.</td></tr>
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
      │
      ▼
  Lexer.analyze()
      │
      ├──► Lista de Token(lexema, tipo, fila, col)
      │
      └──► Lista de LexicalError(lexema, desc, fila, col)
                │                          │
                ▼                          ▼
      Reporte_Token.html       Reporte_Errores.html
</pre>

<h3 style="color:#0d3b2e;margin:20px 0 8px">Restricciones cumplidas</h3>
<ul style="margin-left:20px;line-height:2">
  <li>No se utiliza ninguna librería de análisis léxico (PLY, ANTLR, re.compile para tokenizar, etc.)</li>
  <li>La lectura es estrictamente carácter por carácter (<code>_advance()</code> consume uno a la vez)</li>
  <li>El backtracking es puntual y acotado (solo para distinguir temporada de número)</li>
</ul>
"""
    with open(path, 'w', encoding='utf-8') as f:
        f.write(_base_html('Manual Técnico — LigaBot', body))
    return path
