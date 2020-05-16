const Collection = require("../models/collection.model.js");
const Set = require("../models/set.model.js");
const Subset = require("../models/subset.model.js");


// Retrieve all sets from the database.
exports.findAll = (req, res) => {
  Set.getAll((err, data) => {
    if (err)
      res.status(500).send({
        message:
          err.message || "Some error occurred while retrieving sets."
      });
    else res.render("sets/index", {sets:data});
  });
};

// Show new Set form
exports.new = (req, res) => {
  Collection.findById(req.params.Id, (err, collection) => {
    if (err) {
      if (err.kind === "not_found") {
        res.status(404).send({
          message: `Not found collection with id ${req.params.id}.`
        });
      } else {
        res.status(500).send({
          message: "Error retrieving collection with id " + req.params.Id
        });
      }
    } else res.render("sets/new", {collection:collection});
  });
};

// Create and Save a new Set
exports.create = (req, res) => {
   // Validate request
  if (!req.body) {
    res.status(400).send({
      message: "Content can not be empty!"
    });
  }
  if(req.params.Id == "") {
    res.redirect("/collections/"+ req.params.id);
  }
  Collection.findById(req.params.Id, (err, collection) => {
    if (err) {
      if (err.kind === "not_found") {
        res.status(404).send({
          message: `Not found collection with id ${req.params.id}.`
        });
      } else {
        res.status(500).send({
          message: "Error retrieving collection with id " + req.params.Id
        });
      }
    } else {
          // Create a Set
          const set = new Set({
          collection_id: collection.id,
          no: req.body.no,
          comments: req.body.comments,
          instructions: req.body.instructions,
          condition: req.body.condition
        });
      
        // SAVE SET INFORMATION - Save Set info in the database
        Set.create(set, (err, data) => {
          if (err)
            res.status(500).send({
              message:
                err.message || "Some error occurred while creating the Set."
            });
          else res.redirect("/collections/"+ collection.id);  
        });
        
        // PART OUT - Save the Subsets in the database
        Subset.create(req.body.no, (err, data) => {
               if (err)
            res.status(500).send({
              message:
                err.message || "Some error occurred while creating the SubSet."
            });
           else res.redirect("/collections/"+ collection.id); 
        });
      }
  });
 
};

// Find a single Set with a setId
exports.findOne = (req, res) => {
  Set.findById(req.params.Id, (err, set) => {
    if (err) {
      if (err.kind === "not_found") {
        res.status(404).send({
          message: `Not found Set with id ${req.params.id}.`
        });
      } else {
        res.status(500).send({
          message: "Error retrieving Set with id " + req.params.Id
        });
      }
    } else {
      Set.findAllSubsetsBySetId(set.no, (err, subsetData) => {
        res.render("sets/show", {set:set, subsetData:subsetData});
      });
     
    }
  });
};

//Edit Show edit form for Set with id
exports.editOne = (req,res) => {
   Set.findById(req.params.Id, (err, data) => {
    if (err) {
      if (err.kind === "not_found") {
        res.status(404).send({
          message: `Not found Set with id ${req.params.id}.`
        });
      } else {
        res.status(500).send({
          message: "Error retrieving Set with id " + req.params.Id
        });
      }
    } else res.render("sets/edit", {set:data});
  });
};

// Update a Set identified by the setId in the request
exports.update = (req, res) => {
   // Validate Request

  if (!req.body) {
    res.status(400).send({
      message: "Content can not be empty!"
    });
  }
  
  Set.updateById(
    req.params.Id,
    new Set(req.body),
    (err, data) => {
      if (err) {
        if (err.kind === "not_found") {
          res.status(404).send({
            message: `Not found Set with id ${req.params.Id}.`
          });
        } else {
          res.status(500).send({
            message: "Error updating Set with id " + req.params.Id
          });
        }
      } else res.redirect("/sets/"+ req.params.Id);  
    }
  );
};


// Delete a Set with the specified setId in the request
exports.delete = (req, res) => {
  Set.remove(req.params.Id, (err, data) => {
    if (err) {
      if (err.kind === "not_found") {
        res.status(404).send({
          message: `Not found Set with id ${req.params.Id}.`
        });
      } else {
        res.status(500).send({
          message: "Could not delete Set with id " + req.params.Id
        });
      }
    } else res.redirect("/collections");
  });
};

// Delete all Sets from the database.
exports.deleteAll = (req, res) => {
  Set.removeAll((err, data) => {
    if (err)
      res.status(500).send({
        message:
          err.message || "Some error occurred while removing all Sets."
      });
    else res.redirect("/sets");
  });
};