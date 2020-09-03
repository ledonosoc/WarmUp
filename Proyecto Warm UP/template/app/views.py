from app import app
from flask import render_template,request,redirect
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

    # def Mostrar(self):
    #     print("Tiempo Total                     : " , self.TiempoTotal)
    #     print("Clientes Despachados             : ", self.Clientes_Despachados)
    #     print("Productos en Caja                : ",self.ProductosTotalesCaja)
    #     print("Clientes Totales                 : ", self.Clientes_TotalesCaja)
    #     print("Cola más alta                    : ", self.MaxTam)
    #     print("Promedio productos por cliente   : ",self.ProductosTotalesCaja//self.Clientes_Despachados)

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
#------------- Variables de entrada form: --------------------------------
#---Form----------------------  -> Variable SQL---------------------------

#Simulacion 					-> identificacion	
#Horas_diarias_de_atencion 		-> horas_atencion
#Pasos 							-> pasos_simulacion
#Clientes_esperados_por_dia 	-> clientes_esperados
#distribucion_clientes_uno 		-> clientes_horario_uno
#distribucion_clientes_dos		-> clientes_horario_dos
#distribucion_clientes_tres 	-> clientes_horario_tres
#distribucion_clientes_cuatro	-> clientes_horario_cuatro
#distribucion_clientes_cinco	-> clientes_horario_cinco
#distribucion_clientes_seis		-> clientes_horario_seis
#distribucion_clientes_siete	-> clientes_horario_siete
#distribucion_clientes_ocho		-> clientes_horario_ocho
#distribucion_clientes_nueve	-> clientes_horario_nueve
#distribucion_clientes_diez		-> clientes_horario_diez
#distribucion_cajas_uno			-> cajas_horario_uno
#distribucion_cajas_dos			-> cajas_horario_dos
#distribucion_cajas_tres		-> cajas_horario_tres
#distribucion_cajas_cuatro		-> cajas_horario_cuatro
#distribucion_cajas_cinco		-> cajas_horario_cinco
#distribucion_cajas_seis		-> cajas_horario_seis
#distribucion_cajas_siete		-> cajas_horario_siete
#distribucion_cajas_ocho		-> cajas_horario_ocho
#distribucion_cajas_nueve		-> cajas_horario_nueve
#distribucion_cajas_diez		-> cajas_horario_diez
#Min_productos_por_cliente 		-> minimo_productos
#Max_productos_por_cliente		-> maximo_productos
#Tiempo_seleccion 				-> tiempo_seleccion
#Tiempo_marcado					-> tiempo_despacho
#Tiempo_pago					-> tiempo_pago

@app.route('/resultado', methods=['POST','GET'])
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

			sql ="""insert INTO entradas (identificacion, horas_atencion, pasos_simulacion, clientes_esperados, clientes_horario_uno, 
										clientes_horario_dos, clientes_horario_tres, clientes_horario_cuatro, clientes_horario_cinco, 
										clientes_horario_seis, clientes_horario_siete, clientes_horario_ocho, clientes_horario_nueve, 
										clientes_horario_diez, cajas_horario_uno, cajas_horario_dos, cajas_horario_tres, 
										cajas_horario_cuatro, cajas_horario_cinco, cajas_horario_seis, cajas_horario_siete, 
										cajas_horario_ocho, cajas_horario_nueve, cajas_horario_diez, minimo_productos, maximo_productos, 
										tiempo_seleccion, tiempo_despacho, tiempo_pago) 
					values ('%s','%i','%i','%i','%i',
							'%i','%i','%i','%i',
							'%i','%i','%i','%i',
							'%i','%i','%i','%i',
							'%i','%i','%i','%i',
							'%i','%i','%i','%i','%i',
							'%i','%i','%i')
					returning entradas.id;  
					"""%(identificador,horas_atencion,pasos,clientes_por_dia,dclientesuno,
						dclientesdos,dclientestres,dclientescuatro,dclientescinco,
						dclientesseis,dclientessiete,dclientesocho,dclientesnueve,
						dclientesdiez,dcajauno,dcajados,dcajatres,
						dcajacuatro,dcajacinco,dcajaseis,dcajasiete,
						dcajaocho,dcajanueve,dcajadiez,min_productos,max_productos,
						tiempo_seleccion,tiempo_marcado,tiempo_pago)


			cur.execute(sql)
			entrada_id = cur.fetchone()
			conn.commit()

			tiempo_total_simulado = horas_atencion*60
			Diferencia = 0
			Personas_in_the_middle = []
			UltimoEncolado = 0
			Suma = 0
			ColaAnterior = []
			CantidadDeCajash = [dcajauno,dcajados,dcajatres,dcajacuatro,dcajacinco,dcajaseis,dcajasiete,dcajaocho,dcajanueve,dcajadiez]
			Diferencia = 0
			PersonasPorIntervalo = [dclientesuno,dclientesdos,dclientestres,dclientescuatro,dclientescinco,dclientesseis,dclientessiete,dclientesocho,dclientesnueve,dclientesdiez]
			for f in range(len(PersonasPorIntervalo)):
				Personas = []

				PromedioEntrada = EntrarSupermercado(3600*3,(PersonasPorIntervalo[f] + Diferencia)) #Cada cuanto tiempo entra una persona al Supermercado
				if(len(Personas_in_the_middle) > 0):
					for xc in Personas_in_the_middle:
						Personas.append(xc)
					Personas.extend(CrearListaPersonas(min_productos,max_productos,PersonasPorIntervalo[f] + Diferencia,tiempo_seleccion,tiempo_marcado,tiempo_pago)) # Lista de personas
				else:
					Personas = CrearListaPersonas(min_productos,max_productos,PersonasPorIntervalo[f] + Diferencia,tiempo_seleccion,tiempo_marcado,tiempo_pago)
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
						while len(CajasBajas) > 0:
							CajasBajas.pop()   
				while(Temporizador < 3600*3):
					if(Entra == PromedioEntrada):
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

								Cajas[a].pop()
								DatosCajas[a].Clientes_Despachados += 1
								DatosCajas[Encolar].SetModificaciones()
								DatosCajas[a].SetUpTamPro(len(Cajas[a]))               
					Entra+=1
					Temporizador+=1

				sql=""" insert INTO resultados (entrada_id, tiempo_simulado) values ('%i','%i') returning resultados.id;
				"""%(entrada_id, tiempo_total_simulado)
				cur.execute(sql)
				resultado_id = cur.fetchone()
				conn.commit()

				Promedio_De_Cola = 0

				for i in range(CantidadDeCajash[f]):
					print("CAJA", i )
					Promedio_De_Cola += DatosCajas[i].CalcularPromedio()
				for i in range(CantidadDeCajash[f]):
					if(len(Cajas[i]) > 0):
						Suma += len(Cajas[i])

#Agrego todas estas variables porque no estoy seguro de si los metodos y arreglos 
#(ej:DatosCajas[0].GetClientTotal()) se pueden plotear en flask/render

				ingresadosuno = DatosCajas[0].GetClientTotal()
				ingresadosdos = DatosCajas[1].GetClientTotal()
				ingresadostres = DatosCajas[2].GetClientTotal()
				ingresadoscuatro = DatosCajas[3].GetClientTotal()
				ingresadoscinco = DatosCajas[4].GetClientTotal()
				ingresadosseis = DatosCajas[5].GetClientTotal()
				ingresadossiete = DatosCajas[6].GetClientTotal()
				ingresadosocho = DatosCajas[7].GetClientTotal()
				ingresadosnueve = DatosCajas[8].GetClientTotal()
				ingresadosdiez = DatosCajas[9].GetClientTotal()

				despachadosuno = DatosCajas[0].GetClientDespa()
				despachadosdos = DatosCajas[1].GetClientDespa()
				despachadostres = DatosCajas[2].GetClientDespa()
				despachadoscuatro = DatosCajas[3].GetClientDespa()
				despachadoscinco = DatosCajas[4].GetClientDespa()
				despachadosseis = DatosCajas[5].GetClientDespa()
				despachadossiete = DatosCajas[6].GetClientDespa()
				despachadosocho = DatosCajas[7].GetClientDespa()
				despachadosnueve = DatosCajas[8].GetClientDespa()
				despachadosdiez = DatosCajas[9].GetClientDespa()
				
				promProdsuno = DatosCajas[0].GetPromProds()
				promProdsdos = DatosCajas[1].GetPromProds()
				promProdstres = DatosCajas[2].GetPromProds()
				promProdscuatro = DatosCajas[3].GetPromProds()
				promProdscinco = DatosCajas[4].GetPromProds()
				promProdsseis = DatosCajas[5].GetPromProds()
				promProdssiete = DatosCajas[6].GetPromProds()
				promProdsocho = DatosCajas[7].GetPromProds()
				promProdsnueve = DatosCajas[8].GetPromProds()
				promProdsdiez = DatosCajas[9].GetPromProds()

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

				colaMaxuno = DatosCajas[0].GetColaMax()
				colaMaxdos = DatosCajas[1].GetColaMax()
				colaMaxtres = DatosCajas[2].GetColaMax()
				colaMaxcuatro = DatosCajas[3].GetColaMax()
				colaMaxcinco = DatosCajas[4].GetColaMax()
				colaMaxseis = DatosCajas[5].GetColaMax()
				colaMaxsiete = DatosCajas[6].GetColaMax()
				colaMaxocho = DatosCajas[7].GetColaMax()
				colaMaxnueve = DatosCajas[8].GetColaMax()
				colaMaxdiez = DatosCajas[9].GetColaMax()
				

				sql=""" insert INTRO res_horarios_uno (resultado_id, ingresados, despachados, promedio_productos, promedio_cola, longitud_max_cola)
						values ('%i','%i','%i','%i','%i','%i');
				"""%(resultado_id, ingresadosuno, despachadosuno, promProdsuno, promColauno, colaMaxuno)
				cur.execute(sql)
				conn.commit()
				sql=""" insert INTRO res_horarios_dos (resultado_id, ingresados, despachados, promedio_productos, promedio_cola, longitud_max_cola)
						values ('%i','%i','%i','%i','%i','%i');
				"""%(resultado_id, ingresadosdos, despachadosdos, promProdsdos, promColados, colaMaxdos)
				cur.execute(sql)
				conn.commit()
				sql=""" insert INTRO res_horarios_tres (resultado_id, ingresados, despachados, promedio_productos, promedio_cola, longitud_max_cola)
						values ('%i','%i','%i','%i','%i','%i');
				"""%(resultado_id, ingresadostres, despachadostres, promProdstres, promColatres, colaMaxtres)
				cur.execute(sql)
				conn.commit()
				sql=""" insert INTRO res_horarios_cuatro (resultado_id, ingresados, despachados, promedio_productos, promedio_cola, longitud_max_cola)
						values ('%i','%i','%i','%i','%i','%i');
				"""%(resultado_id, ingresadoscuatro, despachadoscuatro, promProdscuatro, promColacuatro, colaMaxcuatro)
				cur.execute(sql)
				conn.commit()
				sql=""" insert INTRO res_horarios_cinco (resultado_id, ingresados, despachados, promedio_productos, promedio_cola, longitud_max_cola)
						values ('%i','%i','%i','%i','%i','%i');
				"""%(resultado_id, ingresadoscinco, despachadoscinco, promProdscinco, promColacinco, colaMaxcinco)
				cur.execute(sql)
				conn.commit()
				sql=""" insert INTRO res_horarios_seis (resultado_id, ingresados, despachados, promedio_productos, promedio_cola, longitud_max_cola)
						values ('%i','%i','%i','%i','%i','%i');
				"""%(resultado_id, ingresadosseis, despachadosseis, promProdsseis, promColaseis, colaMaxseis)
				cur.execute(sql)
				conn.commit()
				sql=""" insert INTRO res_horarios_siete (resultado_id, ingresados, despachados, promedio_productos, promedio_cola, longitud_max_cola)
						values ('%i','%i','%i','%i','%i','%i');
				"""%(resultado_id, ingresadossiete, despachadossiete, promProdssiete, promColasiete, colaMaxsiete)
				cur.execute(sql)
				conn.commit()
				sql=""" insert INTRO res_horarios_ocho (resultado_id, ingresados, despachados, promedio_productos, promedio_cola, longitud_max_cola)
						values ('%i','%i','%i','%i','%i','%i');
				"""%(resultado_id, ingresadosocho, despachadosocho, promProdsocho, promColaocho, colaMaxocho)
				cur.execute(sql)
				conn.commit()
				sql=""" insert INTRO res_horarios_nueve (resultado_id, ingresados, despachados, promedio_productos, promedio_cola, longitud_max_cola)
						values ('%i','%i','%i','%i','%i','%i');
				"""%(resultado_id, ingresadosnueve, despachadosnueve, promProdsnueve, promColanueve, colaMaxnueve)
				cur.execute(sql)
				conn.commit()
				sql=""" insert INTRO res_horarios_diez (resultado_id, ingresados, despachados, promedio_productos, promedio_cola, longitud_max_cola)
						values ('%i','%i','%i','%i','%i','%i');
				"""%(resultado_id, ingresadosdiez, despachadosdiez, promProdsdiez, promColadiez, colaMaxdiez)
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
	return render_template('resultado.html')



