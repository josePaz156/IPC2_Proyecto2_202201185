from lista import ListaDoblementeEnlazada
import xml.etree.ElementTree as ET
from nodos import Nodo
from nodos import Estructura
from maquetas import Maqueta
import os
from os import startfile, system
import graphviz

lst_maquetas = ListaDoblementeEnlazada()


def leer_archivo(archivo_seleccionado):

    if archivo_seleccionado:
        try:
            with open(archivo_seleccionado) as archivo_xml:
                datos_xml = ET.fromstring(archivo_xml.read())

                for maqueta_xml in datos_xml.findall('.//maqueta'):
                    nombre = maqueta_xml.find('nombre').text.strip()
                    filas = int(maqueta_xml.find('filas').text.strip())
                    columnas = int(maqueta_xml.find('columnas').text.strip())
                    entrada = (int(maqueta_xml.find('entrada/fila').text.strip()), int(maqueta_xml.find('entrada/columna').text.strip()))
                    objetivos = [(objetivo.find('nombre').text.strip(), int(objetivo.find('fila').text.strip()), int(objetivo.find('columna').text.strip())) for objetivo in maqueta_xml.findall('.//objetivo')]
                    estructura = maqueta_xml.find('estructura').text.strip().replace('\n', '').replace(' ', '')

                    lst_estructuras = ListaDoblementeEnlazada()
                    for color in estructura:
                        nueva_estructura = Estructura(color)
                        nuevo_nodo_estructura = Nodo(nueva_estructura)
                        lst_estructuras.agregar_nodo(nuevo_nodo_estructura)

                    maqueta = Maqueta(nombre, filas, columnas, entrada, objetivos, lst_estructuras)
                    new_nodo = Nodo(maqueta)
                    lst_maquetas.agregar_nodo(new_nodo)
                
                print('Archivo cargado correctamente')
                
        except FileNotFoundError as file_err:
            print(f"Error: El archivo {archivo_seleccionado} no se puede leer.")
        except Exception as err:
            print("Error", err)
    
        lst_maquetas.ordenar_alfabeticamente()
        return lst_maquetas
    else:
        print("No se ha seleccionado ningún archivo.")

def crear_grafico():

    if os.path.exists("maqueta.dot"):
        os.remove("maqueta.dot")
    if os.path.exists("maqueta.pdf"):
        os.remove("maqueta.pdf")

    # Buscar maqueta seleccionada
    maqueta_seleccionada = input('Ingrese el nombre de la maqueta: ')

    nodo_encontrado = lst_maquetas.buscar_nodo(maqueta_seleccionada)

    #Obtener informacion del nodo encontado

    nombre = nodo_encontrado.objeto.nombre
    filas = nodo_encontrado.objeto.filas
    columnas = nodo_encontrado.objeto.columnas
    entrada = nodo_encontrado.objeto.entrada
    objetivos = nodo_encontrado.objeto.objetivos
    estructura = nodo_encontrado.objeto.estructura

    if filas == 0 or columnas == 0:
            print('DIMENSIONES INVÁLIDAS:')
            return

    textoDOT = ''' digraph G { \n
    node [shape=plaintext]; \n
    edge [style=invis]; \n

    label = \"Nombre maqueta =  ''' + nombre +  '''\"
    \n

    piso [\n label=<<TABLE border = \"0\" cellspacing=\"0\" cellpadding=\"10\">
    '''

    actual = estructura.cabeza

    for i in range(filas):
        textoDOT += "         <tr>"
        for j in range(columnas):
            if actual.objeto.color == "-":
                textoDOT += f"<td bgcolor=\"white\"></td>"
            elif actual.objeto.color == "*":
                textoDOT += f"<td bgcolor=\"black\"></td>"
            actual = actual.siguiente
        textoDOT += "         </tr>\n"

    textoDOT += "</TABLE>>\n shape=none\n ];"
    textoDOT += "}\n"

    with open("maqueta.dot", "w") as dot_file:
        dot_file.write(textoDOT)

    system('dot -Tpdf maqueta.dot -o maqueta.pdf')
    startfile("maqueta.pdf")
    

def imprimir_menu():
    print('\n--------------- Bienevanido a nuestro programa ---------------')
    print('\n  1. Cargar Archivo')
    print('  2. Gestionar Maquetas')
    print('  3. Resolucion de maquetas')
    print('  4. Ayuda')
    print('  5. Salir')

def limpiar_consola():
    sistema_operativo = os.name
    if sistema_operativo == 'nt':
        os.system('cls')
    else:
        os.system('clear')
    
while True:
    limpiar_consola()
    imprimir_menu()

    opcion = input('Seleccione una pocion: ')

    if opcion == '1':
        archivo_selc = input("ingrese el nombre del archivo: ")
        leer_archivo(archivo_selc)
        input('Presione enter para continuar')

    elif opcion == '2':
        while True:
            limpiar_consola()
            print('\n--------------- Gestion de Maquetas ---------------')
            print('\n  1. Ver listado de maquetas')
            print('  2. Ver configuracion de maquetas')
            print('  3. Regresar al menu principal')
            
            opcion2 = input('Seleccione una opcion: ')

            if opcion2 == '1':

                limpiar_consola()
                print('--------------- Listado de Maquetas ---------------')
                actual = lst_maquetas.cabeza

                if actual is None:
                    print('No hay maquetas.\n')
                    input('Presione enter para continuar')
                else:
                    while actual:
                        print(f"  - {actual.objeto.nombre}")
                        actual = actual.siguiente
                    input('Presione enter para continuar')

            elif opcion2 == '2':

                limpiar_consola()
                crear_grafico()
                input('Presione enter para continuar')
            elif opcion2 == '3': 
                break
            else: 
                print('Opcion no valida')
                input('Presione enter para continuar')
    
    elif opcion == '5':
        print('Gracias por usar nuestro programa vuelva pronto')
        break

    else: 
        print('Opcion no valida, seleccione una opcion valida')
        input('Presione enter para continuar')

