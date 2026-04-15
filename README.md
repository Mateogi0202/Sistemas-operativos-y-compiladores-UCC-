# Simulador de Sistema Operativo: RAM y Swap

Este proyecto es una simulacion educativa de un sistema operativo minimalista escrita en Python. Su objetivo principal es resolver el problema de la falta de memoria RAM mediante el uso de memoria virtual (`swap`).

## Objetivo del proyecto

El sistema muestra como un sistema operativo puede seguir funcionando cuando la RAM no alcanza para todos los procesos.

La solucion simulada hace lo siguiente:

- crea procesos con consumo de RAM y CPU
- los organiza en una cola de ejecucion
- reparte el tiempo de CPU con `Round Robin`
- mueve procesos a `swap` cuando la RAM no alcanza
- libera memoria cuando un proceso termina
- recupera procesos desde `swap` cuando vuelve a haber espacio

## Problema que resuelve

El problema central es la **falta de memoria RAM**.

En un equipo con poca RAM, no todos los programas pueden mantenerse cargados al mismo tiempo. Si el sistema intenta cargar todo directamente en memoria principal, se satura y deja de responder bien.

Este simulador resuelve eso con una idea sencilla:

1. Los procesos que caben se cargan en RAM.
2. Los que no caben pasan a `swap`.
3. Cuando un proceso termina, libera RAM.
4. El sistema intenta volver a traer procesos desde `swap`.

## Conceptos usados

### 1. Proceso

Un proceso representa un programa en ejecucion. En este simulador cada proceso tiene:

- `pid`: identificador unico
- `nombre`: nombre del proceso
- `prioridad`: valor usado para ordenar candidatos cuando hay que liberar RAM
- `memoria_requerida`: cantidad de RAM que necesita
- `cpu_total`: tiempo total que necesita para terminar
- `cpu_restante`: tiempo que le falta por ejecutar
- `estado`: situacion actual del proceso

En esta version, la prioridad se conserva como dato del proceso para mostrarla en pantalla y explicar el modelo, pero la logica principal de swap usa una cola simple.

### 2. RAM

La RAM es la memoria principal disponible en la simulacion.

El sistema lleva el control de:

- memoria usada
- memoria libre
- memoria total

### 3. Swap

`Swap` representa memoria virtual en disco.

No es tan rapida como la RAM, pero permite guardar temporalmente procesos que no pueden permanecer en memoria principal.

En el simulador, `swap` funciona como una cola: el primer proceso que entro es el primero que se intenta devolver a RAM cuando haya espacio.

### 4. Round Robin

`Round Robin` es el algoritmo de planificacion usado para repartir CPU.

Funcionamiento:

- cada proceso recibe un tiempo fijo llamado `quantum`
- si no termina dentro de ese tiempo, vuelve al final de la cola
- el siguiente proceso toma la CPU
- asi todos avanzan de forma justa

## Flujo del simulador

### Al crear un proceso

1. Se verifica si su memoria cabe en la RAM.
2. Si cabe, entra a la cola `ready`.
3. Si no cabe, el sistema intenta liberar espacio moviendo otros procesos a `swap`.
4. Si aun no cabe, el proceso se guarda en `swap`.

### Al ejecutar CPU

1. El sistema toma el primer proceso de la cola `ready`.
2. Le asigna el `quantum`.
3. Si termina, se libera su RAM.
4. Si no termina, vuelve al final de la cola.

### Al liberar memoria

1. La RAM ocupada por el proceso se libera.
2. El sistema vuelve a revisar `swap`.
3. Si hay espacio suficiente, algun proceso regresa a RAM.

## Interfaz del programa

El programa se ejecuta desde consola y muestra un menu interactivo con estas opciones:

- crear proceso
- ejecutar un ciclo de CPU
- ejecutar varios ciclos
- terminar proceso por PID
- ver estado completo del sistema
- ver ayuda rapida
- salir

## Como ejecutar

```bash
python main.py
```

## Ejemplo de uso

Supongamos que la RAM total disponible es 16 unidades y el quantum es 3.

### Paso 1: crear procesos

```text
Proceso 1: Navegador | memoria 4 | CPU 6
Proceso 2: Editor     | memoria 4 | CPU 5
Proceso 3: Juego      | memoria 4 | CPU 7
```

### Paso 2: interpretar la RAM

- el proceso 1 ocupa 4
- el proceso 2 ocupa 4
- ya se usan 8 de 16
- el proceso 3 tambien cabe, pero si la RAM estuviera mas llena podria ir a swap

### Paso 3: ejecutar con Round Robin

Si el quantum es 3:

- el proceso 1 usa 3 unidades de CPU y le quedan 3
- el proceso 2 usa 3 unidades de CPU y le quedan 2
- el proceso 1 vuelve a tomar turno despues de pasar por el final de la cola

### Paso 4: ver liberacion de memoria

Cuando un proceso termina:

- su RAM se libera
- el estado del sistema muestra mas memoria disponible
- procesos en swap pueden regresar a RAM

## Ejemplo para explicar en clase

Puedes explicarlo asi, paso a paso:

1. El sistema inicia con poca RAM.
2. Creo varios procesos y cada uno pide memoria.
3. Los procesos que caben se cargan en `ready`.
4. Si la RAM se llena, el sistema manda procesos a `swap`.
5. El planificador Round Robin reparte CPU en turnos iguales.
6. Cuando un proceso termina, libera RAM.
7. Esa RAM libre permite recuperar procesos desde `swap`.

Con esta logica, el simulador no se bloquea cuando la memoria principal se agota.

## Archivos del proyecto

- `main.py`: interfaz de consola y menu principal
- `sistema_operativo.py`: logica central del simulador
- `proceso.py`: definicion del proceso
- `memoria.py`: control de RAM

## Estados de un proceso

Los procesos pueden pasar por estos estados:

- `nuevo`: creado pero no cargado aun
- `listo`: preparado para ejecutarse en RAM
- `ejecutando`: usando CPU
- `swap`: fuera de RAM, esperando espacio
- `terminado`: ya finalizo su ejecucion
- `rechazado`: el proceso pide mas RAM de la que existe

## Resultado esperado

Al usar el programa, se puede observar:

- cola de procesos listos
- procesos en swap
- memoria usada y libre
- eventos recientes del sistema
- turnos de CPU con Round Robin
- 
