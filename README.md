# Plasta GUI Maker

> Conjunto de utilidades y herramientas para trabajar con [Plasta](https://github.com/informaticameg/plasta) e interfaces en PyQt.

## Lista de utilidades/herramientas

Todas estas herramientas debajo descriptas poseen una GUI para realizar lo mismo que desde código.
### Generar paquete Plasta
Herramienta para generar los 4 archivos de un paquete plasta base.

```
/object_folder_example
  --- __init__.py
  --- manager.py
  --- add.py
  --- gui.py
```
Desde codigo:

<pre><code>from maker import make_plasta_package
data = {
  'className':'Person',
  'addIdeAttr':True,
  'attributes':[
      {'name':'name','type':'Unicode'},
      {'name':'last_name','type':'Unicode'},
      {'name':'email','type':'Unicode'},
      {'name':'age','type':'Int'},
      {'name':'birthday','type':'Date'},
    ],
  'widgetToAttr':{
    'name':'lineEdit',
    'last_name':'lineEdit',
    'email':'lineEdit',
    'age':'spinBox',
    'birthday':'dateEdit',
  },
  'classesToGenerate':{
    'storm':True,'manager':True,'gui':True,'add':True
  },
  'outputFolder':'/some_folder'
}

make_plasta_package.generatePackage(data)</pre></code>


### Crear UI

Herramienta para generar un archivo .ui tipo formulario nuevo/editar

```python
from maker import add_maker_simple

outputFolder = '/some_output_folder/some_file.ui'
fields = {0: {u'field1': u'QLineEdit'}, 1: {u'field2': u'QLineEdit'}}
buttons = {'bt_limpiar': False, 'bt_cancelar_aceptar': False, 'bt_salir_guardar': True, 'bt_salir_aceptar': False}
options = {'tipo': 'Dialog', 'generar_plantilla': False}

add_maker_simple.generarUI(outputFile, fields, buttons, options)
```

#### Valores para parametro 'options':
- tipo: tipo de ventana a generar, posibles valores: (Dialog, MainWindow)
- generar_plantilla: si es True, generará junto con el .ui el archivo .py para manejarlo

#### TODO
- Incluir métodos de las señales/eventos

### Generar clase Storm + .ui

Generador de plantillas para el archivo storm `__init__.py`. Tipos de datos soportados para bases de datos SQLite, MySQL y PostgresSQL.

#### TODO en la GUI
- Generar el archivo .ui para la plantilla 

### Generar señales/metodos

Generador/explorador de señales/eventos de los widgets incluidos en un .ui

#### TODO en la GUI
- Funcionalidad de botones ubicados a la izquiera de los editores de código.

### Generar plantilla para un .ui

Genera el archivo .py para un .ui indicado.


## Ejecutar el programa
```python 
python main.py
```

## Test

```python 
python run_test.py
```

## Contribuir

Las contribuciones son bienvenidas