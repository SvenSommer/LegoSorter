
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

exports.download = (req, res) => {  
  // PART OUT - Save the inlcuded Parts and their prices in the database
  setno = req.params.Id.split("-")[0]
  Set.checkifdownloaded(setno, (err, setalreadydownloaded) => {
    if (!setalreadydownloaded) {
      console.log("downloading set " + setno + "...")
      Subset.create(setno, (err, data) => {
            if (err)
          res.status(500).send({
            message:
              err.message || "Some error occurred while creating the SubSet."
          });
      });

      var set = new Set({
        no: setno
      });
      // SAVE SET INFORMATION - Save Set info in the database
      Set.create(set, (err, data) => {
        if (err)
          res.status(500).send({message: err.message || "Some error occurred while creating the Set."});
        });    
    } else  console.log("Set " + setno + " is already existing!")
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
      Subset.findBySetNo(set.no, (err, subsetData) => {
        if (err) {
          if (err.kind === "not_found") {
            res.status(404).send({
              message: `Not found Subsets for Setid ${req.params.id}.`
            });
          } else {
            res.status(500).send({
              message: "Error retrieving Subsets for Setid " + req.params.Id
            });
          }
        } else {
          
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
              } else
                res.render("sets/show", {set:set, subsetData:subsetData, partcounts: partcounts,minifigscount:minifigscount});
                });
            }
          });
        }
      });
    }
  });   
};