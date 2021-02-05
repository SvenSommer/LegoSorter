const recognisedpart = require("../controller/recognisedpart.controller.js");

module.exports = app => {
  // Create
  app.post("/recognisedpart", recognisedpart.label);
  // EDIT - Retrieve a single recognisedpart with recognisedpartId to edit images
  app.get("/recognisedpart/:Id/edit", recognisedpart.editOne);
  // Delete
  app.delete("/recognisedpart/:Id", recognisedpart.delete);
};