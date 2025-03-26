import json
import requests

def lambda_handler(event, context):
    query = event.get("query", "últimas ofertas")
    api_key = "4678aa15ca9d8b698d5194cc6ee21634c00500427732ac050f68afe8b05530ce"
    api_url = f"https://serpapi.com/search.json?q={query}&hl=es&gl=pe&api_key={api_key}"

    try:
        response = requests.get(api_url)
        data = response.json()

        if "organic_results" in data:
            resultados = []
            for result in data["organic_results"][:3]:
                resultados.append(f"{result['title']} - {result['link']}")

            resultado_final = "\n".join(resultados)
        else:
            resultado_final = "No se encontraron resultados relevantes."

    except Exception as e:
        resultado_final = f"Error al obtener información: {str(e)}"

    return {
        "statusCode": 200,
        "body": json.dumps({"response": resultado_final})
    }
