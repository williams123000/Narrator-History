import requests

# URL del servidor de LM Studio
url = "http://localhost:1234/v1/chat/completions"

# Encabezados de la solicitud
headers = {
    "Content-Type": "application/json"
}

# Cuerpo de la solicitud
data = {
    "model": "lmstudio-community/gemma-2-2b-it-GGUF/gemma-2-2b-it-Q4_K_M.gguf",
    "messages": [
        {"role": "system", "content": "Recuerda que puedes preguntarme cualquier cosa."},
        {"role": "user", "content": "Como estas?"},
    ],
    "temperature": 0.7,
    "max_tokens": -1,
    "stream": False
}

# Realizar la solicitud POST
response = requests.post(url, headers=headers, json=data)

# Mostrar el resultado
if response.status_code == 200:
    completion = response.json()
    print("Respuesta:", completion['choices'][0]['message']['content'])
else:
    print(f"Error: {response.status_code}")
    print(response.text)
