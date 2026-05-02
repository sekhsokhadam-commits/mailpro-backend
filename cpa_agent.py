import os
import psycopg2 # Conector para tu PostgreSQL en Railway
import requests

# Configuración usando los datos de tu imagen
DB_CONFIG = {
    "host": "shuttle.proxy.rlwy.net",
    "port": "34359",
    "user": os.getenv("DB_USER"),
    "pass": os.getenv("DB_PASSWORD"),
    "dbname": "railway"
}

def post_to_facebook(message, link):
    """Publica automáticamente en tu página con 1,922 seguidores"""
    page_id = os.getenv("FB_PAGE_ID")
    access_token = os.getenv("FB_ACCESS_TOKEN")
    url = f"https://graph.facebook.com/{page_id}/feed"
    payload = {"message": message, "link": link, "access_token": access_token}
    return requests.post(url, data=payload)

# Ejemplo de flujo: Promocionar tus diseños de calaveras o monos
def run_agent():
    design_link = "https://www.redbubble.com/people/tu-usuario/shop"
    msg = "¡Nuevo diseño disponible! Estilo urbano para los que buscan algo diferente. 💀🔥"
    response = post_to_facebook(msg, design_link)
    print(f"Estado de la publicación: {response.status_code}")

if __name__ == "__main__":
    run_agent()
