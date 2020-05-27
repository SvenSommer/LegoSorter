const Sorter = require("../models/sorter.model.js");
const request = require('request');

// Retrieve all Sorters from the database.
exports.findAll = (req, res) => {
  Sorter.getAll((err, sorters) => {
    if (err)
      res.status(500).send({
        message:
          err.message || "Some error occurred while retrieving sorters."
      });
    else {
      res.render("sorters/index", {sorters:sorters});
    }
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
    lifter_status_url: req.body.lifter_status_url,
    lifter_update_url: req.lifter_update_url,
    lifter_alterspeed_url: req.body.lifter_alterspeed_url,
    vfeeder_status_url: req.body.vfeeder_status_url,
    vfeeder_update_url: req.body.vfeeder_update_url,
    vfeeder_alterspeed_url: req.body.vfeeder_alterspeed_url,
    conveyor_status_url: req.body.conveyor_status_url,
    conveyor_update_url: req.body.conveyor_update_url,
    conveyor_alterspeed_url: req.body.conveyor_alterspeed_url,
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
  Sorter.findById(req.params.Id, (err, sorter) => {
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
      if(sorter.lifter_status_url != null) {
        request(sorter.lifter_status_url, (err2, res2, body) => {
        if(body != null) {
        lifter_status =  JSON.parse(body);
        request(sorter.conveyor_status_url, (err2, res2, body) => {
          if(body != null) {
          conveyor_status =  JSON.parse(body);
          request(sorter.vfeeder_status_url, (err2, res2, body) => {

            if(body != null) {0
            vfeeder_status =  JSON.parse(body);
            res.render("sorters/show", {sorter:sorter,lifter_status:lifter_status,conveyor_status:conveyor_status,vfeeder_status:vfeeder_status });
            }
          });  
        }

        });
      }
      }); 
    } else console.log("sorter.lifter_status_url is not set");
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

exports.alterspeed = (req,res) => {
  Sorter.findById(req.params.Id, (err, sorter) => {
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
     if(sorter.lifter_status_url != null) {
      request(sorter.lifter_status_url, (err2, res2, body) => {
      if(body != null) {
      lifter_status =  JSON.parse(body);
      request(sorter.conveyor_status_url, (err2, res2, body) => {
        if(body != null) {
        conveyor_status =  JSON.parse(body);
        request(sorter.vfeeder_status_url, (err2, res2, body) => {

          if(body != null) {0
          vfeeder_status =  JSON.parse(body);
                   
          var options = {
            'method': 'PUT',
            'url': 'http://liftercontroller/alterspeed?speedchange=5',
            'headers': {
            }
          };
          request(options, function (error, response) { 
            if (error) throw new Error(error);
            console.log(response.body);
          });

          res.render("sorters/show", {sorter:sorter,lifter_status:lifter_status,conveyor_status:conveyor_status,vfeeder_status:vfeeder_status });
          }
        });  
      }

      });
    }
    }); 
  } else console.log("sorter.lifter_status_url is not set");
   }
 });
};