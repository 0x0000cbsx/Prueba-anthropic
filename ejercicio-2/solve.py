"""Ejercicio B 

Uso: python solve.py < entrada.txt
"""
import sys
import json

CLIMA = {"Bogotá": 14, "Medellín": 24, "Cali": 26}


def calculadora(inp):
    op, a, b = inp.get("operacion"), inp.get("a"), inp.get("b")
    if op == "sumar":
        return str(a + b)
    if op == "restar":
        return str(a - b)
    if op == "multiplicar":
        return str(a * b)
    if op == "dividir":
        if b == 0:
            return "error: división por cero"
        return str(int(a / b))  
    return f"error: operación desconocida: {op}"


def clima(inp):
    ciudad = inp.get("ciudad")
    if ciudad in CLIMA:
        return f"{CLIMA[ciudad]} °C"
    return f"error: ciudad desconocida: {ciudad}"


HERRAMIENTAS = {"calculadora": calculadora, "clima": clima}


def ejecutar(name, inp):
    if name not in HERRAMIENTAS:
        return f"error: herramienta desconocida: {name}"
    return HERRAMIENTAS[name](inp)


def resolver(entrada):
    out = []
    llamadas = errores = 0
    for linea in entrada.splitlines():
        linea = linea.strip()
        if not linea:
            continue
        msg = json.loads(linea)
        if msg["stop_reason"] == "tool_use":
            for bloque in msg["content"]:
                if bloque["type"] != "tool_use":
                    continue
                resultado = ejecutar(bloque["name"], bloque["input"])
                llamadas += 1
                if resultado.startswith("error:"):
                    errores += 1
                out.append(f"tool_result {bloque['id']} {resultado}")
        elif msg["stop_reason"] == "end_turn":
            texto = "".join(b["text"] for b in msg["content"] if b["type"] == "text")
            out.append(f"final: {texto}")
    out.append(f"resumen: {llamadas} llamadas, {errores} errores")
    return "\n".join(out)


if __name__ == "__main__":
    print(resolver(sys.stdin.read()))
