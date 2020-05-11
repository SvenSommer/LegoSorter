const mysql = require("mysql");
const dbConfig = require("../config/db.config.js");

// Create a connection to the database
const connection = mysql.createConnection({
  host: "localhost",
  user: "WebDBUser",
  password: "qF2J%9a84zU",
  database: "LegoSorterDB"
});

connection.connect(function(err) {
  if (err) throw err;
      console.log("Database connected!");
});

module.exports = connection;
