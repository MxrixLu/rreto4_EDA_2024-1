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
from DISClib.ADT.graph import containsVertex, gr
from DISClib.ADT import map as m
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error
assert cf


# Construccion de modelos

def newAnalyzer():
    try:
        analyzer = {'airports': None,
                    'routes': None,
                    'components': None,
                    'paths': None
                    }
        

        analyzer['airports'] = m.newMap(numelements=10000,
                                     maptype='PROBING',
                                     comparefunction=compareAirports)
        analyzer['Cities'] = m.newMap(numelements=10000,
                                     maptype='PROBING',
                                     comparefunction=compareAirports)

        analyzer['routes'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=14000,
                                              comparefunction=compareRoutes)
        analyzer['routes_2'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=False,
                                              size=14000,
                                              comparefunction=compareRoutes)
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:newAnalyzer')

# Funciones para agregar informacion al grafo
def addAirportbyCode(analyzer,airport) : 
    codes = analyzer['airports']
    code = airport['IATA']
    mp.put(codes,code,airport)

def addCity(analyzer,city):
    cities = analyzer['Cities']
    cityID = city['city_ascii']
    mp.put(cities,cityID,city)

def addRoute(analyzer,route):
    try:
        Airports = analyzer['airports']

        distance = float(route['distance_km'])
        departure = mp.get(Airports,route['Departure'])
        destination = mp.get(Airports,route['Destination'])
        containsAirport_1 = gr.containsVertex(analyzer['routes'],route['Departure'])
        containsAirport_2 = gr.containsVertex(analyzer['routes'],route['Destination'])
        if not containsAirport_1 : 
            addAirport(analyzer,route['Departure'] ,departure)
        if not containsAirport_2: 
            addAirport(analyzer,route['Destination'],destination)
        addConnection(analyzer,route['Departure'],route['Destination'],distance)
        

        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:addStopConnection')

def addRoute_2(analyzer,route):
    try:
        Airports = analyzer['airports']

        distance = float(route['distance_km'])
        departure = mp.get(Airports,route['Departure'])
        destination = mp.get(Airports,route['Destination'])
        containsAirport_1 = gr.containsVertex(analyzer['routes_2'],route['Departure'])
        containsAirport_2 = gr.containsVertex(analyzer['routes_2'],route['Destination'])
        if not containsAirport_1 : 
            addAirport_2(analyzer,route['Departure'] ,departure)
        if not containsAirport_2: 
            addAirport_2(analyzer,route['Destination'],destination)
        addConnection(analyzer,route['Departure'],route['Destination'],distance)
        

        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:addStopConnection')
    
def addAirport(analyzer,ID,airport):
    try:
        if not gr.containsVertex(analyzer['routes'], ID):
            gr.insertVertex(analyzer['routes'], ID)
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:addstop')

def addAirport_2(analyzer,ID,airport):
    try:
        if not gr.containsVertex(analyzer['routes_2'], ID):
            gr.insertVertex(analyzer['routes_2'], ID)
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:addstop')

def addRouteStop(analyzer, service):
    """
    Agrega a una estacion, una ruta que es servida en ese paradero
    """
    entry = m.get(analyzer['airports'], service[''])
    if entry is None:
        lstroutes = lt.newList('SINGLE_LINKED')
        lt.addLast(lstroutes, service['ServiceNo'])
        m.put(analyzer['stops'], service['BusStopCode'], lstroutes)
    else:
        lstroutes = entry['value']
        info = service['ServiceNo']
        if not lt.isPresent(lstroutes, info):
            lt.addLast(lstroutes, info)
    return analyzer


def addRouteConnections(analyzer):
    """
    Por cada vertice (cada estacion) se recorre la lista
    de rutas servidas en dicha estación y se crean
    arcos entre ellas para representar el cambio de ruta
    que se puede realizar en una estación.
    """
    lststops = m.keySet(analyzer['stops'])
    for key in lt.iterator(lststops):
        lstroutes = m.get(analyzer['stops'], key)['value']
        prevrout = None
        for route in lt.iterator(lstroutes):
            route = key + '-' + route
            if prevrout is not None:
                addConnection(analyzer, prevrout, route, 0)
                addConnection(analyzer, route, prevrout, 0)
            prevrout = route


def addConnection(analyzer, origin, destination, distance):
    """
    Adiciona un arco entre dos estaciones
    """
    edge = gr.getEdge(analyzer['routes'], origin, destination)
    if edge is None:
        gr.addEdge(analyzer['routes'], origin, destination, distance)
    return analyzer

def addConnection_2(analyzer, origin, destination, distance):
    """
    Adiciona un arco entre dos estaciones
    """
    edge = gr.getEdge(analyzer['routes_2'], origin, destination)
    if edge is None:
        gr.addEdge(analyzer['routes_2'], origin, destination, distance)
    return analyzer

# Funciones para creacion de datos
def newAirport(ID,aiportInfo) : 
    airport = {"ID":ID,
            "Info":aiportInfo}
    return airport
# Funciones de consulta
def totalAirports(routes) : 
    return gr.numVertices(routes)

# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento

# Funciones de comparación
def compareAirports(arpt1,arpt2):
    arptcode = arpt2['key']
    if (arpt1 == arptcode):
        return 0
    elif (arpt1 > arptcode):
        return 1
    else:
        return -1
def compareCities(stop,keyvaluestop):
    stopcode = keyvaluestop['key']
    if (stop == stopcode):
        return 0
    elif (stop > stopcode):
        return 1
    else:
        return -1

def compareRoutes(stop, keyvaluestop):
    stopcode = keyvaluestop['key']
    if (stop == stopcode):
        return 0
    elif (stop > stopcode):
        return 1
    else:
        return -1
