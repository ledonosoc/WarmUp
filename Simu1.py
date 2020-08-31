import random as ran

class persona:
    Tp = 0
    Pcantidad = 0
    def __init__(self ,Cantidad_Minima, Cantidad_Maxima):
        self.Pcantidad = ran.randrange(Cantidad_Minima,Cantidad_Maxima + 1)
    def TiempoPersonal(self, PromedioCompra):
        self.Tp = self.Pcantidad*PromedioCompra
    def CambiarTiempo(self):
        self.Tp = self.Tp - 1
    def getCantidad(self):  #retorna la cantidad de cosas que tiene
        return self.Pcantidad

class DatosCaja:
    TiempoTotal = 0
    Clientes_Despachados = 0
    ProductosTotalesCaja = 0
    Clientes_Espera = 0
    def SetTiempo(self,Persona):
        self.TiempoTotal += Persona.Tp
    def SetProductosTotales(self,Persona):
        self.ProductosTotalesCaja += Persona.Pcantidad
    def ClientesEnCaja(self):
        self.Clientes_Espera += 1

def Q_PersonaToCaja(Cajas,nCaja,Persona):
    Cajas[nCaja].append(Persona)

def DQ_PersonaFromCaja(Cajas,nCaja): #Sujeta a cambios
    Cajas[nCaja].pop()

def CrearListaPersonas(Cantidad_Minima , Cantidad_Maxima, nPersonas, PromedioCompra):
    TotalPersonas = []
    i = 0
    while i < nPersonas:
        P = persona(Cantidad_Minima, Cantidad_Maxima)
        P.TiempoPersonal(PromedioCompra)
        TotalPersonas.append(P)
        i+=1
    return TotalPersonas

def EntrarSupermercado(Horario_Sg, Personas_Horario):
    return Horario_Sg / Personas_Horario

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
    Min = len(Cajas[0])
    for x in Cajas:
        if len(x) < Min:
            Min = x
    return Min
# Codigo de prueba
PromedioEntrada = EntrarSupermercado(3600*3,120) #Cada cuanto tiempo entra una persona al Supermercado
Personas = CrearListaPersonas(0,60,120,60) # Lista de personas
Temporizador = 0
Entra = 0
PersonasDentro = 0
Cajas = CrearCajas(5) # 5 suponiendo que es el parametro que entrega el Cliente
DatosCajas = CrearDatosCaja(5)
CajasBajas = [] # Para el proceso de seleccionar una caja aleatoria 

# O(h) = O(n^3) o cercano, si existe una forma más optima pls avisar <------------ This 
while(Temporizador < 3600*3): # 3600 es 1 hora, solo para testear
    if(Entra == PromedioEntrada):
        PersonasDentro += 1
        Entra = 0
    for x in range(0,PersonasDentro):
        if(Personas[x].Tp == 0):
            MenorCola = BusquedaMenor(Cajas) # Retorna el tamaño de la cola más pequeña, tiempo lineal
            for a in range(0,len(Cajas)):
                if len(Cajas[a]) == MenorCola: # Si existe otra cola de menor tamaño se agrega a un arreglo junto a las demás de igual tam
                    CajasBajas.append(a)
            Encolar = Equal_Caja(CajasBajas) # Retorna un número aleatorio de entre las cajas con el menor tamaño
            Cajas[Encolar].append(Personas[x])
            DatosCaja[Encolar].ClientesEnCaja()
            DatosCaja[Encolar].SetProductosTotales(Personas[x])
            DatosCaja[Encolar].ProductosTotalesCaja(Personas[x])

            while len(CajasBajas) > 0: #Vacia la cola auxiliar
                CajasBajas.pop()              
        else:
            Personas[x].CambiarTiempo() # Reduce en 1 el tiempo del cliente en escoger los productos

    Entra+=1
    Temporizador+=1
    
if __name__ == '__main__':
    while True :
        print(" 1- SIMULAR. ")
        print(" 2- INGRESAR A BASE DE DATOS. ")
        print(" 3- EDITAR ALGUNA SIMULACIÓN ANTERIOR. ")
        print(" 4- SALIR. ")
        opcion = int(input(" INGRESE OPCIÓN. "))
        if (opcion == 1):
            texto = input("Ingrese los datos del simulador (nombre/fecha/N°simulacion): ")
            horasdiarias = int(input("Ingresa horas diarias trabajadas: "))
            periodos = int(input("¿En cuántos períodos dividirá el día laboral?: "))
            clientestotal = int(input("Total de clientes por día: "))
            distribucionporcentual = input(f"La distribución porcentual de los {periodos} periodos: ")
            cajasporperiodo = input(f"La distribución de cajas en los {periodos} periodos: ")
            minprod = int(input("Cantidad Mín de productos : "))
            maxprod = int(input(f"Cantidad máx de productos (debe ser mayor a {minprod} ): "))
            promseleccion = int(input("Ingrese tiempo promedio de selección de productos: "))
            prommarcado = int(input("Ingrese tiempo de marcado por producto: "))
            prompago = int(input("Ingrese tiempo promedio de pago por cliente: "))
            atendidos = 0
            productos = 0
            largo = 0
            distribucion = distribucionporcentual.split("/")
            '''FORMULA--------'''n = horasdiarias/periodos #n es la cantidad de horas que cubre cada periodo
            '''FORMULA--------'''tiempoperiodo = (3600*10*n)/10 #entrega el tiempo en segundos que tiene cada periodo dentro de las 10 hrs 
            # asi creo que es la logica que deberia seguir el cod
            '''
            Esto es como mas o menos creo que deberia ser los pasos del programa.
            obviamente ocupando las clases de arriba y hay que adaptarlas a ese cod

            for i in range(0, periodos):    Aqui recorre los x periodos

                FORMULA--------clientes = (clientestotal*distribucion[i])/100  formula que entrega el total de clientes por periodo
                aqui obtenemos los clientes de este periodo.

                for j in range(0, clientes):  por cada periodo crea los clientes que corresponden y los encola 
                    p = persona(minprod, maxprod)
                    p.tiempopersonal(promseleccion)
                    cola = Cola()
                    cola.encolar(p)
                for k in range(0, tiempoperiodo): va simulando los periodos, aqui va sacando los clientes y simulando sus compras y cambiando sus tiempos 
                    if(p.getTiempo() == 0):
                        atendidos += 1
                        productos += p.getCantidad()
                        cola.desencolar(p)
                    else:
                        ..............
                        '''

            #for i in range(0, len(distribucion)):
            #   print(distribucion[i])
        elif (opcion == 2):
            print("Aún no programado :( ")
        elif (opcion == 3):
            print("Aún no programado :( ")
        elif (opcion == 4):
            print(" MUCHAS GRACIAS POR UTILIZAR NUESTRO SOFTWARE!! :) ")
            break
