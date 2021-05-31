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
 """

import config as cf
import model as md
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros
def model_vacio():
    return md.new_model()
# Funciones para la carga de datos
def cargar_datos(model_vacio:dict,connections:str="connections",countries:str="countries",landing_points:str="landing_points")->None:
    md.cargar_datos_country(model_vacio,countries)
    md.cargar_datos_ldp(model_vacio,landing_points)
    md.cargar_datos_connections(model_vacio,connections)

# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo
