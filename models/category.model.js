const sql = require("../config/db.js");
const blApi = require("../config/bl.api.js");

const Category = function(category) {
  this.category_id = category.category_id;
  this.category_name = category.category_name;
  this.parent_id = category.parent_id;
  this.created = new Date().toISOString().slice(0, 19).replace('T', ' ');
};

Category.saveAll = (result) => {
    blApi.bricklinkClient.send(blApi.Category.all())
     .then(function(categories) {
         categories.forEach(function(category){
         
            var newCategory = new Category({
                category_id : category.category_id,
                category_name : category.category_name,
                parent_id : category.parent_id});
                 
            sql.query("INSERT INTO Categories SET ? ON DUPLICATE KEY UPDATE id=id", newCategory, (err, res) => {
              if (err) {
                console.log("error: ", err);
                result(err, null);
                return;
            }
            
            console.log("created new Category: ", { id: res.insertId, ...newCategory });
            result(null, { id: res.insertId, ...newCategory });
            });
        });
    });
};

Category.getAll = result => {
  sql.query("SELECT * FROM Categories", (err, res) => {
    if (err) {
      console.log("error: ", err);
      result(null, err);
      return;
    }

    //console.log("Categories: ", res);
    result(null, res);
  });
};