import pandas as pd
from openpyxl import Workbook
from openpyxl.writer.excel import save_virtual_workbook

def getExcel(data1):
            
    df1 = pd.DataFrame.from_dict(data1, orient='index')
    df1 = df1.transpose()

    #Escribir en excel existente sin borrar los datos anteriores
        #with pd.ExcelWriter('file.xlsx', mode='a', engine='openpyxl') as writer:

    #Escribir en excel nuevo o borrando los datos anteriores 
    with pd.ExcelWriter('file.xlsx') as writer:            
        df1.to_excel(writer, columns=["Title","H1","H2","H3","Preguntas relacionadas","Búsquedas relacionadas","Descripción", "URL"], sheet_name="ANÁLISIS COMPETENCIA", freeze_panes=(1,1), index=False)
        df1.to_excel(writer, columns=["Palabras","Repeticiones","Densidad %"], sheet_name="PALABRAS CLAVE COMPETENCIA", freeze_panes=(1,1), index=False)
