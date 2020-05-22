const Sorter = require("../models/sorter.model.js");

// Retrieve all Sorters from the database.
exports.findAll = (req, res) => {
  Sorter.getAll((err, sorter) => {
    if (err)
      res.status(500).send({
        message:
          err.message || "Some error occurred while retrieving sorters."
      });
    else res.render("sorter/index", {sorter:sorter});
  });
};

// Create and Save a new Sorter
exports.create = (req, res) => {
   // Validate request
  if (!req.body) {
    res.status(400).send({
      message: "Content can not be empty!"
    });
  }
  // Create a Sorter
  const sorter = new Sorter({
    name: req.body.name,
    separate_conveyor_mode_url: req.body.separate_conveyor_mode_url,
    separate_conveyor_speed_url: req.separate_conveyor_speed_url,
    separate_conveyor_status_url: req.body.separate_conveyor_status_url,
    vibration_motor_mode_url: req.body.vibration_motor_mode_url,
    vibration_motor_speed_url: req.body.vibration_motor_speed_url,
    vibration_motor_status_url: req.body.vibration_motor_status_url,
    dispense_conveyor_mode_url: req.body.dispense_conveyor_mode_url,
    dispense_conveyor_speed_url: req.body.dispense_conveyor_speed_url,
    dispense_conveyor_status_url: req.body.dispense_conveyor_status_url,
    pusher_count: req.body.pusher_count,
    pusher_status_baseurl: req.body.pusher_status_baseurl,
    pusher_mode_baseurl: req.body.pusher_mode_baseurl
  });

  // Save Sorter in the database
  Sorter.create(sorter, (err, data) => {
    if (err)
      res.status(500).send({
        message:
          err.message || "Some error occurred while creating the Sorter."
      });
    else res.redirect("/sorters");  
  });
};



// Find a single Sorter with a sorterId
exports.findOne = (req, res) => {
  Sorter.findById(req.params.Id, (err, data) => {
    if (err) {
      if (err.kind === "not_found") {
        res.status(404).send({
          message: `Not found Sorter with id ${req.params.id}.`
        });
      } else {
        res.status(500).send({
          message: "Error retrieving Sorter with id " + req.params.Id
        });
      }
    } else {
        res.render("sorters/show", {sorter:data });
    }
  });
};

//Edit Show edit form for Sorter with id
exports.editOne = (req,res) => {
   Sorter.findById(req.params.Id, (err, data) => {
    if (err) {
      if (err.kind === "not_found") {
        res.status(404).send({
          message: `Not found Sorter with id ${req.params.id}.`
        });
      } else {
        res.status(500).send({
          message: "Error retrieving Sorter with id " + req.params.Id
        });
      }
    } else { 
      res.render("sorters/edit", {sorter:data});
    }
  });
};

// Update a Sorter identified by the sorterId in the request
exports.update = (req, res) => {
   // Validate Request

  if (!req.body) {
    res.status(400).send({
      message: "Content can not be empty!"
    });
  }
  
  Sorter.updateById(
    req.params.Id,
    new Sorter(req.body),
    (err, data) => {
      if (err) {
        if (err.kind === "not_found") {
          res.status(404).send({
            message: `Not found Sorter with id ${req.params.Id}.`
          });
        } else {
          res.status(500).send({
            message: "Error updating Sorter with id " + req.params.Id
          });
        }
      } else res.redirect("/sorters/"+ req.params.Id);  
    }
  );
};


// Delete a Sorter with the specified sorterId in the request
exports.delete = (req, res) => {
  Sorter.remove(req.params.Id, (err, data) => {
    if (err) {
      if (err.kind === "not_found") {
        res.status(404).send({
          message: `Not found Sorter with id ${req.params.Id}.`
        });
      } else {
        res.status(500).send({
          message: "Could not delete Sorter with id " + req.params.Id
        });
      }
    } else res.redirect("/sorters");
  });
};

// Delete all Sorters from the database.
exports.deleteAll = (req, res) => {
  Sorter.removeAll((err, data) => {
    if (err)
      res.status(500).send({
        message:
          err.message || "Some error occurred while removing all Sorters."
      });
    else res.redirect("/sorters");
  });
};