from lista import ListaDoblementeEnlazada
import xml.etree.ElementTree as ET
from nodos import Nodo
from maquetas import Maqueta
import tkinter as tk
from tkinter import filedialog

lst_maquetas = ListaDoblementeEnlazada()

def abrir_archivo():
    root = tk.Tk()
    root.withdraw()

    while True:  # Bucle externo para solicitar un archivo válido
            archivo = filedialog.askopenfilename(title="Seleccionar archivo")

            if archivo:  # Verificar si se seleccionó un archivo
                leer_archivo(archivo)
                break  # Salir del bucle externo si se seleccionó un archivo válido
            else:
                print("No se seleccionó ningún archivo. Por favor, seleccione un archivo válido.")

def leer_archivo(archivo_seleccionado):
    archivo_xml = None

    while True:
        try:
            archivo_xml = open(archivo_seleccionado)
            break
        except FileNotFoundError as file_err:
            print(f"Error: El archivo {archivo_seleccionado} no se encuentra.")
            archivo_xml = None
    
    try:
        if archivo_xml.readable():
            datos_xml = ET.fromstring(archivo_xml.read())

            for maqueta_xml in datos_xml.findall('.//maqueta'):
                nombre = maqueta_xml.find('nombre').text.strip()
                filas = int(maqueta_xml.find('filas').text.strip())
                columnas = int(maqueta_xml.find('columnas').text.strip())
                entrada = (int(maqueta_xml.find('entrada/fila').text.strip()), int(maqueta_xml.find('entrada/columna').text.strip()))
                objetivos = [(objetivo.find('nombre').text.strip(), int(objetivo.find('fila').text.strip()), int(objetivo.find('columna').text.strip())) for objetivo in maqueta_xml.findall('.//objetivo')]
                estructura = maqueta_xml.find('estructura').text.strip()

                maqueta = Maqueta(nombre, filas, columnas, entrada, objetivos, estructura)
                new_nodo = Nodo(maqueta)
                lst_maquetas.agregar_nodo(new_nodo)
            
            lst_maquetas.ordenar_alfabeticamente()

            return lst_maquetas

    except Exception as err:
        print("Error", err)
    finally:
        archivo_xml.close()

abrir_archivo()
lst_maquetas.imprimir_lista()
actual = lst_maquetas.cabeza
while actual:
    print(f"  - {actual.objeto.nombre}")
    actual = actual.siguiente
