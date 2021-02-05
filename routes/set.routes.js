module.exports = app => {
  const sets = require("../controller/set.controller.js");

  // INDEX - Retrieve all sets
  app.get("/sets", sets.findAll);
  
  // NEW - Show new form
  app.get("/sets/:Id/download", sets.download);
  

  // SHOW - Retrieve a single set with collectionId
  app.get("/sets/:Id",  sets.findOne);

  
};