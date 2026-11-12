"""Ejercicio D 

Uso: python solve.py < entrada.txt


"""
import sys
import math
from fractions import Fraction


class Cubeta:
    def __init__(self, capacidad, recarga):
        self.capacidad = Fraction(capacidad)
        self.recarga = Fraction(recarga)
        self.nivel = Fraction(capacidad)
        self.ultimo = Fraction(0)

    def actualizar(self, t):
        if t > self.ultimo:
            self.nivel = min(self.capacidad, self.nivel + self.recarga * (t - self.ultimo))
            self.ultimo = t

    def espera(self, cantidad):
        falta = cantidad - self.nivel
        return Fraction(0) if falta <= 0 else falta / self.recarga


def resolver(entrada):
    solicitudes = Cubeta(3, 1)
    tokens = Cubeta(100, 20)
    out = []
    for linea in entrada.splitlines():
        partes = linea.split()
        if not partes or partes[0] != "REQUEST":
            continue
        t, nuevos, _de_cache = Fraction(partes[1]), int(partes[2]), int(partes[3])
        solicitudes.actualizar(t)
        tokens.actualizar(t)

        espera = max(solicitudes.espera(1), tokens.espera(nuevos))
        if espera == 0:
            solicitudes.nivel -= 1
            tokens.nivel -= nuevos
            out.append("ok")
        else:
            out.append(f"429 retry-after={math.ceil(espera)}")
    return "\n".join(out)


if __name__ == "__main__":
    print(resolver(sys.stdin.read()))
