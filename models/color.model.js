const sql = require("../config/db.js");
const blApi = require("../config/bl.api.js");

const Color = function(color) {
  this.color_id = color.color_id;
  this.color_name = color.color_name;
  this.color_code = color.color_code;
  this.color_type = color.color_type;
  this.created = new Date().toISOString().slice(0, 19).replace('T', ' ');
};

Color.saveInDB = result => {
  
        result(null, true);
    });

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