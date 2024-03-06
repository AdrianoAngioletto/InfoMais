from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from time import sleep


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
                |          INFO SIMPLES   https://infosimples.com/                          |
                |                                                                           |
                |                                                                           |    
                |                                                                           |
                | Dev:  AdrianoAngioletto                                                   |
                +===========================================================================+
                '''
        print(bemvindo)
        
    
    def EncontraElementos(self, valor: str, Element: object =By.XPATH,):
        
            # função para facilitar a vida, pegar o elemento sem necessidade de ficar escrevendo find .. etc
                                                     
            elemento = self.drive.find_element(Element, valor)
                
            
            return elemento
        
     

    def IniciaElementos(self):
        
        print(' Estamos, Carregando o site por favor aguarde')
        
        self.drive.get('https://infosimples.com/vagas/desafio/commercia/product.html')
        
        sleep(5) # tempo para navegador carregar pagina
        
        produto1 = self.EncontraElementos('/html/body/div/section/div/div[2]/div[1]/div[1]/div[3]/div[1]') # PRODUTO 1 EM OBJETO
        
        self.produto1Texto = produto1.text # PRODUTO 1 TITULO EM STRING
        
        produto1_marca = self.EncontraElementos('/html/body/div/section/div/div[1]') # PRODUTO 1 MARCA OBJETO <
        
        self.produto1_marca = produto1_marca.text # PRODUTO 1 MARCA EM STRING
        
        produto1_categoria = self.EncontraElementos('/html/body/div/section/div/nav/a[4]') # PRODUTO 1 CATEGORIA OBJETO 
        
        self.produto1_categoria = produto1_categoria.text #PRODUTO 1 CATEGORIA EM STRING
        
        
        
        print(self.produto1_marca)
        
    
desafio = Desafio()

desafio.IniciaElementos()
        
        