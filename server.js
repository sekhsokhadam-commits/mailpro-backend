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
