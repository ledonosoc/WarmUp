import random as ran

class persona:
    Tp = 0
    Pcantidad = 0
    Tiempo_DespachoCaja = 0
    TiempoPagandoz = 0
    DesencolarProducto = 0
    PromDespacho = 0
    def __init__(self ,Cantidad_Minima, Cantidad_Maxima):
        self.Pcantidad = ran.randrange(Cantidad_Minima,Cantidad_Maxima + 1)
    def TiempoPersonal(self, PromedioCompra,PromedioDespacho):
        self.Tp = self.Pcantidad*PromedioCompra
        self.TiempoPagandoz = self.Pcantidad*PromedioDespacho
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
    def SetTiempo(self):
        self.TiempoTotal += 1
    def SetProductosTotales(self):
        self.ProductosTotalesCaja += 1
    def Set_ClientesTotalesCaja(self):
        self.Clientes_TotalesCaja += 1
    def Mostrar(self):
        print("Tiempo Total         : " , self.TiempoTotal)
        print("Clientes Despachados : ", self.Clientes_Despachados)
        print("Productos en Caja    : ",self.ProductosTotalesCaja)
        print("Clientes Totales     : ", self.Clientes_TotalesCaja)

def CrearListaPersonas(Cantidad_Minima , Cantidad_Maxima, nPersonas, PromedioCompra,PromedioDespacho):
    TotalPersonas = []
    i = 0
    while i < nPersonas:
        P = persona(Cantidad_Minima, Cantidad_Maxima)
        P.TiempoPersonal(PromedioCompra,PromedioDespacho)
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
# Codigo de prueba
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
            distribucionporcentual = input("La distribución porcentual de los  periodos: ")
            cajasporperiodo = input("La distribución de cajas en los periodos: ")
            minprod = int(input("Cantidad Mín de productos : "))
            maxprod = int(input("Cantidad máx de productos (debe ser mayor a {minprod} ): "))
            promseleccion = int(input("Ingrese tiempo promedio de selección de productos: "))
            prommarcado = int(input("Ingrese tiempo de marcado por producto: "))
            prompago = int(input("Ingrese tiempo promedio de pago por cliente: "))
            distribucion = distribucionporcentual.split("/")
            cajas = cajasporperiodo.split(",")
            for n in range (0, periodos):
                PromedioEntrada = EntrarSupermercado(3600*horasdiarias/periodos,120) #Cada cuanto tiempo entra una persona al Supermercado
                Personas = CrearListaPersonas(minprod,maxprod,int(clientestotal*distribucion[n]),promseleccion,prompago) # Lista de personas
                Temporizador = 0
                Entra = 0
                PersonasDentro = 0
                Cajas = CrearCajas(cajas[n]) #  suponiendo que es el parametro que entrega el Cliente
                DatosCajas = CrearDatosCaja(cajas[n])
                CajasBajas = [] # Para el proceso de seleccionar una caja aleatoria 
                i = 0

                while(Temporizador < 3600*horasdiarias/periodos):
                    if(Entra == PromedioEntrada):
                        PersonasDentro += 1
                        Entra = 0
                    for x in range(0,PersonasDentro):
                        
                        Personas[x].CambiarTiempo() # Reduce en 1 el tiempo del cliente en escoger los productos  
                        if(Personas[x].Tp == 0):
                            MenorCola = BusquedaMenor(Cajas) 
                            for a in range(0,len(Cajas)):
                                if len(Cajas[a]) == MenorCola:
                                    CajasBajas.append(a)
                            Encolar = Equal_Caja(CajasBajas) 
                            Cajas[Encolar].append(Personas[x])
                            DatosCajas[Encolar].Set_ClientesTotalesCaja()
                            while len(CajasBajas) > 0:
                                CajasBajas.pop()              
                    for a in range(5):
                        if(len(Cajas[a]) == 0):
                            continue
                        elif(len(Cajas[a]) > 0):
                            Cajas[a][0].EstoyPagando()
                            Cajas[a][0].PagarProducto() # Al llegar al promedio de pago de 1 producto la persona popea 1 objeto
                            DatosCajas[a].SetTiempo() # LaCaja aumenta en 1 el tiempo que ha atendido gente


                            if(Cajas[a][0].DesencolarProducto == Cajas[a][0].PromDespacho): # se llega al promedio de despacho de un producto
                                DatosCajas[a].SetProductosTotales() #La Caja aumenta en 1 la cantidad de productos que ha recibido
                                Cajas[a][0].ProductoPagado() # Reduce en 1 la cantidad de productos que posee el cliente
                                Cajas[a][0].ResetDesencolarProducto() # resetea el contador para popear productos  
                            if(Cajas[a][0].TiempoPagandoz == 0):     
                                Cajas[a].pop()
                                DatosCajas[a].Clientes_Despachados += 1
                        

                    Entra+=1
                    Temporizador+=1
                for i in range(5):
                    print(DatosCajas[i].Mostrar())
                    print("-------------------")
                for i in range(5):
                    print("Gente en cola caja",i,": ",len(Cajas[i]))

    
