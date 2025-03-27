# 1 - IMPORTAÇÃO DAS BIBLIOTECAS:

import requests  # Realiza a requisição HTTP
from bs4 import BeautifulSoup  #analisa o documento HTML para extrair os dados
import zipfile  #cria os arquivos zip com o arquivo em pdf
import pathlib  #manipulacao de arquivos e caminho dos arquivos

# 2- FUNCAO PARA ACESSAR A PAGINA WEB E EXTRAIR OS LINKS DO PDF:

def get_pdf_links(url): #envia a requisicao get para a url e retornarC! a resposta para o servidor
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'lxml')  #coverterte a resosta em  html para objeto para que possa ser manipulado
    pdf_links = []  #criacao de uma pasta vazia para  armazenar os links dos pdf

    # Encontrar todos os links que terminam com '.pdf'
    for link in soup.find_all('a', href=True):  
        if 'pdf' in link['href']:
            pdf_links.append(link['href'])  #adiciona o link do pfd a uma lista
    
    return pdf_links #retorna a lista com os links dos pfds encontrados

# 3-  FUNÇAO PARA BAIXAR OS ARQUIVOS PDF:

def download_pdfs(pdf_links, download_folder):
    pathlib.Path(download_folder).mkdir(parents=True, exist_ok=True)  #Verifica se a pasta de download existe,caso  nao existir sera criada uma pasta usando makedirs

    pdf_paths = []  #criacao de uma lita  para armazenar os caminhos dos arquivos do pdf baixado.
    for pdf_url in pdf_links:
        if not pdf_url.startswith("http"):
            pdf_url = "https://www.gov.br" + pdf_url  #Corrige links relativos

        pdf_name = os.path.basename(pdf_url)  #Extrai o nome do arquivo PDF a partir do link
        pdf_path = pathlib.Path(download_folder) / pdf_name  #Cria o caminho completo do arquivo pdf salvo 

        #Baixa o arquivo PDF
        response = requests.get(pdf_url)
        with open(pdf_path, 'wb') as f:  #Abre o arquivo em modo binário para escrita
            f.write(response.content)

        pdf_paths.append(pdf_path)  #Adiciona o caminho na lista de arquivos

    return pdf_paths  #Retorna a lista com os caminhos dos arquivos PDF

# 4- FUNCAO PARA COMPACTAR OS ARQUIVOS PDF EM UM UNICO ARQUIVO ZIP:

def compress_pdfs(pdf_paths, zip_filename):
    with zipfile.ZipFile(zip_filename, 'w') as zipf: #cria um novo arquivo zip
        for pdf in pdf_paths:
            zipf.write(pdf, arcname=pathlib.Path(pdf).name)  #Adiciona o arquivo ao ZIP sem o caminho completo

# 5- FUNÇAO PRINCIPAL PARA QUE SEJA EXECUTADO OS PROCESSOS E IMPRIMIR CADA ETAPA:

def main():
    url = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-dasociedade/atualizacao-do-rol-de-procedimentos"
    
    #Obter os links dos PDFs
    print("Obtendo os links dos PDFs...")
    pdf_links = get_pdf_links(url)

    #Baixar os PDFs
    print("Baixando os PDFs...")
    download_folder = "baixados_pdfs"
    pdf_paths = download_pdfs(pdf_links, download_folder)

     #Compactar os PDFs em um arquivo ZIP
    print("Compactando os PDFs em um arquivo ZIP...")
    zip_filename = "rol_procedimentos.zip"
    compress_pdfs(pdf_paths, zip_filename)

    print(f"Arquivos compactados em {zip_filename}")

# 6- EXECUCAO DO CODIGO:

#a função main() será executada apenas quando o script for executado diretamente
if __name__ == "__main__":
    main()
