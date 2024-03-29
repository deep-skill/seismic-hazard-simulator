# seismic-hazard-simulator
Seismic Hazard research


# Instalación de Python y entorno virtual

## 1. Instalación de Python

Primero, vamos a verificar si Python se encuentra instalado en el sistema.

1. **Abrir el menú de inicio:** Haz clic en el botón de inicio en la esquina inferior izquierda de la pantalla (generalmente tiene el ícono de Windows).

2. **Buscar el símbolo del sistema:** Escribe "cmd" en el cuadro de búsqueda y presiona Enter. Esto abrirá el símbolo del sistema, que es una herramienta para ejecutar comandos en Windows.

3. **Verificar Python:** En la ventana del símbolo del sistema, escribe "python --version" (sin comillas) y presiona Enter. Esto solicitará al sistema que muestre la versión de Python instalada, si está presente.
    - Si Python está instalado, verás algo como "Python X.Y.Z", donde X.Y.Z es la versión instalada.
    - Si Python no está instalado, verás un mensaje de error indicando que el comando no se reconoce.

4. **Descargar e instalar Python (si es necesario):** Si Python no está instalado y el usuario desea instalarlo, pueden descargarlo desde el sitio web oficial de Python (https://www.python.org/downloads/) y seguir las instrucciones de instalación. 

## 2. Creación de un entorno virtual:

Ahora crearemos un entorno virtual, que nos permitirá instalar paquetes de Python para cada proyecto en específico, sin afectar al sistema global.

1. **Abrir el símbolo del sistema:** Igual que antes, abre el menú de inicio y busca "cmd" para abrir el símbolo del sistema.

2. **Navegar a la ubicación de la carpeta del Generador:** Nos vamos a dirigir a la ubicación de la carpeta Generador. Utilizaremos el comando cd (cambiar directorio) seguido de la ruta de la carpeta. Por ejemplo:

    ```bash
    cd ruta\de\la\carpeta\Generador
    ```

4. **Crear un nuevo entorno virtual:** Encóntrandonos en la ubicación de la carpeta, ejecutaremos el siguiente comando para crear un nuevo entorno virtual:

    ```bash
    python -m venv nombre_del_entorno
    ```

    Reemplaza `nombre_del_entorno` con el nombre que desees para tu entorno virtual. Por lo general le daremos el nombre de ".env" al entorno (poner un punto al inicio del nombre hará que la carpeta del entorno virtual esté oculta, y así no obstruir con los archivos del proyecto).

5. **Activar el entorno virtual:** Después de crear el entorno virtual, necesitas activarlo. Esto asegura que cuando instales paquetes o ejecutes scripts, se hagan dentro del entorno virtual y no afecten al sistema global. Para activar el entorno virtual, ejecuta el siguiente comando:

    ```bash
    nombre_del_entorno\Scripts\activate
    ```

    Nota: Reemplaza "nombre_del_entorno" con el nombre que hayas elegido para tu entorno virtual.

6. **Desactivar el entorno virtual:** Cuando hayas terminado de trabajar en tu proyecto y quieras salir del entorno virtual, simplemente ejecuta el siguiente comando:

    ```bash
    deactivate
    ```

## 3. Instalación de paquetes de Python

Instalaremos los paquetes necesarios para la ejecución del script en nuestro entorno virtual.

1. **Abrir el símbolo del sistema:** Si aún no lo tienes abierto, abre el símbolo del sistema siguiendo los pasos que mencionamos anteriormente.

2. **Navegar a la ubicación de la carpeta Generador:** Usamos el comando cd seguido de la ruta de la carpeta del generador 
    
    ```bash
    cd ruta\de\la\carpeta\Generador
    ```

3. **Activar el entorno virtual:** Para activar el entorno virtual, ejecuta el siguiente comando:

    ```bash
    nombre_del_entorno\Scripts\activate
    ```

4. **Instalación de paquetes:** Ejecutamos el siguiente comando en el símbolo del sistema
    
    ```bash
    pip install -r requeriments.txt
    ```

# Ejecución

## 4. Ejecución del Script

1. **Archivos del proyecto:** En la carpeta Generador, crear una carpeta con el nombre `Input`, donde copiaremos todos los datos de entrada del proyecto:

    - job.ini
    - source_model.xml
    - source_model_logic_tree.xml
    - gmpe_logic_tree.xml
    - site_model.csv (si se requiere)

3. **Activamos el entorno virtual:** Abrimos el símbolo del sistema, nos dirigimos con el comando `cd` a la ubicación de la carpeta `Generador`. Y activamos el entorno virtual.

    ```bash
    nombre_del_entorno\Scripts\activate
    ```

4. **Ejecución del Generador:** Para ejecutar el script, escribimos el siguiente comando en el símbolo del sistema:

    ```bash
    python SeismicHazardGenerator.py
    ```

5. **Salidas del proyecto:** Luego de que termine la ejecución del script, se generará la carpeta llamada "Output", donde podrá encontrar los datos, las gráficas, las tablas, etc generadas de la librería OpenQuake.