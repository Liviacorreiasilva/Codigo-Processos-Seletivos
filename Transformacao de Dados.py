import pdfplumber #extração de texto das tabelas
import csv

def extrair_dados_da_tabela_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        all_pages_text = []
        for page in pdf.pages:
            # Extraindo a tabela da página
            table = page.extract_table()
            if table:
                all_pages_text.extend(table)
        return all_pages_text

# Extrair dados do Anexo I
dados_tabela = extrair_dados_da_tabela_pdf("Anexo_I.pdf")

# Salvar os dados em um arquivo CSV
def salvar_csv(dados, nome_arquivo):
    with open(nome_arquivo, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(dados)
    print(f'{nome_arquivo} salvo com sucesso!')

# Salvar a tabela extraída no CSV
salvar_csv(dados_tabela, "rol_procedimentos.csv")

# Substituindo abreviações
def substituir_abreviacoes(dados):
    for row in dados:
        if "OD" in row:
            row[row.index("OD")] = "Descrição Completa OD"
        if "AMB" in row:
            row[row.index("AMB")] = "Descrição Completa AMB"
    return dados

# Substituir as abreviações na tabela extraída
dados_modificados = substituir_abreviacoes(dados_tabela)

# Salvar o CSV com os dados modificados
salvar_csv(dados_modificados, "rol_procedimentos_modificado.csv")

# Compactar o CSV
compactar_em_zip("Teste_Livia_correia.zip", ["rol_procedimentos_modificado.csv"])
