const Collection = require("../models/collection.model.js");
const Run = require("../models/run.model.js");
const Partimage = require("../models/partimage.model.js");
const { exec } = require('child_process');


// Retrieve all Runs from the database.
exports.findAll = (req, res) => {
  Run.getAll((err, runs) => {
    if (err)
      res.status(500).send({
        message:
          err.message || "Some error occurred while retrieving sets."
      });
    else res.render("runs/index", {runs:runs});
  });
};

// Show new Run form
exports.new = (req, res) => {
  Run.findById(req.params.Id, (err, collection) => {
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
    } else res.render("runs/new", {collection:collection});
  });
};

// Create and Save a new Run
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
      // Create a Run
      var run = new Run({
      collection_id: collection.id,
      sorter_id: req.body.sorter_id,
      imagefolder : req.body.imagefolder
      });

      Run.create(run, (err, data) => {
        if (err)
          res.status(500).send({
            message:
              err.message || "Some error occurred while creating the Run."
          });
        else res.redirect("/collections/"+ collection.id);  
      });
    }
  });
};

// Find a single Run with a RunId
exports.findOne = (req, res) => {
  Run.findById(req.params.Id, (err, run) => {
    if (err) {
      if (err.kind === "not_found") {
        res.status(404).send({
          message: `Not found Run with id ${req.params.id}.`
        });
      } else {
        res.status(500).send({
          message: "Error retrieving Run with id " + req.params.Id
        });
      }
    } else {
      Partimage.getAllByRunId(run.id, (err, partimages) => {
        if (err) {
          if (err.kind === "not_found") {
            res.status(404).send({
              message: `Not found partimages for Runid ${run.id}.`
            });
          } else {
            res.status(500).send({
              message: "Error retrieving partimages for Runid " + run.id
            });
          }
        } else 
        Run.findRunStatusByRunId(run.run_id, (err, runstatus) => {
          if (err) {
            if (err.kind === "not_found") {
              res.status(404).send({
                message: `Not found Runstatus with Runid ${run.run_id}.`
              });
            } else {
              res.status(500).send({
                message: "Error retrieving Runstatus with id " + run.run_id
              });
            }
          } else {
            res.render("runs/show", {run:run, partimages:partimages, runstatus: runstatus});
          }
        });
      });
    }
  });   
};

//Edit Show edit form for Run with id
exports.editOne = (req,res) => {
   Run.findById(req.params.Id, (err, run) => {
    if (err) {
      if (err.kind === "not_found") {
        res.status(404).send({
          message: `Not found Run with id ${req.params.id}.`
        });
      } else {
        res.status(500).send({
          message: "Error retrieving Run with id " + req.params.Id
        });
      }
    } else res.render("runs/edit", {run:run});
  });
};

// Update a Run identified by the setId in the request
exports.update = (req, res) => {
   // Validate Request

  if (!req.body) {
    res.status(400).send({
      message: "Content can not be empty!"
    });
  }
  
  Run.updateById(
    req.params.Id,
    new Run(req.body),
    (err, data) => {
      if (err) {
        if (err.kind === "not_found") {
          res.status(404).send({
            message: `Not found Run with id ${req.params.Id}.`
          });
        } else {
          res.status(500).send({
            message: "Error updating Run with id " + req.params.Id
          });
        }
      } else res.redirect("/runs/"+ req.params.Id);  
    }
  );
};


// Delete a Run with the specified setId in the request
exports.delete = (req, res) => {
  Run.remove(req.params.Id, (err, data) => {
    if (err) {
      if (err.kind === "not_found") {
        res.status(404).send({
          message: `Not found Run with id ${req.params.Id}.`
        });
      } else {
        res.status(500).send({
          message: "Could not delete Run with id " + req.params.Id
        });
      }
    } else res.redirect("/runs");
  });
};

// Delete all Sets from the database.
exports.deleteAll = (req, res) => {
  Run.removeAll((err, data) => {
    if (err)
      res.status(500).send({
        message:
          err.message || "Some error occurred while removing all Runs."
      });
    else res.redirect("/runs");
  });
};

// Delete all Sets from the database.
exports.startRun = (req, res) => {
 // exec('workon cv && python opencv/pcs1.py -w 1 -c 100 - b 1', (err, stdout, stderr) => {
  exec("curl --location --request PUT 'conveyorcontroller/update?clientmode=SORTER&motormode=ON&speed=10'", (err, stdout, stderr) => {
    if (err) {
      console.log(err);
      return;
    }

    // the *entire* stdout and stderr (buffered)
    console.log(`stdout: ${stdout}`);
    console.log(`stderr: ${stderr}`);
  });
};

exports.stopRun = (req, res) => {
    // exec('workon cv && python opencv/pcs1.py -w 1 -c 100 - b 1', (err, stdout, stderr) => {
     exec("curl --location --request PUT 'conveyorcontroller/update?clientmode=SORTER&motormode=OFF&speed=10'", (err, stdout, stderr) => {
       if (err) {
         console.log(err);
         return;
       }
   
       // the *entire* stdout and stderr (buffered)
       console.log(`stdout: ${stdout}`);
       console.log(`stderr: ${stderr}`);
     });

  res.redirect("/runs/"+ req.params.Id);  
};