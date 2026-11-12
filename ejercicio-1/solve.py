"""Reconstruye mensajes completos a partir de eventos de streaming de la API de Claude.

Uso: python solve.py < entrada.txt
"""
import sys
import json


def resolver(entrada):
    out = []
    for linea in entrada.splitlines():
        if not linea.startswith("data:"):
            continue  
        ev = json.loads(linea[5:].strip())
        t = ev["type"]
        if t == "message_start":
            bloques = {}
            input_tokens = ev["message"]["usage"]["input_tokens"]
            output_tokens = ev["message"]["usage"].get("output_tokens", 0)
            stop_reason = None
        elif t == "content_block_start":
            bloques.setdefault(ev["index"], "")
        elif t == "content_block_delta" and ev["delta"]["type"] == "text_delta":
            bloques[ev["index"]] = bloques.get(ev["index"], "") + ev["delta"]["text"]
        elif t == "message_delta":
            stop_reason = ev["delta"]["stop_reason"]
            output_tokens = ev["usage"]["output_tokens"]
        elif t == "message_stop":
            texto = "".join(bloques[i] for i in sorted(bloques))
            out += [
                f"texto: {texto}",
                f"stop_reason: {stop_reason}",
                f"input_tokens: {input_tokens}",
                f"output_tokens: {output_tokens}",
            ]
        
    return "\n".join(out)


if __name__ == "__main__":
    print(resolver(sys.stdin.read()))
