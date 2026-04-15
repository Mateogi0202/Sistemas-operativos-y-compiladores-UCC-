"""Interfaz de consola del simulador.

Este archivo presenta el menu principal, recibe la entrada del usuario
y llama a la logica del sistema operativo simulado.
"""

from sistema_operativo import SistemaOperativo
import os


def limpiar_pantalla() -> None:
    # Borra la salida anterior para que cada pantalla del menu se vea limpia.
    # En Windows se usa `cls`; en otros sistemas se usa `clear`.
    os.system("cls" if os.name == "nt" else "clear")


def banner() -> None:
    # Encabezado principal del programa.
    # Sirve para identificar rapidamente el simulador y el tema del proyecto.
    print("=" * 62)
    print("        SIMULADOR DE SISTEMA OPERATIVO: RAM Y SWAP")
    print("=" * 62)
    print("Un entorno educativo para ver procesos, CPU y memoria virtual.")
    print()


def mostrar_menu() -> None:
    # Menu numerado para que la interaccion sea sencilla durante la explicacion.
    # Cada opcion llama a una parte distinta de la simulacion.
    print("Menu principal")
    print("  1. Crear proceso")
    print("  2. Ejecutar un ciclo de CPU")
    print("  3. Ejecutar varios ciclos")
    print("  4. Terminar proceso por PID")
    print("  5. Ver estado del sistema")
    print("  6. Ver ayuda rapida")
    print("  0. Salir")
    print()


def pedir_entero(mensaje: str, minimo: int | None = None) -> int:
    # Esta funcion evita errores si el usuario escribe texto en vez de numeros.
    # Si `minimo` existe, tambien valida que el numero no sea demasiado pequeno.
    while True:
        try:
            valor = int(input(mensaje).strip())
            if minimo is not None and valor < minimo:
                # Si el valor no cumple la condicion, se pide otra vez.
                print(f"Ingresa un numero mayor o igual a {minimo}.")
                continue
            return valor
        except ValueError:
            # Se usa este mensaje para guiar al usuario si escribe algo invalido.
            print("Ingresa un numero valido.")


def mostrar_estado_corto(so: SistemaOperativo) -> None:
    # Resumen corto que permite ver el estado general sin entrar al detalle.
    # Se muestra siempre al inicio del menu para que el usuario vea cambios rapido.
    print(f"RAM usada: {so.ram.usada}/{so.ram.total} | libre: {so.ram.libre}")
    print(f"Procesos listos: {len(so.ready)} | en swap: {len(so.swap)} | terminados: {len(so.terminados)}")
    print(f"Quantum: {so.quantum} | fallos de memoria: {so.fallos_memoria}")
    print()


def imprimir_ayuda() -> None:
    # Texto de apoyo para explicar el funcionamiento del sistema.
    # Esta ayuda resume la idea del simulador sin entrar en tecnicismos.
    print("Ayuda rapida")
    print("- Crear proceso: agrega un nuevo proceso al sistema.")
    print("- Ejecutar ciclo: usa Round Robin para darle CPU a un proceso.")
    print("- Terminar proceso: libera memoria manualmente por PID.")
    print("- Estado: muestra RAM, ready, swap y eventos recientes.")
    print("- Si la RAM no alcanza, el sistema mueve procesos a swap.")
    print()


def crear_proceso_interactivo(so: SistemaOperativo) -> None:
    # Pide los datos de un nuevo proceso uno por uno.
    # Esto hace mas facil explicar en clase que significa cada parametro.
    print("Crear proceso")
    # El nombre identifica visualmente al proceso dentro de la simulacion.
    nombre = input("Nombre: ").strip()
    # La prioridad sirve para decidir que procesos se pueden mover a swap antes.
    prioridad = pedir_entero("Prioridad (menor numero = mas alta): ", 0)
    # La memoria requerida indica cuanta RAM necesita el proceso.
    memoria = pedir_entero("Memoria requerida: ", 1)
    # La CPU total representa el trabajo completo que debe ejecutar.
    cpu = pedir_entero("CPU total: ", 1)
    # Se crea el proceso y el sistema decide si entra en RAM o va a swap.
    proceso = so.crear_proceso(nombre, prioridad, memoria, cpu)
    print(f"Proceso creado: PID {proceso.pid} | estado: {proceso.estado}")
    print()


def ejecutar_ciclos_interactivo(so: SistemaOperativo, ciclos: int) -> None:
    # Ejecuta uno o varios ciclos del planificador Round Robin.
    # Cada ciclo representa un turno de CPU para algun proceso listo.
    print(f"Ejecutando {ciclos} ciclo(s)...")
    resultados = so.ejecutar_n_ciclos(ciclos)
    for resultado in resultados:
        # Se imprime cada resultado para que se vea que paso en cada turno.
        print(f"- {resultado}")
    print()


def terminar_proceso_interactivo(so: SistemaOperativo) -> None:
    # Permite finalizar un proceso manualmente por su PID.
    # Esto ayuda a mostrar como se libera memoria en la simulacion.
    pid = pedir_entero("PID a terminar: ", 1)
    print(so.terminar_proceso(pid))
    print()


def main() -> None:
    # Se usa una RAM pequena a proposito para que el efecto de swap se vea rapido.
    # Con mas memoria, el simulador tardaria mas en mostrar este comportamiento.
    so = SistemaOperativo(ram_total=16, quantum=3)
    while True:
        # La pantalla se limpia en cada vuelta para que el menu se vea ordenado.
        limpiar_pantalla()
        # Se imprime el encabezado para ubicar al usuario en el sistema.
        banner()
        # Se muestra el estado corto antes de elegir una opcion.
        mostrar_estado_corto(so)
        # Se despliega el menu con las acciones disponibles.
        mostrar_menu()

        # El usuario selecciona una opcion escribiendo un numero.
        opcion = input("Selecciona una opcion: ").strip()

        # Opcion 0: cerrar el programa.
        if opcion == "0":
            print("Saliendo del simulador...")
            break
        # Opcion 1: crear un nuevo proceso.
        if opcion == "1":
            limpiar_pantalla()
            banner()
            crear_proceso_interactivo(so)
            input("Presiona Enter para continuar...")
            continue
        # Opcion 2: ejecutar un solo ciclo de CPU.
        if opcion == "2":
            limpiar_pantalla()
            banner()
            ejecutar_ciclos_interactivo(so, 1)
            input("Presiona Enter para continuar...")
            continue
        # Opcion 3: ejecutar varios ciclos seguidos.
        if opcion == "3":
            limpiar_pantalla()
            banner()
            ciclos = pedir_entero("Cuantos ciclos deseas ejecutar?: ", 1)
            ejecutar_ciclos_interactivo(so, ciclos)
            input("Presiona Enter para continuar...")
            continue
        # Opcion 4: terminar un proceso por PID.
        if opcion == "4":
            limpiar_pantalla()
            banner()
            terminar_proceso_interactivo(so)
            input("Presiona Enter para continuar...")
            continue
        # Opcion 5: mostrar el estado completo de la simulacion.
        if opcion == "5":
            limpiar_pantalla()
            banner()
            print(so.mostrar_estado())
            print()
            input("Presiona Enter para continuar...")
            continue
        # Opcion 6: mostrar ayuda resumida sobre el sistema.
        if opcion == "6":
            limpiar_pantalla()
            banner()
            imprimir_ayuda()
            input("Presiona Enter para continuar...")
            continue

        # Si el usuario escribe algo fuera del menu, se informa el error.
        print("Opcion invalida. Intenta de nuevo.")
        input("Presiona Enter para continuar...")


if __name__ == "__main__":
    main()
