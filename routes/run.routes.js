module.exports = app => {
  const runs = require("../controller/run.controller.js");

  // INDEX - Retrieve all runs
  app.get("/runs", runs.findAll);

  // NEW - Show new form
  app.get("/collections/:Id/runs/new", runs.new);

  // CREATE - add new run
  app.post("/collections/:Id/runs", runs.create);

  // SHOW - Retrieve a single run with runId
  app.get("/runs/:Id",  runs.findOne);

  // EDIT - Retrieve a single run with runId to edit entries
  app.get("/runs/:Id/edit", runs.editOne);
  
  // UPDATE - Update a run with sorterId
  app.put("runs/:Id", runs.update);
  
  // DELETE - Delete a run with sorterId
  app.delete("/runs/:Id", runs.delete);

  // DESTROY - Delete all runs
  app.delete("/runs", runs.deleteAll);
};