const Collection = require("../models/collection.model.js");

// Create and Save a new Collection
exports.create = (req, res) => {
   // Validate request
  if (!req.body) {
    res.status(400).send({
      message: "Content can not be empty!"
    });
  }
  var date = new Date().toISOString().slice(0, 19).replace('T', ' ');
  // Create a Collection
  const customer = new Collection({
    name: req.body.name,
    weight_kg: req.body.weight_kg,
    origin: req.body.origin,
    origin_url: req.body.origin_url,
    seller: req.body.seller,
    description: req.body.description,
    purchase_date: req.body.purchase_date,
    cost: req.body.cost,
    porto: req.body.porto,
    thumbnail_url: req.body.thumbnail_url,
    created: date
  });

  // Save Collection in the database
  Collection.create(customer, (err, data) => {
    if (err)
      res.status(500).send({
        message:
          err.message || "Some error occurred while creating the Collection."
      });
    else  res.redirect("/collections");  
  });
};

// Retrieve all Collections from the database.
exports.findAll = (req, res) => {
  Collection.getAll((err, data) => {
    if (err)
      res.status(500).send({
        message:
          err.message || "Some error occurred while retrieving collections."
      });
    else res.render("collection/index", {collections:data});
  });
};

// Find a single Collection with a collectionId
exports.findOne = (req, res) => {
  Collection.findById(req.params.Id, (err, data) => {
    if (err) {
      if (err.kind === "not_found") {
        res.status(404).send({
          message: `Not found Customer with id ${req.params.id}.`
        });
      } else {
        res.status(500).send({
          message: "Error retrieving Customer with id " + req.params.Id
        });
      }
    } else res.render("collection/show", {collection:data});
  });
};

// Update a Collection identified by the collectionId in the request
exports.update = (req, res) => {
  
};

// Delete a Collection with the specified collectionId in the request
exports.delete = (req, res) => {
  
};

// Delete all Collections from the database.
exports.deleteAll = (req, res) => {
  
};