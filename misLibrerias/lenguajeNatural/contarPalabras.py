import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
import re

def densidad_palabra(texto, num_palabras):

	palabras = []
	repeticiones = []
	densidad_de_palabras = []

	
	texto = re.sub(r"[^a-zA-Z0-9áéíóúü]|\b(https|http|www|com|es|it|mx|co|de)\b", " ", texto.lower())         

	tokens = [t for t in texto.split()]



	clean_tokens = tokens[:]

	sr = stopwords.words('spanish')

	for token in tokens:

		if token in stopwords.words('spanish') or len(token) < 2: #Si hay preposiciones en español o la palabra es menor de 3 letras, las elimino			
		    clean_tokens.remove(token)


	freq = nltk.FreqDist(clean_tokens)


#---------------------------------------------------------------------

	def tuple_insert(tup,pos,ele): #Función necesaria para poder añadir el % de densidad de palabra clave a la tupla (palabra, repeticiones)
		tup = tup[:pos]+(ele,)+tup[pos:]
		return tup

	
	for x in freq.most_common(num_palabras):
		densidad = round(x[1]*100/len(tokens), 1) #densidad con 1 decimal
		densidad_de_palabras.append(tuple_insert(x,2,densidad))
		
	
	
	return densidad_de_palabras
	


#---------------------------------------------------------------------

#txt="palabras.txt"
#densidad_palabra(txt)
