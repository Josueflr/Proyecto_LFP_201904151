## LigaBot

LigaBot es una aplicación de escritorio con interfaz gráfica que implementa un **analizador léxico manual** para 
un lenguaje de comandos de consulta de fútbol. El usuario ingresa texto en el lenguaje de LigaBot y la aplicación clasifica 
cada elemento en tokens o reporta errores léxicos con su posición exacta (fila y columna).

## Características

* Analizador léxico implementado desde cero en Python
* Interfaz gráfica con Tkinter (modo chat)
* Reconocimiento de palabras reservadas, banderas, cadenas, temporadas, números y símbolos
* Reporte de tokens en HTML
* Reporte de errores léxicos en HTML
* Método del Árbol (de expresión regular → AFD) en HTML
* Manual de Usuario y Manual Técnico en HTML

## Estructura del proyecto

```text
├── main.py
├── gui.py
├── lexer.py
├── reporter.py
├── metodo_arbol.py
├── manual_generator.py
└── reportes
    ├── Reporte_Token.html
    ├── Reporte_Errores.html
    ├── Metodo_Arbol.html
    ├── Manual_Usuario.html
    └── Manual_Tecnico.html


  ## Requisitos

  - Python 3.8 o superior
  - Tkinter (incluido en la instalación estándar de Python)

  ## Ejecución

  ```bash
  python main.py

  Uso

  1. Ejecuta la aplicación con el comando anterior.
  2. Escribe un comando en el campo de texto inferior (ej. RESULTADO "Barcelona" VS "Real Madrid" TEMPORADA 2023-2024).
  3. Presiona Analizar o la tecla Enter.
  4. La aplicación mostrará los tokens reconocidos o los errores encontrados.
  5. Usa los botones del panel lateral para generar los reportes HTML.

  Tokens reconocidos

  ┌───────────────┬──────────────────────────────┬─────────────┐
  │     Token     │         Descripción          │   Ejemplo   │
  ├───────────────┼──────────────────────────────┼─────────────┤
  │ RESULTADO     │ Palabra reservada            │ resultado   │
  ├───────────────┼──────────────────────────────┼─────────────┤
  │ VS            │ Palabra reservada            │ vs          │
  ├───────────────┼──────────────────────────────┼─────────────┤
  │ TEMPORADA     │ Palabra reservada            │ Temporada   │
  ├───────────────┼──────────────────────────────┼─────────────┤
  │ BANDERA_F     │ Bandera de nombre de archivo │ -f          │
  ├───────────────┼──────────────────────────────┼─────────────┤
  │ BANDERA_N     │ Bandera de número            │ -n          │
  ├───────────────┼──────────────────────────────┼─────────────┤
  │ BANDERA_JI    │ Bandera de jornada inicial   │ -ji         │
  ├───────────────┼──────────────────────────────┼─────────────┤
  │ BANDERA_JF    │ Bandera de jornada final     │ -jf         │
  ├───────────────┼──────────────────────────────┼─────────────┤
  │ CADENA        │ Texto entre comillas dobles  │ "Barcelona" │
  ├───────────────┼──────────────────────────────┼─────────────┤
  │ TEMPORADA_VAL │ Valor de temporada           │ 2023-2024   │
  ├───────────────┼──────────────────────────────┼─────────────┤
  │ NUMERO        │ Número de 1 o 2 dígitos      │ 5, 38       │
  ├───────────────┼──────────────────────────────┼─────────────┤
  │ MENOR         │ Símbolo menor que            │ <           │
  ├───────────────┼──────────────────────────────┼─────────────┤
  │ BANDERA_JI    │ Bandera de jornada inicial   │ -ji         │
  ├───────────────┼──────────────────────────────┼─────────────┤
  │ BANDERA_JF    │ Bandera de jornada final     │ -jf         │
  ├───────────────┼──────────────────────────────┼─────────────┤
  │ CADENA        │ Texto entre comillas dobles  │ "Barcelona" │
  ├───────────────┼──────────────────────────────┼─────────────┤
  │ TEMPORADA_VAL │ Valor de temporada           │ 2023-2024   │
  ├───────────────┼──────────────────────────────┼─────────────┤
  │ NUMERO        │ Número de 1 o 2 dígitos      │ 5, 38       │
  ├───────────────┼──────────────────────────────┼─────────────┤
  │ MENOR         │ Símbolo menor que            │ <           │
  ├───────────────┼──────────────────────────────┼─────────────┤
  │ MAYOR         │ Símbolo mayor que            │ >           │
  └───────────────┴──────────────────────────────┴─────────────┘
