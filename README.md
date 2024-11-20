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
* Activar/desactivar y utilizar un par de cursores

(foto canales)

#### Separación de la cuadrícula y tiempo

En las dos columnas de la derecha, se encuentra la configuración de tiempo y separación de la cuadrícula. Se recomienda ajustar _X grid separation_ antes de utilizar cualquier otra herramienta. Para esto, aumentar la separación hasta que deje de aparecer el mensaje de _Time tick too small!_ y ajustar a gusto. Se puede hacer lo mismo con la separación en el eje Y, pero no es esencial para el funcionamiento de otras características. 

La configuración de _Time zoom_ y _Time offset_ funcionan de manera análoga a _V/div_ y _V offset_, pero para el eje del tiempo. Además, la configuración de desplazamiento se puede reiniciar con el botón _Reset offset_.

El par de cursores de tiempo funciona igual que los de tensión en cada canal. Las líneas quedan estáticas en el gráfico independientemente del _zoom_ y _offset_. Esto se puede utilizar para obtener mejor precisión con el cursor.

(foto tiempo)

#### Títulos y unidades

Es posible editar el título del gráfico, así como los de los ejes. Si se activa _X units_ o _Y units_, el título del eje correspondiente llevará especificadas las unidades que se utilizan en ese eje. Si se activa _Legend_, se mostrará la leyenda con los nombres de los canales en el gráfico. Además, si el archivo abierto contiene exactamente dos canales, aparecerá la opción de activar el modo XY, donde en lugar de graficar ambos canales contra el tiempo, se grafica uno contra otro.

#### Actualización del gráfico

Para actualizar la información del gráfico cuando se cambia un campo de texto, se debe presionar _Enter_.
