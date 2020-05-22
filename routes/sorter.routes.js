module.exports = app => {
  const sorters = require("../controller/sorter.controller.js");

  // NEW - Show new form
  app.get("/sorters/new",function(req,res){
        res.render("sorters/new");
  });

  // CREATE - add new collection
  app.post("/sorters", sorters.create);

  // SHOW - Retrieve a single collection with collectionId
  app.get("/sorters/:Id",  sorters.findOne);

  // EDIT - Retrieve a single collection with collectionId to edit entries
  app.get("/sorters/:Id/edit", sorters.editOne);
  
  // UPDATE - Update a collection with collectionId
  app.put("sorters/:Id", sorters.update);
  
  // DELETE - Delete a collection with collectionId
  app.delete("/sorters/:Id", sorters.delete);

  // DESTROY - Delete all collections
  app.delete("/sorters", sorters.deleteAll);
};