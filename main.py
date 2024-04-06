from lista import ListaDoblementeEnlazada
import xml.etree.ElementTree as ET
from nodos import Nodo
from nodos import Estructura
from nodos import Objetivos
from maquetas import Maqueta
import os
from os import startfile, system
from collections import deque

lst_maquetas = ListaDoblementeEnlazada()
lst_maquetas_resueltas = ListaDoblementeEnlazada()


def leer_archivo(archivo_seleccionado):

    if archivo_seleccionado:
        try:
            with open(archivo_seleccionado) as archivo_xml:
                datos_xml = ET.fromstring(archivo_xml.read())

                for maqueta_xml in datos_xml.findall('.//maqueta'):
                    nombre = maqueta_xml.find('nombre').text.strip()
                    filas = int(maqueta_xml.find('filas').text.strip())
                    columnas = int(maqueta_xml.find('columnas').text.strip())
                    etiqueta_entrada = maqueta_xml.find('entrada')
                    fila_in = int(etiqueta_entrada.find('fila').text.strip())
                    columna_in = int(etiqueta_entrada.find('columna').text.strip())
                    # objetivos = [(objetivo.find('nombre').text.strip(), int(objetivo.find('fila').text.strip()), int(objetivo.find('columna').text.strip())) for objetivo in maqueta_xml.findall('.//objetivo')]

                    lst_objetivos = ListaDoblementeEnlazada()
                    for objetivo in maqueta_xml.findall('.//objetivos/objetivo'):
                        nombre_objetivo = objetivo.find('nombre').text.strip()
                        fila_objetivo = int(objetivo.find('fila').text.strip())
                        columna_objetivo = int(objetivo.find('columna').text.strip())
                        nuevo_objetivo = Objetivos(nombre_objetivo, fila_objetivo, columna_objetivo)
                        nuevo_nodo_objetivo = Nodo(nuevo_objetivo)
                        lst_objetivos.agregar_nodo(nuevo_nodo_objetivo)
                                           

                    estructura = maqueta_xml.find('estructura').text.strip().replace('\n', '').replace(' ', '')

                    lst_estructuras = ListaDoblementeEnlazada()
                    for color in estructura:
                        nueva_estructura = Estructura(color)
                        nuevo_nodo_estructura = Nodo(nueva_estructura)
                        lst_estructuras.agregar_nodo(nuevo_nodo_estructura)

                    maqueta = Maqueta(nombre, filas, columnas, fila_in, columna_in, lst_objetivos, lst_estructuras)
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

def crear_grafico(nodo_encontrado):

    if os.path.exists("maqueta.dot"):
        os.remove("maqueta.dot")
    if os.path.exists("maqueta.pdf"):
        os.remove("maqueta.pdf")


    nombre = nodo_encontrado.objeto.nombre
    filas = nodo_encontrado.objeto.filas
    columnas = nodo_encontrado.objeto.columnas
    fila_entrada = nodo_encontrado.objeto.fila_in
    columna_entrada = nodo_encontrado.objeto.col_in
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
        textoDOT += "        <tr>"
        for j in range(columnas):
            objetivo_en_posicion = False
            now = objetivos.cabeza
            while now:
                if now.objeto.fila_ob == i and now.objeto.col_ob == j:
                    objetivo_en_posicion = True
                    textoDOT += f"<td>{now.objeto.nombre_ob}</td>"
                    break
                now = now.siguiente
            if not objetivo_en_posicion:
                if i == fila_entrada and j == columna_entrada:
                    textoDOT += f"<td bgcolor=\"green\"></td>"
                elif actual.objeto.color == "-":
                    textoDOT += f"<td bgcolor=\"white\"></td>"
                elif actual.objeto.color == "*":
                    textoDOT += f"<td bgcolor=\"black\"></td>"
                elif actual.objeto.color == "#":
                    textoDOT += f"<td bgcolor=\"blue\"></td>"
            actual = actual.siguiente
        textoDOT += "        </tr>\n"

    textoDOT += "</TABLE>>\n shape=none\n ];"
    textoDOT += "}\n"

    with open("maqueta.dot", "w") as dot_file:
        dot_file.write(textoDOT)

    system('dot -Tpdf maqueta.dot -o maqueta.pdf')
    startfile("maqueta.pdf")

def resolver_maqueta(maqueta):

    nombre = maqueta.objeto.nombre
    estructura = maqueta.objeto.estructura
    objetivos = maqueta.objeto.objetivos
    filas = maqueta.objeto.filas
    columnas = maqueta.objeto.columnas
    fila_entrada = maqueta.objeto.fila_in
    columna_entrada = maqueta.objeto.col_in

    lista_objetivos = []

    now = objetivos.cabeza
    while now:
        nombre_objetivo = now.objeto.nombre_ob
        lista_objetivos.append(nombre_objetivo)
        now = now.siguiente
    
    matriz = [['-' for _ in range(columnas)] for _ in range(filas)]

    nodo_actual = estructura.cabeza

    for i in range(filas):
        for j in range(columnas):
            objetivo_insertado = False
            now = objetivos.cabeza
            while now:
                if now.objeto.fila_ob == i and now.objeto.col_ob == j:
                    objetivo_insertado = True
                    matriz[i][j] = now.objeto.nombre_ob
                    break
                now = now.siguiente

            if not objetivo_insertado:
                matriz[i][j] = nodo_actual.objeto.color
                nodo_actual = nodo_actual.siguiente
            else: 
                nodo_actual = nodo_actual.siguiente
        
    def movimiento_valido(fila, columna):
        return 0 <= fila < filas and 0 <= columna < columnas and matriz[fila][columna] != "*"

    def bfs(fila, columna):
        visitados = set()
        queue = deque([(fila, columna, [])])

        while queue:
            fila_actual, columna_actual, camino_actual = queue.popleft()
            if matriz[fila_actual][columna_actual] in lista_objetivos:
                yield camino_actual

            for df, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nueva_fila, nueva_columna = fila_actual + df, columna_actual + dc

                if movimiento_valido(nueva_fila, nueva_columna) and (nueva_fila, nueva_columna) not in visitados:
                    nuevo_camino = camino_actual + [(nueva_fila, nueva_columna)]
                    queue.append((nueva_fila, nueva_columna, nuevo_camino))
                    visitados.add((nueva_fila, nueva_columna))

    caminos = list(bfs(fila_entrada, columna_entrada))

    if caminos:

        mejor_camino = min(caminos, key=len)
        for fila, columna in mejor_camino:
            matriz[fila][columna] = "#"

    else:
        print("No se encontraron caminos para recolectar los objetivos.")

    estructura_resuelta = ListaDoblementeEnlazada()
    for i in range (filas):
        for j in range(columnas):
            
            nueva_estructura = Estructura(matriz[i][j])
            nuevo_nodo_estructura = Nodo(nueva_estructura)
            estructura_resuelta.agregar_nodo(nuevo_nodo_estructura)

    maqueta_resuelta = Maqueta(nombre, filas, columnas, fila_entrada, columna_entrada, objetivos, estructura_resuelta)
    nuevo_nodo = Nodo(maqueta_resuelta)
    lst_maquetas_resueltas.agregar_nodo(nuevo_nodo)
    maqueta_a_graficar = lst_maquetas_resueltas.buscar_nodo(nombre)
    crear_grafico(maqueta_a_graficar)

    input('\n Presione enter para continuar')

def ayuda():
    print('\n--------------- Ayuda ---------------')
    print('\n  Nombre: José Rolando Yaquian Paz')
    print('  Carnet: 202201185')
    print('  Carrera: Ingenieria en ciencias y sistemas')
    print('  Link documentacion: https://github.com/josePaz156/IPC2_Proyecto2_202201185')
    input('\n  Presione enter para continuar')

def imprimir_menu():
    print('\n--------------- Bienevanido al programa ---------------')
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

    opcion = input('\n  Seleccione una pocion: ')

    if opcion == '1':
        limpiar_consola()
        archivo_selc = input("ingrese el nombre del archivo: ")
        leer_archivo(archivo_selc)
        input('\n Presione enter para continuar')

    elif opcion == '2':
        while True:
            limpiar_consola()
            print('\n--------------- Gestion de Maquetas ---------------')
            print('\n  1. Ver listado de maquetas')
            print('  2. Ver configuracion de maquetas')
            print('  3. Regresar al menu principal')
            
            opcion2 = input('\n Seleccione una opcion: ')

            if opcion2 == '1':

                limpiar_consola()
                print('--------------- Listado de Maquetas ---------------')
                actual = lst_maquetas.cabeza

                if actual is None:
                    print('\n No hay maquetas.\n')
                    input('Presione enter para continuar')
                else:
                    while actual:
                        print(f"  - {actual.objeto.nombre}")
                        actual = actual.siguiente
                    input('Presione enter para continuar')

            elif opcion2 == '2':

                limpiar_consola()
                actual = lst_maquetas.cabeza

                if actual is None:
                    print('\n No hay maquetas.\n')
                    input('Presione enter para continuar')

                else:
                    maqueta_seleccionada = input('Ingrese el nombre de la maqueta: ')
                    encontrado = lst_maquetas.buscar_nodo(maqueta_seleccionada)
                    crear_grafico(encontrado)
                    input('Presione enter para continuar')

            elif opcion2 == '3': 
                break
            else: 
                print('\n Opcion no valida')
                input('\n Presione enter para continuar')
    
    elif opcion == '3':
        limpiar_consola()
        actual = lst_maquetas.cabeza

        if actual is None:
            print('\n No hay maquetas.\n')
            input('Presione enter para continuar')
        else:
            maqueta_seleccionada = input('Ingrese el nombre de la maqueta: ')
            maqueta_encontrada = lst_maquetas.buscar_nodo(maqueta_seleccionada)
            resolver_maqueta(maqueta_encontrada)

    elif opcion == '4':
        limpiar_consola()
        ayuda()

    elif opcion == '5':
        limpiar_consola()
        print('\n Gracias por usar nuestro programa vuelva pronto \n')
        break

    else: 
        print('Opcion no valida, seleccione una opcion valida')
        input('Presione enter para continuar')

