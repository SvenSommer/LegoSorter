module.exports = app => {
  const categories = require("../controller/category.controller.js");

  // INDEX - Show all colors
  app.get("/categories", categories.findAll);
  
  // CREATE - Receive Colors from Bricklink APi
  app.post("/categories", categories.saveAll);
};