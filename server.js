import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import rateLimit from 'express-rate-limit';
import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';

dotenv.config();

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const EMAILS_FILE = path.join(__dirname, 'emails.json');

const app = express();

// Configurar CORS (más restrictivo)
const corsOptions = {
  origin: process.env.ALLOWED_ORIGINS?.split(',') || ['http://localhost:3000', 'http://localhost:3001'],
  credentials: true
};
app.use(cors(corsOptions));

app.use(express.json({ limit: '10kb' }));

// Rate Limiting - protege contra abuso
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutos
  max: 100, // máximo 100 peticiones por ventana
  message: 'Demasiadas solicitudes, intenta más tarde',
  standardHeaders: true,
  legacyHeaders: false,
});

app.use('/collect', limiter);

// Función para validar email
const isValidEmail = (email) => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(String(email).toLowerCase());
};

// Función para guardar emails en archivo JSON
const saveEmail = async (email) => {
  try {
    let emails = [];
    try {
      const data = await fs.readFile(EMAILS_FILE, 'utf8');
      emails = JSON.parse(data);
    } catch (err) {
      // Archivo no existe o está vacío, comenzar con array vacío
      emails = [];
    }

    // Verificar si el email ya existe
    if (!emails.find(e => e.email === email)) {
      emails.push({
        email,
        timestamp: new Date().toISOString()
      });
      await fs.writeFile(EMAILS_FILE, JSON.stringify(emails, null, 2));
    }
    return true;
  } catch (error) {
    console.error(`[${new Date().toISOString()}] Error guardando email:`, error);
    throw error;
  }
};

// Ruta POST /collect - Recolectar emails
app.post("/collect", async (req, res) => {
  try {
    const { email } = req.body;

    // Validar que email existe y es string
    if (!email || typeof email !== 'string') {
      return res.status(400).json({
        success: false,
        message: "Email requerido y debe ser una cadena de texto"
      });
    }

    // Sanitizar email
    const trimmedEmail = email.trim().toLowerCase();

    // Validar formato de email
    if (!isValidEmail(trimmedEmail)) {
      return res.status(400).json({
        success: false,
        message: "Formato de email inválido"
      });
    }

    // Guardar email en archivo
    await saveEmail(trimmedEmail);

    console.log(`[${new Date().toISOString()}] Email registrado:`, trimmedEmail);

    res.status(201).json({
      success: true,
      message: `Email ${trimmedEmail} registrado correctamente`
    });
  } catch (error) {
    console.error(`[${new Date().toISOString()}] Error en /collect:`, error);
    res.status(500).json({
      success: false,
      message: "Error interno del servidor"
    });
  }
});

// Ruta GET para verificar que el servidor está activo
app.get("/", (req, res) => {
  res.json({
    success: true,
    message: "Servidor mailpro-backend está activo",
    timestamp: new Date().toISOString(),
    version: "1.0.0"
  });
});

// Ruta GET para obtener todos los emails (solo para desarrollo/admin)
app.get("/emails", async (req, res) => {
  try {
    const authToken = req.headers.authorization?.replace('Bearer ', '');
    if (authToken !== process.env.ADMIN_TOKEN) {
      return res.status(401).json({
        success: false,
        message: "No autorizado"
      });
    }

    const data = await fs.readFile(EMAILS_FILE, 'utf8');
    const emails = JSON.parse(data || '[]');
    
    res.json({
      success: true,
      count: emails.length,
      emails
    });
  } catch (error) {
    console.error(`[${new Date().toISOString()}] Error obteniendo emails:`, error);
    res.status(500).json({
      success: false,
      message: "Error interno del servidor"
    });
  }
});

// Manejo de rutas no encontradas
app.use((req, res) => {
  res.status(404).json({
    success: false,
    message: "Ruta no encontrada"
  });
});

// Middleware global de manejo de errores
app.use((err, req, res, next) => {
  console.error(`[${new Date().toISOString()}] Error no manejado:`, err);
  res.status(err.status || 500).json({
    success: false,
    message: "Error interno del servidor",
    error: process.env.NODE_ENV === 'development' ? err.message : undefined
  });
});

// Puerto dinámico para Render
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`[${new Date().toISOString()}] 🚀 Servidor escuchando en puerto ${PORT}`);
  console.log(`[${new Date().toISOString()}] 📧 Emails se guardarán en: ${EMAILS_FILE}`);
});