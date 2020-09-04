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

@app.route('/historial.html')
def historial():
	return render_template('historial.html')


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
	
	def Mostrar(self):
		print("Tiempo Total                     : " , self.TiempoTotal)
		print("Clientes Despachados             : ", self.Clientes_Despachados)
		print("Productos en Caja                : ",self.ProductosTotalesCaja)
		print("Clientes Totales                 : ", self.Clientes_TotalesCaja)
		print("Cola más alta                    : ", self.MaxTam)
		#print("Promedio productos por cliente   : ",self.ProductosTotalesCaja//self.Clientes_Despachados)
		print("Promedio de cola de la caja      : ",self.CalcularPromedio())
	
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
		return self.ProductosTotalesCaja//self.Clientes_Despachados

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

			for f in range(len(PersonasPorIntervalo)):
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

				for i in range(CantidadDeCajash[f]):
					print("CAJA", i )
					Promedio_De_Cola += DatosCajas[i].CalcularPromedio()
					print(DatosCajas[i].Mostrar())
					print("----------------------------")

				for i in range(CantidadDeCajash[f]):
					if(len(Cajas[i]) > 0):
						Suma += len(Cajas[i])
				print("Cola promedio del periodo      :",Promedio_De_Cola // CantidadDeCajash[f])
				print("===============================")

				promColauno = Promedio_De_Cola // CantidadDeCajash[0]
				promColados = Promedio_De_Cola // CantidadDeCajash[1]
				promColatres = Promedio_De_Cola // CantidadDeCajash[2]
				promColacuatro = Promedio_De_Cola // CantidadDeCajash[3]
				promColacinco = Promedio_De_Cola // CantidadDeCajash[4]
				promColaseis = Promedio_De_Cola // CantidadDeCajash[5]
				promColasiete = Promedio_De_Cola // CantidadDeCajash[6]
				promColaocho = Promedio_De_Cola // CantidadDeCajash[7]
				promColanueve = Promedio_De_Cola // CantidadDeCajash[8]
				promColadiez = Promedio_De_Cola // CantidadDeCajash[9]


				sql=""" insert INTRO res_horarios_uno (resultado_id, ingresados, despachados, promedio_productos, promedio_cola, longitud_max_cola)
						values ('%s','%s','%s','%s','%s','%s');
				"""%(resultado_id[0], ingresadosuno, despachadosuno, promProdsuno, promColauno, colaMaxuno)
				cur.execute(sql)
				conn.commit()
				sql=""" insert INTRO res_horarios_dos (resultado_id, ingresados, despachados, promedio_productos, promedio_cola, longitud_max_cola)
						values ('%i','%i','%i','%i','%i','%i');
				"""%(resultado_id[0], ingresadosdos, despachadosdos, promProdsdos, promColados, colaMaxdos)
				cur.execute(sql)
				conn.commit()
				sql=""" insert INTRO res_horarios_tres (resultado_id, ingresados, despachados, promedio_productos, promedio_cola, longitud_max_cola)
						values ('%i','%i','%i','%i','%i','%i');
				"""%(resultado_id[0], ingresadostres, despachadostres, promProdstres, promColatres, colaMaxtres)
				cur.execute(sql)
				conn.commit()
				sql=""" insert INTRO res_horarios_cuatro (resultado_id, ingresados, despachados, promedio_productos, promedio_cola, longitud_max_cola)
						values ('%i','%i','%i','%i','%i','%i');
				"""%(resultado_id[0], ingresadoscuatro, despachadoscuatro, promProdscuatro, promColacuatro, colaMaxcuatro)
				cur.execute(sql)
				conn.commit()
				sql=""" insert INTRO res_horarios_cinco (resultado_id, ingresados, despachados, promedio_productos, promedio_cola, longitud_max_cola)
						values ('%i','%i','%i','%i','%i','%i');
				"""%(resultado_id[0], ingresadoscinco, despachadoscinco, promProdscinco, promColacinco, colaMaxcinco)
				cur.execute(sql)
				conn.commit()
				sql=""" insert INTRO res_horarios_seis (resultado_id, ingresados, despachados, promedio_productos, promedio_cola, longitud_max_cola)
						values ('%i','%i','%i','%i','%i','%i');
				"""%(resultado_id[0], ingresadosseis, despachadosseis, promProdsseis, promColaseis, colaMaxseis)
				cur.execute(sql)
				conn.commit()
				sql=""" insert INTRO res_horarios_siete (resultado_id, ingresados, despachados, promedio_productos, promedio_cola, longitud_max_cola)
						values ('%i','%i','%i','%i','%i','%i');
				"""%(resultado_id[0], ingresadossiete, despachadossiete, promProdssiete, promColasiete, colaMaxsiete)
				cur.execute(sql)
				conn.commit()
				sql=""" insert INTRO res_horarios_ocho (resultado_id, ingresados, despachados, promedio_productos, promedio_cola, longitud_max_cola)
						values ('%i','%i','%i','%i','%i','%i');
				"""%(resultado_id[0], ingresadosocho, despachadosocho, promProdsocho, promColaocho, colaMaxocho)
				cur.execute(sql)
				conn.commit()
				sql=""" insert INTRO res_horarios_nueve (resultado_id, ingresados, despachados, promedio_productos, promedio_cola, longitud_max_cola)
						values ('%i','%i','%i','%i','%i','%i');
				"""%(resultado_id[0], ingresadosnueve, despachadosnueve, promProdsnueve, promColanueve, colaMaxnueve)
				cur.execute(sql)
				conn.commit()
				sql=""" insert INTRO res_horarios_diez (resultado_id, ingresados, despachados, promedio_productos, promedio_cola, longitud_max_cola)
						values ('%i','%i','%i','%i','%i','%i');
				"""%(resultado_id[0], ingresadosdiez, despachadosdiez, promProdsdiez, promColadiez, colaMaxdiez)
				cur.execute(sql)
				conn.commit()
				while(Suma > 0):
					for i in range(CantidadDeCajash[f]):
						if(len(Cajas[i]) > 0):
							ColaAnterior.append(Cajas[i].pop())
							Suma -= 1
				Diferencia = abs(len(Personas) - UltimoEncolado)
				for XD in range(UltimoEncolado,len(Personas)):
					Personas_in_the_middle.append(Personas[XD])
				
				
		except:
			pass
			return render_template("resultado.html",entrada_id=entrada_id[0],tiempo_total_simulado=tiempo_total_simulado, identificador=identificador, horas_atencion=horas_atencion, pasos=pasos, clientes_por_dia=clientes_por_dia, min_productos=min_productos, max_productos=max_productos, tiempo_seleccion=tiempo_seleccion, tiempo_marcado=tiempo_marcado, tiempo_pago=tiempo_pago, dclientesuno=dclientesuno, dclientesdos=dclientesdos,dclientestres=dclientestres, dclientescuatro=dclientescuatro,dclientescinco=dclientescinco, dclientesseis=dclientesseis, dclientessiete=dclientessiete, dclientesocho=dclientesocho, dclientesnueve=dclientesnueve, dclientesdiez=dclientesdiez, dcajauno=dcajauno, dcajados=dcajados, dcajatres=dcajatres, dcajacuatro=dcajacuatro,dcajacinco=dcajacinco, dcajaseis=dcajaseis, dcajasiete=dcajasiete, dcajaocho=dcajaocho, dcajanueve=dcajanueve, dcajadiez=dcajadiez)#, ingresadosuno=ingresadosuno, ingresadosdos=ingresadosdos,ingresadostres=ingresadostres,ingresadoscuatro=ingresadoscuatro, ingresadoscinco=ingresadoscinco, ingresadosseis=ingresadosseis, ingresadossiete=ingresadossiete, ingresadosocho=ingresadosocho, ingresadosnueve=ingresadosnueve, ingresadosdiez=ingresadosdiez, despachadosuno=despachadosuno, despachadosdos=despachadosdos, despachadostres=despachadostres,despachadoscuatro=despachadoscuatro,despachadoscinco=despachadoscinco, despachadosseis=despachadosseis, despachadossiete=despachadossiete, despachadosocho=despachadosocho, despachadosnueve=despachadosnueve, despachadosdiez=despachadosdiez, promProdsuno=promProdsuno, promProdsdos=promProdsdos,promProdstres=promProdstres, promProdscuatro=promProdscuatro,promProdscinco=promProdscinco, promProdsseis=promProdsseis, promProdssiete=promProdssiete,promProdsocho=promProdsocho,promProdsnueve=promProdsnueve,promProdsdiez=promProdsdiez,colaMaxuno=colaMaxuno,colaMaxdos=colaMaxdos,colaMaxtres=colaMaxtres,colaMaxcuatro=colaMaxcuatro,colaMaxcinco=colaMaxcinco,colaMaxseis=colaMaxseis,colaMaxsiete=colaMaxsiete,colaMaxocho=colaMaxocho,colaMaxnueve=colaMaxnueve,colaMaxdiez=colaMaxdiez)#,promColauno=promColauno,promColados=promColados,promColatres=promColatres,promColacuatro=promColacuatro,promColacinco=promColacinco,promColaseis=promColaseis,promColasiete=promColasiete,promColaocho=promColaocho,promColanueve=promColanueve,promColadiez=promColadiez)

