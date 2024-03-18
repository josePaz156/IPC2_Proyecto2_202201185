import xml.etree.ElementTree as ET

xml_file = None

while True:
    try:
        cargar_archivo = input("Ingrese la ruta del archivo: " )
        xml_file = open(cargar_archivo)
        break
    except FileNotFoundError as file_err:
        print(f"Error: El archivo {cargar_archivo} no se encuentra.")
        # Asignar un valor por defecto (puede ser None u otro valor que tenga sentido para tu aplicación)
        xml_file = None

try:
    if xml_file.readable():
        xml_data = ET.fromstring(xml_file.read())

    else:
        print(False)
        print("No se encontro el archivo seleccionado intente nuevamente: ")

except Exception as err:
    print("Error", err)
finally:
    xml_file.close()