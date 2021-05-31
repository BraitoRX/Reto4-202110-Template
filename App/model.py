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




from posixpath import split
from sys import last_traceback
from typing import OrderedDict
import config as cf
import csv
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT import graph as gr
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from math import radians, cos, sin, asin, sqrt
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos
def new_model()->dict:
    model={"graph":gr.newGraph(directed=True,size=1000,comparefunction=Compare_Keys)
        ,"ldp":mp.newMap(maptype="PROBING",comparefunction=Compare_Keys)
        ,"cntry":mp.newMap(maptype="PROBING",comparefunction=Compare_Keys)
        ,"cables":mp.newMap(maptype="PROBING",comparefunction=Compare_Keys)}
    return model
    
# Funciones para agregar informacion al catalogo

# Funciones para creacion de datos
def cargar_datos_connections(model_vacio:dict,nombre:str)->None:
    archivo= csv.DictReader(open(cf.data_dir+nombre+".csv",encoding="utf-8-sig",newline=''),delimiter=csv.excel.delimiter,dialect=csv.excel)
    for linea in archivo:
        crear_conexión(model_vacio,linea)
def cargar_datos_country(model_vacio:dict,nombre:str)->None:
    archivo= csv.DictReader(open(cf.data_dir+nombre+".csv",encoding="utf-8-sig",newline=''),delimiter=csv.excel.delimiter,dialect=csv.excel)
    for linea in archivo:
        add_to_map_cntry(model_vacio,linea)
    

def cargar_datos_ldp(model_vacio:dict,nombre:str)->None:
    archivo= csv.DictReader(open(cf.data_dir+nombre+".csv",encoding="utf-8-sig",newline=''),delimiter=csv.excel.delimiter,dialect=csv.excel)
    for linea in archivo:
        add_to_map(model_vacio,linea)

def pais_ldp(catalog:dict,ldp:str)->str:
    pais1=me.getValue(mp.get(catalog["ldp"],ldp))["name"].split(",")[1].lstrip()
    return pais1

def existe_lp(catalog:dict,vertex:str)->None:
    #TODO Aquí se debe crear un algoritmo que sea capaz de agregar arcos en vertices con un mismo lp
    # , se debe agregar un arco que vaya al siguiente vértice y un arco que se devuelva   
    #Puede que la solución sea una función recursiva.
    vertices= gr.vertices(catalog["graph"])
    for i in range(1,lt.size(vertices)+1):
        elemento2=lt.getElement(vertices,i)
        elemento=lt.getElement(vertices,i).split("-")[0]
        if(vertex.split("-")[0] ==elemento and vertex!=elemento2):
            gr.addEdge(catalog["graph"],vertex,elemento2,0.1)
            add_info_cable(catalog,"","<{}>-<{}>".format(vertex,elemento2))

def crear_cable(cable_name:str,cable_id:str,cable_length:str="0.1 km",cable_rfs:str="",owners:str="",capacityTBPS:str="")->dict:
    dicc={"cable_name":cable_name,"cable_id":cable_id,"cable_length":cable_length,"cable_rfs":cable_rfs,"owners":owners,"capacityTBPS":capacityTBPS}
    return dicc

def add_info_cable(catalog:dict,cable_name:str,cable_id:str,cable_length:str,cable_rfs:str,owners:str,capacityTBPS:str)->None:
    cables=catalog["cables"]
    exist=mp.contains(cables,cable_id)
    if(not exist):
        cable= crear_cable(cable_name,cable_id,cable_length,cable_rfs,owners,capacityTBPS)
        mp.put(cables,cable_id,cable)


def crear_conexión(catalog:dict,linea:OrderedDict)->None:
    vertexA="<{}>-<{}>".format(linea["origin"],linea["cable_id"])
    vertexB="<{}>-<{}>".format(linea["destination"],linea["cable_id"])
    latA=float(me.getValue(mp.get(catalog["ldp"],linea["origin"]))["latitude"])
    lonA=float(me.getValue(mp.get(catalog["ldp"],linea["origin"]))["longitude"])
    lonB=float(me.getValue(mp.get(catalog["ldp"],linea["destination"]))["longitude"])
    latB=float(me.getValue(mp.get(catalog["ldp"],linea["destination"]))["latitude"])
    peso=haversine(lonA,latA,lonB,latB)
    gr.insertVertex(catalog["graph"],vertexA)
    existe_lp(catalog,vertexA)
    gr.insertVertex(catalog["graph"],vertexB)
    existe_lp(catalog,vertexA)
    gr.addEdge(catalog["graph"],vertexA,vertexB,peso)
    add_info_cable(catalog,catalog["cable_name"],catalog["cable_id"],catalog["cable_length"],catalog["cable_rfs"],catalog["owners"],catalog["capacityTBPS"])


def validar_pais()->bool:
    pass
def add_to_map(model_vacio:dict,dato:OrderedDict)->None:
    mapa=model_vacio["ldp"]
    llave=dato["landing_point_id"]
    valor=dato
    mp.put(mapa,llave,valor)

def add_to_map_cntry(model_vacio:dict,dato:OrderedDict)->None:
    mapa=model_vacio["cntry"]
    llave=dato["CountryName"]
    valor=dato
    mp.put(mapa,llave,valor)


def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r
# Funciones de consulta

# Funciones utilizadas para comparar elementos dentro de una lista
def Compare_Keys(key1:str, key2:dict)->None:
    key2 = me.getKey(key2)
    if key1 == key2:
        return 0
    elif key1 > key2:
        return 1
    else:
        return -1
# Funciones de ordenamiento

