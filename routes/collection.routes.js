module.exports = app => {
  const collections = require("../controller/collection.controller.js");

  // INDEX - Retrieve all collections
  app.get("/collections", collections.findAll);
  
  // NEW - Show new form
  app.get("/collections/new",function(req,res){
        res.render("collection/new");
  });
  
  // CREATE - add new collection
  app.post("/collections", collections.create);

  // SHOW - Retrieve a single collection with collectionId
  app.get("/collections/:Id", collections.findOne);

  // SHOW - Retrieve a single collection with collectionId
  app.get("/collections/:Id/edit", collections.findOne);
  
  // UPDATE - Update a collection with collectionId
  app.put("/collections/:Id", collections.update);

  // DELETE - Delete a collection with collectionId
  app.delete("/collections/:Id", collections.delete);

  // DESTROY - Delete all collections
  app.delete("/collections", collections.deleteAll);
};