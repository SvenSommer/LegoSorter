const Recognisedpart = require("../models/recognisedparts.model.js");
const Recognisedimage = require("../models/recognisedimages.model.js");
const Run = require("../models/run.model.js");
const Part = require("../models/part.model.js");
const Color = require("../models/color.model.js");

// NEW - FORM
exports.showlabelTool = (req, res) => {
    Run.findById(req.params.Id, (err, run) => {
      if (err) {
        if (err.kind === "not_found") {
          res.status(404).send({ message: `Not found Run with id ${req.params.id}.`
          });
        } else {
          res.status(500).send({message: "Error retrieving Run with id " + req.params.Id
          });
        }
      } else {
        Recognisedpart.getAllUnLabeledbyRunId(run.run_id, (err, recognisedParts) => {
          if (err) {
            if (err.kind === "not_found") {
              res.status(404).send({message: `Not found partimages for Runid ${run.run_id}.`
              });
            } else {
              res.status(500).send({ message: "Error retrieving partimages for Runid " + run.id
              });
            }
          } else {
            Part.getAllUnique((err, partsdata) => {
              if (err)
                res.status(500).send({message: err.message || "Some error occurred while retrieving parts."
                });
              else {
                Color.getMostUsed((err, colors) => {
                  if (err)
                    res.status(500).send({message:err.message || "Some error occurred while retrieving colors."
                    });
                  else 
                    res.render("recognisedparts/label", {run:run, recognisedParts:recognisedParts, partsdata:partsdata, colors:colors});
                });
              }
            });
          }
        });
      }
    });
  };



//CREATE
exports.label  = (req, res) => {
  if (!req.body) {
    res.status(400).send({
      message: "Content can not be empty!"
    });
  }
  imageids = []
  partid = req.body.PartidsAndImageIds[0].split("-")[0]
  req.body.PartidsAndImageIds.forEach(tmp => {
    imageids.push(tmp.split("-")[1])
  })

 // console.log("partid to Update: " + partid);
 // console.log("imageids to Update: " + imageids);
  var newRecognisedpart = new Recognisedpart({
    no : req.body.Partno,
    run_id : req.body.Run_id,
    color_id : req.body.Color_id,
    identifier : req.body.Identifier,
    score : req.body.Score,
    created :  new Date().toISOString().slice(0, 19).replace('T', ' ')
  });

  Recognisedpart.updateById(partid, newRecognisedpart, (err, partdata) => {
    if (err)
      res.status(500).send({
        message:
          err.message || "Some error occurred while creating the Recognisedpart."
      });
    else {
      imageids.forEach(imageid => {
        var newRecognisedImage = new Recognisedimage({
          image_id : imageid,
          part_id : partid,
          score : req.body.Score
        });
        Recognisedimage.updateById(imageid, newRecognisedImage, (err, imagedata) => {
          if (err)
            res.status(500).send({
              message:
                err.message || "Some error occurred while creating the Recognisedimage."
            });
        });
      });
      res.status(200).send();
    }
  });
};

// UPDATE
exports.editOne = (req,res) => {
  Recognisedpart.findById(req.params.Id, (err, recognisedpart) => {
   if (err) {
     if (err.kind === "not_found") {
       res.status(404).send({
         message: `Not found Recognisedpart with id ${req.params.id}.`
       });
     } else {
       res.status(500).send({
         message: "Error retrieving Recognisedpart with id " + req.params.Id
       });
     }
   } else { 
     res.render("recognisedparts/edit", {recognisedpart:recognisedpart});
     
   }
 });
};
  
// DELETE
exports.delete = (req, res) => {
  Recognisedpart.MarkAsDeletedById(req.params.Id, (err, partid) => {
  if (err)
    res.status(500).send({
    message:
        err.message || "Some error occurred while deleting Recognisedimage."
    });
 

    Recognisedpart.findById(req.params.Id, (err, recognisedpart) => {
      if (err) {
        if (err.kind === "not_found") {
          res.status(404).send({
            message: `Not found Recognisedpart with id ${req.params.id}.`
          });
        } else {
          res.status(500).send({
            message: "Error retrieving Recognisedpart with id " + req.params.Id
          });
        }
      } else { 
        res.redirect("/runs/"+ recognisedpart.run_id);  
        
      }
    });
  });
};