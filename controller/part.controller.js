const Subset = require("../models/subset.model.js");


// Retrieve all parts from the database.
exports.findAllParts = (req, res) => {
  Subset.getAllParts((err, data) => {
    if (err)
      res.status(500).send({
        message:
          err.message || "Some error occurred while retrieving parts."
      });
    else res.render("parts/index", {subsetData:data});
  });
};

// Retrieve all minifigs from the database.
exports.findAllMinifigs = (req, res) => {
  Subset.getAllMinifigs((err, data) => {
    if (err)
      res.status(500).send({
        message:
          err.message || "Some error occurred while retrieving minifigs parts."
      });
    else res.render("parts-minifigs/index", {subsetData:data});
  });
};

exports.findOneMinifig = (req, res) => {
  Subset.getMinifigById((err, part) => {
    if (err)
      res.status(500).send({
        message:
          err.message || "Some error occurred while retrieving mionifig parts with id."
      });
    else res.render("parts-minifigs/show", {part:part});
  });
};
