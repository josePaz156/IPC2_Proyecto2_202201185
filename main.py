from lista import ListaDoblementeEnlazada
import xml.etree.ElementTree as ET
from nodos import Nodo
from nodos import Estructura
from recorrido import Recorrido
from nodos import Objetivos
from maquetas import Maqueta
import os
from os import startfile, system

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

    piso [\n label=<<TABLE border = \"1\" cellspacing=\"0\" cellpadding=\"10\">
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
            actual = actual.siguiente
        textoDOT += "        </tr>\n"

    textoDOT += "</TABLE>>\n shape=none\n ];"
    textoDOT += "}\n"

    with open("maqueta.dot", "w") as dot_file:
        dot_file.write(textoDOT)

    system('dot -Tpdf maqueta.dot -o maqueta.pdf')
    startfile("maqueta.pdf")

def resolver_maqueta(estructura, fila_inicial, columna_inicial, objetivos):
    # Crear un grafo de caminos
    caminos = {}
    for i in range(estructura.filas):
        for j in range(estructura.columnas):
            if (i, j) not in caminos:
                caminos[(i, j)] = []
            if i > 0:
                caminos[(i, j)].append((i - 1, j))
            if i < estructura.filas - 1:
                caminos[(i, j)].append((i + 1, j))
            if j > 0:
                caminos[(i, j)].append((i, j - 1))
            if j < estructura.columnas - 1:
                caminos[(i, j)].append((i, j + 1))

    # Función de backtracking para encontrar el recorrido
    def encontrar_recorrido(fila, col, recorrido, objetivos_recogidos):
        if (fila, col) in objetivos:
            recorrido.recoger_objetivo(objetivos[(fila, col)])
        if recorrido.objetivos_recogidos.issuperset(objetivos.values()):
            return recorrido

        siguientes_pasos = caminos[(fila, col)]
        for paso in siguientes_pasos:
            if estructura.estructura[paso[0]][paso[1]] != "*":
                recorrido_nuevo = Recorrido()
                recorrido_nuevo.agregar_al_camino((fila, col))
                recorrido_nuevo.camino.extend(recorrido.camino)
                recorrido_nuevo.objetivos_recogidos = set(recorrido.objetivos_recogidos)
                recorrido_nuevo.objetivos_recogidos.update(recorrido.objetivos_recogidos)
                encontrado = encontrar_recorrido(paso[0], paso[1], recorrido_nuevo, objetivos)
                if encontrado:
                    return encontrado

        # Si no se encuentra un recorrido que recolecte todos los objetivos,
        # se devuelve el último recorrido encontrado
        return recorrido

    # Llamar a la función de backtracking
    recorrido = encontrar_recorrido(fila_inicial, columna_inicial, Recorrido(), objetivos)

    # Resaltar el recorrido en el mapa
    for paso in recorrido.camino:
        estructura.estructura[paso[0]][paso[1]] = ":"

    return recorrido

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
    
    elif opcion == '3':
        limpiar_consola()
        maqueta_seleccionada = input('Seleccione el nombre de la maqueta: ')
        maqueta_encontrada = lst_maquetas.buscar_nodo(maqueta_seleccionada)
        resolver_maqueta(maqueta_encontrada)

    
    elif opcion == '5':
        print('Gracias por usar nuestro programa vuelva pronto')
        break

    else: 
        print('Opcion no valida, seleccione una opcion valida')
        input('Presione enter para continuar')

