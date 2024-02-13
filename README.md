# seismic-hazard-simulator
Seismic Hazard research


# Pasos para la ejecución del proyecto

## 1. Instalación de Python

Primero, vamos a verificar si Python se encuentra instalado en el sistema.

1. **Abrir el menú de inicio:** Haz clic en el botón de inicio en la esquina inferior izquierda de la pantalla (generalmente tiene el ícono de Windows).

2. **Buscar el símbolo del sistema:** Escribe "cmd" en el cuadro de búsqueda y presiona Enter. Esto abrirá el símbolo del sistema, que es una herramienta para ejecutar comandos en Windows.

3. **Verificar Python:** En la ventana del símbolo del sistema, escribe "python --version" (sin comillas) y presiona Enter. Esto solicitará al sistema que muestre la versión de Python instalada, si está presente.
    - Si Python está instalado, verás algo como "Python X.Y.Z", donde X.Y.Z es la versión instalada.
    - Si Python no está instalado, verás un mensaje de error indicando que el comando no se reconoce.

4. **Descargar e instalar Python (si es necesario):** Si Python no está instalado y el usuario desea instalarlo, pueden descargarlo desde el sitio web oficial de Python (https://www.python.org/downloads/) y seguir las instrucciones de instalación. 

## 2. Creación de un entorno virtual ()

Ahora crearemos un entorno virtual, que nos permitirá instalar paquetes de Python para cada proyecto en específico, sin afectar al sistema global.

1. **Abrir el símbolo del sistema:** Igual que antes, abre el menú de inicio y busca "cmd" para abrir el símbolo del sistema.

2. **Navegar a la ubicación del proyecto:** Nos vamos a dirigir a la ubicación del proyecto que queremos ejecutar. Utilizaremos el comando cd (cambiar directorio) seguido de la ruta de la carpeta del proyecto. Por ejemplo:

    - cd ruta\de\la\carpeta\del\proyecto

3. **Instalar virtualenv (si no está instalado):** Es posible que necesites instalar `virtualenv`, una herramienta que te permite crear entornos virtuales. Puedes instalarlo utilizando el siguiente comando:

    - pip install virtualenv

4. **Crear un nuevo entorno virtual:** Encóntrandonos en la ubicación del proyecto, ejecutaremos el siguiente comando para crear un nuevo entorno virtual:

    - virtualenv nombre_del_entorno

    Reemplaza `nombre_del_entorno` con el nombre que desees para tu entorno virtual. Por lo general le daremos el nombre de ".env" al entorno (poner un punto al inicio del nombre hará que la carpeta del entorno virtual esté oculta, y así no obstruir con los archivos del proyecto).

5. **Activar el entorno virtual:** Después de crear el entorno virtual, necesitas activarlo. Esto asegura que cuando instales paquetes o ejecutes scripts, se hagan dentro del entorno virtual y no afecten al sistema global. Para activar el entorno virtual, ejecuta el siguiente comando:

    - nombre_del_entorno\Scripts\activate

    Nota: Reemplaza "nombre_del_entorno" con el nombre que hayas elegido para tu entorno virtual.

6. **Desactivar el entorno virtual:** Cuando hayas terminado de trabajar en tu proyecto y quieras salir del entorno virtual, simplemente ejecuta el siguiente comando:

    - deactivate

## 3. Instalación de paquetes de Python

Instalaremos los paquetes necesarios para la ejecución del script en nuestro entorno virtual.

1. **Abrir el símbolo del sistema:** Si aún no lo tienes abierto, abre el símbolo del sistema siguiendo los pasos que mencionamos anteriormente.

2. **Navegar a la ubicación del proyecto:** Usamos el comando cd seguido de la ruta de la carpeta del proyecto. 
    
    - cd ruta\de\la\carpeta\del\proyecto

3. **Activar el entorno virtual:** Para activar el entorno virtual, ejecuta el siguiente comando:

    - nombre_del_entorno\Scripts\activate

4. **Instalación de paquetes:** Copiamos el archivo requirements.txt en la ubicación del proyecto. Ejecutamos el siguiente comando en el símbolo del sistema
    
    - pip install -r requirements.txt

## 4. Ejecución del Script

1. **Archivo SeismicHazard.ipynb:** Copiamos el archivo SeismicHazard.ipynb en la ubicación del proyecto. Abrimos el archivo con el editor Visual Studio Code. 

2. **Selección del kernel:** Una vez abierto, en la esquina superior derecha habrá una opción "Seleccionar el kernel" y seleccionamos a nuestro entorno virtual.

3. **Ejecución del archivo:** A la izquierda de la opción "Selección el kernel", encontraremos una opción "Ejecutar todo". Hacemos click a esa opción y el script se ejecutará.

4. **Salidas del proyecto:** Luego de que termine la ejecución del script, se generará la carpeta llamada "output", donde encontrará los datos, las gráficas, las tablas, etc.