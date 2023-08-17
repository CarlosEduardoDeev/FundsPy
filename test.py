import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

def get_fund_data(fund_url):
    response = requests.get(fund_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Encontrar o elemento <div> com a classe "headerTicker__content__price" para o preço
    price_div = soup.find('div', class_='headerTicker__content__price')

    # Verificar se o elemento foi encontrado
    if price_div is not None:
        valor_element = price_div.find('p')
        valor_preco = valor_element.text.strip() if valor_element else "Valor não encontrado"
    else:
        valor_preco = "Elemento <div> headerTicker__content__price não encontrado."

    # Encontrar todos os elementos <div> com a classe "indicators__box"
    indicators_boxes = soup.find_all('div', class_='indicators__box')

    # Valores padrão caso algum valor não seja encontrado
    dy = "Valor não encontrado"
    produto = "Valor não encontrado"
    pvp = "Valor não encontrado"
    valor_por_mes = "Valor não encontrado"
    rentabilidade_mes = "Valor não encontrado"
    ultimo_rendimento = "Valor não encontrado"

    # Verificar se existem elementos <div> encontrados
    if indicators_boxes:
        # Encontrar a segunda indicators__box para Último Rendimento
        segunda_box = indicators_boxes[1]
        b_element_ultimo_rendimento = segunda_box.find('b')
        
        # Verificar se o elemento <b> foi encontrado na segunda indicators__box para Último Rendimento
        if b_element_ultimo_rendimento:
            # Obter o texto dentro do elemento <b> e remover o espaço em branco
            ultimo_rendimento = b_element_ultimo_rendimento.get_text(strip=True)
        
        # Encontrar a terceira indicators__box para Dividend Yield
        terceira_box = indicators_boxes[2]

        # Encontrar o elemento <b> dentro da terceira indicators__box para DY
        b_element_dy = terceira_box.find('b')
        
        # Verificar se o elemento <b> foi encontrado
        if b_element_dy:
            # Obter o texto dentro do elemento <b> e remover o espaço em branco
            dy = b_element_dy.get_text(strip=True)
            
            # Encontrar o primeiro elemento <b> na segunda indicators__box para Produto
            segundo_box = indicators_boxes[1]
            b_element_produto = segundo_box.find('b')
            
            # Verificar se o elemento <b> foi encontrado na segunda indicators__box para Produto
            if b_element_produto:
                # Obter o texto dentro do elemento <b> e remover o espaço em branco
                produto = b_element_produto.get_text(strip=True)
                
                # Encontrar o elemento <b> na sétima indicators__box para P/VP
                setima_box = indicators_boxes[6]
                b_element_pvp = setima_box.find('b')
                
                # Verificar se o elemento <b> foi encontrado na sétima indicators__box para P/VP
                if b_element_pvp:
                    # Obter o texto dentro do elemento <b> e remover o espaço em branco
                    pvp = b_element_pvp.get_text(strip=True)
                    
                    # Encontrar o elemento <b> na quinta indicators__box para Valor por Mês
                    quinta_box = indicators_boxes[4]
                    b_element_valor_por_mes = quinta_box.find('b')
                    
                    # Verificar se o elemento <b> foi encontrado na quinta indicators__box para Valor por Mês
                    if b_element_valor_por_mes:
                        # Obter o texto dentro do elemento <b> e remover o espaço em branco
                        valor_por_mes = b_element_valor_por_mes.get_text(strip=True)
                        
                        # Encontrar o elemento <b> na sexta indicators__box para Rentabilidade no Mês
                        sexta_box = indicators_boxes[5]
                        b_element_rentabilidade_mes = sexta_box.find('b')
                        
                        # Verificar se o elemento <b> foi encontrado na sexta indicators__box para Rentabilidade no Mês
                        if b_element_rentabilidade_mes:
                            # Obter o texto dentro do elemento <b> e remover o espaço em branco
                            rentabilidade_mes = b_element_rentabilidade_mes.get_text(strip=True)
    
    nome_fundo = fund_url.split('/')[-1]

    return {
        "URL": fund_url,
        "Nome do Fundo": nome_fundo.upper(),
        "Preço": valor_preco,
        "Último Rendimento": ultimo_rendimento,
        "Valor Pago por Mês": valor_por_mes,
        "Dividend Yield (DY)": dy,
        "Rentabilidade no Mês": rentabilidade_mes,
        "P/VP": pvp
    }

   
def main():
    # Lista de URLs dos fundos imobiliários
    fund_urls = [
        "https://www.fundsexplorer.com.br/funds/galg11",
        "https://www.fundsexplorer.com.br/funds/btci11",
        "https://www.fundsexplorer.com.br/funds/mchf11",
        "https://www.fundsexplorer.com.br/funds/mxrf11",
        "https://www.fundsexplorer.com.br/funds/vgir11",
        "https://www.fundsexplorer.com.br/funds/vghf11",
        "https://www.fundsexplorer.com.br/funds/vino11",
        "https://www.fundsexplorer.com.br/funds/rura11",
        "https://www.fundsexplorer.com.br/funds/kisu11",
        "https://www.fundsexplorer.com.br/funds/vgia11"

        # Adicione mais URLs aqui
    ]
    
    fund_data = []

    for fund_url in fund_urls:
        fund_info = get_fund_data(fund_url)
        fund_data.append(fund_info)

    df = pd.DataFrame(fund_data)

    # Caminho completo para a pasta onde você deseja salvar os arquivos Excel
    save_folder = "C:/Users/kadug/Documents/PythoWebFunds"

    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    excel_file = os.path.join(save_folder, "fund_data.xlsx")

    # Lê o arquivo Excel existente
    existing_excel_file = "C:/Users/kadug/Documents/PythoWebFunds/Funds2023.xlsx"
    print(existing_excel_file)
    existing_df = pd.read_excel(existing_excel_file)

    # Cria um objeto ExcelWriter para salvar os DataFrames em diferentes planilhas
    with pd.ExcelWriter(excel_file) as writer:
        # Salva o DataFrame da extração em uma nova planilha chamada "Extracao"
        df.to_excel(writer, sheet_name="Extracao", index=False)

        # Salva o DataFrame existente em outra planilha
        existing_df.to_excel(writer, sheet_name="Dados", index=False)

    print("Dados dos fundos e DataFrame existente salvos em", excel_file)

if __name__ == "__main__":
    main()





