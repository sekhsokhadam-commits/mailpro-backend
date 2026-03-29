// server.js
import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';

dotenv.config();

const app = express();

// Configurar CORS
app.use(cors());

app.use(express.json());

// Ruta POST /collect
app.post("/collect", (req, res) => {
  const { email } = req.body;

  if (!email) {
    return res.status(400).json({
      success: false,
      message: "Email requerido"
    });
  }

  console.log("Email recibido:", email);

  res.json({
    success: true,
    message: `Email ${email} guardado`
  });
});

// Ruta GET para verificar que el servidor está activo
app.get("/", (req, res) => {
  res.json({
    success: true,
    message: "Servidor mailpro-backend está activo"
  });
});

// Puerto dinámico para Render
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Servidor escuchando en puerto ${PORT}`);
});