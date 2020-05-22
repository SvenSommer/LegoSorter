const sql = require("../config/db.js");

// constructor
const Partimages = function(partimages) {
  this.run_id = partimages.run_id;
  this.path = partimages.path;
  this.size_kb = partimages.size_kb;
  this.created = new Date().toISOString().slice(0, 19).replace('T', ' ');
};

Partimages.create = (newPartimages, result) => {
  sql.query("INSERT INTO Partimages SET ?", newPartimages, (err, res) => {
    if (err) {
      console.log("error: ", err);
      result(err, null);
      return;
    }

    //console.log("created partimages: ", { id: res.insertId, ...newPartimages });
    result(null, { id: res.insertId, ...newPartimages });
  });
};

Partimages.findById = (partimagesId, result) => {
  sql.query(`SELECT * FROM Partimages WHERE id = ${partimagesId}`, (err, res) => {
    if (err) {
      console.log("error: ", err);
      result(err, null);
      return;
    }

    if (res.length) {
      //console.log("found partimages: ", res[0]);
      result(null, res[0]);
      return;
    }

    // not found Partimages with the id
    result({ kind: "not_found" }, null);
  });
};

Partimages.getAll = result => {
  sql.query("SELECT * FROM Partimages", (err, res) => {
    if (err) {
      console.log("error: ", err);
      result(null, err);
      return;
    }

    //console.log("partimagess: ", res);
    result(null, res);
  });
};

Partimages.updateById = (id, partimages, result) => {
  sql.query(
    "UPDATE Partimages SET run_id = ?, path = ?, size_kb = ?, created = ? WHERE id = ?",
    [partimages.run_id, partimages.path, partimages.size_kb, partimages.created, id],
    (err, res) => {
      if (err) {
        console.log("error: ", err);
        result(null, err);
        return;
      }

      if (res.affectedRows == 0) {
        // not found partimages with the id
        result({ kind: "not_found" }, null);
        return;
      }

      //console.log("updated partimages: ", { id: id, ...partimages });
      result(null, { id: id, ...partimages });
    }
  );
};

Partimages.remove = (id, result) => {
  sql.query("DELETE FROM Partimages WHERE id = ?", id, (err, res) => {
    if (err) {
      console.log("error: ", err);
      result(null, err);
      return;
    }

    if (res.affectedRows == 0) {
      // not found partimages with the id
      result({ kind: "not_found" }, null);
      return;
    }

    console.log("deleted partimages with id: ", id);
    result(null, res);
  });
};

Partimages.removeAll = result => {
  sql.query("DELETE FROM Partimages", (err, res) => {
    if (err) {
      console.log("error: ", err);
      result(null, err);
      return;
    }

    console.log(`deleted ${res.affectedRows} partimages`);
    result(null, res);
  });
};

module.exports = Partimages;