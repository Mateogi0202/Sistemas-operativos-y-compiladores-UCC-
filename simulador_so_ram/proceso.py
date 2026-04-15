"""Modelo de proceso usado por el simulador del sistema operativo.

Este archivo define la estructura basica de un proceso: su memoria,
tiempo de CPU, prioridad y estado dentro del sistema.
"""

from dataclasses import dataclass, field


@dataclass
class Proceso:
    """Representa un proceso dentro del simulador.

    Cada proceso necesita memoria RAM y tiempo de CPU para finalizar.
    El sistema operativo simulado usa estos datos para decidir si el
    proceso entra a RAM, pasa a swap o termina su ejecucion.
    """

    # Identificador unico del proceso.
    pid: int
    # Nombre visible del proceso.
    nombre: str
    # Prioridad del proceso. Un numero menor representa mayor prioridad.
    prioridad: int
    # Cantidad de RAM necesaria para permanecer cargado.
    memoria_requerida: int
    # Tiempo total de CPU que necesita para completar su trabajo.
    cpu_total: int
    # Tiempo de CPU restante. Se calcula al crear el objeto.
    cpu_restante: int = field(init=False)
    # Estado actual del proceso dentro del sistema.
    estado: str = field(default="nuevo")
    # Marca de tiempo del ultimo uso para apoyar decisiones de swap.
    ultimo_uso: int = field(default=0)
    # Indica si el proceso esta cargado actualmente en RAM.
    en_ram: bool = field(default=False)

    def __post_init__(self) -> None:
        # Al crearse, todo el tiempo de CPU queda pendiente por ejecutar.
        self.cpu_restante = self.cpu_total

    def ejecutar(self, quantum: int) -> int:
        # Reduce el tiempo restante usando el quantum asignado en este turno.
        # Si falta menos tiempo del quantum, solo se ejecuta lo pendiente.
        ejecutado = min(quantum, self.cpu_restante)
        self.cpu_restante -= ejecutado
        return ejecutado

    def terminado(self) -> bool:
        # Un proceso termina cuando ya no le queda tiempo de CPU.
        return self.cpu_restante <= 0
