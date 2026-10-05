from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple
import heapq
import math
import time


@dataclass(frozen=True)
class Vuelo:
    origen: str
    destino: str
    precio: float


class GrafoVuelos:
    """Grafo dirigido y ponderado para representar rutas aéreas y sus costos."""

    def __init__(self) -> None:
        self.adyacencia: Dict[str, List[Tuple[str, float]]] = {}

    def agregar_vuelo(self, origen: str, destino: str, precio: float) -> None:
        self.adyacencia.setdefault(origen, []).append((destino, precio))
        self.adyacencia.setdefault(destino, [])

    @classmethod
    def desde_archivo(cls, ruta: str | Path) -> "GrafoVuelos":
        grafo = cls()
        with open(ruta, "r", encoding="utf-8") as archivo:
            for numero, linea in enumerate(archivo, start=1):
                linea = linea.strip()
                if not linea or linea.startswith("#"):
                    continue
                partes = [p.strip() for p in linea.split(",")]
                if len(partes) != 3:
                    raise ValueError(f"Línea {numero} inválida: {linea}")
                origen, destino, precio_txt = partes
                precio = float(precio_txt)
                if precio < 0:
                    raise ValueError("El precio no puede ser negativo.")
                grafo.agregar_vuelo(origen, destino, precio)
        return grafo

    def aeropuertos(self) -> List[str]:
        return sorted(self.adyacencia)

    def vuelos(self) -> List[Vuelo]:
        datos: List[Vuelo] = []
        for origen, vecinos in self.adyacencia.items():
            for destino, precio in vecinos:
                datos.append(Vuelo(origen, destino, precio))
        return sorted(datos, key=lambda v: (v.origen, v.destino, v.precio))

    def ruta_mas_barata(self, origen: str, destino: str) -> Tuple[float, List[str]]:
        if origen not in self.adyacencia:
            raise KeyError(f"Origen no registrado: {origen}")
        if destino not in self.adyacencia:
            raise KeyError(f"Destino no registrado: {destino}")

        distancias = {nodo: math.inf for nodo in self.adyacencia}
        previos: Dict[str, str | None] = {nodo: None for nodo in self.adyacencia}
        distancias[origen] = 0.0
        cola: List[Tuple[float, str]] = [(0.0, origen)]

        while cola:
            costo_actual, nodo_actual = heapq.heappop(cola)
            if costo_actual > distancias[nodo_actual]:
                continue
            if nodo_actual == destino:
                break

            for vecino, precio in self.adyacencia[nodo_actual]:
                nuevo_costo = costo_actual + precio
                if nuevo_costo < distancias[vecino]:
                    distancias[vecino] = nuevo_costo
                    previos[vecino] = nodo_actual
                    heapq.heappush(cola, (nuevo_costo, vecino))

        if math.isinf(distancias[destino]):
            return math.inf, []

        ruta = []
        actual: str | None = destino
        while actual is not None:
            ruta.append(actual)
            actual = previos[actual]
        ruta.reverse()
        return distancias[destino], ruta

    def reporte_general(self) -> str:
        lineas = [
            "REPORTE GENERAL DEL GRAFO DE VUELOS",
            "=" * 44,
            f"Aeropuertos registrados: {len(self.adyacencia)}",
            f"Rutas dirigidas registradas: {len(self.vuelos())}",
            "",
            "AEROPUERTOS:",
            ", ".join(self.aeropuertos()),
            "",
            "RUTAS Y COSTOS:",
        ]
        for vuelo in self.vuelos():
            lineas.append(f"- {vuelo.origen:12s} -> {vuelo.destino:12s}  USD {vuelo.precio:6.2f}")
        return "\n".join(lineas)


def ejecutar_consulta(grafo: GrafoVuelos, origen: str, destino: str) -> str:
    inicio = time.perf_counter_ns()
    costo, ruta = grafo.ruta_mas_barata(origen, destino)
    fin = time.perf_counter_ns()
    tiempo_ms = (fin - inicio) / 1_000_000

    if not ruta:
        return f"No existe ruta disponible de {origen} a {destino}. Tiempo: {tiempo_ms:.6f} ms"

    return (
        f"Consulta: {origen} -> {destino}\n"
        f"Ruta más barata: {' -> '.join(ruta)}\n"
        f"Costo total: USD {costo:.2f}\n"
        f"Tiempo de ejecución: {tiempo_ms:.6f} ms"
    )


def demo() -> None:
    base = Path(__file__).with_name("vuelos.txt")
    grafo = GrafoVuelos.desde_archivo(base)
    print(grafo.reporte_general())
    print("\n" + "-" * 44)
    for origen, destino in [
        ("Quito", "Loja"),
        ("Tena", "Guayaquil"),
        ("Manta", "Quito"),
    ]:
        print(ejecutar_consulta(grafo, origen, destino))
        print("-" * 44)


if __name__ == "__main__":
    demo()
