const SuperSet = require("../models/superset.model.js");

/*
// Create and Save a new SuperSet
exports.create = (req, res) => {
    // Validate request
    if(req.params.Id == "") {
        res.redirect("/collections/"+ 1);
      }
   // Get and Save Superset for Partno
   SuperSet.create(req.params.Id, (err, supersets) => {
     if (err)
       res.status(500).send({
         message:
           err.message || "Some error occurred while creating the Supersets for partno: " + req.params.Id
       });
     else res.redirect("/collections/1");  
   });
 };
*/
 exports.getOrCreate = (req, res) => {
    // Validate request
    if(req.params.Id == "") {
        res.redirect("/collections/"+ 1);
      }
   // Get and Save Superset for Partno
   SuperSet.getOrCreate(req.params.Id, (err, supersets) => {
     if (err)
       res.status(500).send({
         message:
           err.message || "Some error occurred while creating the Supersets for partno: " + req.params.Id
       });
     else {
       
       res.redirect("/collections/1");  
     }
   });
 };