import tkinter as tk
from tkinter import messagebox
import sqlite3

# === BANCO DE DADOS ===
def conectar_banco():
    conexao = sqlite3.connect("tarefas.db")
    cursor = conexao.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            concluida INTEGER DEFAULT 0
        )
    """)
    conexao.commit()
    return conexao

# === FUNÇÕES ===
def carregar_tarefas():
    lista_tarefas.delete(0, tk.END)
    cursor = conexao.cursor()
    cursor.execute("SELECT id, titulo, concluida FROM tarefas")
    for tarefa in cursor.fetchall():
        titulo = tarefa[1]
        if tarefa[2] == 1:
            titulo += " ✔️"
        lista_tarefas.insert(tk.END, f"{tarefa[0]} - {titulo}")

def adicionar_tarefa():
    titulo = entrada_tarefa.get().strip()
    if titulo == "":
        messagebox.showwarning("Aviso", "Digite uma tarefa!")
        return
    cursor = conexao.cursor()
    cursor.execute("INSERT INTO tarefas (titulo) VALUES (?)", (titulo,))
    conexao.commit()
    entrada_tarefa.delete(0, tk.END)
    carregar_tarefas()

def excluir_tarefa():
    selecionado = lista_tarefas.curselection()
    if not selecionado:
        messagebox.showwarning("Aviso", "Selecione uma tarefa para excluir!")
        return
    id_tarefa = int(lista_tarefas.get(selecionado).split(" - ")[0])
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM tarefas WHERE id = ?", (id_tarefa,))
    conexao.commit()
    carregar_tarefas()

def marcar_concluida():
    selecionado = lista_tarefas.curselection()
    if not selecionado:
        messagebox.showwarning("Aviso", "Selecione uma tarefa!")
        return
    id_tarefa = int(lista_tarefas.get(selecionado).split(" - ")[0])
    cursor = conexao.cursor()
    cursor.execute("UPDATE tarefas SET concluida = 1 WHERE id = ?", (id_tarefa,))
    conexao.commit()
    carregar_tarefas()

# === INTERFACE ===
conexao = conectar_banco()

janela = tk.Tk()
janela.title("Gerenciador de Tarefas")
janela.geometry("400x500")
janela.configure(bg="#1e1e1e")

titulo = tk.Label(
    janela,
    text="Minhas Tarefas",
    font=("Arial", 18, "bold"),
    bg="#000000",
    fg="#ffffff"
)
titulo.pack(pady=10)

entrada_tarefa = tk.Entry(
    janela,
    font=("Arial", 14),
    width=25,
    bd=2,
    relief="flat",
    bg="#000000",
    fg="#ffffff",
    insertbackground="white"
)
entrada_tarefa.pack(pady=10)

frame_botoes = tk.Frame(janela, bg="#1e1e1e")
frame_botoes.pack(pady=5)

tk.Button(
    frame_botoes,
    text="Adicionar",
    font=("Arial", 12, "bold"),
    bg="#0078d7",
    fg="white",
    relief="flat",
    command=adicionar_tarefa
).grid(row=0, column=0, padx=5)

tk.Button(
    frame_botoes,
    text="Concluir",
    font=("Arial", 12, "bold"),
    bg="#107c10",
    fg="white",
    relief="flat",
    command=marcar_concluida
).grid(row=0, column=1, padx=5)

tk.Button(
    frame_botoes,
    text="Excluir",
    font=("Arial", 12, "bold"),
    bg="#e81123",
    fg="white",
    relief="flat",
    command=excluir_tarefa
).grid(row=0, column=2, padx=5)

# Lista de tarefas
lista_tarefas = tk.Listbox(
    janela,
    font=("Arial", 14),
    width=30,
    height=15,
    bg="#252526",
    fg="#ffffff",
    selectbackground="#0078d7",
    selectmode=tk.SINGLE
)
lista_tarefas.pack(pady=10)

carregar_tarefas()
janela.mainloop()

# Fecha conexão ao encerrar
conexao.close()
