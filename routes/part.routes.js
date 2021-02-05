module.exports = app => {
  const parts = require("../controller/part.controller.js");

  // INDEX - Retrieve all parts
  app.get("/parts", parts.findAllParts);
  
  app.get("/parts-minifigs", parts.findAllMinifigs);

  // SHOW - Retrieve a single collection with collectionId
  app.get("/parts-minifigs/:Id",  parts.findOneMinifig);
}