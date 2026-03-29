// server.js
const express = require('express');
const app = express();

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

// Puerto dinámico para Render
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Servidor escuchando en puerto ${PORT}`);
});
