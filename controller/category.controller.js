const blApi = require("../config/bl.api.js");
const sql = require("../config/db.js");

const Category = function(category) {
  this.category_id = category.category_id;
  this.category_name = category.category_name;
  this.parent_id = category.parent_id;
  this.created = new Date().toISOString().slice(0, 19).replace('T', ' ');
};

// Retrieve all Collections from the database.
exports.findAll = (req, res) => {
  Category.getAll((err, data) => {
    if (err)
      res.status(500).send({
        message:
          err.message || "Some error occurred while retrieving categoriess."
      });
    else res.render("categories/index", {categorys:data});
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

  // Save Categorys in the database

     blApi.bricklinkClient.send(blApi.Category.all())
     .then(function(categorys) {
         categorys.forEach(function(category){
         
            var newCategory = new Category({
                category_id : category.category_id,
                category_name : category.category_name,
                parent_id : category.parent_id
            });
                 
            sql.query("INSERT INTO Categories SET ? ON DUPLICATE KEY UPDATE id=id", newCategory, (err, res) => {
              if (err) {
                console.log("error: ", err);

                return;
            }
            
            console.log("created new Category: ", { id: res.insertId, ...newCategory });
            });
        });
    res.redirect("/preferences");  
  });
};