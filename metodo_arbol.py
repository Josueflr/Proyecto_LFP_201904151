import os
from reporter import REPORTES_DIR, _ensure_dir, open_report



NULLABLE_TABLE = [
    ("d[1]",          "hoja — símbolo",         "false"),
    ("d[2]",          "hoja — símbolo",         "false"),
    ("ε",             "hoja — épsilon",          "true"),
    ("d[2] | ε",      "nodo OR",                 "nullable(d[2]) OR nullable(ε) = false OR true = <b>true</b>"),
    ("d[1] · (d[2]|ε)", "nodo CONCAT",          "nullable(d[1]) AND nullable(d[2]|ε) = false AND true = <b>false</b>"),
    ("#[3]",          "hoja — símbolo",         "false"),
    ("(d[1]·(d[2]|ε)) · #[3]", "raíz CONCAT", "nullable(left) AND nullable(#) = false AND false = <b>false</b>"),
]

FIRSTPOS_TABLE = [
    ("d[1]",                      "{1}"),
    ("d[2]",                      "{2}"),
    ("ε",                         "∅"),
    ("d[2] | ε",                  "firstpos(d[2]) ∪ firstpos(ε) = {2} ∪ ∅ = <b>{2}</b>"),
    ("d[1] · (d[2]|ε)",          "nullable(d[1])=false → <b>firstpos(d[1]) = {1}</b>"),
    ("#[3]",                      "{3}"),
    ("(d[1]·(d[2]|ε)) · #[3]",  "nullable(left)=false → <b>firstpos(left) = {1}</b>"),
]

LASTPOS_TABLE = [
    ("d[1]",                      "{1}"),
    ("d[2]",                      "{2}"),
    ("ε",                         "∅"),
    ("d[2] | ε",                  "lastpos(d[2]) ∪ lastpos(ε) = {2} ∪ ∅ = <b>{2}</b>"),
    ("d[1] · (d[2]|ε)",          "nullable(d[2]|ε)=true → lastpos(d[1]) ∪ lastpos(d[2]|ε) = {1} ∪ {2} = <b>{1,2}</b>"),
    ("#[3]",                      "{3}"),
    ("(d[1]·(d[2]|ε)) · #[3]",  "nullable(#)=false → <b>lastpos(#[3]) = {3}</b>"),
]

FOLLOWPOS_TABLE = [
    (1, "d", "{2,3}",
     "Desde d[1]·(d[2]|ε): ∀i ∈ lastpos(d[1])={1} → followpos(1) ∪= firstpos(d[2]|ε)={2} → {2}<br>"
     "Desde raíz: ∀i ∈ lastpos(left)={1,2} → followpos(1) ∪= firstpos(#[3])={3} → {2,3}"),
    (2, "d", "{3}",
     "Desde raíz: ∀i ∈ lastpos(left)={1,2} → followpos(2) ∪= firstpos(#[3])={3} → {3}"),
    (3, "#", "∅",
     "Posición marcadora — no genera followpos"),
]

DFA_STATES = [
    ("A", "{1}",   "Inicial",         "No"),
    ("B", "{2,3}", "—",               "Sí  (contiene pos 3)"),
    ("C", "{3}",   "—",               "Sí  (contiene pos 3)"),
]

DFA_TRANSITIONS = [
    ("A = {1}",   "d (0–9)", "B = {2,3}", "followpos(1) = {2,3}"),
    ("B = {2,3}", "d (0–9)", "C = {3}",   "followpos(2) = {3}  (pos 3 tiene símbolo #, no d)"),
    ("C = {3}",   "—",       "muerto",    "pos 3 solo tiene símbolo #"),
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

    # --- DFA States ---
    dfa_st_rows = ''.join(
        _row([st, conj, tipo, acc])
        for st, conj, tipo, acc in DFA_STATES
    )

    # --- DFA Transitions ---
    dfa_tr_rows = ''.join(
        _row([est, inp, sig, raz])
        for est, inp, sig, raz in DFA_TRANSITIONS
    )

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Método del Árbol — LigaBot</title>
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
</style>
</head>
<body>
<header>
  <h1>Método del Árbol — LigaBot</h1>
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
  demás patrones.
</div>
</section>

<!-- 3. Expresión aumentada para NÚMERO -->
<section>
<h2>3. Expresión Aumentada para el Token NÚMERO</h2>
<p>El patrón <code>[0-9][0-9]?</code> se reescribe eliminando el operador <code>?</code>
(azúcar sintáctica):</p>
<div class="formula">[0-9]([0-9])?  →  d · (d | ε)</div>
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

<!-- 5. Anulabilidad -->
<section>
<h2>5. Anulabilidad (nullable)</h2>
<p>Reglas: hoja-símbolo → false; hoja-ε → true; OR → nullable(L) OR nullable(R);
CONCAT → nullable(L) AND nullable(R).</p>
<table>
  <thead><tr><th>#</th><th>Nodo</th><th>Tipo</th><th>nullable</th></tr></thead>
  <tbody>{nul_rows}</tbody>
</table>
</section>

<!-- 6. Primeros (firstpos) -->
<section>
<h2>6. Primeros (firstpos)</h2>
<p>Reglas: hoja-d → {{pos}}; hoja-ε → ∅; OR → fp(L) ∪ fp(R);
CONCAT c₁·c₂ → nullable(c₁)? fp(c₁)∪fp(c₂) : fp(c₁).</p>
<table>
  <thead><tr><th>#</th><th>Nodo</th><th>firstpos</th></tr></thead>
  <tbody>{fp_rows}</tbody>
</table>
</section>

<!-- 7. Últimos (lastpos) -->
<section>
<h2>7. Últimos (lastpos)</h2>
<p>Reglas: hoja-d → {{pos}}; hoja-ε → ∅; OR → lp(L) ∪ lp(R);
CONCAT c₁·c₂ → nullable(c₂)? lp(c₁)∪lp(c₂) : lp(c₂).</p>
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

<!-- 9. Construcción del AFD -->
<section>
<h2>9. Construcción del AFD</h2>
<p>El estado inicial es <strong>firstpos(raíz) = {{1}}</strong>. Un estado es de aceptación
si contiene la posición del marcador (#) = 3.</p>

<h3>Estados del AFD</h3>
<table>
  <thead><tr><th>Estado</th><th>Conjunto de posiciones</th><th>Tipo</th><th>¿Acepta?</th></tr></thead>
  <tbody>{dfa_st_rows}</tbody>
</table>

<h3>Tabla de transiciones</h3>
<table>
  <thead><tr><th>Estado actual</th><th>Entrada</th><th>Estado siguiente</th><th>Razón</th></tr></thead>
  <tbody>{dfa_tr_rows}</tbody>
</table>

<h3>Diagrama del AFD</h3>
<div class="tree-box">
  <span class="node-start">→ [A={1}]</span>  ──── d ────►  <span class="node-accept">((B={2,3}))</span>  ──── d ────►  <span class="node-accept">((C={3}))</span>
                                                                           │
                                              (estado de aceptación)      (estado de aceptación)

  Verificación:
    "5"   → A →(d)→ B  ✔  acepta (1 dígito)
    "38"  → A →(d)→ B →(d)→ C  ✔  acepta (2 dígitos)
    "100" → A →(d)→ B →(d)→ C →(d)→ muerto  ✘  rechaza (3 dígitos)
</div>
</section>

<!-- 10. Coherencia con el lexer -->
<section>
<h2>10. Coherencia entre el AFD y el Analizador Léxico Implementado</h2>
<p>El método <code>_lex_number_or_season()</code> en <code>lexer.py</code> implementa
directamente los estados del AFD anterior:</p>
<ul style="margin-left:20px;line-height:2">
  <li><strong>Estado A:</strong> se entra cuando el carácter actual es un dígito.</li>
  <li><strong>Estado B:</strong> después de consumir el primer dígito; si el siguiente también
      es dígito, se avanza (transición B→C); si no, se emite NUMERO.</li>
  <li><strong>Estado C:</strong> después del segundo dígito; si hay un tercer dígito se
      continúa acumulando para detectar una posible temporada (AAAA-AAAA).</li>
  <li>Si se acumulan exactamente 4 dígitos y el siguiente carácter es <code>-</code>, se
      intenta reconocer una TEMPORADA_VAL; si falla, se reporta error léxico.</li>
</ul>
<div class="highlight">
  El analizador léxico <strong>no utiliza ninguna librería externa</strong> de análisis léxico.
  Toda la lógica se construyó manualmente en Python siguiendo los estados derivados del
  método del árbol.
</div>
</section>

</main>
</body>
</html>"""

    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    return path
