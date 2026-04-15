"""Modelo simple de memoria RAM para la simulacion.

Este archivo controla cuanta memoria total existe, cuanto se ha usado
y cuanto espacio libre queda disponible para nuevos procesos.
"""

class Memoria:
    """Modelo simple de memoria RAM para el simulador."""

    def __init__(self, total: int):
        # Cantidad total de RAM disponible en la simulacion.
        self.total = total
        # Memoria actualmente ocupada por procesos cargados.
        self.usada = 0

    @property
    def libre(self) -> int:
        # Espacio de RAM que aun queda libre.
        return self.total - self.usada

    def puede_asignar(self, cantidad: int) -> bool:
        # Comprueba si hay suficiente espacio para reservar memoria.
        return cantidad <= self.libre

    def asignar(self, cantidad: int) -> bool:
        # Reserva RAM si existe espacio suficiente.
        if not self.puede_asignar(cantidad):
            return False
        self.usada += cantidad
        return True

    def liberar(self, cantidad: int) -> None:
        # Devuelve memoria al sistema cuando un proceso termina o sale de RAM.
        # Se usa max(0, ...) para evitar valores negativos por seguridad.
        self.usada = max(0, self.usada - cantidad)
