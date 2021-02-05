const blApi = require("../config/bl.api.js");
const sql = require("../config/db.js");

const Color = function(color) {
  this.color_id = color.color_id;
  this.color_name = color.color_name;
  this.color_code = color.color_code;
  this.color_type = color.color_type;
  this.created = new Date().toISOString().slice(0, 19).replace('T', ' ');
};

// Retrieve all Colors from the database.
exports.findAll = (req, res) => {
  Color.getAll((err, data) => {
    if (err)
      res.status(500).send({
        message:
          err.message || "Some error occurred while retrieving colors."
      });
    else res.render("colors/index", {colors:data});
  });
};

// Create and Save a new Collection
exports.saveAll = (req, res) => {
   // Validate request
  if (!req.body) {
    res.status(400).send({
      message: "Content can not be empty!"
    });
  }

  // Save Colors in the database

     blApi.bricklinkClient.send(blApi.Color.all())
     .then(function(colors) {
         colors.forEach(function(color){
         
            var newColor = new Color({
                color_id : color.color_id,
                color_name : color.color_name,
                color_code : color.color_code,
                color_type : color.color_type
            });
                 
            sql.query("INSERT INTO Colors SET ? ON DUPLICATE KEY UPDATE id=id", newColor, (err, res) => {
              if (err) {
                console.log("error: ", err);

                return;
            }
            
            console.log("created new Color: ", { id: res.insertId, ...newColor });
            });
        });
    res.redirect("/preferences");  
  });
};