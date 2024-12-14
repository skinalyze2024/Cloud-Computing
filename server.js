const express = require("express");
const app = express();
const axios = require("axios"); // Untuk meneruskan request ke Flask

// Endpoint untuk autentikasi
const authRoutes = require("./routes/auth");
app.use("/", authRoutes);

// Endpoint untuk prediksi (proxy ke Flask)
app.post("/predict", async (req, res) => {
  try {
    const response = await axios.post(
      "http://localhost:8080/predict",
      req.body,
      {
        headers: req.headers,
      }
    );
    res.status(response.status).send(response.data);
  } catch (error) {
    res.status(500).send({ error: "Failed to connect to prediction service" });
  }
});

const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
