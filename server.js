import express from "express";
const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());

app.post("/save-email", (req, res) => {
  const email = req.body.email;
  console.log("Email recibido:", email);
  res.json({ status: "ok" });
});

app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
