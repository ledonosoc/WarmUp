from configuraciones import *
import psycopg2
conn = psycopg2.connect("dbname=%s user=%s password=%s"%(database,user,passwd))


cur = conn.cursor()
sql ="""DROP SCHEMA public CASCADE;
CREATE SCHEMA public;"""

cur.execute(sql)
sql ="""
CREATE TABLE entradas
		   (id serial PRIMARY KEY,
			identificacion varchar(140),
			horas_atencion integer,
			pasos_simulacion integer,
			clientes_esperados integer,
			clientes_horario_uno integer,
			clientes_horario_dos integer,
			clientes_horario_tres integer,
			clientes_horario_cuatro integer,
			clientes_horario_cinco integer,
			clientes_horario_seis integer,
			clientes_horario_siete integer
			clientes_horario_ocho integer,
			clientes_horario_nueve integer,
			clientes_horario_diez integer,
			cajas_horario_uno integer,
			cajas_horario_dos integer,
			cajas_horario_tres integer,
			cajas_horario_cuatro integer,
			cajas_horario_cinco integer,
			cajas_horario_seis integer,
			cajas_horario_siete integer,
			cajas_horario_ocho integer,
			cajas_horario_nueve integer,
			cajas_horario_diez integer,
			minimo_productos integer,
			maximo_productos integer,
			tiempo_seleccion integer,
			tiempo_despacho integer,
			tiempo_pago integer);
"""

cur.execute(sql)

sql ="""
CREATE TABLE resultados
		   (id serial PRIMARY KEY,
		    entrada_id integer,
		    tiempo_simulado integer, 
		    FOREIGN KEY (entradas_id) REFERENCES entradas (id));
"""

cur.execute(sql)

sql ="""
CREATE TABLE res_horarios_uno
		   (id serial PRIMARY KEY,
			resultado_id integer,
			ingresados integer,
			despachados integer,
			promedio_productos integer,
			promedio_cola integer,
			longitud_max_cola integer,
			FOREIGN KEY (resultado_id) REFERENCES resultados (id));
"""
cur.execute(sql)

sql ="""
CREATE TABLE res_horarios_dos
		   (id serial PRIMARY KEY,
			resultado_id integer,
			ingresados integer,
			despachados integer,
			promedio_productos integer,
			promedio_cola integer,
			longitud_max_cola integer,
			FOREIGN KEY (resultado_id) REFERENCES resultados (id));
"""
cur.execute(sql)

sql ="""
CREATE TABLE res_horarios_tres
		   (id serial PRIMARY KEY,
			resultado_id integer,
			ingresados integer,
			despachados integer,
			promedio_productos integer,
			promedio_cola integer,
			longitud_max_cola integer,
			FOREIGN KEY (resultado_id) REFERENCES resultados (id));
"""
cur.execute(sql)

sql ="""
CREATE TABLE res_horarios_cuatro
		   (id serial PRIMARY KEY,
			resultado_id integer,
			ingresados integer,
			despachados integer,
			promedio_productos integer,
			promedio_cola integer,
			longitud_max_cola integer,
			FOREIGN KEY (resultado_id) REFERENCES resultados (id));
"""
cur.execute(sql)

sql ="""
CREATE TABLE res_horarios_cinco
		   (id serial PRIMARY KEY,
			resultado_id integer,
			ingresados integer,
			despachados integer,
			promedio_productos integer,
			promedio_cola integer,
			longitud_max_cola integer,
			FOREIGN KEY (resultado_id) REFERENCES resultados (id));
"""
cur.execute(sql)

sql ="""
CREATE TABLE res_horarios_seis
		   (id serial PRIMARY KEY,
			resultado_id integer,
			ingresados integer,
			despachados integer,
			promedio_productos integer,
			promedio_cola integer,
			longitud_max_cola integer,
			FOREIGN KEY (resultado_id) REFERENCES resultados (id));
"""
cur.execute(sql)

sql ="""
CREATE TABLE res_horarios_siete
		   (id serial PRIMARY KEY,
			resultado_id integer,
			ingresados integer,
			despachados integer,
			promedio_productos integer,
			promedio_cola integer,
			longitud_max_cola integer,
			FOREIGN KEY (resultado_id) REFERENCES resultados (id));
"""
cur.execute(sql)

sql ="""
CREATE TABLE res_horarios_ocho
		   (id serial PRIMARY KEY,
			resultado_id integer,
			ingresados integer,
			despachados integer,
			promedio_productos integer,
			promedio_cola integer,
			longitud_max_cola integer,
			FOREIGN KEY (resultado_id) REFERENCES resultados (id));
"""
cur.execute(sql)

sql ="""
CREATE TABLE res_horarios_nueve
		   (id serial PRIMARY KEY,
			resultado_id integer,
			ingresados integer,
			despachados integer,
			promedio_productos integer,
			promedio_cola integer,
			longitud_max_cola integer,
			FOREIGN KEY (resultado_id) REFERENCES resultados (id));
"""
cur.execute(sql)

sql ="""
CREATE TABLE res_horarios_diez
		   (id serial PRIMARY KEY,
			resultado_id integer,
			ingresados integer,
			despachados integer,
			promedio_productos integer,
			promedio_cola integer,
			longitud_max_cola integer,
			FOREIGN KEY (resultado_id) REFERENCES resultados (id));
"""
cur.execute(sql)


conn.commit()
cur.close()
conn.close()
