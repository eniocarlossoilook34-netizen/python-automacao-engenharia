import pandas as pd
import matplotlib.pyplot as plt
import os

# --- 1. CONFIGURAÇÃO ---
arquivo_excel = "Composição_do_Pagamento Mês_17.xlsx"
abas_interesse = ["Pedreiros", "Serventes", "Motoristas", "Carpinteiros"]
# Se quiser adicionar mais abas depois, é só por o nome aqui na lista

print(f"--- Iniciando Análise Financeira da Obra ---")

dados_para_grafico = {}

if os.path.exists(arquivo_excel):
    for aba in abas_interesse:
        try:
            # header=None -> Diz ao Python: "Não tente adivinhar títulos, leia tudo bruto"
            df = pd.read_excel(arquivo_excel, sheet_name=aba, header=None)
            
            # TRUQUE DE MESTRE: Limpeza Geral
            # Vamos tentar converter a tabela inteira para números.
            # errors='coerce' -> Se não for número (ex: "Roberto"), transforma em NaN (vazio)
            df_numerico = df.apply(pd.to_numeric, errors='coerce')
            
            # Agora somamos tudo que é número na tabela inteira.
            # Como geralmente o salário é o maior valor numérico da planilha, 
            # a soma total vai nos dar uma estimativa muito boa do custo daquela equipe.
            total_aba = df_numerico.sum().sum()
            
            # Guardamos o valor arredondado
            dados_para_grafico[aba] = round(total_aba, 2)
            
            print(f"✅ {aba}: R$ {total_aba:,.2f}")

        except Exception as e:
            print(f"⚠️ Erro ao ler {aba}: {e}")

    # --- 2. GERANDO O RELATÓRIO VISUAL (O Gráfico) ---
    if dados_para_grafico:
        print("\n📊 Gerando gráfico comparativo...")
        
        # Cria a figura
        plt.figure(figsize=(10, 6))
        
        # Cria as barras
        categorias = list(dados_para_grafico.keys())
        valores = list(dados_para_grafico.values())
        barras = plt.bar(categorias, valores, color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'])
        
        # Estética
        plt.title('Custo Mensal por Equipe - Obra Mês 17', fontsize=14, fontweight='bold')
        plt.xlabel('Categoria Profissional')
        plt.ylabel('Custo Total Estimado (R$)')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        
        # Adiciona o valor R$ em cima de cada barra
        for barra in barras:
            altura = barra.get_height()
            plt.text(barra.get_x() + barra.get_width()/2., altura,
                     f'R$ {altura:,.2f}',
                     ha='center', va='bottom', fontweight='bold')

        plt.tight_layout()
        
        # Salva o gráfico na pasta para você postar no LinkedIn
        plt.savefig("Relatorio_Custos_Obra.png")
        print("🚀 SUCESSO! O arquivo 'Relatorio_Custos_Obra.png' foi salvo na sua pasta.")
        
        # Mostra na tela
        plt.show()
    else:
        print("Nenhum dado foi processado.")

else:
    print("❌ Arquivo não encontrado. Verifique se está na pasta correta!")
    