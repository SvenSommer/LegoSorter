module.exports = app => {
    const recognisedset = require("../controller/recognisedset.controller.js");
      
    // NEW - Show new form
    app.get("/collections/:Id/recognisedsets/new", recognisedset.new);
    
    // CREATE - add new set
    app.post("/collections/:Id/recognisedsets", recognisedset.create);
  
    // EDIT - Retrieve a single set with collectionId to edit entries
    app.get("/recognisedsets/:Id/edit", recognisedset.editOne);
    
    // UPDATE - Update a set with collectionId
    app.put("/recognisedsets/:Id", recognisedset.update);
    
    // DELETE - Delete a set with collectionId
    app.delete("/recognisedsets/:Id", recognisedset.delete);
  };