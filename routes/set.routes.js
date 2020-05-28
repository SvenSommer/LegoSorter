module.exports = app => {
  const sets = require("../controller/set.controller.js");

  // INDEX - Retrieve all sets
  app.get("/sets", sets.findAll);
  
  // NEW - Show new form
  app.get("/collections/:Id/sets/new", sets.new);
  
  // CREATE - add new set
  app.post("/collections/:Id/sets", sets.create);

  // SHOW - Retrieve a single set with collectionId
  app.get("/sets/:Id",  sets.findOne);

  // EDIT - Retrieve a single set with collectionId to edit entries
  app.get("/sets/:Id/edit", sets.editOne);
  
  // UPDATE - Update a set with collectionId
  app.put("/sets/:Id", sets.update);
  
  // DELETE - Delete a set with collectionId
  app.delete("/sets/:Id", sets.delete);

  // DESTROY - Delete all sets
  app.delete("/sets", sets.deleteAll);
};