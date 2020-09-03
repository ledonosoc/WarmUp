from configuraciones import *
import psycopg2
conn = psycopg2.connect("dbname=%s user=%s password=%s"%(database,user,passwd))
cur = conn.cursor()

sql =""" insert INTO entradas (identificacion, horas_atencion, pasos_simulacion, clientes_esperados, clientes_horario_uno,
                               clientes_horario_dos, clientes_horario_tres, clientes_horario_cuatro, clientes_horario_cinco,
                               clientes_horario_seis, clientes_horario_siete, clientes_horario_ocho, clientes_horario_nueve,
                               clientes_horario_diez, cajas_horario_uno, cajas_horario_dos, cajas_horario_tres, cajas_horario_cuatro,
                               cajas_horario_cinco, cajas_horario_seis, cajas_horario_siete, cajas_horario_ocho, cajas_horario_nueve,
                               cajas_horario_diez, minimo_productos, maximo_productos, tiempo_seleccion, tiempo_despacho, tiempo_pago)
                       values ('Test','1','1','1','1',
                       		   '1','1','1','1',
                       		   '1','1','1','1',
                       		   '1','1','1','1','1',
                       		   '1','1','1','1','1',
                       		   '1','1','1','1','1','1');  
"""

cur.execute(sql)
conn.commit()


cur.close()
conn.close()
