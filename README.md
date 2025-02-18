José Daniel Pérez Morales, Cohorte-21

# Proyecto "Urban Routes"
El objetivo del proyecto es comprobar la funcionalidad de Urban Routes al solicitar un taxi con opción de tarifa "Comfort"

El IDE usado es PyCharm trabajando con el lenguaje de programación de Python
Librerías de Selenium y Pytest

- Abrir el archivo en PyCharm.

- El proyecto consta de cuatro archivos: 
  --> data.py, que contiene la información para rellenar campos obligatorios.
  --> helpers.py, que contiene la función auxiliar para obtener el código de SMS.
  --> pages.py, que contiene los localizadores y métodos de las diferentes clases.
  --> main.py, que contiene la ejecución de las pruebas. 

Resumen general para la prueba:
  - Llenar campos "Desde" y "Hasta"
  - Clic en "pedir un taxi.
  - Clic en icono "Comfort"
  - Llenar campos "Número de teléfono", "Método de pago" y "Mensaje para el conductor"
  - Seleccionar las opciones "Manta y pañuelos" y agregar dos helados en la opción "Helado" en la ventana de "Requisitos del pedido".

- Ejecuta el comando pytest \projects\qa-project-Urban-Routes-es\main.py