const sql = require("../config/db.js");
const blApi = require("../config/bl.api.js");


// constructor
const Part = function(part) {
  this.no = part.no;
  this.status = 10;
  this.created = new Date().toISOString().slice(0, 19).replace('T', ' ');
};

Part.create = (newPart, result) => {
  blApi.bricklinkClient.getCatalogItem(blApi.ItemType.Part, newPart.no, newPart.color_id)
    .then(function(partinfo){
        newPart.name = partinfo.name;
        newPart.type = partinfo.type;
        newPart.category_id = partinfo.category_id;
        newPart.year = partinfo.year_released;
        newPart.weight_g = partinfo.weight;
        newPart.size = partinfo.dim_x + " x " + partinfo.dim_y + " x " + partinfo.dim_z + " cm";
        newPart.is_obsolete = partinfo.is_obsolete;
        newPart.qty_avg_price = partinfo.qty_avg_price;
        newPart.image_url = partinfo.image_url;
        newPart.thumbnail_url = partinfo.thumbnail_url;
        newPart.status = 10;
        newPart.created = new Date().toISOString().slice(0, 19).replace('T', ' ');
        sql.query("INSERT INTO Parts SET ?", newPart, (err, res) => {
          if (err) {
            console.log("error: ", err);
            result(err, null);
            return;
          }
      
          console.log("created Part: ", { id: res.insertId, ...newPart });
          result(null, { id: res.insertId, ...newPart });
        });
    });
};

Part.findById = (PartId, result) => {
  sql.query(`SELECT * FROM Parts WHERE id = ${PartId}`, (err, res) => {
    if (err) {
      console.log("error: ", err);
      result(err, null);
      return;
    }

    if (res.length) {
      //console.log("found Part: ", res[0]);
      result(null, res[0]);
      return;
    }

    // not found Part with the id
    result({ kind: "not_found" }, null);
  });
};

Part.findByNo = (PartId, result) => {
  sql.query(`SELECT * FROM Parts WHERE no = ${PartId}`, (err, res) => {
    if (err) {
      console.log("error: ", err);
      result(err, null);
      return;
    }

    if (res.length) {
      //console.log("found Part: ", res[0]);
      result(null, res[0]);
      return;
    }

    // not found Part with the id
    result({ kind: "not_found" }, null);
  });
};


Part.getAll = result => {
  sql.query("SELECT * FROM Parts", (err, res) => {
    if (err) {
      console.log("error: ", err);
      result(null, err);
      return;
    }

    //console.log("Parts: ", res);
    result(null, res);
  });
};

Part.updateById = (id, Part, result) => {
  sql.query(
    "UPDATE `Parts` SET comments = ?, instructions = ?, condition = ? WHERE id = ?",
    [Part.comments, Part.instructions, Part.condition, id],
    (err, res) => {
      if (err) {
        console.log("error: ", err);
        result(null, err);
        return;
      }

      if (res.affectedRows == 0) {
        // not found Part with the id
        result({ kind: "not_found" }, null);
        return;
      }

      //console.log("updated Part: ", { id: id, ...Part });
      result(null, { id: id, ...Part });
    }
  );
};

Part.remove = (id, result) => {
  sql.query("DELETE FROM Parts WHERE id = ?", id, (err, res) => {
    if (err) {
      console.log("error: ", err);
      result(null, err);
      return;
    }

    if (res.affectedRows == 0) {
      // not found Part with the id
      result({ kind: "not_found" }, null);
      return;
    }

    console.log("deleted Part with id: ", id);
    result(null, res);
  });
};

Part.removeAll = result => {
  sql.query("DELETE FROM Parts", (err, res) => {
    if (err) {
      console.log("error: ", err);
      result(null, err);
      return;
    }

    console.log(`deleted ${res.affectedRows} Part`);
    result(null, res);
  });
};

Part.findAllSuperSetsByPartId = ({partid:partid,color_id: color_id }, result) => {
  blApi.bricklinkClient.getItemSuperset(blApi.ItemType.Part, partid, color_id)
    .then(function(subpartData){
        result(null, subpartData);
    });
  };

module.exports = Part;