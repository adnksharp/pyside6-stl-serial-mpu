# STL viewer with pySide6 and Arduino

 ![](https://i.imgur.com/OIrwELN.png)

Uso del sensor MPU6050 y PySide6 para visualizar archivos SLT.

## Requisitos

### Librerías de Python
* PySide6
* vtk
* pyserial

```
pip install PySide6 vtk pyserial
```

## Hardware usado

| ![](https://i.imgur.com/OZPGH9D.png) | ![](https://i.imgur.com/nGbuhPc.jpeg) |
|--|--|

* Placa de desarrollo MEGA 2560.
* MPU 6050.

## Funcionamiento 
Despues de cargar el [sketch](ino) en la placa, está se encarga de enviar los datos de orientación del sensor por el puerto serie cada 50 ms.

El programa [main](main.py) se encarga de girar una pieza en base a los datos recibidos.