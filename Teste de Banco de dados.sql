# Baixar arquivos CSV do repositório
url_contabeis = "https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/"
url_operadoras = "https://dadosabertos.ans.gov.br/FTP/PDA/operadoras_de_plano_de_saude_ativas/"

download_pdf(url_contabeis, "demonstracoes_contabeis.csv")
download_pdf(url_operadoras, "operadoras_ativas.csv")

-- Criação das tabelas
CREATE TABLE operadoras (
    id INT PRIMARY KEY,
    nome VARCHAR(255),
    cnpj VARCHAR(14)
);

CREATE TABLE despesas (
    id INT PRIMARY KEY,
    operadora_id INT,
    categoria VARCHAR(255),
    valor DECIMAL(10,2),
    trimestre DATE
);

-- Query analítica
SELECT nome, SUM(valor) as total_despesas
FROM despesas
JOIN operadoras ON despesas.operadora_id = operadoras.id
WHERE categoria = "EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR"
AND trimestre BETWEEN '2024-10-01' AND '2024-12-31'
GROUP BY operadoras.id
ORDER BY total_despesas DESC
LIMIT 10;
