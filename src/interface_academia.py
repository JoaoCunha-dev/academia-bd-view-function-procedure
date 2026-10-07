import os
import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2
import getpass

# ═══════════════════════════════════════════════
#  CONFIGURACAO — igual ao sistema_academia.py
# ═══════════════════════════════════════════════
DB_CONFIG = {
    "host":     "localhost",
    "database": "Academia_db",
    "user":     "postgres",
    "password": os.environ.get("ACADEMIA_DB_PASSWORD", "academia123"),
    "port":     "5432"
}

USUARIOS = {
    "admin":     "1234",
    "professor": "senha"
}

# Cores
BG      = "#1e1e1e"
SURFACE = "#2d2d2d"
ACCENT  = "#4fc3f7"
TEXT    = "#ffffff"
MUTED   = "#aaaaaa"
SUCCESS = "#81c784"
DANGER  = "#e57373"
ENTRY   = "#3a3a3a"

def conectar():
    return psycopg2.connect(**DB_CONFIG)


def cores_situacao(tree):
    """Pinta as linhas da tabela conforme a situacao financeira do aluno."""
    tree.tag_configure("Em dia",         foreground=SUCCESS)
    tree.tag_configure("Vence em breve", foreground="#ffd54f")
    tree.tag_configure("Vencido",        foreground=DANGER)
    tree.tag_configure("Sem pagamento",  foreground=MUTED)


# ════════════════════════════════════════════════
#  TELA DE LOGIN
# ════════════════════════════════════════════════

class TelaLogin:
    def __init__(self, root, ao_logar):
        self.root = root
        self.ao_logar = ao_logar
        self.root.title("Academia - Login")
        self.root.geometry("360x420")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)
        self._centralizar()
        self._build()

    def _centralizar(self):
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - 180
        y = (self.root.winfo_screenheight() // 2) - 210
        self.root.geometry(f"+{x}+{y}")

    def _build(self):
        frame = tk.Frame(self.root, bg=BG)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(frame, text="ACADEMIA", font=("Segoe UI", 26, "bold"),
                 bg=BG, fg=ACCENT).pack(pady=(0, 4))
        tk.Label(frame, text="Sistema de Gerenciamento", font=("Segoe UI", 10),
                 bg=BG, fg=MUTED).pack(pady=(0, 30))

        # Usuario
        tk.Label(frame, text="Usuario", font=("Segoe UI", 10),
                 bg=BG, fg=MUTED).pack(anchor="w")
        self.e_usuario = tk.Entry(frame, font=("Segoe UI", 11),
                                   bg=ENTRY, fg=TEXT, insertbackground=TEXT,
                                   relief="flat", bd=8, width=28)
        self.e_usuario.pack(pady=(4, 14))

        # Senha
        tk.Label(frame, text="Senha", font=("Segoe UI", 10),
                 bg=BG, fg=MUTED).pack(anchor="w")
        self.e_senha = tk.Entry(frame, font=("Segoe UI", 11),
                                 bg=ENTRY, fg=TEXT, insertbackground=TEXT,
                                 relief="flat", bd=8, width=28, show="*")
        self.e_senha.pack(pady=(4, 24))

        tk.Button(frame, text="Entrar", command=self._login,
                  bg=ACCENT, fg="#000000", font=("Segoe UI", 11, "bold"),
                  relief="flat", bd=0, padx=20, pady=8, cursor="hand2",
                  width=24).pack()

        self.lbl_erro = tk.Label(frame, text="", font=("Segoe UI", 9),
                                  bg=BG, fg=DANGER)
        self.lbl_erro.pack(pady=(12, 0))

        tk.Label(frame, text="admin / 1234   professor / senha",
                 font=("Segoe UI", 8), bg=BG, fg=MUTED).pack(pady=(16, 0))

        self.e_usuario.focus()
        self.e_usuario.bind("<Return>", lambda e: self.e_senha.focus())
        self.e_senha.bind("<Return>", lambda e: self._login())

    def _login(self):
        u = self.e_usuario.get().strip()
        s = self.e_senha.get().strip()
        if USUARIOS.get(u) == s:
            for w in self.root.winfo_children():
                w.destroy()
            self.ao_logar(u)
        else:
            self.lbl_erro.config(text="Usuario ou senha incorretos.")
            self.e_senha.delete(0, tk.END)


# ════════════════════════════════════════════════
#  JANELA PRINCIPAL
# ════════════════════════════════════════════════

class AppPrincipal:
    def __init__(self, root, usuario):
        self.root = root
        self.usuario = usuario
        self.root.title(f"Academia — {usuario}")
        self.root.geometry("1000x580")
        self.root.configure(bg=BG)
        self._centralizar()
        self._build()
        self._mostrar("alunos_lista")

    def _centralizar(self):
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - 500
        y = (self.root.winfo_screenheight() // 2) - 290
        self.root.geometry(f"+{x}+{y}")

    def _build(self):
        # Sidebar
        self.sidebar = tk.Frame(self.root, bg=SURFACE, width=180)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        tk.Label(self.sidebar, text="ACADEMIA", font=("Segoe UI", 13, "bold"),
                 bg=SURFACE, fg=ACCENT).pack(pady=(24, 2))
        tk.Label(self.sidebar, text=f"usuario: {self.usuario}", font=("Segoe UI", 8),
                 bg=SURFACE, fg=MUTED).pack(pady=(0, 20))

        tk.Frame(self.sidebar, bg="#444444", height=1).pack(fill="x", padx=16, pady=4)

        self.nav_btns = {}
        itens = [
            ("Listar Alunos",   "alunos_lista"),
            ("Cadastrar Aluno", "alunos_cadastro"),
            ("Buscar Aluno",    "alunos_busca"),
            ("Pagamentos",      "pagamentos"),
            ("Relatorios",      "relatorios"),
        ]
        for texto, chave in itens:
            b = tk.Button(
                self.sidebar, text=texto,
                command=lambda c=chave: self._mostrar(c),
                bg=SURFACE, fg=MUTED,
                font=("Segoe UI", 10), relief="flat", bd=0,
                anchor="w", padx=20, pady=10, cursor="hand2",
                activebackground=BG, activeforeground=TEXT,
            )
            b.pack(fill="x")
            self.nav_btns[chave] = b

        tk.Frame(self.sidebar, bg="#444444", height=1).pack(fill="x", padx=16, pady=16)

        tk.Button(self.sidebar, text="Sair",
                  command=lambda: self.root.destroy(),
                  bg=SURFACE, fg=DANGER, font=("Segoe UI", 10),
                  relief="flat", bd=0, pady=8, cursor="hand2").pack()

        # Conteudo
        self.conteudo = tk.Frame(self.root, bg=BG)
        self.conteudo.pack(side="left", fill="both", expand=True)

        self.paineis = {
            "alunos_lista":    PainelListar(self.conteudo),
            "alunos_cadastro": PainelCadastrar(self.conteudo),
            "alunos_busca":    PainelBuscar(self.conteudo),
            "pagamentos":      PainelPagamentos(self.conteudo),
            "relatorios":      PainelRelatorios(self.conteudo),
        }
        self.painel_atual = None

    def _mostrar(self, chave):
        if self.painel_atual:
            self.painel_atual.pack_forget()
        for c, b in self.nav_btns.items():
            if c == chave:
                b.config(bg=BG, fg=TEXT, font=("Segoe UI", 10, "bold"))
            else:
                b.config(bg=SURFACE, fg=MUTED, font=("Segoe UI", 10, "normal"))
        self.painel_atual = self.paineis[chave]
        self.painel_atual.pack(fill="both", expand=True)
        self.painel_atual.atualizar()


# ════════════════════════════════════════════════
#  PAINEL: LISTAR ALUNOS
# ════════════════════════════════════════════════

class PainelListar(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=BG)
        self._build()

    def _build(self):
        tk.Label(self, text="Alunos Cadastrados", font=("Segoe UI", 16, "bold"),
                 bg=BG, fg=TEXT).pack(anchor="w", padx=24, pady=(20, 4))
        tk.Label(self, text="Alunos com situacao financeira (dados vindos da VIEW vw_situacao_alunos).",
                 font=("Segoe UI", 9), bg=BG, fg=MUTED).pack(anchor="w", padx=24)
        tk.Frame(self, bg="#444444", height=1).pack(fill="x", padx=24, pady=12)

        # Tabela
        frame_t = tk.Frame(self, bg=SURFACE)
        frame_t.pack(fill="both", expand=True, padx=24, pady=(0, 8))

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Dark.Treeview",
            background=SURFACE, foreground=TEXT,
            fieldbackground=SURFACE, rowheight=28,
            font=("Segoe UI", 10))
        style.configure("Dark.Treeview.Heading",
            background="#3a3a3a", foreground=ACCENT,
            font=("Segoe UI", 10, "bold"))
        style.map("Dark.Treeview",
            background=[("selected", ACCENT)],
            foreground=[("selected", "#000000")])

        cols = ["ID", "Nome", "Email", "Telefone", "Plano", "Situacao", "Vencimento"]
        self.tree = ttk.Treeview(frame_t, columns=cols,
                                  show="headings", style="Dark.Treeview")
        larguras = [30, 100, 140, 90, 75, 105, 80]
        for col, larg in zip(cols, larguras):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=larg, anchor="w")

        sb = ttk.Scrollbar(frame_t, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)
        cores_situacao(self.tree)

        # Rodape
        rod = tk.Frame(self, bg=BG)
        rod.pack(fill="x", padx=24, pady=(0, 16))

        tk.Button(rod, text="Atualizar", command=self.atualizar,
                  bg=SURFACE, fg=TEXT, font=("Segoe UI", 9),
                  relief="flat", padx=12, pady=6, cursor="hand2").pack(side="left")

        tk.Button(rod, text="Deletar Selecionado", command=self._deletar,
                  bg=DANGER, fg=TEXT, font=("Segoe UI", 9),
                  relief="flat", padx=12, pady=6, cursor="hand2").pack(side="left", padx=8)

        self.lbl_total = tk.Label(rod, text="", font=("Segoe UI", 9),
                                   bg=BG, fg=MUTED)
        self.lbl_total.pack(side="right")

    def atualizar(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        try:
            conn = conectar()
            cur = conn.cursor()
            # VIEW: situacao financeira de cada aluno
            cur.execute("""
                SELECT aluno_id, nome, email, telefone, plano, situacao, data_vencimento
                FROM vw_situacao_alunos
                ORDER BY nome
            """)
            rows = cur.fetchall()
            for r in rows:
                vals = (r[0], r[1], r[2] or "—", r[3] or "—", r[4] or "—",
                        r[5], r[6].strftime("%d/%m/%Y") if r[6] else "—")
                self.tree.insert("", "end", values=vals, tags=(r[5],))
            self.lbl_total.config(text=f"Total: {len(rows)} aluno(s)")
            cur.close(); conn.close()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def _deletar(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Atencao", "Selecione um aluno para deletar.")
            return
        vals = self.tree.item(sel[0])["values"]
        if not messagebox.askyesno("Confirmar", f"Deletar '{vals[1]}'?"):
            return
        try:
            conn = conectar()
            cur = conn.cursor()
            cur.execute("DELETE FROM alunos WHERE id=%s", (vals[0],))
            conn.commit()
            cur.close(); conn.close()
            self.atualizar()
            messagebox.showinfo("Sucesso", "Aluno deletado!")
        except Exception as e:
            messagebox.showerror("Erro", str(e))


# ════════════════════════════════════════════════
#  PAINEL: CADASTRAR ALUNO
# ════════════════════════════════════════════════

class PainelCadastrar(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=BG)
        self._build()

    def _build(self):
        tk.Label(self, text="Cadastrar Aluno", font=("Segoe UI", 16, "bold"),
                 bg=BG, fg=TEXT).pack(anchor="w", padx=24, pady=(20, 4))
        tk.Label(self, text="Preencha os dados e clique em Salvar.",
                 font=("Segoe UI", 9), bg=BG, fg=MUTED).pack(anchor="w", padx=24)
        tk.Frame(self, bg="#444444", height=1).pack(fill="x", padx=24, pady=12)

        form = tk.Frame(self, bg=BG)
        form.pack(anchor="w", padx=40)

        self.entries = {}
        campos = ["Nome", "Email", "Telefone"]
        for campo in campos:
            tk.Label(form, text=campo, font=("Segoe UI", 10),
                     bg=BG, fg=MUTED).pack(anchor="w", pady=(8, 2))
            e = tk.Entry(form, font=("Segoe UI", 11),
                         bg=ENTRY, fg=TEXT, insertbackground=TEXT,
                         relief="flat", bd=8, width=36)
            e.pack(anchor="w", ipady=4)
            self.entries[campo] = e

        tk.Label(form, text="Plano", font=("Segoe UI", 10),
                 bg=BG, fg=MUTED).pack(anchor="w", pady=(8, 2))
        self.combo = ttk.Combobox(form, state="readonly",
                                   font=("Segoe UI", 11), width=34)
        self.combo["values"] = ["Mensal", "Trimestral", "Anual"]
        self.combo.current(0)
        self.combo.pack(anchor="w", ipady=4)

        tk.Button(form, text="Salvar Aluno", command=self._salvar,
                  bg=SUCCESS, fg="#000000", font=("Segoe UI", 11, "bold"),
                  relief="flat", padx=20, pady=8, cursor="hand2").pack(anchor="w", pady=20)

        self.lbl_msg = tk.Label(form, text="", font=("Segoe UI", 10),
                                 bg=BG, fg=SUCCESS)
        self.lbl_msg.pack(anchor="w")

    def atualizar(self):
        pass

    def _salvar(self):
        nome     = self.entries["Nome"].get().strip()
        email    = self.entries["Email"].get().strip()
        telefone = self.entries["Telefone"].get().strip()
        plano    = self.combo.get()

        if not nome:
            self.lbl_msg.config(text="Nome e obrigatorio.", fg=DANGER)
            return
        try:
            conn = conectar()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO alunos (nome, email, telefone, plano) VALUES (%s,%s,%s,%s)",
                (nome, email or None, telefone or None, plano)
            )
            conn.commit()
            cur.close(); conn.close()
            for e in self.entries.values():
                e.delete(0, tk.END)
            self.combo.current(0)
            self.lbl_msg.config(text="Aluno cadastrado com sucesso!", fg=SUCCESS)
        except Exception as e:
            self.lbl_msg.config(text=f"Erro: {e}", fg=DANGER)


# ════════════════════════════════════════════════
#  PAINEL: BUSCAR ALUNO
# ════════════════════════════════════════════════

class PainelBuscar(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=BG)
        self._build()

    def _build(self):
        tk.Label(self, text="Buscar Aluno", font=("Segoe UI", 16, "bold"),
                 bg=BG, fg=TEXT).pack(anchor="w", padx=24, pady=(20, 4))
        tk.Label(self, text="Busca por nome usando ILIKE (aceita partes do nome).",
                 font=("Segoe UI", 9), bg=BG, fg=MUTED).pack(anchor="w", padx=24)
        tk.Frame(self, bg="#444444", height=1).pack(fill="x", padx=24, pady=12)

        # Campo de busca
        busca_frame = tk.Frame(self, bg=BG)
        busca_frame.pack(anchor="w", padx=24, pady=(0, 12))

        self.e_busca = tk.Entry(busca_frame, font=("Segoe UI", 11),
                                 bg=ENTRY, fg=TEXT, insertbackground=TEXT,
                                 relief="flat", bd=8, width=32)
        self.e_busca.pack(side="left", ipady=4)
        self.e_busca.bind("<Return>", lambda e: self._buscar())

        tk.Button(busca_frame, text="Buscar", command=self._buscar,
                  bg=ACCENT, fg="#000000", font=("Segoe UI", 10, "bold"),
                  relief="flat", padx=14, pady=6, cursor="hand2").pack(side="left", padx=8)

        tk.Button(busca_frame, text="Todos", command=self._todos,
                  bg=SURFACE, fg=TEXT, font=("Segoe UI", 10),
                  relief="flat", padx=14, pady=6, cursor="hand2").pack(side="left")

        # Tabela resultado
        frame_t = tk.Frame(self, bg=SURFACE)
        frame_t.pack(fill="both", expand=True, padx=24, pady=(0, 16))

        cols = ["ID", "Nome", "Email", "Telefone", "Plano"]
        self.tree = ttk.Treeview(frame_t, columns=cols,
                                  show="headings", style="Dark.Treeview")
        larguras = [40, 200, 220, 130, 110]
        for col, larg in zip(cols, larguras):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=larg, anchor="w")

        sb = ttk.Scrollbar(frame_t, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)

        self.lbl_resultado = tk.Label(self, text="", font=("Segoe UI", 9),
                                       bg=BG, fg=MUTED)
        self.lbl_resultado.pack(anchor="w", padx=24)

    def atualizar(self):
        self._todos()

    def _buscar(self):
        termo = self.e_busca.get().strip()
        self._executar(f"%{termo}%" if termo else "%")

    def _todos(self):
        self.e_busca.delete(0, tk.END)
        self._executar("%")

    def _executar(self, termo):
        for item in self.tree.get_children():
            self.tree.delete(item)
        try:
            conn = conectar()
            cur = conn.cursor()
            cur.execute(
                "SELECT id, nome, email, telefone, plano FROM alunos "
                "WHERE nome ILIKE %s ORDER BY nome",
                (termo,)
            )
            rows = cur.fetchall()
            for r in rows:
                self.tree.insert("", "end", values=r)
            self.lbl_resultado.config(text=f"{len(rows)} resultado(s) encontrado(s)")
            cur.close(); conn.close()
        except Exception as e:
            messagebox.showerror("Erro", str(e))


# ════════════════════════════════════════════════
#  PAINEL: PAGAMENTOS  (FUNCTION + PROCEDURE)
# ════════════════════════════════════════════════

class PainelPagamentos(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=BG)
        self.alunos = []   # [(id, nome)]
        self.planos = []   # [(id, nome, preco)]
        self._build()

    def _build(self):
        tk.Label(self, text="Pagamentos", font=("Segoe UI", 16, "bold"),
                 bg=BG, fg=TEXT).pack(anchor="w", padx=24, pady=(20, 4))
        tk.Label(self, text="Valor calculado pela FUNCTION fn_calcular_valor; "
                            "pagamento gravado pela PROCEDURE sp_registrar_pagamento.",
                 font=("Segoe UI", 9), bg=BG, fg=MUTED, wraplength=640,
                 justify="left").pack(anchor="w", padx=24)
        tk.Frame(self, bg="#444444", height=1).pack(fill="x", padx=24, pady=12)

        form = tk.Frame(self, bg=BG)
        form.pack(anchor="w", padx=24)

        tk.Label(form, text="Aluno", font=("Segoe UI", 10), bg=BG, fg=MUTED).grid(row=0, column=0, sticky="w")
        tk.Label(form, text="Plano", font=("Segoe UI", 10), bg=BG, fg=MUTED).grid(row=0, column=1, sticky="w", padx=(16, 0))
        tk.Label(form, text="Valor (R$)", font=("Segoe UI", 10), bg=BG, fg=MUTED).grid(row=0, column=2, sticky="w", padx=(16, 0))

        self.cb_aluno = ttk.Combobox(form, state="readonly", font=("Segoe UI", 10), width=24)
        self.cb_aluno.grid(row=1, column=0, ipady=3)
        self.cb_plano = ttk.Combobox(form, state="readonly", font=("Segoe UI", 10), width=22)
        self.cb_plano.grid(row=1, column=1, padx=(16, 0), ipady=3)
        self.e_valor = tk.Entry(form, font=("Segoe UI", 11), bg=ENTRY, fg=TEXT,
                                insertbackground=TEXT, relief="flat", bd=6, width=10)
        self.e_valor.grid(row=1, column=2, padx=(16, 0), ipady=3)

        # qualquer mudanca de aluno/plano invalida o valor calculado
        self.cb_aluno.bind("<<ComboboxSelected>>", lambda e: self._limpar_valor())
        self.cb_plano.bind("<<ComboboxSelected>>", lambda e: self._limpar_valor())

        botoes = tk.Frame(self, bg=BG)
        botoes.pack(anchor="w", padx=24, pady=14)
        tk.Button(botoes, text="Calcular valor  (Function)", command=self._calcular,
                  bg=ACCENT, fg="#000000", font=("Segoe UI", 10, "bold"),
                  relief="flat", padx=14, pady=7, cursor="hand2").pack(side="left")
        tk.Button(botoes, text="Registrar pagamento  (Procedure)", command=self._registrar,
                  bg=SUCCESS, fg="#000000", font=("Segoe UI", 10, "bold"),
                  relief="flat", padx=14, pady=7, cursor="hand2").pack(side="left", padx=10)

        self.lbl_msg = tk.Label(self, text="", font=("Segoe UI", 10), bg=BG, fg=SUCCESS,
                                wraplength=620, justify="left")
        self.lbl_msg.pack(anchor="w", padx=24)

        tk.Label(self, text="Ultimos pagamentos", font=("Segoe UI", 11, "bold"),
                 bg=BG, fg=TEXT).pack(anchor="w", padx=24, pady=(14, 4))
        frame_t = tk.Frame(self, bg=SURFACE)
        frame_t.pack(fill="both", expand=True, padx=24, pady=(0, 16))
        cols = ["ID", "Aluno", "Plano", "Valor", "Data"]
        self.tree = ttk.Treeview(frame_t, columns=cols, show="headings", style="Dark.Treeview", height=6)
        for c, w in zip(cols, [40, 200, 120, 100, 100]):
            self.tree.heading(c, text=c)
            self.tree.column(c, width=w, anchor="w")
        sb = ttk.Scrollbar(frame_t, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)

    # ── dados ─────────────────────────────────────
    def atualizar(self):
        try:
            conn = conectar()
            cur = conn.cursor()
            cur.execute("SELECT id, nome FROM alunos ORDER BY nome")
            self.alunos = cur.fetchall()
            cur.execute("SELECT id, nome, preco FROM planos ORDER BY preco")
            self.planos = cur.fetchall()
            self.cb_aluno["values"] = [f"{a[0]} - {a[1]}" for a in self.alunos]
            self.cb_plano["values"] = [f"{p[0]} - {p[1]} (R$ {float(p[2]):.2f})" for p in self.planos]
            self._carregar_pagamentos(cur)
            cur.close(); conn.close()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def _carregar_pagamentos(self, cur):
        for item in self.tree.get_children():
            self.tree.delete(item)
        cur.execute("""
            SELECT pg.id, a.nome, pl.nome, pg.valor, pg.data_pagamento
            FROM pagamentos pg
            INNER JOIN alunos a  ON pg.aluno_id = a.id
            INNER JOIN planos pl ON pg.plano_id = pl.id
            ORDER BY pg.data_pagamento DESC, pg.id DESC
            LIMIT 30
        """)
        for r in cur.fetchall():
            self.tree.insert("", "end", values=(
                r[0], r[1], r[2], f"R$ {float(r[3]):.2f}", r[4].strftime("%d/%m/%Y")))

    def _ids(self):
        i, j = self.cb_aluno.current(), self.cb_plano.current()
        if i < 0 or j < 0:
            self.lbl_msg.config(text="Selecione o aluno e o plano.", fg=DANGER)
            return None
        return self.alunos[i][0], self.planos[j][0]

    def _limpar_valor(self):
        self.e_valor.delete(0, tk.END)
        self.lbl_msg.config(text="")

    # ── FUNCTION ──────────────────────────────────
    def _calcular(self):
        ids = self._ids()
        if not ids:
            return
        try:
            conn = conectar()
            cur = conn.cursor()
            cur.execute("SELECT fn_calcular_valor(%s, %s)", ids)   # <- FUNCTION
            valor = cur.fetchone()[0]
            cur.execute("SELECT preco FROM planos WHERE id = %s", (ids[1],))
            preco = cur.fetchone()[0]
            cur.close(); conn.close()
            self.e_valor.delete(0, tk.END)
            self.e_valor.insert(0, f"{float(valor):.2f}")
            if valor < preco:
                nota = "desconto de fidelidade aplicado"
            elif valor > preco:
                nota = "multa por atraso aplicada"
            else:
                nota = "sem desconto ou multa"
            self.lbl_msg.config(
                text=f"Valor calculado pelo banco: R$ {float(valor):.2f} "
                     f"(plano R$ {float(preco):.2f} — {nota}).", fg=ACCENT)
        except Exception as e:
            self.lbl_msg.config(text=f"Erro: {e}", fg=DANGER)

    # ── PROCEDURE ─────────────────────────────────
    def _registrar(self):
        ids = self._ids()
        if not ids:
            return
        try:
            valor = float(self.e_valor.get().strip().replace(",", "."))
        except ValueError:
            self.lbl_msg.config(text="Clique em 'Calcular valor' ou informe um valor valido.", fg=DANGER)
            return
        conn = None
        try:
            conn = conectar()
            cur = conn.cursor()
            cur.execute("CALL sp_registrar_pagamento(%s, %s, %s)", (ids[0], ids[1], valor))   # <- PROCEDURE
            conn.commit()
            self._carregar_pagamentos(cur)
            cur.close(); conn.close()
            self._limpar_valor()
            self.lbl_msg.config(text="Pagamento registrado pela procedure com sucesso!", fg=SUCCESS)
        except Exception as e:
            if conn:
                conn.rollback(); conn.close()
            self.lbl_msg.config(text=f"Erro: {str(e).splitlines()[0]}", fg=DANGER)


# ════════════════════════════════════════════════
#  PAINEL: RELATORIOS COM JOIN
# ════════════════════════════════════════════════

class PainelRelatorios(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=BG)
        self._build()

    def _build(self):
        tk.Label(self, text="Relatorios", font=("Segoe UI", 16, "bold"),
                 bg=BG, fg=TEXT).pack(anchor="w", padx=24, pady=(20, 4))
        tk.Label(self, text="Situacao financeira (VIEW) e consultas com INNER JOIN e LEFT JOIN.",
                 font=("Segoe UI", 9), bg=BG, fg=MUTED).pack(anchor="w", padx=24)
        tk.Frame(self, bg="#444444", height=1).pack(fill="x", padx=24, pady=12)

        # Botoes para alternar
        btn_frame = tk.Frame(self, bg=BG)
        btn_frame.pack(anchor="w", padx=24, pady=(0, 12))

        self.tipo = tk.StringVar(value="view")

        tk.Radiobutton(btn_frame, text="VIEW — Situacao",
                       variable=self.tipo, value="view",
                       command=self.atualizar,
                       bg=BG, fg=TEXT, selectcolor=SURFACE,
                       activebackground=BG, font=("Segoe UI", 10),
                       indicatoron=False, relief="flat",
                       padx=12, pady=6, cursor="hand2").pack(side="left", padx=(0, 8))

        tk.Radiobutton(btn_frame, text="LEFT JOIN — Alunos",
                       variable=self.tipo, value="left",
                       command=self.atualizar,
                       bg=BG, fg=TEXT, selectcolor=SURFACE,
                       activebackground=BG, font=("Segoe UI", 10),
                       indicatoron=False, relief="flat",
                       padx=12, pady=6, cursor="hand2").pack(side="left", padx=(0, 8))

        tk.Radiobutton(btn_frame, text="INNER JOIN — Planos",
                       variable=self.tipo, value="inner",
                       command=self.atualizar,
                       bg=BG, fg=TEXT, selectcolor=SURFACE,
                       activebackground=BG, font=("Segoe UI", 10),
                       indicatoron=False, relief="flat",
                       padx=12, pady=6, cursor="hand2").pack(side="left")

        # Descricao do JOIN
        self.lbl_desc = tk.Label(self, text="", font=("Segoe UI", 9, "italic"),
                                  bg=BG, fg=ACCENT)
        self.lbl_desc.pack(anchor="w", padx=24, pady=(0, 8))

        # Tabela
        frame_t = tk.Frame(self, bg=SURFACE)
        frame_t.pack(fill="both", expand=True, padx=24, pady=(0, 16))

        self.tree = ttk.Treeview(frame_t, show="headings", style="Dark.Treeview")
        sb = ttk.Scrollbar(frame_t, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)

        self.lbl_total = tk.Label(self, text="", font=("Segoe UI", 9),
                                   bg=BG, fg=MUTED)
        self.lbl_total.pack(anchor="w", padx=24)

    def atualizar(self):
        t = self.tipo.get()
        if t == "view":
            self._view_situacao()
        elif t == "left":
            self._left_join()
        else:
            self._inner_join()

    def _view_situacao(self):
        self.lbl_desc.config(
            text="VIEW vw_situacao_alunos: situacao financeira consolidada de todos os alunos."
        )
        cols = ["Aluno", "Plano", "Ult. Pgto", "Vencimento", "Dias", "Total Pago", "Situacao"]
        self.tree["columns"] = cols
        for c, w in zip(cols, [100, 85, 85, 100, 40, 85, 125]):
            self.tree.heading(c, text=c)
            self.tree.column(c, width=w, anchor="w")
        cores_situacao(self.tree)
        for item in self.tree.get_children():
            self.tree.delete(item)
        try:
            conn = conectar()
            cur = conn.cursor()
            cur.execute("""
                SELECT nome, plano, ultimo_pagamento, data_vencimento,
                       dias_para_vencer, total_pago, situacao
                FROM vw_situacao_alunos
                ORDER BY CASE situacao WHEN 'Vencido' THEN 1 WHEN 'Vence em breve' THEN 2
                                       WHEN 'Sem pagamento' THEN 3 ELSE 4 END, nome
            """)
            rows = cur.fetchall()
            fmt = lambda d: d.strftime("%d/%m/%Y") if d else "—"
            for r in rows:
                self.tree.insert("", "end", tags=(r[6],), values=(
                    r[0], r[1] or "—", fmt(r[2]), fmt(r[3]),
                    r[4] if r[4] is not None else "—",
                    f"R$ {float(r[5]):.2f}", r[6]))
            self.lbl_total.config(text=f"Total: {len(rows)} aluno(s)")
            cur.close(); conn.close()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def _left_join(self):
        self.lbl_desc.config(
            text="LEFT JOIN: retorna TODOS os alunos, mesmo sem pagamento registrado."
        )
        cols = ["Nome", "Plano", "Total Pago", "Qtd Pagamentos"]
        self.tree["columns"] = cols
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=180, anchor="w")
        for item in self.tree.get_children():
            self.tree.delete(item)
        try:
            conn = conectar()
            cur = conn.cursor()
            cur.execute("""
                SELECT a.nome, a.plano,
                       COALESCE(SUM(pg.valor), 0),
                       COUNT(pg.id)
                FROM alunos a
                LEFT JOIN pagamentos pg ON pg.aluno_id = a.id
                GROUP BY a.nome, a.plano
                ORDER BY a.nome
            """)
            rows = cur.fetchall()
            for r in rows:
                self.tree.insert("", "end",
                    values=(r[0], r[1], f"R$ {float(r[2]):.2f}", f"{r[3]} pgto(s)"))
            self.lbl_total.config(text=f"Total: {len(rows)} aluno(s)")
            cur.close(); conn.close()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def _inner_join(self):
        self.lbl_desc.config(
            text="INNER JOIN: retorna apenas alunos com correspondencia na tabela de planos."
        )
        cols = ["Nome", "Email", "Plano", "Preco", "Duracao"]
        self.tree["columns"] = cols
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=150, anchor="w")
        for item in self.tree.get_children():
            self.tree.delete(item)
        try:
            conn = conectar()
            cur = conn.cursor()
            cur.execute("""
                SELECT a.nome, a.email,
                       pl.nome, pl.preco, pl.duracao_meses
                FROM alunos a
                INNER JOIN planos pl ON a.plano = pl.nome
                ORDER BY pl.preco DESC, a.nome
            """)
            rows = cur.fetchall()
            for r in rows:
                self.tree.insert("", "end",
                    values=(r[0], r[1] or "—", r[2],
                            f"R$ {float(r[3]):.2f}", f"{r[4]} mes(es)"))
            self.lbl_total.config(text=f"Total: {len(rows)} aluno(s)")
            cur.close(); conn.close()
        except Exception as e:
            messagebox.showerror("Erro", str(e))


# ════════════════════════════════════════════════
#  INICIO
# ════════════════════════════════════════════════

if __name__ == "__main__":
    root = tk.Tk()
    root.configure(bg=BG)

    def ao_logar(usuario):
        AppPrincipal(root, usuario)

    TelaLogin(root, ao_logar)
    root.mainloop()
