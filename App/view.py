"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

from App.controller import distancia
import config as cf
import sys
import controller
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
assert cf

sys.setrecursionlimit(1000000000)

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido")
    print("1- Iniciar Analizador")
    print("2- Cargar información de los aeropuertos y rutas")
    print("3- Requerimiento 1: Encontrar puntos de interconexión aérea")
    print("4- Requerimiento 2: Encontrar clústeres de tráfico aéreo")
    print("5- Requerimiento 3: Encontrar la ruta más corta entre ciudades")
    print("6- Requerimiento 4: Utilizar las millas de viajero")
    print("7- Requerimiento 5: Cuantificar el efecto de un aeropuerto cerrado")
    print("8- Salir del programa")


catalog = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar:\n')
    if int(inputs[0]) == 1:
        print("\nInicializando....")
        analyzer = controller.init()

    elif int(inputs[0]) == 2:
        print("Cargando datos .... ")
        services = controller.loadServices(analyzer)
        num_1 = services[1]
        num_2 = services[2]
        cities = services[3]
        airport_inicial = services[4]
        airport_final = services[5]
        print(f'Total de aeropuertos = {num_1}')
        print(f'Total de rutas aéreas = {num_2}')
        print(f'Total de ciudades = {cities} ')
        print('El primer aeropuerto fue: ' + str(airport_inicial))
        print('El último aeropuerto fue: ' + str(airport_final))


    elif int(inputs[0]) == 3:
        pass
    elif int(inputs[0]) == 4:
        pass
    elif int(inputs[0]) == 5:
        pass
    elif int(inputs[0]) == 6:
        mst = controller.mst(analyzer['routes'])
        distanciaMillas = controller.distancia(analyzer['routes'],mst)
        distanciaKm = (distanciaMillas*1.6)
        print("La cantidad de nodos de la red de expansion minima es: " ,mp.size(mst['marked']))
        print("La distancia total de la red de expansion minima es de: ",distanciaKm,"km")
    elif int(inputs[0]) == 7:
        pass
    else:
        sys.exit(0)
sys.exit(0)
