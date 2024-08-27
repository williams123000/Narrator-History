import requests

# URL del servidor de LM Studio
url = "http://127.0.0.1:1234/v1/completions"

# Configuración de la solicitud
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer your_api_key_here"  # Solo si tu servidor está protegido con una API Key
}

data = {
    "model": "lmstudio-community/gemma-2-2b-it-Q4_K_M.gguf",  # El identificador del modelo cargado
    "prompt": "Hola, ¿cómo estás?",  # El texto inicial para el completado
    "max_tokens": 50,  # Número máximo de tokens a generar
    "temperature": 0.7  # Ajusta la temperatura para controlar la creatividad
}

# Hacer la solicitud POST
response = requests.post(url, headers=headers, json=data)

# Mostrar el resultado
if response.status_code == 200:
    completion = response.json()
    print("Respuesta:", completion['choices'][0]['text'])
    print("Modelo:", completion['model'])
    print("Tokens generados:", completion['tokens'])
    print("Tiempo de respuesta:", completion['time'])
    
else:
    print(f"Error: {response.status_code}")
    print(response.text)
