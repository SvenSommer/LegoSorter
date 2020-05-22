module.exports = app => {
  const colors = require("../controller/color.controller.js");

  // INDEX - Show all colors
  app.get("/colors", colors.findAll);
  
  // CREATE - Receive Colors from Bricklink APi
  app.post("/colors", colors.saveAll);
};