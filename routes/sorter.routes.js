module.exports = app => {
  const sorters = require("../controller/sorter.controller.js");

  // INDEX - Retrieve all sorter
  app.get("/sorters", sorters.findAll);

  // NEW - Show new form
  app.get("/sorters/new",function(req,res){
        res.render("sorters/new");
  });

  // CREATE - add new sorter
  app.post("/sorters", sorters.create);

  // SHOW - Retrieve a single sorter with sorterId
  app.get("/sorters/:Id",  sorters.findOne);

  // EDIT - Retrieve a single sorter with sorterId to edit entries
  app.get("/sorters/:Id/edit", sorters.editOne);
  
  // UPDATE - Update a sorter with sorterId
  app.put("sorters/:Id", sorters.update);
  
  // DELETE - Delete a sorter with sorterId
  app.delete("/sorters/:Id", sorters.delete);

  // DESTROY - Delete all sorters
  app.delete("/sorters", sorters.deleteAll);
};