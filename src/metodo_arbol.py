import os
from .reporter import REPORTES_DIR, _ensure_dir, open_report



NULLABLE_TABLE = [
    ("d[1]",          "hoja - simbolo",         "false"),
    ("d[2]",          "hoja - simbolo",         "false"),
    ("ε",             "hoja - epsilon",          "true"),
    ("d[2] | ε",      "nodo OR",                 "nullable(d[2]) OR nullable(ε) = false OR true = <b>true</b>"),
    ("d[1] · (d[2]|ε)", "nodo CONCAT",          "nullable(d[1]) AND nullable(d[2]|ε) = false AND true = <b>false</b>"),
    ("#[3]",          "hoja - simbolo",         "false"),
    ("(d[1]·(d[2]|ε)) · #[3]", "raíz CONCAT", "nullable(left) AND nullable(#) = false AND false = <b>false</b>"),
]

FIRSTPOS_TABLE = [
    ("d[1]",                      "{1}"),
    ("d[2]",                      "{2}"),
    ("ε",                         "∅"),
    ("d[2] | ε",                  "firstpos(d[2]) ∪ firstpos(ε) = {2} ∪ ∅ = <b>{2}</b>"),
    ("d[1] · (d[2]|ε)",          "nullable(d[1])=false -> <b>firstpos(d[1]) = {1}</b>"),
    ("#[3]",                      "{3}"),
    ("(d[1]·(d[2]|ε)) · #[3]",  "nullable(left)=false -> <b>firstpos(left) = {1}</b>"),
]

LASTPOS_TABLE = [
    ("d[1]",                      "{1}"),
    ("d[2]",                      "{2}"),
    ("ε",                         "∅"),
    ("d[2] | ε",                  "lastpos(d[2]) ∪ lastpos(ε) = {2} ∪ ∅ = <b>{2}</b>"),
    ("d[1] · (d[2]|ε)",          "nullable(d[2]|ε)=true -> lastpos(d[1]) ∪ lastpos(d[2]|ε) = {1} ∪ {2} = <b>{1,2}</b>"),
    ("#[3]",                      "{3}"),
    ("(d[1]·(d[2]|ε)) · #[3]",  "nullable(#)=false -> <b>lastpos(#[3]) = {3}</b>"),
]

FOLLOWPOS_TABLE = [
    (1, "d", "{2,3}",
     "Desde d[1]·(d[2]|ε): ∀i ∈ lastpos(d[1])={1} -> followpos(1) ∪= firstpos(d[2]|ε)={2} -> {2}<br>"
     "Desde raíz: ∀i ∈ lastpos(left)={1,2} -> followpos(1) ∪= firstpos(#[3])={3} -> {2,3}"),
    (2, "d", "{3}",
     "Desde raíz: ∀i ∈ lastpos(left)={1,2} -> followpos(2) ∪= firstpos(#[3])={3} -> {3}"),
    (3, "#", "∅",
     "Posicion marcadora - no genera followpos"),
]

DFA_STATES = [
    ("A", "{1}",   "Inicial",         "No"),
    ("B", "{2,3}", "-",               "Si  (contiene pos 3)"),
    ("C", "{3}",   "-",               "Si  (contiene pos 3)"),
]

DFA_TRANSITIONS = [
    ("A = {1}",   "d (0-9)", "B = {2,3}", "followpos(1) = {2,3}"),
    ("B = {2,3}", "d (0-9)", "C = {3}",   "followpos(2) = {3}  (pos 3 tiene simbolo #, no d)"),
    ("C = {3}",   "-",       "muerto",    "pos 3 solo tiene simbolo #"),
]

# -- AFD completo del lexer LigaBot (22 estados q0-q21) ------------------------

FULL_AFD_STATES = [
    ("q0",  "Estado inicial / limpio",
     "Inicial", "No", "-"),
    ("q1",  "Leyendo letras consecutivas",
     "-", "No", "Palabra reservada o ERROR al salir"),
    ("q2",  "1 digito acumulado",
     "-", "No", "NUMERO si no continua digito"),
    ("q3",  "2 digitos acumulados",
     "-", "No", "NUMERO si no continua digito"),
    ("q4",  "3 digitos acumulados",
     "-", "No", "ERROR al salir"),
    ("q5",  "4 digitos acumulados",
     "-", "No", "-> q6 si sigue '-', -> q21 si sigue digito, ERROR si otro"),
    ("q6",  "Leido <code>DDDD-</code>, espera 1er digito del 2do grupo",
     "-", "No", "ERROR si no sigue digito"),
    ("q7",  "Leido <code>DDDD-D</code>",
     "-", "No", "ERROR si no sigue digito"),
    ("q8",  "Leido <code>DDDD-DD</code>",
     "-", "No", "ERROR si no sigue digito"),
    ("q9",  "Leido <code>DDDD-DDD</code>",
     "-", "No", "ERROR si no sigue digito"),
    ("q10", "Leido <code>DDDD-DDDD</code> - temporada completa",
     "Si", "Si", "TEMPORADA_VAL"),
    ("q11", "Dentro de cadena literal (tras la comilla de apertura)",
     "-", "No", "-"),
    ("q12", "Cadena cerrada con comilla de cierre",
     "Si", "Si", "CADENA"),
    ("q13", "Leido <code>-</code>, espera sufijo de bandera",
     "-", "No", "-"),
    ("q14", "Leido <code>-f</code> o <code>-F</code>",
     "Si", "Si", "BANDERA_F"),
    ("q15", "Leido <code>-n</code> o <code>-N</code>",
     "Si", "Si", "BANDERA_N"),
    ("q16", "Leido <code>-j/-J</code>, espera <code>i/I</code> o <code>f/F</code>",
     "-", "No", "-"),
    ("q17", "Leido <code>-ji/-jI/-Ji/-JI</code>",
     "Si", "Si", "BANDERA_JI"),
    ("q18", "Leido <code>-jf/-jF/-Jf/-JF</code>",
     "Si", "Si", "BANDERA_JF"),
    ("q19", "Leido <code>&lt;</code>",
     "Si", "Si", "MENOR"),
    ("q20", "Leido <code>&gt;</code>",
     "Si", "Si", "MAYOR"),
    ("q21", "Desbordamiento: mas de 4 digitos consecutivos",
     "-", "No", "ERROR al salir"),
]

FULL_AFD_TRANSITIONS = [
    ("q0",  "espacio / tab / \\r / \\n",             "q0",  "Descartar - no produce token"),
    ("q0",  "letra [a-zA-Z]",                        "q1",  "Iniciar lexema de palabra"),
    ("q0",  "dígito [0-9]",                          "q2",  "Iniciar lexema numérico"),
    ("q0",  "<code>\"</code>",                        "q11", "Iniciar cadena literal"),
    ("q0",  "<code>-</code>",                         "q13", "Posible bandera"),
    ("q0",  "<code>&lt;</code>",                      "q19", "Token MENOR (1 carácter)"),
    ("q0",  "<code>&gt;</code>",                      "q20", "Token MAYOR (1 carácter)"),
    ("q0",  "cualquier otro carácter",               "q0",  "ERROR: carácter no reconocido"),
    ("q1",  "letra [a-zA-Z]",                        "q1",  "Acumular letra"),
    ("q1",  "no-letra / EOF",                        "q0",  "Emitir KEYWORD si reservada, o [X] ERROR"),
    ("q2",  "dígito [0-9]",                          "q3",  "Acumular 2.º dígito"),
    ("q2",  "no-dígito / EOF",                       "q0",  "Emitir NUMERO (1 dígito)"),
    ("q3",  "dígito [0-9]",                          "q4",  "Acumular 3.er dígito"),
    ("q3",  "no-dígito / EOF",                       "q0",  "Emitir NUMERO (2 dígitos)"),
    ("q4",  "dígito [0-9]",                          "q5",  "Acumular 4.º dígito"),
    ("q4",  "no-dígito / EOF",                       "q0",  "ERROR: 3 dígitos no forman token válido"),
    ("q5",  "<code>-</code>",                         "q6",  "Iniciar sufijo de temporada"),
    ("q5",  "dígito [0-9]",                          "q21", "Desbordamiento"),
    ("q5",  "otro / EOF",                            "q0",  "ERROR: 4 dígitos sin '-' no es token"),
    ("q6",  "dígito [0-9]",                          "q7",  "1.er dígito del 2.º grupo"),
    ("q6",  "otro / EOF",                            "q0",  "ERROR: temporada incompleta"),
    ("q7",  "dígito [0-9]",                          "q8",  "2.º dígito del 2.º grupo"),
    ("q7",  "otro / EOF",                            "q0",  "ERROR: temporada incompleta"),
    ("q8",  "dígito [0-9]",                          "q9",  "3.er dígito del 2.º grupo"),
    ("q8",  "otro / EOF",                            "q0",  "ERROR: temporada incompleta"),
    ("q9",  "dígito [0-9]",                          "q10", "4.º dígito - temporada completa"),
    ("q9",  "otro / EOF",                            "q0",  "ERROR: temporada incompleta"),
    ("q10", "(sin consumir siguiente carácter)",     "q0",  "Emitir TEMPORADA_VAL"),
    ("q11", "<code>\"</code>",                        "q12", "Cerrar cadena"),
    ("q11", "\\n / EOF",                             "q0",  "ERROR: cadena no cerrada"),
    ("q11", "cualquier otro",                        "q11", "Acumular carácter interior"),
    ("q12", "(sin consumir siguiente carácter)",     "q0",  "Emitir CADENA"),
    ("q13", "<code>f</code> / <code>F</code>",        "q14", "-"),
    ("q13", "<code>n</code> / <code>N</code>",        "q15", "-"),
    ("q13", "<code>j</code> / <code>J</code>",        "q16", "-"),
    ("q13", "otro / EOF",                            "q0",  "ERROR: bandera no reconocida"),
    ("q14", "(sin consumir siguiente carácter)",     "q0",  "Emitir BANDERA_F"),
    ("q15", "(sin consumir siguiente carácter)",     "q0",  "Emitir BANDERA_N"),
    ("q16", "<code>i</code> / <code>I</code>",        "q17", "-"),
    ("q16", "<code>f</code> / <code>F</code>",        "q18", "-"),
    ("q16", "otro / EOF",                            "q0",  "ERROR: bandera no reconocida"),
    ("q17", "(sin consumir siguiente carácter)",     "q0",  "Emitir BANDERA_JI"),
    ("q18", "(sin consumir siguiente carácter)",     "q0",  "Emitir BANDERA_JF"),
    ("q19", "(sin consumir siguiente carácter)",     "q0",  "Emitir MENOR"),
    ("q20", "(sin consumir siguiente carácter)",     "q0",  "Emitir MAYOR"),
    ("q21", "dígito [0-9]",                          "q21", "Seguir acumulando dígitos extra"),
    ("q21", "no-dígito / EOF",                       "q0",  "ERROR: demasiados dígitos"),
]

TOKEN_REGEX_TABLE = [
    ("RESULTADO",    "RESULTADO",
     "(R|r)(E|e)(S|s)(U|u)(L|l)(T|t)(A|a)(D|d)(O|o)"),
    ("VS",           "VS",
     "(V|v)(S|s)"),
    ("TEMPORADA",    "TEMPORADA",
     "(T|t)(E|e)(M|m)(P|p)(O|o)(R|r)(A|a)(D|d)(A|a)"),
    ("JORNADA",      "JORNADA",
     "(J|j)(O|o)(R|r)(N|n)(A|a)(D|d)(A|a)"),
    ("GOLES",        "GOLES",
     "(G|g)(O|o)(L|l)(E|e)(S|s)"),
    ("LOCAL",        "LOCAL",
     "(L|l)(O|o)(C|c)(A|a)(L|l)"),
    ("VISITANTE",    "VISITANTE",
     "(V|v)(I|i)(S|s)(I|i)(T|t)(A|a)(N|n)(T|t)(E|e)"),
    ("TOTAL",        "TOTAL",
     "(T|t)(O|o)(T|t)(A|a)(L|l)"),
    ("TABLA",        "TABLA",
     "(T|t)(A|a)(B|b)(L|l)(A|a)"),
    ("PARTIDOS",     "PARTIDOS",
     "(P|p)(A|a)(R|r)(T|t)(I|i)(D|d)(O|o)(S|s)"),
    ("TOP",          "TOP",
     "(T|t)(O|o)(P|p)"),
    ("SUPERIOR",     "SUPERIOR",
     "(S|s)(U|u)(P|p)(E|e)(R|r)(I|i)(O|o)(R|r)"),
    ("INFERIOR",     "INFERIOR",
     "(I|i)(N|n)(F|f)(E|e)(R|r)(I|i)(O|o)(R|r)"),
    ("ADIOS",        "ADIOS",
     "(A|a)(D|d)(I|i)(O|o)(S|s)"),
    ("BANDERA_F",    "-f",
     "-(f|F)"),
    ("BANDERA_N",    "-n",
     "-(n|N)"),
    ("BANDERA_JI",   "-ji",
     "-(j|J)(i|I)"),
    ("BANDERA_JF",   "-jf",
     "-(j|J)(f|F)"),
    ("CADENA",       '"texto"',
     '"([^"\\n])*"'),
    ("TEMPORADA_VAL","AAAA-AAAA",
     "[0-9][0-9][0-9][0-9]-[0-9][0-9][0-9][0-9]"),
    ("NUMERO",       "N (1-2 dígitos)",
     "[0-9][0-9]?"),
    ("MENOR",        "<",
     "<"),
    ("MAYOR",        ">",
     ">"),
]


def _row(cells, tag='td'):
    return '<tr>' + ''.join(f'<{tag}>{c}</{tag}>' for c in cells) + '</tr>'


def generate_metodo_arbol():
    _ensure_dir()
    path = os.path.join(REPORTES_DIR, 'Metodo_Arbol.html')

    # --- Tabla de tokens ---
    tok_rows = ''.join(
        _row([tok, lex, f'<code>{rx}</code>'])
        for tok, lex, rx in TOKEN_REGEX_TABLE
    )

    # --- Nullable ---
    nul_rows = ''.join(
        _row([n, nodo, val])
        for n, (nodo, tipo, val) in enumerate(NULLABLE_TABLE, 1)
    )

    # --- Firstpos ---
    fp_rows = ''.join(
        _row([n, nodo, val])
        for n, (nodo, val) in enumerate(FIRSTPOS_TABLE, 1)
    )

    # --- Lastpos ---
    lp_rows = ''.join(
        _row([n, nodo, val])
        for n, (nodo, val) in enumerate(LASTPOS_TABLE, 1)
    )

    # --- Followpos ---
    fol_rows = ''.join(
        f'<tr><td class="c">{pos}</td><td><code>{sym}</code></td>'
        f'<td class="c"><b>{fp}</b></td><td class="small">{calc}</td></tr>'
        for pos, sym, fp, calc in FOLLOWPOS_TABLE
    )

    # --- DFA States (NUMERO example) ---
    dfa_st_rows = ''.join(
        _row([st, conj, tipo, acc])
        for st, conj, tipo, acc in DFA_STATES
    )

    # --- DFA Transitions (NUMERO example) ---
    dfa_tr_rows = ''.join(
        _row([est, inp, sig, raz])
        for est, inp, sig, raz in DFA_TRANSITIONS
    )

    # --- Full AFD States (all 22) ---
    full_st_rows = ''.join(
        f'<tr><td><code><b>{st}</b></code></td><td>{desc}</td>'
        f'<td class="c">{marca}</td><td class="c">{acepta}</td><td>{token}</td></tr>'
        for st, desc, marca, acepta, token in FULL_AFD_STATES
    )

    # --- Full AFD Transitions ---
    full_tr_rows = ''.join(
        f'<tr><td><code>{est}</code></td><td>{inp}</td>'
        f'<td><code>{sig}</code></td><td>{accion}</td></tr>'
        for est, inp, sig, accion in FULL_AFD_TRANSITIONS
    )

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Metodo del Arbol - LigaBot</title>
<style>
  *{{margin:0;padding:0;box-sizing:border-box}}
  body{{font-family:'Segoe UI',Arial,sans-serif;background:#edf3ee;color:#222;font-size:.92rem}}
  header{{background:#0d3b2e;color:#fff;padding:16px 28px}}
  header h1{{font-size:1.25rem;font-weight:600}}
  header p{{font-size:.82rem;color:#7fc4a0;margin-top:3px}}
  main{{padding:28px;max-width:1050px;margin:0 auto}}
  section{{margin-bottom:36px}}
  h2{{color:#0d3b2e;font-size:1.1rem;border-left:4px solid #0d3b2e;padding-left:10px;margin-bottom:14px}}
  h3{{color:#2e7d8c;font-size:.95rem;margin:18px 0 8px}}
  p{{margin-bottom:10px;line-height:1.6}}
  table{{width:100%;border-collapse:collapse;background:#fff;border-radius:8px;
         overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,.08);margin-bottom:14px}}
  thead tr{{background:#0d3b2e;color:#fff}}
  th,td{{padding:9px 13px;text-align:left;border-bottom:1px solid #cde3d4;vertical-align:top}}
  tbody tr:hover{{background:#f0f6f2}}
  tbody tr:last-child td{{border-bottom:none}}
  code{{background:#e4f2ea;padding:1px 5px;border-radius:3px;font-size:.85rem;color:#b83232}}
  .c{{text-align:center;font-weight:bold}}
  .small{{font-size:.8rem;color:#555}}
  .tree-box{{background:#fff;border-radius:8px;box-shadow:0 2px 8px rgba(0,0,0,.08);
             padding:20px 28px;font-family:'Consolas',monospace;font-size:.88rem;
             line-height:1.8;white-space:pre}}
  .node-accept{{color:#27ae60;font-weight:bold}}
  .node-start{{color:#e67e22;font-weight:bold}}
  .highlight{{background:#fef9e7;border-left:3px solid #f39c12;padding:10px 14px;
              border-radius:0 6px 6px 0;margin:12px 0}}
  .formula{{background:#e4f2ea;border-left:3px solid #2e7d8c;padding:10px 14px;
            border-radius:0 6px 6px 0;margin:10px 0;font-family:'Consolas',monospace}}
  .accept-row{{background:#f0fff4}}
  .error-row{{background:#fff5f5}}
  .diagram-img{{max-width:100%;border-radius:8px;box-shadow:0 2px 12px rgba(0,0,0,.12);
               display:block;margin:14px auto}}
  .diagram-caption{{text-align:center;font-size:.82rem;color:#666;margin-top:4px;margin-bottom:18px}}
</style>
</head>
<body>
<header>
  <h1>Metodo del Arbol - LigaBot</h1>
  <p>Construcción directa del AFD a partir de la expresión regular (Fase 1)</p>
</header>
<main>

<!-- 1. Especificación de tokens -->
<section>
<h2>1. Especificación de Tokens y Expresiones Regulares</h2>
<p>La siguiente tabla define cada token del lenguaje LigaBot con su expresión regular
correspondiente. Las palabras reservadas son <em>case-insensitive</em>.</p>
<table>
  <thead><tr><th>Token</th><th>Lexema / Patrón</th><th>Expresión Regular</th></tr></thead>
  <tbody>{tok_rows}</tbody>
</table>
</section>

<!-- 2. Expresión regular combinada -->
<section>
<h2>2. Expresión Regular Combinada</h2>
<p>La expresión regular que reconoce <em>cualquier</em> token del lenguaje es la unión de todas
las expresiones individuales:</p>
<div class="formula">
R = token₁ | token₂ | … | token₂₃
  = (R|r)(E|e)… | (V|v)(S|s) | … | [0-9][0-9]? | &lt; | &gt;
</div>
<p>Para el método del árbol se aumenta la expresión con el símbolo marcador <code>#</code>:</p>
<div class="formula">R_aug = R · #</div>
<div class="highlight">
  <strong>Nota académica:</strong> por la extensión de la expresión combinada (más de 300 nodos
  hoja para las 23 categorías), se aplica el método completo sobre el token
  <strong>NÚMERO</strong> (<code>[0-9][0-9]?</code>) como caso representativo.
  Este token es idóneo porque cubre los operadores ·, | y ε que aparecen en todos los
  demás patrones. El AFD completo de los 22 estados se muestra en la sección 10.
</div>
</section>

<!-- 3. Expresión aumentada para NÚMERO -->
<section>
<h2>3. Expresión Aumentada para el Token NÚMERO</h2>
<p>El patrón <code>[0-9][0-9]?</code> se reescribe eliminando el operador <code>?</code>
(azúcar sintáctica):</p>
<div class="formula">[0-9]([0-9])?  ->  d · (d | ε)</div>
<p>Donde <strong>d</strong> representa cualquier dígito <code>[0-9]</code>. La expresión
aumentada queda:</p>
<div class="formula">R_aug = (d · (d | ε)) · #</div>
<p>Asignamos una posición a cada hoja (símbolo no-épsilon):</p>
<table>
  <thead><tr><th>Posición</th><th>Símbolo</th><th>Descripción</th></tr></thead>
  <tbody>
    <tr><td class="c">1</td><td><code>d</code></td><td>Primer dígito (obligatorio)</td></tr>
    <tr><td class="c">2</td><td><code>d</code></td><td>Segundo dígito (opcional)</td></tr>
    <tr><td class="c">3</td><td><code>#</code></td><td>Marcador de fin (aumentado)</td></tr>
  </tbody>
</table>
</section>

<!-- 4. Árbol sintáctico -->
<section>
<h2>4. Árbol Sintáctico</h2>
<p>La expresión <code>(d[1] · (d[2] | ε)) · #[3]</code> genera el siguiente árbol:</p>
<div class="tree-box">
               · ← raíz (CONCAT)
              / \\
             ·   #[3]
        (CONCAT) \\
            / \\   posición 3
         d[1]  |
    (pos 1)  (OR)
             / \\
           d[2]  ε
         (pos 2)
</div>
</section>

<!-- imagen árbol -->
<section>
<h2>4b. Diagrama - Arbol Sintactico</h2>
<img src="../assets/arbol.png" alt="Árbol Sintáctico" class="diagram-img">
<p class="diagram-caption">Árbol sintáctico de la expresión aumentada  R_aug = (d[1] · (d[2] | ε)) · #[3]</p>
</section>

<!-- 5. Anulabilidad -->
<section>
<h2>5. Anulabilidad (nullable)</h2>
<p>Reglas: hoja-símbolo -> false; hoja-ε -> true; OR -> nullable(L) OR nullable(R);
CONCAT -> nullable(L) AND nullable(R).</p>
<table>
  <thead><tr><th>#</th><th>Nodo</th><th>Tipo</th><th>nullable</th></tr></thead>
  <tbody>{nul_rows}</tbody>
</table>
</section>

<!-- 6. Primeros (firstpos) -->
<section>
<h2>6. Primeros (firstpos)</h2>
<p>Reglas: hoja-d -> {{pos}}; hoja-ε -> ∅; OR -> fp(L) ∪ fp(R);
CONCAT c₁·c₂ -> nullable(c₁)? fp(c₁)∪fp(c₂) : fp(c₁).</p>
<table>
  <thead><tr><th>#</th><th>Nodo</th><th>firstpos</th></tr></thead>
  <tbody>{fp_rows}</tbody>
</table>
</section>

<!-- 7. Últimos (lastpos) -->
<section>
<h2>7. Últimos (lastpos)</h2>
<p>Reglas: hoja-d -> {{pos}}; hoja-ε -> ∅; OR -> lp(L) ∪ lp(R);
CONCAT c₁·c₂ -> nullable(c₂)? lp(c₁)∪lp(c₂) : lp(c₂).</p>
<table>
  <thead><tr><th>#</th><th>Nodo</th><th>lastpos</th></tr></thead>
  <tbody>{lp_rows}</tbody>
</table>
</section>

<!-- 8. Followpos -->
<section>
<h2>8. Siguientes (followpos)</h2>
<p>Para cada nodo CONCAT c₁·c₂: ∀p ∈ lastpos(c₁), followpos(p) ∪= firstpos(c₂).</p>
<table>
  <thead><tr><th>Pos</th><th>Símbolo</th><th>followpos</th><th>Cálculo</th></tr></thead>
  <tbody>{fol_rows}</tbody>
</table>
</section>

<!-- 9. Construcción del AFD (NÚMERO) -->
<section>
<h2>9. Construcción del AFD para NÚMERO</h2>
<p>Con la tabla de followpos calculada se aplica el algoritmo de construcción directa
del AFD. El alfabeto de entrada es Σ = {{ d }}, donde <em>d</em> representa cualquier
dígito [0-9]. La posición del marcador es 3.</p>

<h3>Algoritmo de construcción — paso a paso</h3>
<div class="highlight">
  <strong>Reglas del algoritmo:</strong><br>
  1. El estado inicial del AFD es <code>firstpos(raíz) = {{1}}</code>.<br>
  2. Un estado es de aceptación si su conjunto contiene la posición 3 (marcador #).<br>
  3. Para cada estado S y cada símbolo a ∈ Σ: el estado destino es
     <code>U {{ followpos(p) | p ∈ S  AND  symbol(p) = a }}</code>.<br>
  4. Si el conjunto resultante es vacío, la transición va a un estado muerto (rechaza).<br>
  5. Repetir hasta que no haya estados nuevos sin procesar.
</div>

<table>
  <thead><tr>
    <th>Paso</th><th>Estado actual</th><th>Símbolo</th>
    <th>Posiciones con ese símbolo</th><th>followpos aplicado</th><th>Estado destino</th>
  </tr></thead>
  <tbody>
    <tr>
      <td class="c">1</td>
      <td><strong>A = {{1}}</strong> (inicial)</td>
      <td><code>d</code></td>
      <td>{{1}} — pos 1 tiene símbolo d</td>
      <td>followpos(1) = {{2, 3}}</td>
      <td class="node-accept"><strong>B = {{2,3}}</strong> — acepta (contiene 3)</td>
    </tr>
    <tr>
      <td class="c">2</td>
      <td class="node-accept"><strong>B = {{2,3}}</strong></td>
      <td><code>d</code></td>
      <td>{{2}} — pos 2 tiene símbolo d (pos 3 tiene #, no d)</td>
      <td>followpos(2) = {{3}}</td>
      <td class="node-accept"><strong>C = {{3}}</strong> — acepta (contiene 3)</td>
    </tr>
    <tr>
      <td class="c">3</td>
      <td class="node-accept"><strong>C = {{3}}</strong></td>
      <td><code>d</code></td>
      <td>∅ — pos 3 tiene símbolo #, no d</td>
      <td>∅ (conjunto vacío)</td>
      <td>Estado muerto (rechaza)</td>
    </tr>
  </tbody>
</table>

<p>El algoritmo termina: no hay estados nuevos por procesar. El AFD resultante tiene
<strong>3 estados</strong> (A, B, C), dos de ellos de aceptación.</p>

<h3>Estados del AFD (NÚMERO)</h3>
<table>
  <thead><tr><th>Estado</th><th>Conjunto de posiciones</th><th>Tipo</th><th>¿Acepta?</th></tr></thead>
  <tbody>{dfa_st_rows}</tbody>
</table>

<h3>Tabla de transiciones (NÚMERO)</h3>
<table>
  <thead><tr><th>Estado actual</th><th>Entrada</th><th>Estado siguiente</th><th>Razón</th></tr></thead>
  <tbody>{dfa_tr_rows}</tbody>
</table>

<h3>Diagrama del AFD (NUMERO)</h3>
<div class="tree-box">
  <span class="node-start">[A={{1}}]</span>  ---- d ---->  <span class="node-accept">((B={{2,3}}))</span>  ---- d ---->  <span class="node-accept">((C={{3}}))</span>

                              (acepta 1 digito)          (acepta 2 digitos)

  Verificacion:
    "5"   : A --(d)--> B                    [OK]  acepta 1 digito
    "38"  : A --(d)--> B --(d)--> C         [OK]  acepta 2 digitos
    "100" : A --(d)--> B --(d)--> C --(d)--> muerto   [rechaza: 3 digitos]
</div>
</section>

<!-- imagen AFD NUMERO -->
<section>
<h2>9b. Diagrama - AFD para NUMERO (3 estados)</h2>
<img src="../assets/tabla de siguientes.png" alt="Tablas método del árbol" class="diagram-img">
<p class="diagram-caption">Tablas nullable, firstpos, lastpos y followpos del token NÚMERO</p>
</section>

<!-- 10. AFD completo 22 estados -->
<section>
<h2>10. AFD Completo del Analizador Lexico LigaBot - 22 Estados (q0-q21)</h2>
<p>Aplicando el metodo del arbol a la expresion regular combinada de todos los tokens se
obtiene un AFD con <strong>22 estados</strong>. Cada estado corresponde a una etapa de
reconocimiento distinta. Los estados marcados como <strong>Si</strong> en la columna Acepta
son de aceptacion inmediata: emiten el token correspondiente sin consumir el caracter siguiente.</p>

<h3>Tabla de estados</h3>
<table>
  <thead><tr>
    <th>Estado</th><th>Descripción</th>
    <th class="c">Acepta</th><th class="c">¿Acepta?</th>
    <th>Token emitido / acción</th>
  </tr></thead>
  <tbody>{full_st_rows}</tbody>
</table>

<h3>Tabla de transiciones completa</h3>
<table>
  <thead><tr>
    <th>Estado actual</th><th>Entrada</th>
    <th>Estado siguiente</th><th>Acción</th>
  </tr></thead>
  <tbody>{full_tr_rows}</tbody>
</table>

<div class="highlight">
  <strong>Estados de aceptación inmediata</strong> (q10, q12, q14, q15, q17, q18, q19, q20):
  cuando el AFD llega a uno de estos estados, emite el token y regresa a q0
  <em>sin consumir</em> el carácter actual - ese carácter lo evaluará q0 en la siguiente
  iteración del ciclo principal.
</div>
</section>

<!-- imágenes AFD completo -->
<section>
<h2>10b. Diagrama - AFD Completo (22 estados)</h2>
<img src="../assets/Automata finito determinista.png" alt="AFD Completo 22 estados" class="diagram-img">
<p class="diagram-caption">Autómata Finito Determinista completo del Analizador Léxico LigaBot (q0 - q21)</p>
</section>

<section>
<h2>10c. Tabla de Transiciones Completa</h2>
<img src="../assets/Tabla de transacciones.png" alt="Tabla de transiciones" class="diagram-img">
<p class="diagram-caption">Tabla de transiciones del AFD completo con todas las 47 transiciones (q0 - q21)</p>
</section>

<!-- 11. Coherencia con el lexer -->
<section>
<h2>11. Coherencia entre el AFD y el Analizador Léxico Implementado</h2>
<p>El método <code>analyze()</code> en <code>lexer.py</code> implementa el AFD completo
(22 estados) mediante un único bucle <code>while</code>. La variable <code>state</code>
almacena el estado actual (q0-q21); en cada iteración se evalúa el par
(estado, carácter) y se avanza al estado siguiente.</p>
<table>
<thead><tr><th>Método</th><th>Descripción</th></tr></thead>
<tbody>
<tr><td><code>analyze()</code></td>
    <td>Bucle principal del AFD. Evalúa el par (estado, carácter) y ejecuta la
    transición correspondiente. Retorna <code>(tokens, errores)</code>.</td></tr>
<tr><td><code>_char()</code></td>
    <td>Retorna el carácter actual <em>sin consumirlo</em> (lookahead de 1 carácter).
    Retorna <code>None</code> al llegar al EOF.</td></tr>
<tr><td><code>_advance()</code></td>
    <td>Consume el carácter actual, actualiza <code>fila</code>/<code>columna</code>
    y lo retorna.</td></tr>
<tr><td><code>_emit(lexema, tipo, fila, col)</code></td>
    <td>Añade un <code>Token</code> a la lista de tokens reconocidos.</td></tr>
<tr><td><code>_emit_error(lexema, desc, fila, col)</code></td>
    <td>Añade un <code>LexicalError</code> a la lista de errores léxicos
    (recuperación en modo pánico: se descarta el lexema y se continúa desde q0).</td></tr>
</tbody>
</table>
<ul style="margin-left:20px;line-height:2">
  <li><strong>q0 (inicial):</strong> decide qué tipo de token comienza según el primer carácter.</li>
  <li><strong>q1:</strong> acumula letras; emite palabra reservada (o error) al encontrar un no-letra.</li>
  <li><strong>q2-q3:</strong> acumulan dígitos; emiten NUMERO (1 ó 2 dígitos) al salir del patrón.</li>
  <li><strong>q4-q10:</strong> detectan el patrón <code>DDDD-DDDD</code> para TEMPORADA_VAL.</li>
  <li><strong>q11-q12:</strong> reconocen cadenas entre comillas dobles.</li>
  <li><strong>q13-q18:</strong> reconocen las cuatro banderas (<code>-f</code>, <code>-n</code>, <code>-ji</code>, <code>-jf</code>).</li>
  <li><strong>q19, q20:</strong> emiten los tokens de un solo carácter MENOR y MAYOR.</li>
  <li><strong>q21:</strong> estado de error por desbordamiento (más de 4 dígitos consecutivos).</li>
</ul>
<div class="highlight">
  El analizador léxico <strong>no utiliza ninguna librería externa</strong> de análisis léxico
  ni backtracking. El lookahead de un carácter (<code>_char()</code> sin consumir) es
  suficiente para decidir cada transición del AFD.
</div>
</section>

</main>
</body>
</html>"""

    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    return path
