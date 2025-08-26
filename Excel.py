import xlrd

def credenciales():
	with xlrd.open_workbook('Credenciales.xlsx') as libro:
		nombres = []
		claves = []
		for hoja in libro.sheets():
			for i in range(1,hoja.nrows):
				fila = hoja.row(i)
				nombres.append(fila[0].value)
				claves.append(fila[1].value)

	return nombres,claves

nombres,claves = credenciales()
print(nombres)
print(claves)
