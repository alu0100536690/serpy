def tuple_insert(tup,pos,ele): #Función necesaria para poder añadir el % de densidad de palabra clave a la tupla (palabra, repeticiones)
	tup = tup[:pos]+(ele,)+tup[pos:]
	return tup
