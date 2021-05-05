import pandas as pd
import gspread
from gspread_dataframe import get_as_dataframe, set_with_dataframe
from gspread_formatting.dataframe import format_with_dataframe

def getGoogleSheet(data1):

    df1 = pd.DataFrame.from_dict(data1, orient='index')
    df1 = df1.transpose()
    #Escribir en google sheet
    #https://www.youtube.com/watch?v=A1URtaaA-v0
    #Claves de API
    gc = gspread.service_account(filename='claves-drive.json')

    sh = gc.create('Hola-mundo') #Crea un sheet llamado "Hola mundo"
    sh.share('mibebebelloes@gmail.com', perm_type='user', role='writer')

    #Abre un sheet existente, en este caso, "Hola-mundo"
    sh = gc.open("Hola-mundo")

    # Seleccionar primera hoja

    #worksheet = sh.get_worksheet(0)     
    #sh.del_worksheet(worksheet)

    worksheet = sh.add_worksheet(title="ANÁLISIS COMPETENCIA", rows="1000", cols="20")
    
    set_with_dataframe(worksheet, df1)
    format_with_dataframe(worksheet, df1, include_column_header=True)
    #df2 = get_as_dataframe(worksheet)


