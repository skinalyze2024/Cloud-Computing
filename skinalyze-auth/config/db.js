// Localhost
const mysql = require("mysql2");

const db = mysql.createConnection({
  host: "localhost", 
  user: "root", 
  password: "", 
  database: "skinalyze", 
});

db.connect((err) => {
  if (err) {
    console.error("Koneksi Database Gagal Bro:", err.stack);
    return;
  }
  console.log("Koneksi Database Berhasil Bro.");
});

module.exports = db;


// GCP
// const mysql = require("mysql2");

// const db = mysql.createConnection({
//   host: "34.128.84.0",
//   user: "root",
//   password: "12345db",
//   database: "skinalyze",
//   port: 3306,
// });

// db.connect((err) => {
//   if (err) {
//     console.error("Koneksi Database Gagal Bro:", err.stack);
//     return;
//   }
//   console.log("Koneksi Database Berhasil Bro.");
// });

// module.exports = db;