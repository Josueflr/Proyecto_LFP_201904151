
import sys, os, pathlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lexer import Lexer, TokenType

_PASS = 0
_FAIL = 0

def run(text):
    return Lexer(text).analyze()

def ok(desc, condition, detail=""):
    global _PASS, _FAIL
    if condition:
        print(f"  PASS  {desc}")
        _PASS += 1
    else:
        print(f"  FAIL  {desc}  -->  {detail}")
        _FAIL += 1

def check(desc, text, exp_tok, exp_err, exp_types=None):
    t, e = run(text)
    types_ok = True
    if exp_types is not None:
        types_ok = [x.token_type for x in t] == exp_types
    cond = (len(t) == exp_tok) and (len(e) == exp_err) and types_ok
    detail = f"tokens={len(t)} (esp {exp_tok}), errores={len(e)} (esp {exp_err})"
    if exp_types and len(t) == exp_tok and not types_ok:
        detail += f" | tipos={[x.token_type for x in t]}"
    ok(desc, cond, detail)

print("=" * 62)
print("  LigaBot Lexer — Tests Automaticos Fase 1")
print("=" * 62)

print("\n[1] Palabras reservadas — MAYUSCULAS (1 token c/u, 0 errores)")
for w in ['RESULTADO', 'VS', 'TEMPORADA', 'JORNADA', 'GOLES',
          'LOCAL', 'VISITANTE', 'TOTAL', 'TABLA', 'PARTIDOS',
          'TOP', 'SUPERIOR', 'INFERIOR', 'ADIOS']:
    check(w, w, 1, 0, [w])

print("\n[2] Palabras reservadas — minusculas (case-insensitive)")
for w in ['resultado', 'vs', 'temporada', 'jornada', 'goles',
          'local', 'visitante', 'total', 'tabla', 'partidos',
          'top', 'superior', 'inferior', 'adios']:
    check(w, w, 1, 0, [w.upper()])

# ---------------------------------------------------------
print("\n[3] Palabras reservadas — MiXtO")
casos = [
    ('Resultado',   'RESULTADO'),  ('rEsUlTaDo',  'RESULTADO'),
    ('TeMpOrAdA',   'TEMPORADA'),  ('GoLeS',       'GOLES'),
    ('LoCaL',       'LOCAL'),      ('ViSiTaNtE',   'VISITANTE'),
    ('ToTaL',       'TOTAL'),      ('TaBLa',        'TABLA'),
    ('PaRtIdOs',    'PARTIDOS'),   ('SuPeRiOr',    'SUPERIOR'),
    ('InFeRiOr',    'INFERIOR'),   ('AdIoS',        'ADIOS'),
    ('Vs',          'VS'),         ('Top',          'TOP'),
    ('JoRnAdA',     'JORNADA'),
]
for w, typ in casos:
    check(w, w, 1, 0, [typ])

# ---------------------------------------------------------
print("\n[4] Banderas validas — todas las variantes de case")
for flag, typ in [
    ('-f',  'BANDERA_F'), ('-F',  'BANDERA_F'),
    ('-n',  'BANDERA_N'), ('-N',  'BANDERA_N'),
    ('-ji', 'BANDERA_JI'), ('-jI', 'BANDERA_JI'),
    ('-Ji', 'BANDERA_JI'), ('-JI', 'BANDERA_JI'),
    ('-jf', 'BANDERA_JF'), ('-jF', 'BANDERA_JF'),
    ('-Jf', 'BANDERA_JF'), ('-JF', 'BANDERA_JF'),
]:
    check(flag, flag, 1, 0, [typ])

# ---------------------------------------------------------
print("\n[5] Banderas invalidas (0 tokens, 1 error)")
for f in ['-a', '-b', '-c', '-d', '-e', '-g', '-h', '-k',
          '-m', '-o', '-p', '-q', '-r', '-s', '-t', '-u',
          '-v', '-w', '-x', '-y', '-z',
          '-jk', '-jz', '-ja', '-jb', '-jJ', '-jX', '--']:
    check(f, f, 0, 1)

print("\n[5b] Bandera incompleta al final de entrada")
check("'-' solo", '-', 0, 1)
check("'-j' solo", '-j', 0, 1)
check("'-J' solo", '-J', 0, 1)

# ---------------------------------------------------------
print("\n[6] Cadenas validas (1 token CADENA, 0 errores)")
cadenas = [
    '"Real Madrid"', '"Betis"', '"Rayo Vallecano"',
    '"AD Almeria"', '"Sporting de Gijon"', '"Barcelona"',
    '"Las Palmas"', '"CD Malaga"', '"Athletic Club"',
    '"Real Sociedad"', '"a"', '"123"',
    '"equipo con espacios y numeros 99"',
    '""',                  # cadena vacia
    '"  "',                # solo espacios
    '"<>"',                # simbolos dentro de cadena
    '"RESULTADO"',         # palabra reservada dentro de cadena
    '"jornada_1"',         # underscore dentro de cadena (valido)
    '"tabla_2023"',        # underscore dentro de cadena (valido)
    '"-f"',                # bandera dentro de cadena
    '"1979-1980"',         # temporada dentro de cadena
    '"FC Barcelona"',
    '"Real Madrid CF"',
]
for s in cadenas:
    check(s, s, 1, 0, ['CADENA'])

# ---------------------------------------------------------
print("\n[7] Cadenas no cerradas (0 tokens, 1 error)")
for s in ['"Real Madrid', '"Betis', '"sin cerrar', '"',
          '"cadena sin cerrar RESULTADO']:
    t, e = run(s)
    ok(f"no cerrada {repr(s)[:45]}", len(t) == 0 and len(e) == 1,
       f"tokens={len(t)}, errores={len(e)}")


t, e = run('"abre\ncierra"')
ok("cadena con newline: 0 tokens, 3 errores (recovery)",
   len(t) == 0 and len(e) == 3,
   f"tokens={len(t)}, errores={len(e)}")

# ---------------------------------------------------------
print("\n[8] Temporadas validas (1 token TEMPORADA_VAL, 0 errores)")
for s in ['1979-1980', '2023-2024', '2000-2001', '1990-1991',
          '1899-1900', '9999-0000', '0000-0000', '1234-5678',
          '0001-9998', '1000-9999', '1111-2222']:
    check(s, s, 1, 0, ['TEMPORADA_VAL'])

# ---------------------------------------------------------
print("\n[9] Numeros validos 1-2 digitos (1 token NUMERO, 0 errores)")
for n in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
          '10', '11', '38', '99', '00', '01', '09']:
    check(f"NUMERO '{n}'", n, 1, 0, ['NUMERO'])

# ---------------------------------------------------------
print("\n[10] Numeros invalidos >2 digitos (0 token NUMERO/TEMPORADA, >=1 error)")
for n in ['100', '999', '1234', '00000', '123']:
    t, e = run(n)
    no_num  = all(x.token_type != 'NUMERO' for x in t)
    no_temp = all(x.token_type != 'TEMPORADA_VAL' for x in t)
    ok(f"invalido '{n}' -> no NUMERO/TEMPORADA, error",
       no_num and no_temp and len(e) >= 1,
       f"tipos={[x.token_type for x in t]}, errores={len(e)}")

# ---------------------------------------------------------
print("\n[11] Temporadas malformadas (sin TEMPORADA_VAL, >=1 error)")
for s in ['1979-198', '1979-19800', '1979-',
          '2023-202', '2023-20240', '9999-999']:
    t, e = run(s)
    no_temp = all(x.token_type != 'TEMPORADA_VAL' for x in t)
    ok(f"malformada '{s}'", no_temp and len(e) >= 1,
       f"tipos={[x.token_type for x in t]}, errores={len(e)}")

# ---------------------------------------------------------
print("\n[12] Simbolos < y >")
check("MENOR '<'",  '<',   1, 0, ['MENOR'])
check("MAYOR '>'",  '>',   1, 0, ['MAYOR'])
check("'< >'",      '< >', 2, 0, ['MENOR', 'MAYOR'])
check("'<>'",       '<>',  2, 0, ['MENOR', 'MAYOR'])

# ---------------------------------------------------------
print("\n[13] Caracteres no reconocidos (0 tokens, 1 error cada uno)")
for ch in list('$@!#%^&*()_=+[]{}|\\;:\',/?~`'):
    check(f"char '{ch}'", ch, 0, 1)
check("char '.'", '.', 0, 1)

# ---------------------------------------------------------
print("\n[14] Palabras no reconocidas (0 tokens, 1 error)")
for w in ['HOLA', 'mundo', 'EQUIPO', 'Jugador', 'Barcelona',
          'Madrid', 'abc', 'XYZ', 'RESULTADOS', 'TEMPORADAS',
          'JORNADAS', 'GOLESLOCAL', 'ADIOSO', 'TOPS',
          'TOTALMENTE', 'A', 'z']:
    check(f"'{w}'", w, 0, 1)

check("'INFERIOR2' = INFERIOR + NUMERO (2 tokens, 0 errores)", 'INFERIOR2', 2, 0,
      ['INFERIOR', 'NUMERO'])
check("'VS2' = VS + NUMERO (2 tokens, 0 errores)", 'VS2', 2, 0,
      ['VS', 'NUMERO'])

# ---------------------------------------------------------
print("\n[15] Fila y columna — tracking correcto")

t, e = run("RESULTADO\nVS")
ok("RESULTADO fila=1 col=1",
   len(t) == 2 and t[0].fila == 1 and t[0].columna == 1,
   f"got fila={t[0].fila if t else '?'}, col={t[0].columna if t else '?'}")
ok("VS fila=2 col=1",
   len(t) == 2 and t[1].fila == 2 and t[1].columna == 1,
   f"got fila={t[1].fila if len(t)>1 else '?'}, col={t[1].columna if len(t)>1 else '?'}")

t, e = run('RESULTADO "Betis"')
ok('"Betis" empieza en columna 11',
   len(t) == 2 and t[1].columna == 11,
   f'col={t[1].columna if len(t)>1 else "?"}')

t, e = run("GOLES\nLOCAL\n\"Betis\"")
ok("3 lineas: filas 1, 2, 3",
   len(t) == 3 and t[0].fila == 1 and t[1].fila == 2 and t[2].fila == 3,
   f"filas={[x.fila for x in t]}")

t, e = run("GOLES\n$LOCAL")
ok("$ en fila=2, col=1",
   len(e) >= 1 and e[0].fila == 2 and e[0].columna == 1,
   f"error fila={e[0].fila if e else '?'}, col={e[0].columna if e else '?'}")

t, e = run("TABLA $")
ok("$ columna=7 en 'TABLA $'",
   len(e) >= 1 and e[0].columna == 7,
   f"error col={e[0].columna if e else '?'}")

t, e = run("RESULTADO\n-f")
ok("-f en fila=2 col=1",
   len(t) == 2 and t[1].fila == 2 and t[1].columna == 1,
   f"-f: fila={t[1].fila if len(t)>1 else '?'}, col={t[1].columna if len(t)>1 else '?'}")

print("\n[16] Comandos completos validos — conteos CORRECTOS")

check('RESULTADO "Betis" VS "Rayo Vallecano" TEMPORADA <1979-1980>',
      'RESULTADO "Betis" VS "Rayo Vallecano" TEMPORADA <1979-1980>',
      8, 0)  

check('GOLES LOCAL "Betis" TEMPORADA <1979-1980>',
      'GOLES LOCAL "Betis" TEMPORADA <1979-1980>',
      7, 0)  

check('GOLES VISITANTE "Betis" TEMPORADA <1979-1980>',
      'GOLES VISITANTE "Betis" TEMPORADA <1979-1980>',
      7, 0)  

check('GOLES TOTAL "Betis" TEMPORADA <1979-1980>',
      'GOLES TOTAL "Betis" TEMPORADA <1979-1980>',
      7, 0) 

check('JORNADA 1 TEMPORADA <1979-1980>',
      'JORNADA 1 TEMPORADA <1979-1980>',
      6, 0) 

check('JORNADA 1 TEMPORADA <1979-1980> -f "jornada_1"',
      'JORNADA 1 TEMPORADA <1979-1980> -f "jornada_1"',
      8, 0)  

check('TABLA TEMPORADA <1979-1980>',
      'TABLA TEMPORADA <1979-1980>',
      5, 0)  

check('TABLA TEMPORADA <2023-2024> -f "tabla_2023"',
      'TABLA TEMPORADA <2023-2024> -f "tabla_2023"',
      7, 0)  

check('PARTIDOS "Betis" TEMPORADA <1979-1980>',
      'PARTIDOS "Betis" TEMPORADA <1979-1980>',
      6, 0)  

check('PARTIDOS "Betis" TEMPORADA <1979-1980> -ji 1 -jf 5 -f "partidos_betis"',
      'PARTIDOS "Betis" TEMPORADA <1979-1980> -ji 1 -jf 5 -f "partidos_betis"',
      12, 0)  

check('TOP SUPERIOR TEMPORADA <1979-1980>',
      'TOP SUPERIOR TEMPORADA <1979-1980>',
      6, 0) 

check('TOP SUPERIOR TEMPORADA <1979-1980> -n 3',
      'TOP SUPERIOR TEMPORADA <1979-1980> -n 3',
      8, 0)  

check('TOP INFERIOR TEMPORADA <1979-1980>',
      'TOP INFERIOR TEMPORADA <1979-1980>',
      6, 0) 

check('TOP INFERIOR TEMPORADA <2023-2024> -n 5',
      'TOP INFERIOR TEMPORADA <2023-2024> -n 5',
      8, 0)  

check('ADIOS', 'ADIOS', 1, 0)

print("\n[17] Comandos en minusculas y mixto")
check('resultado "Betis" vs "Rayo Vallecano" temporada <1979-1980>',
      'resultado "Betis" vs "Rayo Vallecano" temporada <1979-1980>',
      8, 0)
check('goles local "Barcelona" temporada <2023-2024>',
      'goles local "Barcelona" temporada <2023-2024>',
      7, 0)  
check('top superior temporada <1979-1980> -n 10',
      'top superior temporada <1979-1980> -n 10',
      8, 0)  
check('tabla temporada <1979-1980> -f "mi_tabla"',
      'tabla temporada <1979-1980> -f "mi_tabla"',
      7, 0)  

print("\n[18] Comandos con errores mixtos (tokens validos + errores)")

check('resultado$ "Betis" VS "Rayo Vallecano"',
      'resultado$ "Betis" VS "Rayo Vallecano"',
      4, 1)

check('GOLES LOCAL "Betis" TEMPORADA <1979-1980> @extra',
      'GOLES LOCAL "Betis" TEMPORADA <1979-1980> @extra',
      7, 2)  

check('TABLA TEMPORADA <1979-1980> -x',
      'TABLA TEMPORADA <1979-1980> -x',
      5, 1)  


check('TOP SUPERIOR TEMPORADA <1979-198> (6 tokens, 2 errores por recovery)',
      'TOP SUPERIOR TEMPORADA <1979-198>',
      6, 2)


check('PARTIDOS "Betis" TEMPORADA <1979-1980> -ji 100',
      'PARTIDOS "Betis" TEMPORADA <1979-1980> -ji 100',
      7, 1)  


check('"cadena sin cerrar RESULTADO', '"cadena sin cerrar RESULTADO', 0, 1)


print("\n[19] Casos borde especiales")

check("< 1979-1980 > (3 tokens)",
      '< 1979-1980 >', 3, 0, ['MENOR', 'TEMPORADA_VAL', 'MAYOR'])

check("-f \"archivo con espacios\" (2 tokens)",
      '-f "archivo con espacios"', 2, 0, ['BANDERA_F', 'CADENA'])

check("JORNADA 38 TEMPORADA <2023-2024> -ji 1 -jf 38 (10 tokens)",
      'JORNADA 38 TEMPORADA <2023-2024> -ji 1 -jf 38',
      10, 0) 

check('RESULTADO "FC Barcelona" VS "Real Madrid CF" TEMPORADA <1979-1980> (8 tokens)',
      'RESULTADO "FC Barcelona" VS "Real Madrid CF" TEMPORADA <1979-1980>',
      8, 0)

check("top inferior temporada <2023-2024> -n 1 (8 tokens)",
      'top inferior temporada <2023-2024> -n 1',
      8, 0)  

t, e = run('')
ok("Entrada vacia: 0 tokens, 0 errores", len(t) == 0 and len(e) == 0)


t, e = run('   \t  \n  \r\n  ')
ok("Solo blancos: 0 tokens, 0 errores", len(t) == 0 and len(e) == 0)


check("4 palabras reservadas seguidas",
      'RESULTADO VS TABLA ADIOS', 4, 0)


t, e = run('"RESULTADO"')
ok('"RESULTADO" dentro de cadena es CADENA, no RESULTADO',
   len(t) == 1 and t[0].token_type == 'CADENA')
check("underscore solo", '_', 0, 1)
check('"jornada_1" es CADENA valida', '"jornada_1"', 1, 0, ['CADENA'])
t, e = run('-fb')
ok("'-fb': BANDERA_F + error('b')",
   len(t) == 1 and t[0].token_type == 'BANDERA_F' and len(e) == 1,
   f"tokens={[x.token_type for x in t]}, errores={len(e)}")


check("'9abc' = NUMERO + error", '9abc', 1, 1)
check('cadena vacia ""', '""', 1, 0, ['CADENA'])


t, e = run('$ @ ! # %')
ok("5 errores de caracter invalido", len(t) == 0 and len(e) == 5,
   f"tokens={len(t)}, errores={len(e)}")

print("\n[20] Verificacion de restriccion: NO usar librerias prohibidas")
import ast as _ast

LIBS_PROHIBIDAS = {
    're',           # modulo regex de Python
    'ply',          # PLY (Python Lex-Yacc)
    'antlr4',       # ANTLR runtime
    'sly',          # SLY lexer
    'lark',         # Lark parser
    'pyparsing',    # PyParsing
    'nltk',         # Natural Language Toolkit
    'spacy',        # spaCy NLP
    'tokenize',     # tokenizador de Python (tokenize.tokenize)
}

RE_FUNCIONES = {'compile', 'match', 'search', 'findall', 'finditer',
                'sub', 'split', 'fullmatch', 'scanner'}

proyecto = pathlib.Path(__file__).parent
archivos_py = [f for f in proyecto.glob('*.py')
               if f.name != pathlib.Path(__file__).name]

violaciones = []
for archivo in sorted(archivos_py):
    src = archivo.read_text(encoding='utf-8', errors='replace')
    try:
        tree = _ast.parse(src, filename=str(archivo))
    except SyntaxError as e:
        violaciones.append(f"{archivo.name}: SyntaxError → {e}")
        continue

    for nodo in _ast.walk(tree):
        if isinstance(nodo, _ast.Import):
            for alias in nodo.names:
                base = alias.name.split('.')[0]
                if base in LIBS_PROHIBIDAS:
                    violaciones.append(
                        f"{archivo.name}:{nodo.lineno}  import {alias.name}")

        elif isinstance(nodo, _ast.ImportFrom):
            base = (nodo.module or '').split('.')[0]
            if base in LIBS_PROHIBIDAS:
                violaciones.append(
                    f"{archivo.name}:{nodo.lineno}  from {nodo.module} import ...")

        elif isinstance(nodo, _ast.Call):
            func = nodo.func
            if (isinstance(func, _ast.Attribute)
                    and isinstance(func.value, _ast.Name)
                    and func.value.id == 're'
                    and func.attr in RE_FUNCIONES):
                violaciones.append(
                    f"{archivo.name}:{nodo.lineno}  re.{func.attr}(...)")

ok("Ningun archivo del proyecto importa librerias de analisis lexico prohibidas",
   len(violaciones) == 0,
   "violaciones: " + "; ".join(violaciones) if violaciones else "")

lexer_src = (proyecto / 'lexer.py').read_text(encoding='utf-8')
lexer_tree = _ast.parse(lexer_src)
imports_en_lexer = [
    n for n in _ast.walk(lexer_tree)
    if isinstance(n, (_ast.Import, _ast.ImportFrom))
]
ok("lexer.py no tiene ningún import (implementacion 100% manual)",
   len(imports_en_lexer) == 0,
   f"imports encontrados: {imports_en_lexer}")

print("\n" + "=" * 62)
total = _PASS + _FAIL
pct   = int(100 * _PASS / total) if total else 0
print(f"  RESULTADO FINAL: {_PASS}/{total} ({pct}%) tests pasados")
if _FAIL > 0:
    print(f"  *** {_FAIL} test(s) FALLIDOS — revisar arriba ***")
else:
    print("  *** Todos los tests pasaron correctamente ***")
print("=" * 62)
