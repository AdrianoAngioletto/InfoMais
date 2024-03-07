from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from time import sleep
import pyautogui
import json
import os
import unicodedata


"""
author =  AdrianoAngioletto

Description =  separei em metodos, o scraping, para que fique legivel cada tópico.


"""


class Desafio:

    chrome_opcao = ChromeOptions() # instanciando classe options
    chrome_opcao.add_argument('--start-maximized') # deixando tela maximizada.
    drive = Chrome(chrome_opcao)  # instancia do objeto chrome, importante para abrir navegador. podendo tambem ser utilizado outros.
    
    
    def __init__(self) -> None:
        
        bemvindo = '''
                +===========================================================================+
                |             DESAFIO WEB SCRAPING                                          |
                |                                                                           |
                |                                                                           |
                |          INFOS SIMPLES   https://infosimples.com/                         |
                |                                                                           |
                |                                                                           |    
                |                                                                           |
                | Dev:  AdrianoAngioletto                                                   |
                +===========================================================================+
                '''
        print(bemvindo)
        
    
    def EncontraElementos(self, valor: str, Element: object =By.XPATH,) -> object:
        
            # função para facilitar a vida, pegar o elemento sem necessidade de ficar escrevendo find .. etc
                                                     
            elemento = self.drive.find_element(Element, valor)
                
            
            return elemento
    
    
    def limpar_descricao(self, descricao):
        #funcao responsavel por arrumar texto
        
        
        descricao_sem_quebras = descricao.replace('\n', ' ').replace('\r', '')
        
        # Normaliza os caracteres especiais
        descricao_normalizada = unicodedata.normalize('NFKD', descricao_sem_quebras).encode('ASCII', 'ignore').decode('utf-8')

        return descricao_normalizada

        

    def IniciaProdutos(self)-> None:
            
        # função responsavel por iniciar o site, pegar os elementos relacionado a Produtos e converter o 
        # objeto no tipo de dado necessario.
        
        self.drive.get('https://infosimples.com/vagas/desafio/commercia/product.html')
        
        sleep(5) # tempo para navegador carregar pagina
        
                
        javascript = 'window.alert("BEM VINDO AO ROBÔ, INFO-MAIS-DESAFIO, Aguarde iremos pegar todos dados")'
        
        self.drive.execute_script(javascript)

        
        sleep(4) # time obrigatorio para o aviso em javascript 
        
        pyautogui.hotkey('enter') # só para o javascript não parar a exec, se caso usuario nao apertar em nada
        

        
        produto1 = self.EncontraElementos('/html/body/div/section/div/div[2]/div[1]/div[1]/div[3]/div[1]') # PRODUTO 1 EM OBJETO
        
        self.produto1Texto = produto1.text # PRODUTO 1 TITULO EM STRING
        
        produto1_marca = self.EncontraElementos('/html/body/div/section/div/div[1]') # PRODUTO 1 MARCA OBJETO <
        
        self.produto1_marca = produto1_marca.text # PRODUTO 1 MARCA EM STRING
        
        produto1_categoria = self.EncontraElementos('/html/body/div/section/div/nav') # PRODUTO 1 CATEGORIA OBJETO 
        
        self.produto1_categoria = produto1_categoria.text.replace('>' , ' ') #PRODUTO 1 CATEGORIA EM STRING
        
        descricao_geral_dos_produtos = self.EncontraElementos('/html/body/div/section/div/div[3]') # OBJETO DIV, ONDE FICA DESCRICAO DOS PRODUTOS
        
        self.descricao = descricao_geral_dos_produtos.text # DESCRIÇÃO GERAL EM TEXTO
        
        self.descricao_edit = self.descricao.replace("Description", "") # Aqui só removi a palavra Description pq não é necessaria.
        
        self.descricao_edit = self.limpar_descricao(self.descricao_edit)# chamei metodo pra corrigir o texto
        
        valor_produto_1_atual = self.EncontraElementos('/html/body/div/section/div/div[2]/div[1]/div[1]/div[3]/div[2]') # PEGANDO OBJETO
        
        valor_produto_1_antigo = self.EncontraElementos('/html/body/div/section/div/div[2]/div[1]/div[1]/div[3]/div[3]') # OBJETO

        texto_valor_produto_1_atual = valor_produto_1_atual.text # CONVERTENDO EM TEXTO PQ É UM OBJETO
        
        texto_valor_produto_1_antigo = valor_produto_1_antigo.text # CONVERTENDO EM TEXTO PQ É UM OBJETO
        
        # CONVERTENDO PARA FLOAT E TIRANDO O $
        self.valor_produto_1_atual_float = float(texto_valor_produto_1_atual.replace("R$ ", "").replace(",", "."))
        self.valor_produto_1_antigo_float = float(texto_valor_produto_1_antigo.replace("R$ ", "").replace(",", "."))

        print(f'valor novo {self.valor_produto_1_atual_float}, valor veio {self.valor_produto_1_antigo_float}')

        
        


        print(f'valor novo {self.valor_produto_1_atual_float},', f' valor veio {self.valor_produto_1_antigo_float}')
       
    def IniciaPropriedadesProduto(self)-> None:
                
         # funcão responsavel por pegar Propriedades como manda o PDF.       
        tabela_produtos = self.EncontraElementos('/html/body/div/section/div/div[4]/table') # TABELA TODA OBJETO
                
        self.texto_tabela = tabela_produtos.text # TABELA EM TEXTO
        
        tabela_produtos_adicionais = self.EncontraElementos('//*[@id="propadd"]/table') # TABELA PRODUTOS ADICIONAIS OBJETO
        
        self.texto_tabela_adicionais = tabela_produtos_adicionais.text  # TABELA ADICIONAL TEXTO
        
        # ESSE IF É PARA TRATAR OS -  E PALAVRA NONE, MÁS LEGIVEL.
        if '-' in self.texto_tabela_adicionais or self.texto_tabela_adicionais == 'None':
                           
                self.texto_tabela_adicionais = self.texto_tabela_adicionais.replace('-', '0')
                self.texto_tabela_adicionais = self.texto_tabela_adicionais.replace('None', '0')
                
        if 'Storage temperature 0 0 25ºC' in self.texto_tabela_adicionais:
                # AQUI PARA ADICIONAR DE VOLTA O - QUE FOI RETIRADO NO PRIMEIRO IF
                self.texto_tabela_adicionais = self.texto_tabela_adicionais.replace('Storage temperature 0 0 25ºC', 'Storage temperature 0 - 25ºC')
                
                self.texto_tabela = self.limpar_descricao(self.texto_tabela)
                self.texto_tabela_adicionais = self.limpar_descricao(self.texto_tabela_adicionais)

    def calcular_media_avaliacoes(*avaliacoes)-> float:
        
 
        # AQUI TOU ASSUMINDO QUE 1 ESTRELA, EQUIVALE HÁ 1. DAI POR DIANTE
        mapeamento_estrelas = {'★': 1, '★★': 2, '★★★': 3, '★★★★': 4, '★★★★★': 5}
        
        # Converte as avaliações para valores numéricos e calcula a média
        valores_avaliacoes = [mapeamento_estrelas.get(avaliacao, 0) for avaliacao in avaliacoes]
        media_avaliacoes = sum(valores_avaliacoes) / len(valores_avaliacoes)
        
        # ARENDONDA DUAS CASAS DECIMAIS.
        media_avaliacoes = round(media_avaliacoes, 2)
        
        
        return media_avaliacoes


    def ProdutosReview(self)-> None:
            
         # FUNCAO RESPONSAVEL, POR PEGAR AS REVIEWS.
         
            # ----- PRIMEIRA VIEW -------------- #

            self.primeira_review = self.EncontraElementos('//*[@id="comments"]/div[1]')
            
            primeira_review =  self.primeira_review.text
            
            linhas = primeira_review.split('\n')

            review_dict = {
                'NOME': linhas[0].strip(),
                'DATA': linhas[1].strip(),
                'SCORE': linhas[2].strip(),
                'AVALIAÇÃO': linhas[3].strip()
                }
            
    
            # ----- FIM  DA PRIMEIRA  REVIEW -------------- #
            

            # ----- Segunda VIEW -------------- #
            
            self.segunda_review = self.EncontraElementos('//*[@id="comments"]/div[2]')
            
            segunda_review =  self.segunda_review.text
            
            linhas = segunda_review.split('\n')

            review2_dict = {
                'NOME': linhas[0].strip(),
                'DATA': linhas[1].strip(),
                'SCORE': linhas[2].strip(),
                'AVALIAÇÃO': linhas[3].strip()
                }
            
          # ----- FIM DA SEGUNDA REVIEW -------------- #
          
          
            # ----- TERCEIRA VIEW -------------- #
            
            self.terceira_review = self.EncontraElementos('//*[@id="comments"]/div[3]')
            
            terceira_review =  self.terceira_review.text
            
            linhas = terceira_review.split('\n')

            review3_dict = {
                'NOME': linhas[0].strip(),
                'DATA': linhas[1].strip(),
                'SCORE': linhas[2].strip(),
                'AVALIAÇÃO': linhas[3].strip()
                }
            
            
            # ----- FIM DA TERCEIRA REVIEW -------------- #
            
            
            # PARTE DA MEDIA BASEADO NAS ESTRELAS
            self.avaliacao1 = '★★★★☆'
            self.avaliacao2 = '★☆☆☆☆'
            self.avaliacao3 = '★★★★★'
        
            media_avaliacoes = self.calcular_media_avaliacoes(self.avaliacao1, self.avaliacao2, self.avaliacao3)
            
            url_pagina = 'https://infosimples.com/vagas/desafio/commercia/product.html'
            

    def CriaPasta(self)-> object:
            
         # função responsavel por criar pasta para salvar o json
            
        caminho = os.getcwd()
        
        caminho_pasta = os.path.join(caminho, 'Arquivos_Json')
        
        if not os.path.exists(caminho_pasta):
                
                print('criando pasta, para json')
        
                os.makedirs(caminho_pasta)
                
        else:
                print('pasta ja criada')
        
        return caminho_pasta
                
            
            
    
    def ConverteJson(self)-> None:
            
        # funcao responsavel, por salvar os arquivos no json
            
        json_produtos = {
            'produto1Texto': self.produto1Texto,
            'produto1_marca': self.produto1_marca,
            'produto1_categoria': self.produto1_categoria,
            'descricao_edit': self.descricao_edit,
            'valor_produto_1_atual_float': self.valor_produto_1_atual_float,
            'valor_produto_1_antigo_float': self.valor_produto_1_antigo_float,
            'texto_tabela': self.texto_tabela,
            'texto_tabela_adicionais': self.texto_tabela_adicionais,
            'media_avaliacoes': self.calcular_media_avaliacoes(self.avaliacao1, self.avaliacao2, self.avaliacao3),
            'url_pagina': 'https://infosimples.com/vagas/desafio/commercia/product.html'
        }

        
        json_data = json.dumps(json_produtos, indent=2)

        retorno_caminho = self.CriaPasta()
        
        caminho_arquivo_json = os.path.join(retorno_caminho, 'Dados.json')

        with open(caminho_arquivo_json, 'w') as arquivo:
            arquivo.write(json_data)

        print(f'JSON salvo em {caminho_arquivo_json}')
        
        

                        
    
desafio = Desafio()
desafio.IniciaProdutos()
desafio.IniciaPropriedadesProduto()
desafio.ProdutosReview()
desafio.ConverteJson()