import tkinter as tk
from tkinter import scrolledtext, messagebox
from .reporter import (generate_token_report, generate_error_report,
                       generate_syntax_error_report, open_report)
from .metodo_arbol import generate_metodo_arbol
from .manual_generator import generate_manual_usuario, generate_manual_tecnico
from .data_source import DataSource
from .chatbot import Chatbot

DARK_BLUE   = '#0d3b2e'
MID_BLUE    = '#2e7d8c'
LIGHT_BG    = '#edf3ee'
WHITE       = '#ffffff'
GREEN       = '#1e8c4e'
RED         = '#b83232'
GRAY        = '#6b7c85'
PURPLE      = '#7d3c98'
TEAL        = '#0e7a6e'
ORANGE      = '#d35400'

PLACEHOLDER = 'Escriba un comando de LigaBot...'


class LigaBotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("LigaBot - Fase 2")
        self.root.geometry("980x620")
        self.root.minsize(800, 500)
        self.root.configure(bg=LIGHT_BG)

        self.all_tokens       = []
        self.all_lex_errors   = []
        self.all_syn_errors   = []
        self._adios           = False

        # Cargar CSV y crear chatbot
        self.ds     = DataSource()
        self.bot    = Chatbot(self.ds)

        self._build()
        self._show_welcome()

    def _build(self):
        self._build_header()
        self._build_body()
        self._build_footer()

    # -- Header ----------------------------------------------------------------

    def _build_header(self):
        hdr = tk.Frame(self.root, bg=DARK_BLUE, height=52)
        hdr.pack(fill='x')
        hdr.pack_propagate(False)

        tk.Label(hdr, text='LigaBot',
                 font=('Segoe UI', 13, 'bold'),
                 bg=DARK_BLUE, fg=WHITE).pack(side='left', padx=20, pady=10)

        tk.Label(hdr, text='Fase 2 - Analisis Sintactico y Chatbot',
                 font=('Segoe UI', 9), bg=DARK_BLUE, fg='#7fc4a0'
                 ).pack(side='left', padx=4)

        # Estado del CSV
        if self.ds.loaded:
            csv_text  = f'CSV cargado: LaLigaBot-LFP.csv  ({len(self.ds.rows):,} partidos)'
            csv_color = '#7fc4a0'
        else:
            csv_text  = f'CSV no disponible: {self.ds.error}'
            csv_color = '#f1948a'

        tk.Label(hdr, text=csv_text,
                 font=('Segoe UI', 8), bg=DARK_BLUE, fg=csv_color
                 ).pack(side='right', padx=20)

    # -- Body ------------------------------------------------------------------

    def _build_body(self):
        body = tk.Frame(self.root, bg=LIGHT_BG)
        body.pack(fill='both', expand=True, padx=10, pady=10)

        # ---- Área de conversación (izquierda) ----
        left = tk.Frame(body, bg=LIGHT_BG)
        left.pack(side='left', fill='both', expand=True)

        tk.Label(left, text='Conversación:',
                 font=('Segoe UI', 8), bg=LIGHT_BG, fg=GRAY).pack(anchor='w')

        self.output = scrolledtext.ScrolledText(
            left, wrap=tk.WORD, state='disabled',
            font=('Segoe UI', 10), bg=WHITE, fg='#222',
            relief='flat', bd=1, cursor='arrow', padx=12, pady=10
        )
        self.output.pack(fill='both', expand=True, pady=(3, 0))

        # Estilos de texto
        self.output.tag_configure('bot',
                                  foreground=DARK_BLUE,
                                  font=('Segoe UI', 10, 'bold'))
        self.output.tag_configure('user',
                                  foreground='#444',
                                  font=('Segoe UI', 10, 'italic'))
        self.output.tag_configure('ok',
                                  foreground=GREEN,
                                  font=('Segoe UI', 10))
        self.output.tag_configure('report',
                                  foreground=TEAL,
                                  font=('Segoe UI', 9, 'italic'))
        self.output.tag_configure('err',
                                  foreground=RED,
                                  font=('Segoe UI', 10))
        self.output.tag_configure('warn',
                                  foreground=ORANGE,
                                  font=('Segoe UI', 9))
        self.output.tag_configure('detail',
                                  foreground='#8b2318',
                                  font=('Consolas', 9))
        self.output.tag_configure('sep',
                                  foreground='#ccc',
                                  font=('Consolas', 8))

        # ---- Panel lateral (derecha) ----
        right = tk.Frame(body, bg=LIGHT_BG, width=195)
        right.pack(side='right', fill='y', padx=(10, 0))
        right.pack_propagate(False)

        tk.Label(right, text='Reportes léxicos',
                 font=('Segoe UI', 7, 'bold'), bg=LIGHT_BG,
                 fg=GRAY).pack(anchor='w', pady=(0, 2))
        self._btn(right, 'Reporte de Tokens',         MID_BLUE, self._open_tokens)
        self._btn(right, 'Reporte Errores Léxicos',   RED,      self._open_errors)
        self._btn(right, 'Reporte Errores Sintácticos', ORANGE, self._open_syn_errors)

        tk.Frame(right, bg='#ccc', height=1).pack(fill='x', pady=8)

        tk.Label(right, text='Limpiar',
                 font=('Segoe UI', 7, 'bold'), bg=LIGHT_BG,
                 fg=GRAY).pack(anchor='w', pady=(0, 2))
        self._btn(right, 'Limpiar Tokens',      GRAY, self._clear_tokens)
        self._btn(right, 'Limpiar Errores',     GRAY, self._clear_errors)

        tk.Frame(right, bg='#ccc', height=1).pack(fill='x', pady=8)

        tk.Label(right, text='Documentación',
                 font=('Segoe UI', 7, 'bold'), bg=LIGHT_BG,
                 fg=GRAY).pack(anchor='w', pady=(0, 2))
        self._btn(right, 'Método del Árbol',  PURPLE, self._open_arbol)
        self._btn(right, 'Manual de Usuario', GREEN,  self._open_man_usr)
        self._btn(right, 'Manual Técnico',    TEAL,   self._open_man_tec)

    def _btn(self, parent, label, color, cmd):
        tk.Button(
            parent, text=label, command=cmd,
            font=('Segoe UI', 9), bg=color, fg=WHITE,
            relief='flat', cursor='hand2', pady=6,
            activebackground=color, activeforeground=WHITE, bd=0
        ).pack(fill='x', pady=2)

    # -- Footer ----------------------------------------------------------------

    def _build_footer(self):
        foot = tk.Frame(self.root, bg='#ccddd0', pady=8, padx=10)
        foot.pack(fill='x', side='bottom')

        self._entry_var = tk.StringVar()

        entry_wrap = tk.Frame(foot, bg=WHITE, relief='solid', bd=1)
        entry_wrap.pack(side='left', fill='x', expand=True)

        self.entry = tk.Entry(
            entry_wrap, textvariable=self._entry_var,
            font=('Segoe UI', 11), relief='flat', bg=WHITE, fg='#aaa', bd=6
        )
        self.entry.pack(fill='x', expand=True)
        self.entry.insert(0, PLACEHOLDER)
        self.entry.bind('<FocusIn>',  self._focus_in)
        self.entry.bind('<FocusOut>', self._focus_out)
        self.entry.bind('<Return>',   lambda _: self._send())

        self.send_btn = tk.Button(
            foot, text='  Enviar  ', command=self._send,
            font=('Segoe UI', 10, 'bold'), bg=DARK_BLUE, fg=WHITE,
            relief='flat', cursor='hand2', pady=5,
            activebackground=MID_BLUE
        )
        self.send_btn.pack(side='right', padx=(8, 0))

    # -- Lógica principal ------------------------------------------------------

    def _show_welcome(self):
        self._print(
            'LigaBot: Bienvenido a LigaBot Fase 2.\n'
            'Ingrese un comando (RESULTADO, JORNADA, GOLES, TABLA, PARTIDOS, TOP, ADIOS).',
            'bot'
        )
        if not self.ds.loaded:
            self._print(
                f'  Advertencia: CSV no cargado: {self.ds.error}', 'warn'
            )
        self._print('-' * 60, 'sep')

    def _send(self):
        if self._adios:
            return
        text = self._entry_var.get().strip()
        if not text or text == PLACEHOLDER:
            return

        self._print(f'Tú: {text}', 'user')
        self._entry_var.set('')
        self.entry.configure(fg='#333')

        response, lex_errors, parse_error, report_path = self.bot.process(text)

        # Acumular tokens y errores (re-analizar léxicamente para tenerlos)
        from .lexer import Lexer
        lx = Lexer(text)
        toks, lerrs = lx.analyze()
        self.all_tokens.extend(toks)
        self.all_lex_errors.extend(lerrs)

        if parse_error:
            self.all_syn_errors.append(parse_error)

        # Mostrar respuesta
        tag = 'ok' if (not lex_errors and not parse_error) else 'err'
        if 'Error' in response or 'error' in response:
            tag = 'err'
        elif report_path:
            tag = 'ok'

        self._print(response, tag)

        if report_path:
            self._print(f'  >> Reporte generado: {report_path}', 'report')
            open_report(report_path)

        # Mostrar detalles de errores léxicos
        for e in lex_errors:
            self._print(
                f'  [L] fila {e.fila}, col {e.columna}: {e.descripcion}', 'detail'
            )

        # Si fue ADIOS, deshabilitar entrada
        if response.strip() == 'LigaBot: ADIOS':
            self._adios = True
            self.entry.configure(state='disabled', bg='#f0f0f0')
            self.send_btn.configure(state='disabled')

        self._print('-' * 60, 'sep')

    # -- Helpers ---------------------------------------------------------------

    def _print(self, text, tag=''):
        self.output.configure(state='normal')
        self.output.insert(tk.END, text + '\n', tag)
        self.output.configure(state='disabled')
        self.output.see(tk.END)

    def _focus_in(self, _):
        if self.entry.get() == PLACEHOLDER:
            self.entry.delete(0, tk.END)
            self.entry.configure(fg='#333')

    def _focus_out(self, _):
        if not self.entry.get():
            self.entry.insert(0, PLACEHOLDER)
            self.entry.configure(fg='#aaa')

    # -- Botones ---------------------------------------------------------------

    def _open_tokens(self):
        if not self.all_tokens:
            messagebox.showinfo('Sin tokens',
                                'No hay tokens registrados. Envíe algún comando primero.')
            return
        open_report(generate_token_report(self.all_tokens))

    def _open_errors(self):
        open_report(generate_error_report(self.all_lex_errors))

    def _open_syn_errors(self):
        open_report(generate_syntax_error_report(self.all_syn_errors))

    def _clear_tokens(self):
        self.all_tokens.clear()
        self.all_lex_errors.clear()
        self._print('LigaBot: Tokens y errores léxicos borrados.', 'ok')

    def _clear_errors(self):
        self.all_syn_errors.clear()
        self._print('LigaBot: Errores sintácticos borrados.', 'ok')

    def _open_arbol(self):
        open_report(generate_metodo_arbol())

    def _open_man_usr(self):
        open_report(generate_manual_usuario())

    def _open_man_tec(self):
        open_report(generate_manual_tecnico())
