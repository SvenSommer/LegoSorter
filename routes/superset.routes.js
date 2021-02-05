module.exports = app => {
    const supersets = require("../controller/superset.controller.js");
  
    app.get("/supersets/:Id/create", supersets.getOrCreate);
  };