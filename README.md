# UTN PROYECTO FINAL PYGAME
Proyecto realizado con la libreria de pygame para entregar en laboratio 1 y programacion 1, UTN

Alumno: Gustavo Adrian Arias Contreras
Division E

## Descripcion del proyecto

El juego esta creado para jugarse como un plataformas al estilo super meat boy, donde el objetivo es esquivar los obstaculos e ir agarrando items para llegar a un punto en concreto en este caso para obtener el trofeo con el mayor puntaje posible

![trofeo](https://raw.githubusercontent.com/GustavoACC/gustavoArias-pygame-tp-final/main/recursos/Items/Checkpoints/End/End%20(Idle).png)

## Controles

Teclas de control:

Tecla "D" para moverse a la derecha
Tecla "A" para moverse a la izquierda
Tecla "W" para saltar
Tecla "F10" para reset rapido

## Desbloqueo de niveles

Para desbloquear un nivel se debe superar el anterior al menos 1 vez obteniendo el trofeo del mismo

## Items

Items los cuales se les puede asignar el valor que se desee desde la configuracion del nivel

![aple](https://raw.githubusercontent.com/GustavoACC/gustavoArias-pygame-tp-final/main/recursos/Items/Fruits/Apple.png)
![banana](https://raw.githubusercontent.com/GustavoACC/gustavoArias-pygame-tp-final/main/recursos/Items/Fruits/Bananas.png)
![strawberry](https://raw.githubusercontent.com/GustavoACC/gustavoArias-pygame-tp-final/main/recursos/Items/Fruits/Strawberry.png)

## Trampas

Trampas que general daño al contacto

![saw](https://raw.githubusercontent.com/GustavoACC/gustavoArias-pygame-tp-final/main/recursos/traps/saw/Off.png)

## Armado del nivel

### Terreno y csv

para la generacion del mapa se necesita un archivo csv, el mismo se puede generar con un programa gratuito llamado [Tiled](https://www.mapeditor.org/)

![terrain](https://raw.githubusercontent.com/GustavoACC/gustavoArias-pygame-tp-final/main/recursos/terrain/terrain22x11.png)

Se necesita crear por una grilla de 63x38

![tiled_example]()

Luego de armar el mapa deseado se exporta como csv y se reemplaza el del nivel que se desea con el mismo nombre

### Configuracion

Cada carpeta de nivel (levels/level-1 por ejemplo) tiene su archivo start-config.json en el cual se pueden agregar todas las plataformas, items y trampas que se deseen, ademas de la posicion inicial del jugador, la cantidad de vidas y el tiempo disponible en el nivel para ser completado, asi como el path de la musica y el fondo

## Guardado

El guardado de la partida se encuentra dentro de la carpeta saves es un json que contiene el nombre del jugador, los niveles desbloqueados y su mejor puntaje hasta el momento en cada nivel