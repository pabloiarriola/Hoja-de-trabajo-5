#Universidad del Valle de Guatemala
#Hoja de Trabajo 5
#27/8/2015
#Pablo Arriola 131115

import itertools
import random
import simpy
from pprint import pprint

RANDOM_SEED = 42
MEMORIA_RAM = 100 #memoria RAM
NIVEL_DE_MEMORIA = [1,100] #la memoria RAM disponible
CANT_PROCESOS = 26 #la cantidad de procesos 
VELOCIDAD = 1 #instrucciones que ejecuta por unidad de tiempo

intervalo = 10 #la creacion de procesos sigue una distribucion exp con intervalo = 10
capacidad = 1 #un solo cpu
lista = list()



def proceso (nombre, env, cpu, memoria):
    memoria = simpy.Container(env,MEMORIA_RAM,init=MEMORIA_RAM)
    

    with cpu.request() as req:
        print ('%s llegando a %1.f' % (nombre, env.now))
        start = env.now
        
        #se pide la cantidad de memoria necesaria 
        yield req
        
        #Se da la memoria pedida
        memoria_requerida = random.randint(*NIVEL_DE_MEMORIA)
        
        yield memoria.get(memoria_requerida)

        #la ejecucion de instrucciones toma tiempo
        yield env.timeout(memoria_requerida/VELOCIDAD)
        
        tiempo_proceso = env.now - start
        print ('%s termino ejecutando instrucciones en %.1f segundos.' %(nombre, tiempo_proceso))
        #print (memoria_requerida)
        #print (memoria.level)
        
        lista.append(tiempo_proceso)
        #print (lista)
        total=sum(lista)
        print ('PROMEDIO DE TIEMPO QUE ESTA EL PROCESO EN LA COMPUTADORA HASTA EL MOMENTO %1.f' %(total/CANT_PROCESOS))
        
        
def memoria_control (env, cpu):
    #se revisa periodicamente la cantidad de memoria disponible
    while True:
        if memoria.level/memoria.capacity *100 <10:
            print ('Revisando memori RAM a %d' % env.now)
            print ('Memoria RAM disponible: %d' % memorial.level)
            
        yield env.timeout(10) #se revisa cada 10 segundos 


def proceso_generador(env, cpu, memoria):
    
    for i in range(CANT_PROCESOS):
        c=0
        
        t = random.expovariate(1.0/intervalo)
        yield env.timeout(t)
        env.process(proceso('Proceso %d' %i, env, cpu, memoria))
    

#se inicia la simulacion
random.seed(RANDOM_SEED)

#se crea el ambiente
env = simpy.Environment()
cpu = simpy.Resource(env, capacidad)#cantidad de cpu
memoria = simpy.Container(env,MEMORIA_RAM,init=MEMORIA_RAM)#capacidad de la memoria




env.process(memoria_control(env,memoria))
env.process(proceso_generador(env,cpu,memoria))


 
#se corre la simulacion
env.run()

    

