const Collection = require("../models/collection.model.js");
const Recognisedset = require("../models/recognisedset.model.js");
const Set = require("../models/set.model.js");
const Subset = require("../models/subset.model.js");


// Show new Set form
exports.new = (req, res) => {
    console.log("exports.new")
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
      } else res.render("recognisedsets/new", {collection:collection});
    });
  };

  // Create and Save a new Set
exports.create= (req, res) => {
    console.log("exports.create")
     // Validate request
    if (!req.body) {
      res.status(400).send({
        message: "Content can not be empty!"
      });
    }
    if(req.params.Id == "") {
      res.redirect("/collections/"+ req.params.id);
    }
    setNumber = req.body.no.replace(/\s+/g, '');
  
    req.params.Id = req.params.Id.replace(/\s+/g, '');
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
        console.log("Adding set " + setNumber + " to collection_id " + collection.id)
          
          // PART OUT - Save the inlcuded Parts and their prices in the database
          Subset.create(setNumber, (err, data) => {
                 if (err)
              res.status(500).send({
                message:
                  err.message || "Some error occurred while creating the SubSet."
              });
             else res.redirect("/collections/"+ collection.id); 
          });
  
          var set = new Set({
            no: setNumber
          });
            Set.checkifdownloaded(setNumber, (err, setalreadydownloaded) => {
                if (!setalreadydownloaded) {
                    // SAVE SET INFORMATION - Save Set info in the database
                    Set.create(set, (err, data) => {
                        if (err)
                            res.status(500).send({message: err.message || "Some error occurred while creating the Set."});
                        else {
                            var recognisedSet = new Recognisedset({
                            collection_id: collection.id,
                            setNo : setNumber,
                            comments : req.body.comments,
                            instructions: req.body.instructions,
                            condition: req.body.condition
                            })
                            Recognisedset.create(recognisedSet, (err, data) => {
                            if (err)
                            res.status(500).send({  message: err.message || "Some error occurred while creating the recognisedSet." });
                            else 
                                res.redirect("/collections/"+ collection.id);  
                            });
                        } 
                    });
                } else {
                    var recognisedSet = new Recognisedset({
                        collection_id: collection.id,
                        setNo : setNumber,
                        comments : req.body.comments,
                        instructions: req.body.instructions,
                        condition: req.body.condition
                    })
                    Recognisedset.create(recognisedSet, (err, data) => {
                        if (err)
                        res.status(500).send({  message: err.message || "Some error occurred while creating the recognisedSet." });
                        else 
                        res.redirect("/collections/"+ collection.id);  
                    });
                }
            });
        }
    });
  };


//Edit Show edit form for Recognisedset with id
exports.editOne = (req,res) => {
    Recognisedset.findById(req.params.Id, (err, data) => {
     if (err) {
       if (err.kind === "not_found") {
         res.status(404).send({message: `Not found Recognisedset with id ${req.params.id}.` 
        });
       } else {
         res.status(500).send({message: "Error retrieving Recognisedset with id " + req.params.Id });
       }
     } else 
     res.render("recognisedsets/edit", {set:data});
   });
 };
 
 // Update a Recognisedset identified by the setId in the request
 exports.update = (req, res) => {
    // Validate Request
   console.log("Set id: " + req.params.Id)
   if (!req.body) {
     res.status(400).send({
       message: "Content can not be empty!"
     });
   }
   var setid = req.params.Id
   Recognisedset.findById(setid, (err, recognisedset) => {
    if (err) {
      if (err.kind === "not_found") {
        res.status(404).send({message: `Not found Recognisedset with id ${setid}.` 
       });
      } else {
        res.status(500).send({message: "Error retrieving Recognisedset with id " + setid});
      }
    } else {
      var set = new Recognisedset({
        collection_id: recognisedset.collection_id,
        setNo : recognisedset.setNo,
        comments : req.body.comments,
        instructions: req.body.instructions,
        condition: req.body.condition
    });
      console.log("gonna update with set.properties:" + set)
      Recognisedset.updateById(
        setid,
        set,
        (err, data) => {
          if (err) {
            if (err.kind === "not_found") {
              res.status(404).send({
                message: `Not found Recognisedset with id ${setid}.`
              });
            } else {
              res.status(500).send({
                message: "Error updating Recognisedset with id " + setid
              });
            }
          } else res.redirect("/collections/" +  data.collection_id) ;  
            }
        );
      }
  });
 };
 
 
 // Delete a Recognisedset with the specified setId in the request
 exports.delete = (req, res) => {
    Recognisedset.remove(req.params.Id, (err, data) => {
     if (err) {
       if (err.kind === "not_found") {
         res.status(404).send({
           message: `Not found Recognisedset with id ${req.params.Id}.`
         });
       } else {
         res.status(500).send({
           message: "Could not delete Recognisedset with id " + req.params.Id
         });
       }
     } else res.redirect("/collections/");  
   });
 };