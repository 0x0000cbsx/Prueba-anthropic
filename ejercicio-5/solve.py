"""Ejercicio E

Uso: python solve.py < entrada.txt

"""
import sys
import json
import unicodedata
from collections import defaultdict
from decimal import Decimal, ROUND_HALF_UP


def normalizar(texto):
    texto = unicodedata.normalize("NFD", texto.lower())
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    texto = "".join(c if c.isalnum() else " " for c in texto)
    return texto.split()


def pasa(esperado, respuesta):
    e, r = normalizar(esperado), normalizar(respuesta)
    if not e:
        return False
    return any(r[i:i + len(e)] == e for i in range(len(r) - len(e) + 1))


def resolver(entrada):
    aprobadas = defaultdict(int)
    totales = defaultdict(int)
    for linea in entrada.splitlines():
        linea = linea.strip()
        if not linea:
            continue
        caso = json.loads(linea)
        cat = caso["categoria"]
        totales[cat] += 1
        if pasa(caso["esperado"], caso["respuesta"]):
            aprobadas[cat] += 1

    out = [f"{cat}: {aprobadas[cat]}/{totales[cat]}" for cat in sorted(totales)]
    a, n = sum(aprobadas.values()), sum(totales.values())
    pct = (Decimal(a) * 100 / Decimal(n)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP) if n else Decimal("0.0")
    out.append(f"total: {a}/{n} ({pct}%)")
    return "\n".join(out)


if __name__ == "__main__":
    print(resolver(sys.stdin.read()))
