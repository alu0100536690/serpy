import pandas as pd
import gspread
from gspread_dataframe import get_as_dataframe, set_with_dataframe
from gspread_formatting.dataframe import format_with_dataframe

def getGoogleSheet(data):

    print("\n\nEL DATA TITLE ES: ", data['Title'])
    dfAnalisisCompetencia = {
        'Pos nT': data['nT'],
        'Title': data['Title'],
        'Pos H1': data['nH1'],
        'H1': data['H1'],
        'Pos H2': data['nH2'],        
        'H2': data['H2'],
        'Pos H3': data['nH3'],
        'H3': data['H3'],
        'Pos desc': data['nDescripción'],
        'Descripción': data['Descripción'],
        'Pos URL': data['nURL'],
        'URL': data['URL']

    } 

    print("\n\n\n",dfAnalisisCompetencia,"\n\n\n")

    dfDensidadPalabra = {
        'Palabras': data['Palabras'],
        'Repeticiones': data['Repeticiones'],
        'Densidad %': data['Densidad %']

    }
 
    print("\n\n\n",dfDensidadPalabra,"\n\n\n")

    
    df1 = pd.DataFrame.from_dict(dfAnalisisCompetencia, orient='index')
    df1 = df1.transpose()

    df2 = pd.DataFrame.from_dict(dfDensidadPalabra, orient='index')
    df2 = df2.transpose()
    #Escribir en google sheet
    #https://www.youtube.com/watch?v=A1URtaaA-v0
    #Claves de API
    gc = gspread.service_account(filename='claves-drive.json')

    sh = gc.create('Hola-mundo') #Crea un sheet llamado "Hola mundo"
    sh.share('mibebebelloes@gmail.com', perm_type='user', role='writer')

    #Abre un sheet existente, en este caso, "Hola-mundo"
    sh = gc.open("Hola-mundo") 
    
    analisisCompetencia = sh.add_worksheet(title="ANÁLISIS COMPETENCIA", rows="1000", cols="20")
    densidadPalabra = sh.add_worksheet(title="DENSIDAD DE PALABRA", rows="1000", cols="20")
    preguntasRelacionadas = sh.add_worksheet(title="PREGUNTAS RELACIONADAS", rows="1000", cols="20")
    busquedasRelacionadas = sh.add_worksheet(title="BÚSQUEDAS RELACIONADAS", rows="1000", cols="20")    
    topURLs = sh.add_worksheet(title="TOP URLs", rows="1000", cols="20")
    keywordResearch = sh.add_worksheet(title="KEYWORD RESEARCH", rows="1000", cols="20")
    encabezados = sh.add_worksheet(title="ENCABEZADOS", rows="100", cols="10")

    # Seleccionar primera hoja
    #worksheet = sh.get_worksheet(0)       
    sh.del_worksheet(sh.get_worksheet(0)) #Elimina la hoja "Sheet1" que sale por defecto.
    
    
    set_with_dataframe(analisisCompetencia, df1)
    format_with_dataframe(analisisCompetencia, df1, include_column_header=True)
 
    set_with_dataframe(densidadPalabra, df2)
    format_with_dataframe(densidadPalabra, df2, include_column_header=True)