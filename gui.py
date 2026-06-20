import tkinter as tk
from tkinter import scrolledtext, messagebox
from lexer import Lexer
from reporter import generate_token_report, generate_error_report, open_report
from metodo_arbol import generate_metodo_arbol
from manual_generator import generate_manual_usuario, generate_manual_tecnico

DARK_BLUE  = '#0d3b2e'
MID_BLUE   = '#2e7d8c'
LIGHT_BG   = '#edf3ee'
WHITE      = '#ffffff'
GREEN      = '#1e8c4e'
RED        = '#b83232'
GRAY       = '#6b7c85'
PURPLE     = '#7d3c98'
TEAL       = '#0e7a6e'
PLACEHOLDER = 'Escriba texto para analizar...'


class LigaBotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("LigaBot — Análisis Léxico")
        self.root.geometry("920x580")
        self.root.minsize(760, 480)
        self.root.configure(bg=LIGHT_BG)

        self.all_tokens = []
        self.all_errors = []

        self._build()

    def _build(self):
        self._build_header()
        self._build_body()
        self._build_footer()
        self._print('LigaBot: Bienvenido al analizador léxico de LigaBot. '
                    'Ingrese texto en el campo inferior y presione Analizar.', 'bot')
        self._print('─' * 60, 'sep')

    def _build_header(self):
        hdr = tk.Frame(self.root, bg=DARK_BLUE, height=48)
        hdr.pack(fill='x')
        hdr.pack_propagate(False)
        tk.Label(hdr, text='LigaBot', font=('Segoe UI', 13, 'bold'),
                 bg=DARK_BLUE, fg=WHITE).pack(side='left', padx=20, pady=10)
        tk.Label(hdr, text='Fase 1 — Análisis Léxico',
                 font=('Segoe UI', 9), bg=DARK_BLUE, fg='#7fc4a0').pack(side='right', padx=20)

    def _build_body(self):
        body = tk.Frame(self.root, bg=LIGHT_BG)
        body.pack(fill='both', expand=True, padx=10, pady=10)

        # --- Área de resultado (izquierda) ---
        left = tk.Frame(body, bg=LIGHT_BG)
        left.pack(side='left', fill='both', expand=True)

        tk.Label(left, text='Resultado del análisis:',
                 font=('Segoe UI', 8), bg=LIGHT_BG, fg=GRAY).pack(anchor='w')

        self.output = scrolledtext.ScrolledText(
            left, wrap=tk.WORD, state='disabled',
            font=('Consolas', 10), bg=WHITE, fg='#222',
            relief='flat', bd=1, cursor='arrow',
            padx=10, pady=8
        )
        self.output.pack(fill='both', expand=True, pady=(3, 0))

        self.output.tag_configure('bot',  foreground=DARK_BLUE,
                                  font=('Segoe UI', 10, 'bold'))
        self.output.tag_configure('user', foreground='#555',
                                  font=('Segoe UI', 9, 'italic'))
        self.output.tag_configure('ok',   foreground=GREEN,
                                  font=('Segoe UI', 10))
        self.output.tag_configure('err',  foreground=RED,
                                  font=('Segoe UI', 10))
        self.output.tag_configure('detail', foreground='#8b2318',
                                  font=('Consolas', 9))
        self.output.tag_configure('sep',  foreground='#ccc',
                                  font=('Consolas', 9))

        # --- Panel lateral (derecha) ---
        right = tk.Frame(body, bg=LIGHT_BG, width=185)
        right.pack(side='right', fill='y', padx=(10, 0))
        right.pack_propagate(False)

        self._btn(right, 'Reporte de Tokens',  MID_BLUE,  self._open_tokens)
        self._btn(right, 'Reporte de Errores', RED,       self._open_errors)
        self._btn(right, 'Limpiar Tokens',     GRAY,      self._clear_tokens)
        self._btn(right, 'Limpiar Errores',    GRAY,      self._clear_errors)

        tk.Frame(right, bg=LIGHT_BG, height=10).pack()

        self._btn(right, 'Método del Árbol',   PURPLE,    self._open_arbol)
        self._btn(right, 'Manual de Usuario',  GREEN,     self._open_man_usr)
        self._btn(right, 'Manual Técnico',     TEAL,      self._open_man_tec)

    def _btn(self, parent, label, color, cmd):
        tk.Button(
            parent, text=label, command=cmd,
            font=('Segoe UI', 9), bg=color, fg=WHITE,
            relief='flat', cursor='hand2', pady=7,
            activebackground=color, activeforeground=WHITE, bd=0
        ).pack(fill='x', pady=3)

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
        self.entry.bind('<Return>',   lambda _: self._analyze())

        tk.Button(
            foot, text='  Analizar  ', command=self._analyze,
            font=('Segoe UI', 10, 'bold'), bg=DARK_BLUE, fg=WHITE,
            relief='flat', cursor='hand2', pady=5,
            activebackground=MID_BLUE
        ).pack(side='right', padx=(8, 0))

    # Lógica de análisis  
    def _analyze(self):
        text = self._entry_var.get().strip()
        if not text or text == PLACEHOLDER:
            return

        self._print(f'Tú: {text}', 'user')

        lexer = Lexer(text)
        tokens, errors = lexer.analyze()

        self.all_tokens.extend(tokens)
        self.all_errors.extend(errors)

        if not errors:
            self._print(
                f'LigaBot: Texto aceptado — {len(tokens)} token(s) reconocido(s).',
                'ok'
            )
        else:
            self._print(
                f'LigaBot: {len(tokens)} token(s) reconocido(s) | '
                f'{len(errors)} error(es) léxico(s):',
                'err'
            )
            for e in errors:
                self._print(
                    f'  [fila {e.fila}, col {e.columna}] {e.descripcion}',
                    'detail'
                )

        self._print('─' * 60, 'sep')
        self._entry_var.set('')
        self.entry.configure(fg='#333')

    
    # Helpers de salida  
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

    # Acciones de los botones 
    def _open_tokens(self):
        if not self.all_tokens:
            messagebox.showinfo('Sin tokens',
                                'No hay tokens registrados. Analice algún texto primero.')
            return
        open_report(generate_token_report(self.all_tokens))

    def _open_errors(self):
        open_report(generate_error_report(self.all_errors))

    def _clear_tokens(self):
        self.all_tokens.clear()
        self._print('LigaBot: Lista de tokens borrada.', 'ok')

    def _clear_errors(self):
        self.all_errors.clear()
        self._print('LigaBot: Lista de errores borrada.', 'ok')

    def _open_arbol(self):
        open_report(generate_metodo_arbol())

    def _open_man_usr(self):
        open_report(generate_manual_usuario())

    def _open_man_tec(self):
        open_report(generate_manual_tecnico())
