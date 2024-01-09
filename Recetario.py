# %% Importaciones y librerías
from pathlib import Path 
from IPython.core.display import clear_output # Limpia la consola

# %% Funciones
def carpetas_dict(ruta:Path)->dict:
    '''
    Retorna un diccionario que contiene las categorías enumeradas.
    '''

    # listar las categorías del recetario
    lista_carpetas = [fichero.name for fichero in ruta.iterdir() if fichero.is_dir()] 

    # Diccionario de carpetas   
    return dict(enumerate(lista_carpetas))

def contar_archivos(ruta:Path,*args:str)->int:
    '''
    Retorna un int equivalente al  numero de archivos en un directorio o grupo de directorios.
    '''
    # Inicializar contador
    total_archivos = 0
    
    # Recorrer las carpetas y contar los archivos
    for carpeta in args:
        total_archivos += len(list(ruta.joinpath(carpeta).iterdir()))
    
    # Retornar numero total de archivos
    return total_archivos

def recetas_dict(carpeta:str)->dict:
    '''
    Retorna un diccionario que contiene las recetas enumeradas.
    '''

    # Diccionario de recetas enumeradas
    return dict(enumerate([receta.name for receta in Path(ruta,carpeta).iterdir()]))

def seleccionar_capeta(carpetas:dict)->str:
    '''
    Retorna el nombre de la carpeta selecionada como un str.
    '''
    
    # Inicializar la variable carpeta_index
    carpeta_index = 'x'

    # Pedir la entrada hasta que sea correcta
    while carpeta_index not in carpetas.keys():
        carpeta_index = int(input(f'Elija una carpeta:\n{carpetas}\n'))

    # Nombre de la carpeta elejida
    return carpetas[carpeta_index]

def seleccionar_receta(carpeta:str)->str:
    '''
    Retorna el nombre de la receta elegida
    '''
    
    # listar las categorías del directorio
    recetas = recetas_dict(carpeta)

    # Inicializar la variable receta_index
    receta_index = 'x'

    # Pedir la entrada hasta que sea correcta
    while (receta_index not in recetas.keys()):
        receta_index = int(input(f'Elija una receta:\n{recetas}\n'))

    # Nombre de la receta elejida
    return recetas[receta_index]

def leer_receta(ruta:Path,carpeta:str,receta:str)->None:
    '''
    Imprime en pantalla el texto de la receta pedida.
    '''

    # Abrir el archivo indicado y leer su contenido
    with open(Path(ruta,carpeta,receta)) as archivo:
        return f'{archivo.read()}\n{"-"*60}\n'
    
def volver_al_inicio()->bool:
    '''
    Retorna True luego de que el usuario presiona cualquier tecla.
    '''

    # Convertir la entrada en un Booleano, si es cero, la combierte e uno.
    return bool(input('Para volver al inicio presione cualquier tecla\n')+'1')

#    %% main

# %% Declaración de variables

# Crear el Path del fichero recetas
ruta = Path.cwd()/'Recetas'

# Variable Limpiar 
limpiar = False

# Imprimir el mensaje de bienvenida
print(f'¡Bienvanido al recetario!\n')

# Correr el script hasta que el usiario pida lo contrario
while True:

    # Actualizar/Inicializar diccionario de carpetas
    carpetas = carpetas_dict(ruta)

    # Calcular numero de archivos 
    numero_archivos = contar_archivos(ruta,*carpetas.values()) # Con el asterisco(*) entiende que carpetas.values() es una lista

    # Limpiar consola luego de la primera interación
    if limpiar: 
        clear_output()

    # Imprimir el numero de archivos y la direccion del directorio.
    print(f'''Actualmente tus recetas se encuentran en:{ruta}\n
El numero total de archivos es de {numero_archivos}\n''')

    # Variable opción elegida
    opcion_elejida = 'x'

    # Leer la entrada del usuario (opción elejida)
    while opcion_elejida not in '123456':
        opcion_elejida = input('''Elija una de las siguientes opciónes:
        [1] - Leer receta
        [2] - Crear receta
        [3] - Crear categoría
        [4] - Eliminar receta
        [5] - Eliminar categoría
        [6] - Finalizar Programa\n''')    

    # Opción 1: Leer receta
    if opcion_elejida == '1':
        
        # Seleccionar la carpeta que se desea abrir
        carpeta = seleccionar_capeta(carpetas)

        # Verificar que la carpeta no esté vacia.
        if contar_archivos(ruta,carpeta) >= 1:

            # Seleccionar receta
            receta = seleccionar_receta(carpeta)

            # Imprimir receta en pantalla
            print(leer_receta(ruta,carpeta,receta))
        
        # Si la carpeta está vacía
        else:
            print('No hay recetas en esta categoría.')

        # Volver al inicio
        limpiar = volver_al_inicio()

    # Opción 2: Crear receta
    elif opcion_elejida == '2':

        # Seleccionar la carpeta que se desea abrir
        carpeta = seleccionar_capeta(carpetas)

        # Leer nombre de la receta nueva
        nombre_receta_nueva = input('Ingrese el nombre de la nueva receta\n') +'.txt'

        # Crear archivo nuevo
        nueva_receta = Path(ruta,carpeta,nombre_receta_nueva)

        # Contenido de la reseta
        texto_receta = input('Ingrese el contenido de la nueva receta:\n')

        # Crear el nuevo archivo y escribir en el
        with open(nueva_receta, 'w') as texto:
            texto.write(texto_receta)

        # Imprimir en pantalla
        print(f'Nuevo archivo creado: {nombre_receta_nueva}\n{"-"*60}\n')

        # Volver al inicio
        limpiar = volver_al_inicio()
        
    # Opción 3: Crear categoría
    elif opcion_elejida == '3':

        #Leer nombre de la categoría nueva
        nombre_carpeta_nueva = input('Ingrese en nombre de la nueva carpeta:\n').capitalize()
        
        #Crear nueva carpeta
        Path(ruta,nombre_carpeta_nueva).mkdir()

        # Imprimir en pantalla
        print(f'Nueva categoría creada: {nombre_carpeta_nueva}\n{"-"*60}\n')

        # Volver al inicio
        limpiar = volver_al_inicio()

    # Opción 4: Eliminar receta
    elif opcion_elejida == '4':
        
        # Seleccionar la carpeta que se desea abrir
        carpeta = seleccionar_capeta(carpetas)

        # Verificar que la carpeta no esté vacia.
        if contar_archivos(ruta,carpeta) >= 1:

            # Seleccionar receta
            receta = seleccionar_receta(carpeta)

            # Eliminar Receta
            Path(ruta,carpeta,receta).unlink()

            # Imprimir en pantalla
            print(f'Archivo eliminado: {receta}\n{"-"*60}\n')
        
        # Si la carpeta está vacía
        else:
            print('No hay recetas en esta categoría.')

        # Volver al inicio
        limpiar = volver_al_inicio()      

    # Opción 5: Eliminar categoría
    elif opcion_elejida == '5':

        # Selecionar la carpeta que se ese eliminar
        carpeta = seleccionar_capeta(carpetas)

        # Eliminar carpeta
        Path(ruta,carpeta).rmdir()

        # Imprimir en pantalla
        print(f'Categoría eliminada: {carpeta}\n{"-"*60}\n')

        # Volver al inicio
        limpiar = volver_al_inicio()

    # Opción 6: Finalizar programa
    elif opcion_elejida == '6':
        print(f'{"-"*60}\nFin del programa')
        break
    
    # Resetear la variable opcion_elejida
    opcion_elejida = 'x'