"""Ejercicio C 

Uso: python solve.py < entrada.txt

"""
import sys
import json
from decimal import Decimal, ROUND_HALF_UP

MILLON = Decimal(1_000_000)
P_IN = Decimal("3")
P_OUT = Decimal("15")
P_CW = P_IN * Decimal("1.25")
P_CR = P_IN * Decimal("0.1")


def fmt(x):
    return "$" + str(x.quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP))


def resolver(entrada):
    out = []
    total = sin_cache = Decimal(0)
    aciertos = n = 0
    for linea in entrada.splitlines():
        linea = linea.strip()
        if not linea:
            continue
        u = json.loads(linea)
        inp = u.get("input_tokens", 0)
        cw = u.get("cache_creation_input_tokens", 0)
        cr = u.get("cache_read_input_tokens", 0)
        outp = u.get("output_tokens", 0)

        costo = (inp * P_IN + cw * P_CW + cr * P_CR + outp * P_OUT) / MILLON
        costo_sin = ((inp + cw + cr) * P_IN + outp * P_OUT) / MILLON

        n += 1
        total += costo
        sin_cache += costo_sin
        if cr > 0:
            aciertos += 1
        out.append(f"solicitud {n}: {fmt(costo)}")

    out.append(f"total: {fmt(total)}")
    out.append(f"sin_cache: {fmt(sin_cache)}")
    out.append(f"ahorro: {fmt(sin_cache - total)}")
    out.append(f"aciertos_de_cache: {aciertos}/{n}")
    return "\n".join(out)


if __name__ == "__main__":
    print(resolver(sys.stdin.read()))
