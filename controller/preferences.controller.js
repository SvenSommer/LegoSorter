const Sorter = require("../models/sorter.model.js");

// Retrieve all Collections from the database.
exports.findOne = (req, res) => {
   Sorter.getAll((err, sorter) => {
    if (err)
      res.status(500).send({
        message:
          err.message || "Some error occurred while retrieving sorters."
      });
    else
    res.render("preferences/show", {sorter:sorter});
   });
};