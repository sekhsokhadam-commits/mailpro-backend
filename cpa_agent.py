import os
import psycopg2
from flask import Flask, request, jsonify, redirect
import hashlib

app = Flask(__name__)

# CONFIG

DATABASE_URL = os.environ.get ("DATABASE_URL")
SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")
FROM_EMAIL = os.environ.get("FROM_EMAIL", "noreply@mailpro.com")
FROM_NAME = os.environ.get("FROM_NAME", "MailPro")
PORT = int(os.environ.get("PORT", 8080))

AFFILIATE_LINKS = {
"oferta1": "https://go.hotmart.com/H101177980R",
"oferta2": "https://go.hotmart.com/H101177980R",
"oferta3": "https://go.hotmart.com/H101177980R",
}

# BASE DE DATOS

def get_db():
try:
conn = psycopg2.connect(DATABASE_URL)
return conn
except Exception as e:
print("[DB ERROR] " + str(e))
return None

def init_db():
conn = get_db()
if not conn:
print(”[ERROR] No se pudo conectar a la base de datos.”)
return
try:
cur = conn.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS leads (
id SERIAL PRIMARY KEY,
email VARCHAR(255) UNIQUE NOT NULL,
nombre VARCHAR(255),
ip VARCHAR(100),
fuente VARCHAR(255),
creado_en TIMESTAMP DEFAULT NOW(),
email_enviado BOOLEAN DEFAULT FALSE,
ultimo_email TIMESTAMP
);
""")
cur.execute("""
CREATE TABLE IF NOT EXISTS clicks (
id SERIAL PRIMARY KEY,
lead_email VARCHAR(255),
oferta VARCHAR(100),
ip VARCHAR(100),
creado_en TIMESTAMP DEFAULT NOW()
);
""")
conn.commit()
cur.close()
conn.close()
print("[DB] Tablas listas.")
except Exception as e:
print("[DB INIT ERROR] " + str(e))

# ENVIO DE EMAIL

def enviar_email_bienvenida(email, nombre=""):
if not SENDGRID_API_KEY:
print(”[EMAIL] SENDGRID_API_KEY no configurada.")
return False
try:
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

```
    nombre_display = nombre if nombre else "amigo/a"
    afiliado_url = AFFILIATE_LINKS.get("oferta1")
    ref = hashlib.md5(email.encode()).hexdigest()[:8]

    html_content = """
    <html>
    <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
        <h1 style="color: #2c3e50;">Bienvenido/a """ + nombre_display + """!</h1>
        <p>Gracias por registrarte. Tenemos algo especial para ti:</p>
        <div style="background: #f8f9fa; border-left: 4px solid #e74c3c; padding: 20px; margin: 20px 0;">
            <h2 style="color: #e74c3c;">Oferta Exclusiva</h2>
            <p>Hemos seleccionado esta oportunidad especialmente para ti.</p>
            <a href='""" + afiliado_url + """?ref=""" + ref + """'
               style="background:#e74c3c;color:white;padding:12px 24px;text-decoration:none;border-radius:5px;display:inline-block;">
               Ver Oferta
            </a>
        </div>
        <p style="color: #7f8c8d; font-size: 12px;">
            MailPro - Marketing Automatico
        </p>
    </body>
    </html>
    """

    message = Mail(
        from_email=(FROM_EMAIL, FROM_NAME),
        to_emails=email,
        subject="Tu oferta exclusiva esta aqui!",
        html_content=html_content
    )
    sg = SendGridAPIClient(SENDGRID_API_KEY)
    sg.send(message)
    print("[EMAIL] Enviado a " + email)
    return True
except Exception as e:
    print("[EMAIL ERROR] " + str(e))
    return False
```

def _marcar_email_enviado(email):
conn = get_db()
if not conn:
return
try:
cur = conn.cursor()
cur.execute(
“UPDATE leads SET email_enviado=TRUE, ultimo_email=NOW() WHERE email=%s”,
(email,)
)
conn.commit()
cur.close()
conn.close()
except Exception as e:
print(”[MARCAR ERROR] “ + str(e))

# RUTAS

@app.route("/")
def health():
return jsonify({
"status": "MailPro CPA Agent activo",
"version": "1.0.0",
"sendgrid_configurado": bool(SENDGRID_API_KEY),
"db_configurada": bool(DATABASE_URL),
"endpoints": ["/register", "/track/<oferta>", “stats”, “/leads”]
})

@app.route("/register", methods=["POST”, "/OPTIONS"])
def register():
if request.method == "OPTIONS":
return _cors_preflight()

```
data = request.get_json(silent=True) or request.form
email = (data.get("email") or "").strip().lower()
nombre = (data.get("nombre") or data.get("name") or "").strip()
fuente = data.get("fuente") or data.get("source") or request.referrer or "directo"
ip = request.headers.get("X-Forwarded-For", request.remote_addr)

if not email or "@" not in email:
    return jsonify({"status": "error", "mensaje": "Email invalido"}), 400

conn = get_db()
if not conn:
    return jsonify({"status": "error", "mensaje": "Error de base de datos"}), 500

try:
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO leads (email, nombre, ip, fuente) VALUES (%s, %s, %s, %s) ON CONFLICT (email) DO NOTHING RETURNING id",
        (email, nombre, ip, fuente)
    )
    result = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    if result:
        enviado = enviar_email_bienvenida(email, nombre)
        if enviado:
            _marcar_email_enviado(email)
        return _cors_response(jsonify({
            "status": "success",
            "mensaje": "Registro exitoso",
            "email_enviado": enviado
        }))
    else:
        return _cors_response(jsonify({
            "status": "duplicado",
            "mensaje": "Este email ya esta registrado"
        }))

except Exception as e:
    print("[REGISTER ERROR] " + str(e))
    return jsonify({"status": "error", "mensaje": str(e)}), 500
```

@app.route(”/track/<oferta>”)
def track_click(oferta):
ip = request.headers.get(“X-Forwarded-For”, request.remote_addr)
email_ref = request.args.get(“ref”, “anonimo”)

```
conn = get_db()
if conn:
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO clicks (lead_email, oferta, ip) VALUES (%s, %s, %s)",
            (email_ref, oferta, ip)
        )
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print("[TRACK ERROR] " + str(e))

destino = AFFILIATE_LINKS.get(oferta)
if not destino:
    return jsonify({"error": "Oferta no encontrada"}), 404

return redirect(destino)
```

@app.route(”/stats”)
def stats():
conn = get_db()
if not conn:
return jsonify({“error”: “Sin conexion a DB”}), 500

```
try:
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM leads")
    total_leads = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM leads WHERE email_enviado=TRUE")
    emails_enviados = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM clicks")
    total_clicks = cur.fetchone()[0]

    cur.execute("SELECT oferta, COUNT(*) as clicks FROM clicks GROUP BY oferta ORDER BY clicks DESC")
    clicks_por_oferta = [{"oferta": r[0], "clicks": r[1]} for r in cur.fetchall()]

    cur.execute("SELECT COUNT(*) FROM leads WHERE creado_en > NOW() - INTERVAL '24 hours'")
    leads_hoy = cur.fetchone()[0]

    cur.close()
    conn.close()

    return jsonify({
        "total_leads": total_leads,
        "emails_enviados": emails_enviados,
        "total_clicks": total_clicks,
        "leads_hoy": leads_hoy,
        "clicks_por_oferta": clicks_por_oferta
    })
except Exception as e:
    return jsonify({"error": str(e)}), 500
```

@app.route(”/leads”)
def get_leads():
conn = get_db()
if not conn:
return jsonify({“error”: “Sin conexion a DB”}), 500

```
try:
    cur = conn.cursor()
    cur.execute("""
        SELECT email, nombre, fuente, creado_en, email_enviado
        FROM leads ORDER BY creado_en DESC LIMIT 50
    """)
    leads = [{
        "email": r[0],
        "nombre": r[1],
        "fuente": r[2],
        "registrado": r[3].isoformat() if r[3] else None,
        "email_enviado": r[4]
    } for r in cur.fetchall()]
    cur.close()
    conn.close()
    return jsonify({"leads": leads, "total": len(leads)})
except Exception as e:
    return jsonify({"error": str(e)}), 500
```

# CORS

def _cors_preflight():
resp = app.make_default_options_response()
resp.headers[“Access-Control-Allow-Origin”] = “*”
resp.headers[“Access-Control-Allow-Methods”] = “POST, GET, OPTIONS”
resp.headers[“Access-Control-Allow-Headers”] = “Content-Type”
return resp

def _cors_response(response):
response.headers[“Access-Control-Allow-Origin”] = “*”
return response

@app.after_request
def add_cors(response):
response.headers[“Access-Control-Allow-Origin”] = “*”
return response

# INICIO

if **name** == “**main**”:
init_db()
app.run(host=“0.0.0.0”, port=PORT)