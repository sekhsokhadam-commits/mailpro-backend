import os
import psycopg2
from flask import Flask, request, jsonify

app = Flask(__name__)

# Conexión ultra-segura a la base de datos
def get_db_connection():
    try:
        db_url = os.getenv('DATABASE_URL')
        if not db_url:
            return None
        return psycopg2.connect(db_url)
    except Exception as e:
        print(f"Error de conexión: {e}")
        return None

@app.route('/')
def home():
    return "✅ Sistema MailPro Operativo"

@app.route('/track', methods=['POST'])
def track_lead():
    data = request.json
    if not data or 'email' not in data:
        return jsonify({"status": "error", "message": "Email faltante"}), 400
    
    email = data.get('email')
    conn = get_db_connection()
    
    if conn:
        try:
            cur = conn.cursor()
            cur.execute('INSERT INTO leads (email) VALUES (%s)', (email,))
            conn.commit()
            cur.close()
            conn.close()
            return jsonify({"status": "success"}), 200
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500
    return jsonify({"status": "error", "message": "DB offline"}), 500

if __name__ == "__main__":
    # Railway inyecta el puerto automáticamente aquí
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
