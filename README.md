# LigaBot

Proyecto del curso de Lenguajes Formales y de Programación — USAC, vacaciones junio 2026.

Es un chatbot de escritorio que permite consultar estadísticas históricas de La Liga española (temporadas 1979-1980 a 2019-2020) escribiendo comandos en un lenguaje formal definido para el proyecto.

---

## Fases

**Fase 1 — Analizador Léxico**
Implementación de un AFD de 22 estados construido con el Método del Árbol directamente desde las expresiones regulares de 23 tokens. Sin librerías externas de análisis léxico.

**Fase 2 — Analizador Sintáctico y Chatbot**
Parser de descenso recursivo para 8 comandos, integrado con una fuente de datos CSV y una interfaz gráfica en Tkinter.

---

---

## Cómo ejecutar

```bash
python main.py
```

---

## Comandos

```
RESULTADO "Equipo1" VS "Equipo2" TEMPORADA <AAAA-AAAA>
JORNADA N TEMPORADA <AAAA-AAAA> [-f "nombre"]
GOLES LOCAL|VISITANTE|TOTAL "Equipo" TEMPORADA <AAAA-AAAA>
TABLA TEMPORADA <AAAA-AAAA> [-f "nombre"]
PARTIDOS "Equipo" TEMPORADA <AAAA-AAAA> [-f "nombre"] [-ji N] [-jf N]
TOP SUPERIOR|INFERIOR TEMPORADA <AAAA-AAAA> [-n N]
ADIOS
```

Los comandos son **case-insensitive** (`resultado`, `RESULTADO`, `Resultado` son equivalentes).

---

## Estructura del proyecto

```
├── main.py
├── LaLigaBot-LFP.csv
├── src/
│   ├── lexer.py             # AFD 22 estados
│   ├── parser.py            # descenso recursivo
│   ├── chatbot.py           # pipeline principal
│   ├── data_source.py       # consultas al CSV
│   ├── reporter.py          # generación de HTMLs
│   ├── gui.py               # interfaz Tkinter
│   ├── metodo_arbol.py      # HTML del Método del Árbol
│   └── manual_generator.py  # manuales HTML
├── images/                  # imágenes
├── docs/                    # documentación Word
├── tests/
│   └── test_lexer_automatico.py
└── reportes/                # HTMLs generados al usar el chatbot
```

---

## Tests

```bash
python tests/test_lexer_automatico.py
```

254 casos de prueba que verifican el lexer e incluyen una comprobación de que no se usan librerías de análisis léxico prohibidas (`re`, `ply`, `antlr4`, etc.).

---


