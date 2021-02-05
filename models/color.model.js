const sql = require("../config/db.js");
const blApi = require("../config/bl.api.js");

const Color = function(color) {
  this.color_id = color.color_id;
  this.color_name = color.color_name;
  this.color_code = color.color_code;
  this.color_type = color.color_type;
  this.lower_treshold = color.lower_treshold;
  this.upper_treshold = color.upper_treshold;
  this.created = new Date().toISOString().slice(0, 19).replace('T', ' ');
};

Color.getAll = result => {
  sql.query("SELECT * FROM Colors", (err, res) => {
    if (err) {
      console.log("error: ", err);
      result(null, err);
      return;
    }

    //console.log("Colors: ", res);
    result(null, res);
  });
};

Color.getMostUsed = result => {
  sql.query(`SELECT count(*) as count ,p.color_id, c.color_name, c.color_code, c.color_type, c.lower_treshold, c.upper_treshold 
              FROM LegoSorterDB.Parts p
              LEFT JOIN LegoSorterDB.Colors c ON p.color_id = c.color_id
              WHERE color_name IS NOT NULL
              GROUP BY p.color_id, c.color_name, c.color_code, c.color_type, c.lower_treshold, c.upper_treshold ORDER by count desc`, (err, res) => {
    if (err) {
      console.log("error: ", err);
      result(null, err);
      return;
    }
    result(null, res);
  });
};


module.exports = Color;