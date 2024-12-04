import os
import tkinter as tk
from tkinter import messagebox

# Caminho para o arquivo hosts no Windows
hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
redirect_ip = "127.0.0.1"

def block_site(url):
    """Bloqueia o domínio principal do site no arquivo hosts."""
    domain = url.split("//")[-1].split("/")[0]  # Extrai o domínio principal
    try:
        # Abre o arquivo hosts para edição
        with open(hosts_path, 'r+') as file:
            content = file.read()
            # Verifica se o domínio já foi bloqueado
            if domain not in content:
                # Escreve a nova linha de bloqueio
                file.write(f"\n{redirect_ip} {domain}\n")
                file.write(f"{redirect_ip} www.{domain}\n")
                messagebox.showinfo("Sucesso", f"Site {domain} bloqueado com sucesso!")
            else:
                messagebox.showinfo("Info", f"Site {domain} já está bloqueado.")
    except PermissionError:
        messagebox.showerror("Erro", "Permissões insuficientes. Execute o script como administrador.")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro: {e}")

def unblock_site(url):
    """Desbloqueia o domínio principal do site no arquivo hosts."""
    domain = url.split("//")[-1].split("/")[0]  # Extrai o domínio principal
    try:
        # Abre o arquivo hosts para edição
        with open(hosts_path, 'r+') as file:
            content = file.readlines()
            file.seek(0)
            # Filtra as linhas que não contêm o domínio a ser desbloqueado
            content = [line for line in content if domain not in line]
            file.truncate(0)  # Limpa o conteúdo do arquivo
            file.writelines(content)
            messagebox.showinfo("Sucesso", f"Site {domain} desbloqueado com sucesso!")
    except PermissionError:
        messagebox.showerror("Erro", "Permissões insuficientes. Execute o script como administrador.")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro: {e}")

def show_blocked_sites():
    """Exibe os sites bloqueados no arquivo hosts."""
    try:
        with open(hosts_path, 'r') as file:
            content = file.readlines()
            blocked_sites = [line.split()[1] for line in content if line.startswith(redirect_ip)]
            if blocked_sites:
                blocked_sites = "\n".join(blocked_sites)
                messagebox.showinfo("Sites Bloqueados", f"Sites Bloqueados:\n{blocked_sites}")
            else:
                messagebox.showinfo("Sem Sites Bloqueados", "Não há sites bloqueados no momento.")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao ler os sites bloqueados: {e}")

# GUI para o usuário interagir
def show_gui():
    def on_block_click():
        url = url_entry.get("1.0", "end-1c")  # Obtém o texto do campo de entrada
        if url:
            block_site(url)
        else:
            messagebox.showerror("Erro", "Por favor, insira uma URL válida.")

    def on_unblock_click():
        url = url_entry.get("1.0", "end-1c")  # Obtém o texto do campo de entrada
        if url:
            unblock_site(url)
        else:
            messagebox.showerror("Erro", "Por favor, insira uma URL válida.")

    def on_show_blocked_click():
        show_blocked_sites()

    # Janela principal com o tema escuro e design elegante
    window = tk.Tk()
    window.title("Bloqueador de Sites")
    window.geometry("600x500")  # Tamanho da janela
    window.config(bg="#2e2e2e")  # Cor de fundo escura

    # Estilo de fonte
    font_style = ("Helvetica", 14)
    title_font = ("Helvetica", 16, "bold")

    # Layout da GUI
    title_label = tk.Label(window, text="Bloqueador de Sites", font=title_font, bg="#2e2e2e", fg="#FF5722")
    title_label.pack(padx=20, pady=20)

    label = tk.Label(window, text="Digite a URL do site a bloquear/desbloquear:", font=font_style, bg="#2e2e2e", fg="white")
    label.pack(padx=20, pady=10)

    # Campo de texto para URLs, agora usando o tk.Text para permitir mais altura
    url_entry = tk.Text(window, width=60, height=3, font=font_style, bd=0, relief="solid", bg="#444444", fg="white", wrap="word")
    url_entry.pack(padx=20, pady=10)

    # Função para estilizar os botões
    def style_button(button):
        button.config(
            font=font_style,
            bg="#4CAF50",
            fg="white",
            relief="flat",
            bd=0,
            padx=10,
            pady=10
        )
        button.bind("<Enter>", lambda e: button.config(bg="#45a049"))
        button.bind("<Leave>", lambda e: button.config(bg="#4CAF50"))

    # Botões com estilo moderno
    block_button = tk.Button(window, text="Bloquear Site", command=on_block_click)
    style_button(block_button)
    block_button.pack(padx=10, pady=10)

    unblock_button = tk.Button(window, text="Desbloquear Site", command=on_unblock_click)
    style_button(unblock_button)
    unblock_button.pack(padx=10, pady=10)

    show_button = tk.Button(window, text="Mostrar Sites Bloqueados", command=on_show_blocked_click)
    style_button(show_button)
    show_button.pack(padx=10, pady=10)

    window.mainloop()

# Executa a interface gráfica
show_gui()
