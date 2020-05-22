module.exports = app => {
  const preferences = require("../controller/preferences.controller.js");

  // INDEX - Show all colors
  app.get("/preferences", preferences.findOne);
};