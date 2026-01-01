from fpdf import FPDF
from datetime import datetime
import os

# --- CONFIGURAÇÃO ---
nome_arquivo_saida = "Relatorio_Obra_Mes17.pdf"
imagem_grafico = "Relatorio_Custos_Obra.png"
nome_autor = "Enio Oliveira - Engenharia"

class PDF(FPDF):
    def header(self):
        # Seleciona fonte Arial, Negrito, tamanho 12
        self.set_font('Helvetica', 'B', 12)
        # Título no topo da página
        self.cell(0, 10, 'Relatório Executivo de Custos - Obra CAPIXABAS', border=False, new_x="LMARGIN", new_y="NEXT", align='C')
        self.ln(5) # Pula uma linha de 5mm

    def footer(self):
        # Vai para 1.5 cm do final da página
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        # Número da página e Data de Geração
        data_hoje = datetime.now().strftime("%d/%m/%Y")
        texto_rodape = f'Gerado em {data_hoje} por {nome_autor} | Página {self.page_no()}'
        self.cell(0, 10, texto_rodape, align='C')

# --- CRIAÇÃO DO DOCUMENTO ---
print("📄 Iniciando geração do PDF...")

# Cria o objeto PDF (Orientação Portrait, Unidade mm, Formato A4)
pdf = PDF(orientation='P', unit='mm', format='A4')
pdf.add_page()

# 1. Título da Seção
pdf.set_font('Helvetica', 'B', 16)
pdf.cell(0, 10, 'Análise de Mão de Obra', new_x="LMARGIN", new_y="NEXT", align='L')
pdf.ln(5)

# 2. Texto Explicativo (Contexto)
pdf.set_font('Helvetica', '', 12)
texto_intro = (
    "Este relatório apresenta a consolidação dos custos mensais referentes ao 'Mês 17'. "
    "A análise foi realizada via processamento automatizado de dados, unificando as abas "
    "de pagamentos de Pedreiros, Serventes, Motoristas e Carpinteiros."
)
# multi_cell permite que o texto quebre linhas automaticamente (como um parágrafo)
pdf.multi_cell(0, 10, texto_intro)
pdf.ln(5)

# 3. Inserindo o Gráfico
if os.path.exists(imagem_grafico):
    print("🖼️ Inserindo gráfico no PDF...")
    # x=10 (margem esquerda), y=None (logo abaixo do texto), w=190 (largura quase total do A4)
    pdf.image(imagem_grafico, x=10, w=190)
else:
    print("⚠️ AVISO: Imagem do gráfico não encontrada! O PDF ficará sem o gráfico.")
    pdf.cell(0, 10, "[ERRO: Gráfico não encontrado]", new_x="LMARGIN", new_y="NEXT")

# 4. Conclusão
pdf.ln(10) # Pula espaço depois da imagem
pdf.set_font('Helvetica', 'B', 12)
pdf.cell(0, 10, 'Conclusão Automática:', new_x="LMARGIN", new_y="NEXT")

pdf.set_font('Helvetica', '', 12)
pdf.multi_cell(0, 10, "Os dados indicam a distribuição orçamentária atual. Recomenda-se revisão dos custos da categoria de maior impacto (Motoristas) para o próximo ciclo.")

# --- SALVAR ---
try:
    pdf.output(nome_arquivo_saida)
    print(f"✅ SUCESSO! PDF salvo como '{nome_arquivo_saida}'.")
except PermissionError:
    print("❌ ERRO: O arquivo PDF já está aberto! Feche o PDF e tente de novo.")