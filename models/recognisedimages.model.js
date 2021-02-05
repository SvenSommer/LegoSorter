const sql = require("../config/db.js");

// constructor
const Recognisedimages = function(recognisedimages) {
  this.image_id = recognisedimages.image_id;
  this.part_id = recognisedimages.part_id;
  this.score = recognisedimages.score;
  this.created = new Date().toISOString().slice(0, 19).replace('T', ' ');
};

Recognisedimages.create = (newRecognisedimages, result) => {
  sql.query("INSERT INTO Recognisedimages SET ?", newRecognisedimages, (err, res) => {
    if (err) {
      console.log("error: ", err);
      result(err, null);
      return;
    }

    //console.log("created recognisedimages: ", { id: res.insertId, ...newRecognisedimages });
    result(null, { id: res.insertId, ...newRecognisedimages });
  });
};

Recognisedimages.findById = (recognisedimageId, result) => {
  sql.query(`SELECT * FROM Recognisedimages WHERE id = ${recognisedimageId}`, (err, res) => {
    if (err) {
      console.log("error: ", err);
      result(err, null);
      return;
    }

    if (res.length) {
      //console.log("found recognisedimages: ", res[0]);
      result(null, res[0]);
      return;
    }

    // not found Recognisedimages with the id
    result({ kind: "not_found" }, null);
  });
};

Recognisedimages.getAll = result => {
  sql.query("SELECT * FROM Recognisedimages", (err, res) => {
    if (err) {
      console.log("error: ", err);
      result(null, err);
      return;
    }

    //console.log("recognisedimagess: ", res);
    result(null, res);
  });
};

Recognisedimages.updateById = (id, recognisedimage, result) => {
  sql.query(
    "UPDATE Recognisedimages SET image_id = ?, part_id = ?, score = ?, created = ? WHERE image_id = ?",
    [recognisedimage.image_id, recognisedimage.part_id, recognisedimage.score, recognisedimage.created, id],
    (err, res) => {
      if (err) {
        console.log("error: ", err);
        result(null, err);
        return;
      }

      if (res.affectedRows == 0) {
        // not found recognisedimage with the id
        result({ kind: "not_found" }, null);
        return;
      }

      //console.log("updated recognisedimage: ", { id: id, ...recognisedimage });
      result(null, { id: id, ...recognisedimage });
    }
  );
};


Recognisedimages.remove = (id, result) => {
  sql.query("DELETE FROM Recognisedimages WHERE id = ?", id, (err, res) => {
    if (err) {
      console.log("error: ", err);
      result(null, err);
      return;
    }

    if (res.affectedRows == 0) {
      // not found recognisedimages with the id
      result({ kind: "not_found" }, null);
      return;
    }

    console.log("deleted recognisedimages with id: ", id);
    result(null, res);
  });
};

Recognisedimages.removeAll = result => {
  sql.query("DELETE FROM Recognisedimages", (err, res) => {
    if (err) {
      console.log("error: ", err);
      result(null, err);
      return;
    }

    console.log(`deleted ${res.affectedRows} recognisedimages`);
    result(null, res);
  });
};

module.exports = Recognisedimages;