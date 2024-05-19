"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import stack as st
from DISClib.ADT import queue as qu
from DISClib.ADT import map as mp
from DISClib.ADT import minpq as mpq
from DISClib.ADT import indexminpq as impq
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import graph as gr
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Algorithms.Graphs import bellmanford as bf
from DISClib.Algorithms.Graphs import bfs
from DISClib.Algorithms.Graphs import dfs
from DISClib.Algorithms.Graphs import prim
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import insertionsort as ins
from DISClib.Algorithms.Sorting import selectionsort as se
from DISClib.Algorithms.Sorting import mergesort as merg
from DISClib.Algorithms.Sorting import quicksort as quk
assert cf
from haversine import haversine, Unit
"""
Se define la estructura de un catálogo de videos. El catálogo tendrá
dos listas, una para los videos, otra para las categorias de los mismos.
"""

# Construccion de modelos


def new_data_structs():
    """
    Inicializa las estructuras de datos del modelo. Las crea de
    manera vacía para posteriormente almacenar la información.
    """
    
    data_struct = {  'airports': None,
                    'distance_graph': None, 
                    'time_graph': None}
    
    data_struct['airports'] = mp.newMap(maptype='PROBING')
    data_struct['coordinates'] = mp.newMap(maptype='PROBING')
    data_struct['comercial_distance'] = gr.newGraph('ADJ_LIST', directed=False)
    data_struct['militar_distance'] = gr.newGraph('ADJ_LIST', directed=False)
    data_struct['carga_distance'] = gr.newGraph('ADJ_LIST', directed=False)
    data_struct['comercial_time'] = gr.newGraph('ADJ_LIST', directed=False)
    data_struct['militar_time'] = gr.newGraph('ADJ_LIST', directed=False)

    
    return data_struct


# Funciones para agregar informacion al modelo

def add_airport(data_structs, data):
    """
    Función para agregar nuevos elementos a la lista
    """
    entry = mp.get(data_structs['airports'], data['ICAO'])
    
    if entry is None:
        mp.put(data_structs['airports'], data['ICAO'], data)
        
    entry2 = mp.get(float(data['LATITUD'].replace(',', '.')) , float(data['LONGITUD'].replace(',', '.')))
    
    if entry2 is None:
        mp.put(data_structs['coordinates_com'], entry2, data['ICAO'])
        

def add_vertex_comercial(data_structs, data):
    g_comercial_distance = data_structs['comercial_distance']
    g_comercial_time = data_structs['comercial_time']
    data['tipo'] = 'comercial'
    data['concurrencia'] = 0
    if not gr.containsVertex(g_comercial_distance, data['ICAO']):
        gr.insertVertex(g_comercial_distance, data['ICAO'])
    if not gr.containsVertex(g_comercial_time, data['ICAO']):
        gr.insertVertex(g_comercial_time, data['ICAO'])

def add_vertex_militar(data_structs, data):
    g_distance = data_structs['militar_distance']
    g_time = data_structs['militar_time']
    data['tipo'] = 'militar'
    data['concurrencia'] = 0
    if not gr.containsVertex(g_distance, data['ICAO']):
        gr.insertVertex(g_distance, data['ICAO'])
    if not gr.containsVertex(g_time, data['ICAO']):
        gr.insertVertex(g_time, data['ICAO'])
    
def add_vertex_carga(data_structs, data):
    g_distance = data_structs['carga_distance']
    data['tipo'] = 'carga'
    data['concurrencia'] = 0
    if not gr.containsVertex(g_distance, data['ICAO']):
        gr.insertVertex(g_distance, data['ICAO'])

def add_edges(data_structs, data):
    
    aero_origin= me.getValue(mp.get(data_structs['airports'], data['ORIGEN']))
    origin = float(aero_origin['LATITUD'].replace(',', '.')), float(aero_origin['LONGITUD'].replace(',', '.'))
    aero_destin = me.getValue(mp.get(data_structs['airports'], data['DESTINO']))
    destination = float(aero_destin['LATITUD'].replace(',', '.')), float(aero_destin['LONGITUD'].replace(',', '.'))
    
    distance = haversine(origin, destination)
    
    time = data['TIEMPO_VUELO']
    
    if data['TIPO_VUELO'] == 'AVIACION_COMERCIAL':
        g_distance = data_structs['comercial_distance']
        g_time = data_structs['comercial_time']
    elif data['TIPO_VUELO'] == 'MILITAR':
        g_distance = data_structs['militar_distance']
        g_time = data_structs['militar_time']
    elif data['TIPO_VUELO'] == 'AVIACION_CARGA':
        g_distance = data_structs['carga_distance']
        
    if not gr.containsVertex(g_distance, data['ORIGEN']):
        gr.addEdge(g_distance, data['ORIGEN'], data['DESTINO'], distance)
    if not data['TIPO_VUELO'] == 'AVIACION_CARGA':
        if not gr.containsVertex(g_time, data['ORIGEN']):
            gr.addEdge(g_time, data['ORIGEN'], data['DESTINO'], time)
            
# Funciones para creacion de datos

def new_data(id, info):
    """
    Crea una nueva estructura para modelar los datos
    """
    #TODO: Crear la función para estructurar los datos
    pass


# Funciones de consulta

def get_data(data_structs, id):
    """
    Retorna un dato a partir de su ID
    """
    #TODO: Crear la función para obtener un dato de una lista
    pass


def data_size(data_structs):
    """
    Retorna el tamaño de la lista de datos
    """
    #TODO: Crear la función para obtener el tamaño de una lista
    pass


def req_1(data_structs, origen, destino):
    """
    Función que soluciona el requerimiento 1
    """
    comercial_graph = data_structs['comercial_distance']
    punto_origen = punto_mas_cercano(origen[0], origen[1], data_structs['coordinates'])
    punto_destino = punto_mas_cercano(destino[0], destino[1], data_structs['coordinates'])
    
    init = punto_origen[0]
    fin =  punto_destino[0]
    
    camino_dfs = dfs.DepthFirstSearch(comercial_graph, init)
    
    camino = dfs.pathTo(camino_dfs, fin)
    distancia = float(haversine((punto_origen[1], punto_origen[2]), (punto_destino[1], punto_destino[2])))
    tamaño = st.size(camino)

    print(distancia)
    return camino, distancia, tamaño

def req_2(data_structs, origen, destino):
    """
    Función que soluciona el requerimiento 2
    """
    comercial_graph = data_structs['comercial_distance']
    punto_origen = punto_mas_cercano(origen[0], origen[1], data_structs['coordinates'])
    punto_destino = punto_mas_cercano(destino[0], destino[1], data_structs['coordinates'])
    
    init = punto_origen[0]
    fin =  punto_destino[0]
        
    camino_bfs = bfs.BreathFirstSearch(comercial_graph, init)
    
    camino = bfs.pathTo(camino_bfs, fin)
    distancia  = 0
    vis_vertex = lt.newList('ARRAY_LIST')
    for vertex in lt.iterator(camino):
        lt.addLast(vis_vertex, vertex['vertexA'])
        lt.addLast(vis_vertex, vertex['vertexB'])
        distancia += vertex['weight']
    tamaño = lt.size(vis_vertex)

    print(tamaño)
    return camino, distancia, tamaño


def req_3(data_structs):
    """
    Función que soluciona el requerimiento 3
    """
    # TODO: Realizar el requerimiento 3
    pass


def req_4(data_structs):
    """
    Función que soluciona el requerimiento 4
    """
    # TODO: Realizar el requerimiento 4
    pass


def req_5(data_structs):
    """
    Función que soluciona el requerimiento 5
    """
    # TODO: Realizar el requerimiento 5
    pass


def req_6(data_structs):
    """
    Función que soluciona el requerimiento 6
    """
    # TODO: Realizar el requerimiento 6
    pass


def req_7(data_structs):
    """
    Función que soluciona el requerimiento 7
    """
    # TODO: Realizar el requerimiento 7
    pass


def req_8(data_structs):
    """
    Función que soluciona el requerimiento 8
    """
    # TODO: Realizar el requerimiento 8
    pass


# Funciones utilizadas para comparar elementos dentro de una lista

def compare(data_1, data_2):
    """
    Función encargada de comparar dos datos
    """
    #TODO: Crear función comparadora de la lista
    pass

def punto_mas_cercano(lat, lon, mapa_puntos):
    id_mas_cercano = None
    distancia_minima = float("inf")
    
    for id_punto in lt.iterator(mp.keySet(mapa_puntos)):  
        latitud_punto = id_punto[0]
        longitud_punto = id_punto[1]
        distancia = haversine((lat, lon), (latitud_punto, longitud_punto))

        if distancia < distancia_minima:
            distancia_minima = distancia
            id_mas_cercano = me.getValue(mp.get(mapa_puntos, id_punto))

    return id_mas_cercano, latitud_punto, longitud_punto

# Funciones de ordenamiento


def sort_criteria(data_1, data_2):
    """sortCriteria criterio de ordenamiento para las funciones de ordenamiento

    Args:
        data1 (_type_): _description_
        data2 (_type_): _description_

    Returns:
        _type_: _description_
    """
    #TODO: Crear función comparadora para ordenar
    pass


def sort(data_structs):
    """
    Función encargada de ordenar la lista con los datos
    """
    #TODO: Crear función de ordenamiento
    pass
