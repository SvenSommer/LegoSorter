const Collection = require("../models/collection.model.js");
const Subset = require("../models/subset.model.js");

// Retrieve all Collections from the database.
exports.findAll = (req, res) => {
  Collection.getAll((err, data) => {
    if (err)
      res.status(500).send({
        message:
          err.message || "Some error occurred while retrieving collections."
      });
    else res.render("collections/index", {collections:data});
  });
};

// Create and Save a new Collection
exports.create = (req, res) => {
   // Validate request
  if (!req.body) {
    res.status(400).send({
      message: "Content can not be empty!"
    });
  }
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
  });

  // Save Collection in the database
  Collection.create(customer, (err, data) => {
    if (err)
      res.status(500).send({
        message:
          err.message || "Some error occurred while creating the Collection."
      });
    else res.redirect("/collections");  
  });
};



// Find a single Collection with a collectionId
exports.findOne = (req, res) => {
  Collection.findById(req.params.Id, (err, data) => {
    if (err) {
      if (err.kind === "not_found") {
        res.status(404).send({
          message: `Not found Collection with id ${req.params.id}.`
        });
      } else {
        res.status(500).send({
          message: "Error retrieving Collection with id " + req.params.Id
        });
      }
    } else {
        Collection.findAllSetsByCollectionId(req.params.Id, (err, sets) => {
          sets.forEach(function(set){
             Subset.CountPartsBySetNo(set.no, (err, partcounts) => {
              if (err) {
                res.status(500).send({
                message: "Error retrieving PartCount for Setid " + req.params.Id
                });
              } else{
                Subset.CountMinifigsBySetNo(set.no, (err, minifigscount) => {
                if (err) {
                  res.status(500).send({
                  message: "Error retrieving Minifigs Count for Setid " + req.params.Id
                  });
                } 
                  
                });
              } // 
            }); //Count parts
          
          }); // sets for each
           Collection.SumallSetInfosByCollectionId(req.params.Id, (err, setssum) => {
            if (err) {
                
                res.status(500).send({
                message: "Error retrieving setsCount for collectionid " + req.params.Id
                });
              } else{
                console.log(setssum)
                res.render("collections/show", {collection:data, sets : sets,setssum:setssum });
              }
             
           });
      });
      
    }
  
  });
};

//Edit Show edit form for Collection with id
exports.editOne = (req,res) => {
   Collection.findById(req.params.Id, (err, data) => {
    if (err) {
      if (err.kind === "not_found") {
        res.status(404).send({
          message: `Not found Collection with id ${req.params.id}.`
        });
      } else {
        res.status(500).send({
          message: "Error retrieving Collection with id " + req.params.Id
        });
      }
    } else { 
      res.render("collections/edit", {collection:data});
      
    }
  });
};

// Update a Collection identified by the collectionId in the request
exports.update = (req, res) => {
   // Validate Request

  if (!req.body) {
    res.status(400).send({
      message: "Content can not be empty!"
    });
  }
  
  Collection.updateById(
    req.params.Id,
    new Collection(req.body),
    (err, data) => {
      if (err) {
        if (err.kind === "not_found") {
          res.status(404).send({
            message: `Not found Collection with id ${req.params.Id}.`
          });
        } else {
          res.status(500).send({
            message: "Error updating Collection with id " + req.params.Id
          });
        }
      } else res.redirect("/collections/"+ req.params.Id);  
    }
  );
};


// Delete a Collection with the specified collectionId in the request
exports.delete = (req, res) => {
  Collection.remove(req.params.Id, (err, data) => {
    if (err) {
      if (err.kind === "not_found") {
        res.status(404).send({
          message: `Not found Collection with id ${req.params.Id}.`
        });
      } else {
        res.status(500).send({
          message: "Could not delete Collection with id " + req.params.Id
        });
      }
    } else res.redirect("/collections");
  });
};

// Delete all Collections from the database.
exports.deleteAll = (req, res) => {
  Collection.removeAll((err, data) => {
    if (err)
      res.status(500).send({
        message:
          err.message || "Some error occurred while removing all Collections."
      });
    else res.redirect("/collections");
  });
};