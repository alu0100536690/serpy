from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.crawler import CrawlerProcess
from scrapy.loader import ItemLoader
from bs4 import BeautifulSoup
import requests
import re
import time

from misLibrerias.lenguajeNatural.contarPalabras import densidad_palabra
from misLibrerias.exportacionDatos.exportarGoogleSheet import getGoogleSheet
from misLibrerias.exportacionDatos.exportarExcel import getExcel



class DatosSerps(Item):
    url = Field()
    h1 = Field()
    h2 = Field()
    h3 = Field()
    title = Field()
    description = Field()
    preguntas_relacionadas = Field()
    busquedas_relacionadas = Field()

class SerpsGoogle(CrawlSpider):
    name = 'serp'  
    start_urls = []
    
    
    def __init__(self, *args, **kwargs):
        super(SerpsGoogle, self).__init__(*args, **kwargs)

        idioma = ""
        pais = "" #España
        num_resultados = ""
        busqueda = ""
        busquedas = []
        motor = ""

        busqueda = kwargs['busqueda']
        
        busquedas = busqueda.split(", ")


        num_resultados = kwargs['num_resultados_serps']
        idioma = kwargs['idioma']
        pais = kwargs['pais']
        motor = kwargs['motor']

       
        for search in busquedas:
            # URL SEMILLA
            self.start_urls.append('https://www.'+str(motor)+'/search?q='+str(search)+'&num='+str(num_resultados)+'&gl='+str(pais)+'&hl='+str(idioma))


    custom_settings = {
 
        "DOWNLOADER_MIDDLEWARES":{ #Necesito instalar la librería -> pip3 install Scrapy-UserAgents para rotar users agents automaticamente.
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'scrapy_useragents.downloadermiddlewares.useragents.UserAgentsMiddleware': 500,
        },

        "USER_AGENTS": [
            ('Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:87.0) Gecko/20100101 Firefox/87.0'),
            ('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'),
            ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.36 Safari/537.36'),  # chrome
            ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'),  # chrome
            ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_16_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36')  # firefox

            
        ]

    }


    download_delay = 1
    


    def limpiartexto(self, texto):
     
        nuevoTexto = re.sub(r'<[^>]*>','',texto) #limpiar texto con expresiones regulares
        return nuevoTexto

   
    def parse(self, response):
        
        data = []        
        title = []
        h1 = []
        h2 = []
        h3 = []        
        description = []       
        preguntas_relacionadas = []
        busquedas_relacionadas = []

       # Order these in order of preference
        description_selectors = [
            {"name": "description"},
            {"name": "og:description"},
            {"property": "description"}
        ]

        ArrayURLSERPS = []

 

        sel = Selector(response)
        urlSerps = sel.xpath('//*[@id="center_col"]')
        item = ItemLoader(DatosSerps(), urlSerps)
                                  
        item.add_xpath('url', '//*[h3]//parent::a/@href[not(contains(., "https://www.google") or contains(., "/search?"))]')
        item.add_xpath('description', '//*[@id="rso"]/div/div/div/div/span', MapCompose(self.limpiartexto)) 
        item.add_xpath('preguntas_relacionadas', '//g-accordion-expander/descendant::div/text()')
        item.add_xpath('busquedas_relacionadas', '//*[@id="w3bYAd"]/div/div/div/div/a/div[2]', MapCompose(self.limpiartexto))
        
        #title = sel.xpath('//h3/text()').extract() #Coge el título incompleto desde google
        #item.add_value('title', title) 
        
        ArrayURLSERPS = item.get_collected_values('url') #Array de urls de la serps
        
        for x in range(0,len(ArrayURLSERPS)):
            try:
                reqs = requests.get(ArrayURLSERPS[x], timeout=5)
                #status = response.status_code
                #print("\n\n\nEl STATUS DE ", ArrayURLSERPS[x], "ES : ", status)			   
                soup = BeautifulSoup(reqs.text, 'lxml')

                if (soup.title is not None):
                    title.append(soup.title.string)
                #else:
                     #title.append('')              

                for selector in description_selectors:
                    description_tag = soup.find(attrs=selector)
                    if description_tag and description_tag.get('content'):
                        description.append(description_tag['content'])                                                
                        break
                    
                    #else:
                        #description.append('')
                        #desciption.add_value('')

            except:
                continue
            
			
            for heading in soup.find_all(["h1", "h2", "h3"]):                    
                    
                if(heading.name == "h1"):
                    h1.append(heading.text.strip())
                #else:
                    #h1.append('')

                if(heading.name == "h2"):
                    h2.append(heading.text.strip())                

                if(heading.name == "h3"):
                    h3.append(heading.text.strip())  
                			


        item.add_value('title', title)
        item.add_value('h1', h1)
        item.add_value('h2', h2)
        item.add_value('h3', h3)
        item.add_value('description', description)
        item.add_value('preguntas_relacionadas',preguntas_relacionadas)
        item.add_value('busquedas_relacionadas',busquedas_relacionadas)
        
        yield item.load_item()
        
        #title = item.get_collected_values('title')
        #description = item.get_collected_values('description')
        preguntas_relacionadas = item.get_collected_values('preguntas_relacionadas')
        busquedas_relacionadas = item.get_collected_values('busquedas_relacionadas')

        print("Importando datos...")  

         
        densidad_palabras = densidad_palabra(str(title+h1+h2+h3+description), 100) #numero de palabras claves que quiero obtener
		
        palabras = []
        repeticiones = []
        densidad = []

        for x in densidad_palabras:
            palabras.append(x[0])
            repeticiones.append(x[1])
            densidad.append(x[2])

        data1 = {
            'Palabras': palabras,
            'Repeticiones': repeticiones,
            'Densidad %': densidad,
            'Title': title,
            'H1': h1,
            'H2': h2,
            'H3': h3,
            'Preguntas relacionadas': preguntas_relacionadas,
            'Búsquedas relacionadas': busquedas_relacionadas,
            'Descripción': description,
            'URL': ArrayURLSERPS
  
        }


        getGoogleSheet(data1) #Crea fichero Google sheet
        getExcel(data1) #Crea fichero Excel
       


        

#scrapy crawl serp -a busqueda="mejores carritos de bebe" -a num_resultados_serps=10 -a idioma=es -a pais=ES -a motor=google.es
#con process ejecuto scrapy automáticamente sin escribir -> scrapy crawl .....
#process = CrawlerProcess()
#process.crawl(SerpsGoogle)
#process.start()
#scrapy crawl serp -t json -o serp.json
