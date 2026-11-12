# comprobar_stream.py
# Script para comprobar si la radio esta emitiendo en Icecast
# Lo lanzo con cron cada 5 minutos en la Raspberry del estudio
# Autor: David Uhagon Vega

import urllib.request
import json
import datetime

URL_ESTADO = "http://localhost:8000/status-json.xsl"
PUNTO_MONTAJE = "/radio"
FICHERO_LOG = "log_stream.txt"


def escribir_log(texto):
    hora = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    with open(FICHERO_LOG, "a") as f:
        f.write(hora + " - " + texto + "\n")


def comprobar():
    try:
        respuesta = urllib.request.urlopen(URL_ESTADO, timeout=5)
        datos = json.loads(respuesta.read().decode("utf-8"))
    except Exception as e:
        escribir_log("ERROR: no se puede conectar con Icecast (" + str(e) + ")")
        return False

    fuentes = datos["icestats"].get("source", [])
    # si solo hay una fuente icecast no devuelve una lista, devuelve un diccionario
    if isinstance(fuentes, dict):
        fuentes = [fuentes]

    for fuente in fuentes:
        if fuente.get("listenurl", "").endswith(PUNTO_MONTAJE):
            oyentes = fuente.get("listeners", 0)
            escribir_log("OK: emitiendo con " + str(oyentes) + " oyentes")
            return True

    escribir_log("AVISO: Icecast funciona pero no hay nadie emitiendo en " + PUNTO_MONTAJE)
    return False


if __name__ == "__main__":
    comprobar()
