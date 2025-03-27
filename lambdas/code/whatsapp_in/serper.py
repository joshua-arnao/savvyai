import urllib.request
import json
import os
import re

SERPER_API_KEY = os.environ.get("SERPER_API_KEY")

def search_serper(query):
    if not SERPER_API_KEY:
        return [{"title": "Error", "snippet": "No API key configured.", "link": ""}]

    url = "https://google.serper.dev/search"
    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "q": f"{query} en Perú",
        "gl": "pe",
        "hl": "es"
    }
    data = json.dumps(payload).encode("utf-8")

    req = urllib.request.Request(url, data=data, headers=headers, method="POST")

    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode())
            top_results = result.get("organic", [])[:3]
            return [
                {
                    "title": r["title"],
                    "link": r["link"],
                    "snippet": r["snippet"]
                } for r in top_results
            ]
    except Exception as e:
        return [{"title": "Error", "snippet": str(e), "link": ""}]


def extraer_info_util(result):
    title = result.get("title", "")
    snippet = result.get("snippet", "")
    link = result.get("link", "")

    texto = f"{title} {snippet}"

    # 1. Buscar descuento
    match_descuento = re.search(r"(\d{1,3})\s?%|(\d{1,3})\s?(por ciento|dscto)", texto.lower())
    descuento = match_descuento.group(0) if match_descuento else "No especificado"

    # 2. Buscar marca (simplificado, se puede hacer mejor con lista de marcas conocidas)
    posibles_marcas = re.findall(r"\b([A-Z][a-zA-Z]{2,})\b", title)
    marca = posibles_marcas[0] if posibles_marcas else "No identificada"

    # 3. Buscar tienda en el dominio del link
    match_tienda = re.search(r"https?://(?:www\.)?([^/.]+)", link)
    tienda = match_tienda.group(1) if match_tienda else "No detectada"

    return {
        "descuento": descuento,
        "marca": marca,
        "tienda": tienda
    }