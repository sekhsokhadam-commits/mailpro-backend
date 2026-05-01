import os
import psycopg2
from flask import Flask, request, jsonify

app = Flask(__name__)

# Configuración de conexión con manejo de errores robusto
def get_db_connection():
    try:
        # Usa la variable de entorno DATABASE_URL configurada en Railway
        db_url = os.getenv('DATABASE_URL')
        if not db_url:
            print("ERROR: La variable DATABASE_URL no está configurada.")
            return None
        conn = psycopg2.connect(db_url)
        return conn
    except Exception as e:
        print(f"Error crítico al conectar a Postgres: {e}")
        return None

@app.route('/')
def health_check():
    return "✅ CPA Agent MailPro está activo y funcionando."

@app.route('/track', methods=['POST'])
def track_lead():
    data = request.json
    if not data or 'email' not in data:
        return jsonify({"status": "error", "message": "Email requerido"}), 400
    
    email = data.get('email')
    conn = get_db_connection()
    
    if conn:
        try:
            cur = conn.cursor()
            # Asegúrate de que la tabla 'leads' existe en tu base de datos
            cur.execute('INSERT INTO leads (email) VALUES (%s)', (email,))
            conn.commit()
            cur.close()
            conn.close()
            return jsonify({"status": "success", "message": "Lead capturado con éxito"}), 200
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500
    else:
        return jsonify({"status": "error", "message": "No se pudo conectar a la base de datos"}), 500

if __name__ == "__main__":
    # CRÍTICO: Railway requiere leer el puerto de la variable de entorno PORT
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
