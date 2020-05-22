const sql = require("../config/db.js");

// constructor
const Recognisedparts = function(recognisedparts) {
  this.no = recognisedparts.no;
  this.color_id = recognisedparts.color_id;
  this.score = recognisedparts.score;
  this.created = new Date().toISOString().slice(0, 19).replace('T', ' ');
};

Recognisedparts.create = (newRecognisedparts, result) => {
  sql.query("INSERT INTO Recognisedparts SET ?", newRecognisedparts, (err, res) => {
    if (err) {
      console.log("error: ", err);
      result(err, null);
      return;
    }

    //console.log("created recognisedparts: ", { id: res.insertId, ...newRecognisedparts });
    result(null, { id: res.insertId, ...newRecognisedparts });
  });
};

Recognisedparts.findById = (recognisedpartsId, result) => {
  sql.query(`SELECT * FROM Recognisedparts WHERE id = ${recognisedpartsId}`, (err, res) => {
    if (err) {
      console.log("error: ", err);
      result(err, null);
      return;
    }

    if (res.length) {
      //console.log("found recognisedparts: ", res[0]);
      result(null, res[0]);
      return;
    }

    // not found Recognisedparts with the id
    result({ kind: "not_found" }, null);
  });
};

Recognisedparts.getAll = result => {
  sql.query("SELECT * FROM Recognisedparts", (err, res) => {
    if (err) {
      console.log("error: ", err);
      result(null, err);
      return;
    }

    //console.log("recognisedpartss: ", res);
    result(null, res);
  });
};

Recognisedparts.updateById = (id, recognisedparts, result) => {
  sql.query(
    "UPDATE Recognisedparts SET no = ?, color_id = ?, score = ?, created = ? WHERE id = ?",
    [recognisedparts.no, recognisedparts.color_id, recognisedparts.score, recognisedparts.created, id],
    (err, res) => {
      if (err) {
        console.log("error: ", err);
        result(null, err);
        return;
      }

      if (res.affectedRows == 0) {
        // not found recognisedparts with the id
        result({ kind: "not_found" }, null);
        return;
      }

      //console.log("updated recognisedparts: ", { id: id, ...recognisedparts });
      result(null, { id: id, ...recognisedparts });
    }
  );
};

Recognisedparts.remove = (id, result) => {
  sql.query("DELETE FROM Recognisedparts WHERE id = ?", id, (err, res) => {
    if (err) {
      console.log("error: ", err);
      result(null, err);
      return;
    }

    if (res.affectedRows == 0) {
      // not found recognisedparts with the id
      result({ kind: "not_found" }, null);
      return;
    }

    console.log("deleted recognisedparts with id: ", id);
    result(null, res);
  });
};

Recognisedparts.removeAll = result => {
  sql.query("DELETE FROM Recognisedparts", (err, res) => {
    if (err) {
      console.log("error: ", err);
      result(null, err);
      return;
    }

    console.log(`deleted ${res.affectedRows} recognisedparts`);
    result(null, res);
  });
};

module.exports = Recognisedparts;