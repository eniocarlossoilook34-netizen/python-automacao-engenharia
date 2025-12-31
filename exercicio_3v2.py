import tkinter as tk
from tkinter import simpledialog, messagebox

# Configuração inicial para esconder a janela principal "fantasma" do Tkinter
root = tk.Tk()
root.withdraw() 

def programa_visual():
    # Loop Infinito para o programa rodar até o usuário querer sair
    while True:
        # 1. Entrada de Dados (Pop-up com campo de digitação)
        # O próprio Tkinter já trata se é número ou letra (askfloat)
        valor_1 = simpledialog.askfloat("Entrada", "Digite o primeiro valor:")
        
        # Se o usuário clicar em Cancelar, o valor será None. Paramos o programa.
        if valor_1 is None: 
            break

        valor_2 = simpledialog.askfloat("Entrada", "Digite o segundo valor:")
        if valor_2 is None:
            break

        # 2. Lógica de Comparação
        mensagem_final = ""
        
        if valor_1 > valor_2:
            mensagem_final = f"O valor {valor_1} é MAIOR que {valor_2}"
        elif valor_1 < valor_2:
            mensagem_final = f"O valor {valor_2} é MAIOR que {valor_1}"
        else:
            mensagem_final = f"Os dois valores são IGUAIS: {valor_1}"

        # 3. Saída Visual (Pop-up de alerta)
        messagebox.showinfo("Resultado da Comparação", mensagem_final)
        
        # Pergunta se quer continuar
        resposta = messagebox.askyesno("Continuar?", "Deseja comparar novos números?")
        if not resposta:
            break

# Executa o programa
programa_visual()