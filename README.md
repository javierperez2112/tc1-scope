# tc1-scope
GUI en Python para visualizar datos de osciloscopio en .csv

## Instrucciones de uso

### Ejecución del programa
Para abrir la GUI, se debe ejecutar el archivo _gui.py_.
```python3 /src/gui.py```
Se debería abrir una ventana de bienvenida así:

(foto bienvenida)

### Selección del archivo .csv
Para buscar el archivo deseado, presionar _Browse_, seleccionar el archivo en la nueva ventana, y presionar _open_ para abrirlo en la aplicación.

(foto browse)

Si el archivo es válido, se abrirá una ventana con el gráfico correspondiente.

(foto gráfico)

### Manejo de la aplicación

#### Canales

Para cada canal del osciloscopio guardado en el archivo, aparecerá un canal en la ventana. Para cada canal se puede:
* Activar/desactivar el canal
* Editar el nombre del canal
* Cambiar el zoom en tensión (V/div)
* Cambiar el desplazamiento en tensión (V offset)
* Cambiar el color en el gráfico
* Utilizar un cursor

(foto canales)

#### Separación de la cuadrícula y tiempo

En las dos columnas de la derecha, se encuentra la configuración de tiempo y separación de la cuadrícula. Se recomienda ajustar _X grid separation_ antes de utilizar cualquier otra herramienta.

#### Títulos y unidades


