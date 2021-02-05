const partimage = require("../controller/partimage.controller.js");

module.exports = app => {
  // Delete
  app.post("/partimage/delete", partimage.delete);
};