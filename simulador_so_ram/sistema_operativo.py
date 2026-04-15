"""Nucleo del sistema operativo simulado.

Este archivo contiene la logica principal del proyecto:
- crea procesos
- asigna memoria RAM
- usa swap cuando la RAM no alcanza
- ejecuta procesos con Round Robin
"""

from collections import deque

from memoria import Memoria
from proceso import Proceso


class SistemaOperativo:
    def __init__(self, ram_total: int = 1024, quantum: int = 3):
        # Memoria RAM disponible en la simulacion.
        self.ram = Memoria(ram_total)
        # Tiempo maximo que recibe cada proceso por turno.
        self.quantum = quantum

        # Tabla general de procesos creados.
        self.procesos: dict[int, Proceso] = {}
        # Procesos listos para usar CPU.
        self.ready: deque[Proceso] = deque()
        # Procesos que no caben en RAM en este momento.
        self.swap: deque[Proceso] = deque()
        # Procesos que ya terminaron.
        self.terminados: list[Proceso] = []

        # Contadores basicos para mostrar el comportamiento del sistema.
        self.reloj = 0
        self.siguiente_pid = 1
        self.fallos_memoria = 0

        # Mensajes recientes para ver que hizo el sistema.
        self.eventos: list[str] = []

    def _registrar_evento(self, mensaje: str) -> None:
        self.eventos.append(f"t={self.reloj}: {mensaje}")
        self.eventos = self.eventos[-10:]

    def _cargar_desde_swap(self) -> None:
        # Intenta traer procesos desde swap mientras haya espacio en RAM.
        while self.swap and self.ram.puede_asignar(self.swap[0].memoria_requerida):
            proceso = self.swap.popleft()
            self.ram.asignar(proceso.memoria_requerida)
            proceso.estado = "listo"
            proceso.en_ram = True
            self.ready.append(proceso)
            self._registrar_evento(f"Proceso {proceso.pid} regreso de swap a RAM")

    def crear_proceso(self, nombre: str, prioridad: int, memoria_requerida: int, cpu_total: int) -> Proceso:
        # Crea un nuevo proceso con un PID unico.
        proceso = Proceso(
            pid=self.siguiente_pid,
            nombre=nombre,
            prioridad=prioridad,
            memoria_requerida=memoria_requerida,
            cpu_total=cpu_total,
        )
        self.siguiente_pid += 1
        self.procesos[proceso.pid] = proceso

        # Si el proceso pide mas memoria que la RAM total, no puede ejecutarse.
        if memoria_requerida > self.ram.total:
            proceso.estado = "rechazado"
            self._registrar_evento(f"Proceso {proceso.pid} rechazado por falta de RAM total")
            return proceso

        # Si cabe en RAM, se carga directamente.
        if self.ram.asignar(memoria_requerida):
            proceso.estado = "listo"
            proceso.en_ram = True
            self.ready.append(proceso)
            self._registrar_evento(f"Proceso {proceso.pid} cargado en RAM")
            return proceso

        # Si no cabe, se mueve a swap y se intenta luego.
        proceso.estado = "swap"
        self.swap.append(proceso)
        self.fallos_memoria += 1
        self._registrar_evento(f"Proceso {proceso.pid} enviado a swap")
        return proceso

    def ejecutar_ciclo(self) -> str:
        # Antes de ejecutar, intenta recuperar procesos desde swap.
        self._cargar_desde_swap()

        # Si no hay procesos listos, no se puede usar la CPU.
        if not self.ready:
            self._registrar_evento("No habia procesos listos")
            return "No hay procesos listos."

        # Round Robin toma el primer proceso de la cola.
        proceso = self.ready.popleft()
        proceso.estado = "ejecutando"

        # El proceso usa solo el tiempo permitido por el quantum.
        ejecutado = proceso.ejecutar(self.quantum)
        self.reloj += ejecutado

        # Si termina, se libera la memoria ocupada.
        if proceso.terminado():
            self.ram.liberar(proceso.memoria_requerida)
            proceso.estado = "terminado"
            proceso.en_ram = False
            self.terminados.append(proceso)
            self.procesos.pop(proceso.pid, None)
            self._registrar_evento(f"Proceso {proceso.pid} termino y libero RAM")
            self._cargar_desde_swap()
            return f"Proceso {proceso.pid} terminado."

        # Si no termina, vuelve al final de la cola ready.
        proceso.estado = "listo"
        self.ready.append(proceso)
        self._registrar_evento(f"Proceso {proceso.pid} uso quantum y volvio a ready")
        return f"Proceso {proceso.pid} ejecuto {ejecutado} unidades de CPU."

    def terminar_proceso(self, pid: int) -> str:
        # Termina un proceso por solicitud del usuario.
        proceso = self.procesos.get(pid)
        if proceso is None:
            return f"PID {pid} no existe."

        if proceso in self.ready:
            self.ready.remove(proceso)
        if proceso in self.swap:
            self.swap.remove(proceso)

        if proceso.en_ram:
            self.ram.liberar(proceso.memoria_requerida)

        proceso.estado = "terminado"
        proceso.en_ram = False
        self.terminados.append(proceso)
        self.procesos.pop(pid, None)
        self._registrar_evento(f"Proceso {pid} terminado manualmente")
        self._cargar_desde_swap()
        return f"Proceso {pid} terminado y memoria liberada."

    def ejecutar_n_ciclos(self, ciclos: int) -> list[str]:
        # Ejecuta varios ciclos seguidos.
        resultados = []
        for _ in range(ciclos):
            resultados.append(self.ejecutar_ciclo())
        return resultados

    def mostrar_estado(self) -> str:
        # Devuelve un texto con el estado actual del sistema.
        lineas = [
            f"RAM: usada {self.ram.usada}/{self.ram.total} | libre {self.ram.libre}",
            f"Quantum: {self.quantum}",
            f"Procesos listos: {len(self.ready)} | en swap: {len(self.swap)} | terminados: {len(self.terminados)}",
            f"Fallos de memoria: {self.fallos_memoria}",
        ]

        if self.ready:
            lineas.append("Ready:")
            for p in self.ready:
                lineas.append(
                    f"  PID {p.pid} | {p.nombre} | prioridad {p.prioridad} | RAM {p.memoria_requerida} | CPU {p.cpu_restante}"
                )

        if self.swap:
            lineas.append("Swap:")
            for p in self.swap:
                lineas.append(
                    f"  PID {p.pid} | {p.nombre} | prioridad {p.prioridad} | RAM {p.memoria_requerida} | CPU {p.cpu_restante}"
                )

        if self.eventos:
            lineas.append("Eventos recientes:")
            for evento in self.eventos:
                lineas.append(f"  {evento}")

        return "\n".join(lineas)
