import math
import matplotlib.pyplot as plt

# --- ÁREA DAS FERRAMENTAS (FUNÇÕES) ---


def resolver_bhaskara(a, b, c):
    """
    Calcula as raízes de uma equação quadrática.
    Entrada: coeficientes a, b, c.
    Saída: Uma lista com as raízes [x1, x2] ou None se não houver raízes.
    """
    # 1. Calcula o Delta
    delta = b**2 - 4 * a * c

    # 2. Verifica raízes
    if delta < 0:
        return None  # "None" é o jeito do Python dizer "Vazio" ou "Nada"
    else:
        x1 = (-b + math.sqrt(delta)) / (2 * a)
        x2 = (-b - math.sqrt(delta)) / (2 * a)
        return [x1, x2] # Devolve a lista com os dois resultados

def gerar_grafico(a, b, c):
    """
    Gera o gráfico visual da parábola.
    """
    print(f"Gerando gráfico para {a}x² + {b}x + {c}...")
    
    eixo_x = range(-15, 16)
    eixo_y = []
    
    for x in eixo_x:
        y = (a * (x**2)) + (b * x) + c
        eixo_y.append(y)
        
    plt.figure(figsize=(8, 6))
    plt.plot(eixo_x, eixo_y, label=f'{a}x² + {b}x + {c}')
    plt.axhline(0, color='black', linewidth=1)
    plt.axvline(0, color='black', linewidth=1)
    plt.title(f"Função Quadrática: {a}x² + {b}x + {c}")
    plt.legend()
    plt.grid(True, linestyle='--')
    plt.show()

# --- ÁREA DE EXECUÇÃO (MAIN) ---
# É aqui que o programa realmente começa a rodar.

print("--- Sistema de Análise Quadrática v2.0 ---")

# Coletamos os dados
val_a = float(input("Digite A: "))
val_b = float(input("Digite B: "))
val_c = float(input("Digite C: "))

# CHAMADA DA FUNÇÃO 1: O Cálculo
# Note que eu jogo os valores val_a, val_b, val_c para dentro da "máquina"
resultado = resolver_bhaskara(val_a, val_b, val_c)

# Verificamos o que a função devolveu
if resultado == None:
    print("❌ Não há raízes reais (Delta negativo).")
else:
    # Como o resultado é uma lista [x1, x2], acessamos pelos índices 0 e 1
    print(f"✅ Sucesso! As raízes são: {resultado[0]:.2f} e {resultado[1]:.2f}")

# CHAMADA DA FUNÇÃO 2: O Gráfico
# Perguntamos se o usuário quer ver o gráfico
ver_grafico = input("Deseja ver o gráfico? (s/n): ")

if ver_grafico.lower() == 's':
    gerar_grafico(val_a, val_b, val_c)
else:

    print("Ok, encerrando o programa.")
