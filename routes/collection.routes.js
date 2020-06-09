module.exports = app => {
  const collections = require("../controller/collection.controller.js");

  // INDEX - Retrieve all collections
  app.get("/collections", collections.findAll);
  
  // NEW - Show new form
  app.get("/collections/new",function(req,res){
        res.render("collections/new");
  });
  
  // CREATE - add new collection
  app.post("/collections", collections.create);

  // SHOW - Retrieve a single collection with collectionId
  app.get("/collections/:Id",  collections.findOne);

  // EDIT - Retrieve a single collection with collectionId to edit entries
  app.get("/collections/:Id/edit", collections.editOne);
  
  // UPDATE - Update a collection with collectionId
  app.put("/collections/:Id", collections.update);
  
  // DELETE - Delete a collection with collectionId
  app.delete("/collections/:Id", collections.delete);

  // DESTROY - Delete all collections
  app.delete("/collections", collections.deleteAll);
};