from app import app
from flask import Flask,jsonify,request,redirect,url_for
from flask import render_template
from .configuraciones import *
import random as ran
#from app import configuraciones
import psycopg2
conn = psycopg2.connect("dbname=%s user=%s password=%s"%(database,user,passwd))
cur = conn.cursor()


@app.route('/')
@app.route('/index')
def index(): 
	return render_template("index.html")

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/historial')
def historial():

	sql ="""
	select id,identificacion from entradas order by id;"""
	cur.execute(sql)
	simus  = cur.fetchall()
	print(simus)
	
	return render_template("historial.html", simus=simus )

@app.route('/historial/<his_id>', methods=['GET'])
def post(his_id):

	sql ="""
	select * from entradas where id = %s;
	"""%(his_id)
	# print sql
	cur.execute(sql)
	entry = cur.fetchall()

	sql ="""
	select * from resultados
	where resultados.entrada_id = %s;
	"""%(his_id)
	# print sql
	cur.execute(sql)
	result  = cur.fetchall()

	sql ="""
	select * from res_horarios_uno
	where res_horarios_uno.resultado_id = %s;
	"""%(result[0][0])
	# print sql
	cur.execute(sql)
	resultuno  = cur.fetchall()

	sql ="""
	select * from res_horarios_dos
	where res_horarios_dos.resultado_id = %s;
	"""%(result[0][0])
	# print sql
	cur.execute(sql)
	resultdos  = cur.fetchall()

	sql ="""
	select * from res_horarios_tres
	where res_horarios_tres.resultado_id = %s;
	"""%(result[0][0])
	# print sql
	cur.execute(sql)
	resulttres  = cur.fetchall()

	sql ="""
	select * from res_horarios_cuatro
	where res_horarios_cuatro.resultado_id = %s;
	"""%(result[0][0])
	# print sql
	cur.execute(sql)
	resultcuatro  = cur.fetchall()

	sql ="""
	select * from res_horarios_cinco
	where res_horarios_cinco.resultado_id = %s;
	"""%(result[0][0])
	# print sql
	cur.execute(sql)
	resultcinco  = cur.fetchall()

	sql ="""
	select * from res_horarios_seis
	where res_horarios_seis.resultado_id = %s;
	"""%(result[0][0])
	# print sql
	cur.execute(sql)
	resultseis  = cur.fetchall()

	sql ="""
	select * from res_horarios_siete
	where res_horarios_siete.resultado_id = %s;
	"""%(result[0][0])
	# print sql
	cur.execute(sql)
	resultsiete  = cur.fetchall()

	sql ="""
	select * from res_horarios_ocho
	where res_horarios_ocho.resultado_id = %s;
	"""%(result[0][0])
	# print sql
	cur.execute(sql)
	resultocho  = cur.fetchall()

	sql ="""
	select * from res_horarios_nueve
	where res_horarios_nueve.resultado_id = %s;
	"""%(result[0][0])
	# print sql
	cur.execute(sql)
	resultnueve  = cur.fetchall()

	sql ="""
	select * from res_horarios_diez
	where res_horarios_diez.resultado_id = %s;
	"""%(result[0][0])
	# print sql
	cur.execute(sql)
	resultdiez  = cur.fetchall()

	return render_template("especifico.html", entry=entry, result=result, resultuno = resultuno, resultdos=resultdos, resulttres=resulttres, resultcuatro= resultcuatro, resultcinco = resultcinco, resultseis=resultseis, resultsiete=resultsiete, resultocho = resultocho, resultnueve = resultnueve, resultdiez= resultdiez)

class persona:

	Tp = 0
	Pcantidad = 0
	TiempoPagandoz = 0
	DesencolarProducto = 0
	PromDespacho = 0

	def __init__(self ,Cantidad_Minima, Cantidad_Maxima):
		self.Pcantidad = ran.randrange(Cantidad_Minima,Cantidad_Maxima + 1)

	def TiempoPersonal(self, PromedioCompra,PromedioDespacho,TiempoPagarEnCaja):
		self.Tp = self.Pcantidad*PromedioCompra
		self.TiempoPagandoz = self.Pcantidad*PromedioDespacho + TiempoPagarEnCaja
		self.PromDespacho = PromedioDespacho

	def CambiarTiempo(self):
		self.Tp = self.Tp - 1

	def EstoyPagando(self):
		self.TiempoPagandoz = self.TiempoPagandoz - 1

	def PagarProducto(self):
		self.DesencolarProducto = self.DesencolarProducto + 1

	def ResetDesencolarProducto(self):
		self.DesencolarProducto = 0

	def ProductoPagado(self):
		if(self.Pcantidad == 0):
			return
		else:
			self.Pcantidad -= 1

class DatosCaja:
	TiempoTotal = 0
	Clientes_Despachados = 0
	ProductosTotalesCaja = 0
	Clientes_TotalesCaja = 0
	MaxTam = 0
	NumeroDeModificaciones = 0
	TamParaPromedio = 0

	def MaxTama(self,Tam):
		if(Tam > self.MaxTam):
			self.MaxTam = Tam

	def SetTiempo(self):
		self.TiempoTotal += 1

	def SetProductosTotales(self):
		self.ProductosTotalesCaja += 1

	def Set_ClientesTotalesCaja(self):
		self.Clientes_TotalesCaja += 1

	def GetTiempo(self):
		return self.TiempoTotal
	def GetClientDespa(self):
		return self.Clientes_Despachados
	def GetProdTotalesCajas(self):
		return self.ProductosTotalesCaja
	def GetClientTotal(self):
		return self.Clientes_TotalesCaja
	def GetColaMax(sefl):
		return self.MaxTam
	def GetPromProds(self):
		return self.ProductosTotalesCaja//self.Clientes_TotalesCaja

	def GetCl(self):
		return self.Clientes_TotalesCaja

	def SetUpTamPro(self, a):
		self.TamParaPromedio +=a

	def SetModificaciones(self):
		self.NumeroDeModificaciones += 1

	def CalcularPromedio(self):
		if self.NumeroDeModificaciones == 0:
			return 0
		else:
			return self.TamParaPromedio // self.NumeroDeModificaciones
	def Mostrar(self):
		print("Tiempo Total                     : " , self.TiempoTotal)
		print("Clientes Despachados             : ", self.Clientes_Despachados)
		print("Productos en Caja                : ",self.ProductosTotalesCaja)
		print("Clientes Totales                 : ", self.Clientes_TotalesCaja)
		print("Cola más alta                    : ", self.MaxTam)
		print("Promedio de cola de la caja      : ",self.CalcularPromedio())
		#print("Promedio productos por cliente   : ",self.ProductosTotalesCaja//self.Clientes_Despachados)

def CrearListaPersonas(Cantidad_Minima , Cantidad_Maxima, nPersonas, PromedioCompra,PromedioDespacho,TiempoPagarEnCaja):
	TotalPersonas = []
	i = 0
	while i < nPersonas:
		P = persona(Cantidad_Minima, Cantidad_Maxima)
		P.TiempoPersonal(PromedioCompra,PromedioDespacho,TiempoPagarEnCaja)
		TotalPersonas.append(P)
		i+=1
	return TotalPersonas

def EntrarSupermercado(Horario_Sg, Personas_Horario):
	return Horario_Sg // Personas_Horario

def CrearCajas(NumeroDeCajas):
	Cajas = []
	for x in range(0,NumeroDeCajas):
		Cajas.append([])
	return Cajas

def CrearDatosCaja(NumeroDeCajas):
	Diccionario = {}
	for x in range(NumeroDeCajas):
		Diccionario[x] = DatosCaja()
	return Diccionario

def Equal_Caja(CajasIguales):
	return CajasIguales[ran.randrange(0, len(CajasIguales))]

def BusquedaMenor(Cajas):
	Minimo = len(Cajas[0])
	for x in Cajas:
		if len(x) < Minimo:
			Minimo = len(x)
	return Minimo

def PorcentajeEntero(total,porc):
	return (porc*total)//100

@app.route('/resultado', methods=['GET','POST'])
def resultado():
	if request.method == "POST":
		try:
			identificador = request.form['Simulacion']
			horas_atencion = request.form['Horas_diarias_de_atencion']
			pasos = request.form['Pasos']
			clientes_por_dia = request.form['Clientes_esperados_por_dia']
			dclientesuno = request.form['distribucion_clientes_uno']
			dclientesdos = request.form['distribucion_clientes_dos']
			dclientestres = request.form['distribucion_clientes_tres']
			dclientescuatro = request.form['distribucion_clientes_cuatro']
			dclientescinco = request.form['distribucion_clientes_cinco']
			dclientesseis = request.form['distribucion_clientes_seis']
			dclientessiete = request.form['distribucion_clientes_siete']
			dclientesocho = request.form['distribucion_clientes_ocho']
			dclientesnueve = request.form['distribucion_clientes_nueve']
			dclientesdiez = request.form['distribucion_clientes_diez']
			dcajauno = request.form['distribucion_cajas_uno']
			dcajados = request.form['distribucion_cajas_dos']
			dcajatres = request.form['distribucion_cajas_tres']
			dcajacuatro = request.form['distribucion_cajas_cuatro']
			dcajacinco = request.form['distribucion_cajas_cinco']
			dcajaseis = request.form['distribucion_cajas_seis']
			dcajasiete = request.form['distribucion_cajas_siete']
			dcajaocho = request.form['distribucion_cajas_ocho']
			dcajanueve = request.form['distribucion_cajas_nueve']
			dcajadiez = request.form['distribucion_cajas_diez']
			min_productos = request.form['Min_productos_por_cliente']
			max_productos = request.form['Max_productos_por_cliente']
			tiempo_seleccion = request.form['Tiempo_seleccion']
			tiempo_marcado = request.form['Tiempo_marcado']
			tiempo_pago = request.form['Tiempo_pago']

			sql ="""insert INTO entradas (identificacion, horas_atencion, pasos_simulacion, clientes_esperados, clientes_horario_uno, clientes_horario_dos, clientes_horario_tres, clientes_horario_cuatro, clientes_horario_cinco, clientes_horario_seis, clientes_horario_siete, clientes_horario_ocho, clientes_horario_nueve,clientes_horario_diez, cajas_horario_uno, cajas_horario_dos, cajas_horario_tres,cajas_horario_cuatro, cajas_horario_cinco, cajas_horario_seis, cajas_horario_siete,cajas_horario_ocho, cajas_horario_nueve, cajas_horario_diez, minimo_productos, maximo_productos,tiempo_seleccion, tiempo_despacho, tiempo_pago) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s') returning entradas.id; """%(identificador,horas_atencion,pasos,clientes_por_dia,dclientesuno,dclientesdos,dclientestres,dclientescuatro,dclientescinco,dclientesseis,dclientessiete,dclientesocho,dclientesnueve,dclientesdiez,dcajauno,dcajados,dcajatres,dcajacuatro,dcajacinco,dcajaseis,dcajasiete,dcajaocho,dcajanueve,dcajadiez,min_productos,max_productos,tiempo_seleccion,tiempo_marcado,tiempo_pago)
			cur.execute(sql)
			entrada_id = cur.fetchone()
			conn.commit()

			tiempo_total_simulado = int(horas_atencion)*60
			Diferencia = 0
			Personas_in_the_middle = []
			UltimoEncolado = 0
			Suma = 0
			ColaAnterior = []
			CantidadDeCajash = [int(dcajauno),int(dcajados),int(dcajatres),int(dcajacuatro),int(dcajacinco),int(dcajaseis),int(dcajasiete),int(dcajaocho),int(dcajanueve),int(dcajadiez)]
			Diferencia = 0
			PersonasPorIntervalo = [PorcentajeEntero(int(clientes_por_dia),int(dclientesuno)),PorcentajeEntero(int(clientes_por_dia),int(dclientesdos)),PorcentajeEntero(int(clientes_por_dia),int(dclientestres)),PorcentajeEntero(int(clientes_por_dia),int(dclientescuatro)),PorcentajeEntero(int(clientes_por_dia),int(dclientescinco)),PorcentajeEntero(int(clientes_por_dia),int(dclientesseis)),PorcentajeEntero(int(clientes_por_dia),int(dclientessiete)),PorcentajeEntero(int(clientes_por_dia),int(dclientesocho)),PorcentajeEntero(int(clientes_por_dia),int(dclientesnueve)),PorcentajeEntero(int(clientes_por_dia),int(dclientesdiez))]
			sql=""" insert INTO resultados (entrada_id, tiempo_simulado) values ('%s','%s') returning resultados.id; """%(entrada_id[0], tiempo_total_simulado)
			cur.execute(sql)
			resultado_id = cur.fetchone()
			conn.commit()

			for f in range(0,10):
				Personas = []

				PromedioEntrada = EntrarSupermercado((int(horas_atencion)/10)*3600,(PersonasPorIntervalo[f] + Diferencia)) #Cada cuanto tiempo entra una persona al Supermercado
				if(len(Personas_in_the_middle) > 0):
					for xc in Personas_in_the_middle:
						Personas.append(xc)
					Personas.extend(CrearListaPersonas(int(min_productos),int(max_productos),PersonasPorIntervalo[f] + Diferencia,int(tiempo_seleccion),int(tiempo_marcado),int(tiempo_pago))) # Lista de personas
				else:
					Personas = CrearListaPersonas(int(min_productos),int(max_productos),PersonasPorIntervalo[f] + Diferencia,int(tiempo_seleccion),int(tiempo_marcado),int(tiempo_pago))
				Temporizador = 0
				Entra = 0
				PersonasDentro = 0
				Cajas = CrearCajas(CantidadDeCajash[f]) # 5 suponiendo que es el parametro que entrega el Cliente
				DatosCajas = CrearDatosCaja(CantidadDeCajash[f])
				CajasBajas = [] # Para el proceso de seleccionar una caja aleatoria

				while(len(ColaAnterior) > 0): #Encola todo lo que alcanzó a quedar encolado en el periodo anterior
						MenorCola = BusquedaMenor(Cajas)
						for a in range(len(Cajas)):
							if len(Cajas[a]) == MenorCola:
								CajasBajas.append(a)
						Encolar = Equal_Caja(CajasBajas)

						Cajas[Encolar].append(ColaAnterior.pop())
						DatosCajas[Encolar].Set_ClientesTotalesCaja()
						DatosCajas[Encolar].SetUpTamPro(len(Cajas[Encolar]))
						DatosCajas[Encolar].SetModificaciones()
						while len(CajasBajas) > 0:
							CajasBajas.pop()  
				while(Temporizador < (int(horas_atencion)/10)*3600):
					if(Entra == PromedioEntrada):
						if (PersonasDentro < (len(Personas)-Diferencia)):
							PersonasDentro += 1
							Entra = 0
					for x in range(0,PersonasDentro + Diferencia):
						Personas[x].CambiarTiempo() # Reduce en 1 el tiempo del cliente en escoger los productos  
						if(Personas[x].Tp == 0):
							UltimoEncolado = x
							MenorCola = BusquedaMenor(Cajas) 
							for a in range(0,len(Cajas)):
								if len(Cajas[a]) == MenorCola:
									CajasBajas.append(a)
							Encolar = Equal_Caja(CajasBajas) 
							Cajas[Encolar].append(Personas[x])
							DatosCajas[Encolar].Set_ClientesTotalesCaja()
							DatosCajas[Encolar].SetUpTamPro(len(Cajas[Encolar]))
							DatosCajas[Encolar].SetModificaciones()
							while len(CajasBajas) > 0:
								CajasBajas.pop()            
					for a in range(CantidadDeCajash[f]):
						if(len(Cajas[a]) == 0):
							continue
						elif(len(Cajas[a]) > 0):

							Cajas[a][0].EstoyPagando() #Reduce en 1 el tiempo que debería tomar ser popeado
							Cajas[a][0].PagarProducto() # Al llegar al promedio de pago de 1 producto la persona popea 1 objeto
							DatosCajas[a].SetTiempo() # LaCaja aumenta en 1 el tiempo que ha atendido gente
							DatosCajas[a].MaxTama(len(Cajas[a]))

							if(Cajas[a][0].DesencolarProducto == Cajas[a][0].PromDespacho): # se llega al promedio de despacho de un producto
								if(Cajas[a][0].Pcantidad > 0):
									DatosCajas[a].SetProductosTotales() #La Caja aumenta en 1 la cantidad de productos que ha recibido
									Cajas[a][0].ProductoPagado() # Reduce en 1 la cantidad de productos que posee el cliente
									Cajas[a][0].ResetDesencolarProducto() # resetea el contador para popear productos  

							if(Cajas[a][0].TiempoPagandoz <= 0):

								Cajas[a].pop(0)
								DatosCajas[a].Clientes_Despachados += 1
								DatosCajas[Encolar].SetModificaciones()
								DatosCajas[a].SetUpTamPro(len(Cajas[a]))               
					Entra+=1
					Temporizador+=1

				Promedio_De_Cola = 0
				Promedio_De_Prods = 0
#--------------- Estos print son para confirmar que el try llegó hasta acá!, no son necesarios para el render 
				for i in range(CantidadDeCajash[f]):

					Promedio_De_Cola += DatosCajas[i].CalcularPromedio()
					Promedio_De_Prods += DatosCajas[i].ProductosTotalesCaja//DatosCajas[i].Clientes_Despachados
					if f == 0:
						ingresadosuno = 0
						despachadosuno = 0
						colaMaxuno = 0
						ingresadosuno += DatosCajas[i].Clientes_TotalesCaja
						despachadosuno += DatosCajas[i].Clientes_Despachados
						colaMaxuno = DatosCajas[i].MaxTam
						continue
					if f == 1:
						ingresadosdos = 0
						despachadosdos = 0
						colaMaxdos = 0
						ingresadosdos += DatosCajas[i].Clientes_TotalesCaja
						despachadosdos += DatosCajas[i].Clientes_Despachados
						colaMaxdos = DatosCajas[i].MaxTam
						continue
					if f == 2:
						ingresadostres = 0
						despachadostres = 0
						colaMaxtres = 0
						ingresadostres += DatosCajas[i].Clientes_TotalesCaja
						despachadostres += DatosCajas[i].Clientes_Despachados
						colaMaxtres = DatosCajas[i].MaxTam
						continue
					if f == 3:
						ingresadoscuatro = 0
						despachadoscuatro = 0
						colaMaxcuatro = 0
						ingresadoscuatro += DatosCajas[i].Clientes_TotalesCaja
						despachadoscuatro += DatosCajas[i].Clientes_Despachados
						colaMaxcuatro = DatosCajas[i].MaxTam
						continue
					if f == 4:
						ingresadoscinco = 0
						despachadoscinco = 0
						colaMaxcinco = 0
						ingresadoscinco += DatosCajas[i].Clientes_TotalesCaja
						despachadoscinco += DatosCajas[i].Clientes_Despachados
						colaMaxcinco = DatosCajas[i].MaxTam
						continue
					if f == 5:
						ingresadosseis = 0
						despachadosseis = 0
						colaMaxseis= 0
						ingresadosseis += DatosCajas[i].Clientes_TotalesCaja
						despachadosseis += DatosCajas[i].Clientes_Despachados
						colaMaxseis = DatosCajas[i].MaxTam
						continue
					if f == 6:
						ingresadossiete = 0
						despachadossiete = 0
						colaMaxsiete = 0
						ingresadossiete += DatosCajas[i].Clientes_TotalesCaja
						despachadossiete += DatosCajas[i].Clientes_Despachados
						colaMaxsiete = DatosCajas[i].MaxTam
						continue
					if f == 7:
						ingresadosocho = 0
						despachadosocho = 0
						colaMaxocho = 0
						ingresadosocho += DatosCajas[i].Clientes_TotalesCaja
						despachadosocho += DatosCajas[i].Clientes_Despachados
						colaMaxocho = DatosCajas[i].MaxTam
						continue
					if f == 8:
						ingresadosnueve = 0
						despachadosnueve = 0
						colaMaxnueve = 0
						ingresadosnueve += DatosCajas[i].Clientes_TotalesCaja
						despachadosnueve += DatosCajas[i].Clientes_Despachados
						colaMaxnueve = DatosCajas[i].MaxTam
						continue
					if f == 9:
						ingresadosdiez = 0
						despachadosdiez = 0
						colaMaxdiez = 0
						ingresadosdiez += DatosCajas[i].Clientes_TotalesCaja
						despachadosdiez += DatosCajas[i].Clientes_Despachados
						colaMaxdiez = DatosCajas[i].MaxTam
						continue

				if f == 0:
					promColauno = Promedio_De_Cola // CantidadDeCajash[f]
					promProdsuno = Promedio_De_Prods// CantidadDeCajash[f]
					continue
				if f == 1:
					promColados = Promedio_De_Cola // CantidadDeCajash[f]
					promProdsdos = Promedio_De_Prods// CantidadDeCajash[f]
					continue
				if f == 2:
					promColatres = Promedio_De_Cola // CantidadDeCajash[f]
					promProdstres = Promedio_De_Prods// CantidadDeCajash[f]
					continue
				if f == 3:
					promColacuatro = Promedio_De_Cola // CantidadDeCajash[f]
					promProdscuatro = Promedio_De_Prods// CantidadDeCajash[f]
					continue
				if f == 4:
					promColacinco = Promedio_De_Cola // CantidadDeCajash[f]
					promProdscinco = Promedio_De_Prods// CantidadDeCajash[f]
					continue
				if f == 5:
					promColaseis = Promedio_De_Cola // CantidadDeCajash[f]
					promProdsseis = Promedio_De_Prods// CantidadDeCajash[f]
					continue
				if f == 6:
					promColasiete = Promedio_De_Cola // CantidadDeCajash[f]
					promProdssiete = Promedio_De_Prods// CantidadDeCajash[f]
					continue
				if f == 7:
					promColaocho = Promedio_De_Cola // CantidadDeCajash[f]
					promProdsocho = Promedio_De_Prods// CantidadDeCajash[f]
					continue
				if f == 8:
					promColanueve = Promedio_De_Cola // CantidadDeCajash[f]
					promProdsnueve = Promedio_De_Prods// CantidadDeCajash[f]
					continue
				if f == 9:
					promColadiez = Promedio_De_Cola // CantidadDeCajash[f]
					promProdsdiez = Promedio_De_Prods// CantidadDeCajash[f]
					continue

				for i in range(CantidadDeCajash[f]):
					if(len(Cajas[i]) > 0):
						Suma += len(Cajas[i])
				
				while(Suma > 0):
					for i in range(CantidadDeCajash[f]):
						if(len(Cajas[i]) > 0):
							ColaAnterior.append(Cajas[i].pop())
							Suma -= 1
				Diferencia = abs(len(Personas) - UltimoEncolado)	
				for XD in range(UltimoEncolado,len(Personas)):
					Personas_in_the_middle.append(Personas[XD])
				print("ke pex")

			sql=""" insert INTO res_horarios_uno (resultado_id, ingresados, despachados, promedio_productos, promedio_cola, longitud_max_cola) values ('%s','%s','%s','%s','%s','%s'); """%(resultado_id[0], ingresadosuno, despachadosuno, promProdsuno, promColauno, colaMaxuno)
			cur.execute(sql)
			conn.commit()

			sql=""" insert INTO res_horarios_dos (resultado_id, ingresados, despachados, promedio_productos, promedio_cola, longitud_max_cola) values ('%s','%s','%s','%s','%s','%s'); """%(resultado_id[0], ingresadosdos, despachadosdos, promProdsdos, promColados, colaMaxdos)
			cur.execute(sql)
			conn.commit()

			sql=""" insert INTO res_horarios_tres (resultado_id, ingresados, despachados, promedio_productos, promedio_cola, longitud_max_cola) values ('%s','%s','%s','%s','%s','%s'); """%(resultado_id[0], ingresadostres, despachadostres, promProdstres, promColatres, colaMaxtres)
			cur.execute(sql)
			conn.commit()

			sql=""" insert INTO res_horarios_cuatro (resultado_id, ingresados, despachados, promedio_productos, promedio_cola, longitud_max_cola) values ('%s','%s','%s','%s','%s','%s'); """%(resultado_id[0], ingresadoscuatro, despachadoscuatro, promProdscuatro, promColacuatro, colaMaxcuatro)
			cur.execute(sql)
			conn.commit()

			sql=""" insert INTO res_horarios_cinco (resultado_id, ingresados, despachados, promedio_productos, promedio_cola, longitud_max_cola) values ('%s','%s','%s','%s','%s','%s'); """%(resultado_id[0], ingresadoscinco, despachadoscinco, promProdscinco, promColacinco, colaMaxcinco)
			cur.execute(sql)
			conn.commit()

			sql=""" insert INTO res_horarios_seis (resultado_id, ingresados, despachados, promedio_productos, promedio_cola, longitud_max_cola) values ('%s','%s','%s','%s','%s','%s'); """%(resultado_id[0], ingresadosseis, despachadosseis, promProdsseis, promColaseis, colaMaxseis)
			cur.execute(sql)
			conn.commit()

			sql=""" insert INTO res_horarios_siete (resultado_id, ingresados, despachados, promedio_productos, promedio_cola, longitud_max_cola) values ('%s','%s','%s','%s','%s','%s'); """%(resultado_id[0], ingresadossiete, despachadossiete, promProdssiete, promColasiete, colaMaxsiete)
			cur.execute(sql)
			conn.commit()

			sql=""" insert INTO res_horarios_ocho (resultado_id, ingresados, despachados, promedio_productos, promedio_cola, longitud_max_cola) values ('%s','%s','%s','%s','%s','%s'); """%(resultado_id[0], ingresadosocho, despachadosocho, promProdsocho, promColaocho, colaMaxocho)
			cur.execute(sql)
			conn.commit()

			sql=""" insert INTO res_horarios_nueve (resultado_id, ingresados, despachados, promedio_productos, promedio_cola, longitud_max_cola) values ('%s','%s','%s','%s','%s','%s'); """%(resultado_id[0], ingresadosnueve, despachadosnueve, promProdsnueve, promColanueve, colaMaxnueve)
			cur.execute(sql)
			conn.commit()

			sql=""" insert INTO res_horarios_diez (resultado_id, ingresados, despachados, promedio_productos, promedio_cola, longitud_max_cola) values ('%s','%s','%s','%s','%s','%s'); """%(resultado_id[0], ingresadosdiez, despachadosdiez, promProdsdiez, promColadiez, colaMaxdiez)
			cur.execute(sql)
			conn.commit()
			return render_template("resultado.html",entrada_id=entrada_id[0],tiempo_total_simulado=tiempo_total_simulado, identificador=identificador, horas_atencion=horas_atencion, pasos=pasos, clientes_por_dia=clientes_por_dia, min_productos=min_productos, max_productos=max_productos, tiempo_seleccion=tiempo_seleccion, tiempo_marcado=tiempo_marcado, tiempo_pago=tiempo_pago, dclientesuno=dclientesuno, dclientesdos=dclientesdos,dclientestres=dclientestres, dclientescuatro=dclientescuatro,dclientescinco=dclientescinco, dclientesseis=dclientesseis, dclientessiete=dclientessiete, dclientesocho=dclientesocho, dclientesnueve=dclientesnueve, dclientesdiez=dclientesdiez, dcajauno=dcajauno, dcajados=dcajados, dcajatres=dcajatres, dcajacuatro=dcajacuatro,dcajacinco=dcajacinco, dcajaseis=dcajaseis, dcajasiete=dcajasiete, dcajaocho=dcajaocho, dcajanueve=dcajanueve, dcajadiez=dcajadiez, ingresadosuno=ingresadosuno, ingresadosdos=ingresadosdos,ingresadostres=ingresadostres,ingresadoscuatro=ingresadoscuatro, ingresadoscinco=ingresadoscinco, ingresadosseis=ingresadosseis, ingresadossiete=ingresadossiete, ingresadosocho=ingresadosocho, ingresadosnueve=ingresadosnueve, ingresadosdiez=ingresadosdiez, despachadosuno=despachadosuno, despachadosdos=despachadosdos, despachadostres=despachadostres,despachadoscuatro=despachadoscuatro,despachadoscinco=despachadoscinco, despachadosseis=despachadosseis, despachadossiete=despachadossiete, despachadosocho=despachadosocho, despachadosnueve=despachadosnueve, despachadosdiez=despachadosdiez, promProdsuno=promProdsuno, promProdsdos=promProdsdos,promProdstres=promProdstres, promProdscuatro=promProdscuatro,promProdscinco=promProdscinco, promProdsseis=promProdsseis, promProdssiete=promProdssiete,promProdsocho=promProdsocho,promProdsnueve=promProdsnueve,promProdsdiez=promProdsdiez,colaMaxuno=colaMaxuno,colaMaxdos=colaMaxdos,colaMaxtres=colaMaxtres,colaMaxcuatro=colaMaxcuatro,colaMaxcinco=colaMaxcinco,colaMaxseis=colaMaxseis,colaMaxsiete=colaMaxsiete,colaMaxocho=colaMaxocho,colaMaxnueve=colaMaxnueve,colaMaxdiez=colaMaxdiez,promColauno=promColauno,promColados=promColados,promColatres=promColatres,promColacuatro=promColacuatro,promColacinco=promColacinco,promColaseis=promColaseis,promColasiete=promColasiete,promColaocho=promColaocho,promColanueve=promColanueve,promColadiez=promColadiez)
		except:
			pass
# este return tiene comentada las variables mas adelante por la misma razón anterior
			return render_template("resultado.html",entrada_id=entrada_id[0],tiempo_total_simulado=tiempo_total_simulado, identificador=identificador, horas_atencion=horas_atencion, pasos=pasos, clientes_por_dia=clientes_por_dia, min_productos=min_productos, max_productos=max_productos, tiempo_seleccion=tiempo_seleccion, tiempo_marcado=tiempo_marcado, tiempo_pago=tiempo_pago, dclientesuno=dclientesuno, dclientesdos=dclientesdos,dclientestres=dclientestres, dclientescuatro=dclientescuatro,dclientescinco=dclientescinco, dclientesseis=dclientesseis, dclientessiete=dclientessiete, dclientesocho=dclientesocho, dclientesnueve=dclientesnueve, dclientesdiez=dclientesdiez, dcajauno=dcajauno, dcajados=dcajados, dcajatres=dcajatres, dcajacuatro=dcajacuatro,dcajacinco=dcajacinco, dcajaseis=dcajaseis, dcajasiete=dcajasiete, dcajaocho=dcajaocho, dcajanueve=dcajanueve, dcajadiez=dcajadiez, ingresadosuno=ingresadosuno, ingresadosdos=ingresadosdos,ingresadostres=ingresadostres,ingresadoscuatro=ingresadoscuatro, ingresadoscinco=ingresadoscinco, ingresadosseis=ingresadosseis, ingresadossiete=ingresadossiete, ingresadosocho=ingresadosocho, ingresadosnueve=ingresadosnueve, ingresadosdiez=ingresadosdiez, despachadosuno=despachadosuno, despachadosdos=despachadosdos, despachadostres=despachadostres,despachadoscuatro=despachadoscuatro,despachadoscinco=despachadoscinco, despachadosseis=despachadosseis, despachadossiete=despachadossiete, despachadosocho=despachadosocho, despachadosnueve=despachadosnueve, despachadosdiez=despachadosdiez, promProdsuno=promProdsuno, promProdsdos=promProdsdos,promProdstres=promProdstres, promProdscuatro=promProdscuatro,promProdscinco=promProdscinco, promProdsseis=promProdsseis, promProdssiete=promProdssiete,promProdsocho=promProdsocho,promProdsnueve=promProdsnueve,promProdsdiez=promProdsdiez,colaMaxuno=colaMaxuno,colaMaxdos=colaMaxdos,colaMaxtres=colaMaxtres,colaMaxcuatro=colaMaxcuatro,colaMaxcinco=colaMaxcinco,colaMaxseis=colaMaxseis,colaMaxsiete=colaMaxsiete,colaMaxocho=colaMaxocho,colaMaxnueve=colaMaxnueve,colaMaxdiez=colaMaxdiez,promColauno=promColauno,promColados=promColados,promColatres=promColatres,promColacuatro=promColacuatro,promColacinco=promColacinco,promColaseis=promColaseis,promColasiete=promColasiete,promColaocho=promColaocho,promColanueve=promColanueve,promColadiez=promColadiez)

