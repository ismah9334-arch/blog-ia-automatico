import os
import json
import requests
import google.generativeai as genai

# Configuración
API_KEY = os.environ.get("GEMINI_API_KEY")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
DATA_FILE = "data.json"

if not API_KEY:
    print("Error: Falta la GEMINI_API_KEY")
    exit(1)

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

prompt = """
Eres un experto en SEO y marketing de afiliados. Escribe un artículo de blog sobre una herramienta SaaS de Inteligencia Artificial que no esté ya en nuestra lista.
El formato de salida DEBE ser estrictamente un JSON válido con esta estructura:
{
  "slug": "url-amigable-del-tema",
  "title": "Título SEO Atractivo",
  "description": "Meta descripción corta",
  "content": "<article><h1>Título</h1><p>Contenido detallado...</p><a href='#' class='btn-affiliate'>Prueba la herramienta aquí</a></article>"
}
No devuelvas Markdown rodeando el JSON, solo devuelve el objeto JSON puro.
"""

def notificar_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": mensaje}
    requests.post(url, json=payload)

try:
    print("Invocando a la IA...")
    response = model.generate_content(prompt)
    raw_text = response.text.strip()
    
    if raw_text.startswith("```json"):
        raw_text = raw_text[7:-3].strip()
        
    nuevo_articulo = json.loads(raw_text)
    
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        articulos = json.load(f)
        
    articulos.append(nuevo_articulo)
    
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(articulos, f, ensure_ascii=False, indent=2)
        
    print(f"Artículo generado exitosamente: {nuevo_articulo['title']}")
    
    if len(articulos) >= 50 and len(articulos) < 52:
        notificar_telegram(f"¡Masa crítica alcanzada! Tenemos {len(articulos)} artículos listos en la nube para monetizar. Es tu turno.")
        
except Exception as e:
    print(f"Error generando artículo: {e}")
    exit(1)
