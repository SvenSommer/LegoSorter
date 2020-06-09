module.exports = app => {
  const parts = require("../controller/part.controller.js");

  // INDEX - Retrieve all parts
  app.get("/parts", parts.findAll);

};