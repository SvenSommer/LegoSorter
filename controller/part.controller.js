const Subset = require("../models/subset.model.js");


// Retrieve all parts from the database.
exports.findAll = (req, res) => {
  Subset.getAll((err, data) => {
    if (err)
      res.status(500).send({
        message:
          err.message || "Some error occurred while retrieving parts."
      });
    else res.render("parts/index", {subsetData:data});
  });
};