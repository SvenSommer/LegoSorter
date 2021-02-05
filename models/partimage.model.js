const sql = require("../config/db.js");

// constructor
const Partimage =  function(partimage) {
  this.camera = partimage.camera;
  this.run_id = partimage.run_id;
  this.path = partimage.path;
  this.size_kb = partimage.size_kb;
  this.created = partimage.created;
  this.imported = partimage.imported;
  this.deleted = partimage.deleted;
  this.dimension = partimage.w * partimage.h;
};

Partimage.create = (newPartimage, result) => {
  sql.query("INSERT INTO Partimages SET ?", newPartimage, (err, res) => {
    if (err) {
      console.log("error: ", err);
      result(err, null);
      return;
    }

    //console.log("created partimage: ", { id: res.insertId, ...newPartimage });
    result(null, { id: res.insertId, ...newPartimage });
  });
};

Partimage.findById = (partimageId, result) => {
  sql.query(`SELECT * FROM Partimages WHERE id = ${partimageId}`, (err, res) => {
    if (err) {
      console.log("error: ", err);
      result(err, null);
      return;
    }

    if (res.length) {
      //console.log("found partimage: ", res[0]);
      result(null, res[0]);
      return;
    }

    // not found Partimage with the id
    result({ kind: "not_found" }, null);
  });
};

Partimage.getAllByRunId = (runId, result) => {
  sql.query(`SELECT * FROM Partimages WHERE run_id = ${runId} ORDER BY created, size_kb`, (err, res) => {
    if (err) {
      console.log("error: ", err);
      result(err, null);
      return;
    }
      result(null, res);
      return;
  });
};

/*
Partimage.getAllUnlabeledByRunId = (runId, result) => {
  sql.query(`SELECT pi.id as part_id, pi.path as part_path, pi.size_kb as size FROM Partimages pi LEFT JOIN Recognisedimages ri ON ri.image_id = pi.id WHERE pi.deleted IS NULL AND run_id = ${runId} AND ri.part_id IS NULL ORDER BY part_path`, (err, res) => {
    if (err) {
      console.log("error: ", err);
      result(err, null);
      return;
    }
      result(null, res);
      return;
  });
};

*/

Partimage.getAll = result => {
  sql.query("SELECT * FROM Partimages", (err, res) => {
    if (err) {
      console.log("error: ", err);
      result(null, err);
      return;
    }

    //console.log("partimages: ", res);
    result(null, res);
  });
};

Partimage.updateById = (id, partimage, result) => {
  sql.query(
    "UPDATE Partimages SET run_id = ?, path = ?, size_kb = ?, created = ?, imported = ? WHERE id = ?",
    [partimage.run_id, partimage.path, partimage.size_kb, partimage.created,partimage.imported, id],
    (err, res) => {
      if (err) {
        console.log("error: ", err);
        result(null, err);
        return;
      }

      if (res.affectedRows == 0) {
        // not found partimage with the id
        result({ kind: "not_found" }, null);
        return;
      }

      //console.log("updated partimage: ", { id: id, ...partimage });
      result(null, { id: id, ...partimage });
    }
  );
};

Partimage.remove = (id, result) => {
  sql.query("DELETE FROM Partimages WHERE id = ?", id, (err, res) => {
    if (err) {
      console.log("error: ", err);
      result(null, err);
      return;
    }

    if (res.affectedRows == 0) {
      // not found partimage with the id
      result({ kind: "not_found" }, null);
      return;
    }

    console.log("deleted Partimages with id: ", id);
    result(null, res);
  });
};


Partimage.MarkAsDeletedById = (recognisedimageId, result) => {
  var deleted = new Date().toISOString().slice(0, 19).replace('T', ' ');
  sql.query(
    "UPDATE Partimages SET deleted = ? WHERE id = ?",
    [deleted, recognisedimageId],
    (err, res) => {
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

      //console.log("updated recognisedimages: ", { id: id, ...recognisedimages });
      result(null, { recognisedimageId: recognisedimageId});
    }
  );
};


Partimage.removeAll = result => {
  sql.query("DELETE FROM Partimages", (err, res) => {
    if (err) {
      console.log("error: ", err);
      result(null, err);
      return;
    }

    console.log(`deleted ${res.affectedRows} partimage`);
    result(null, res);
  });
};

module.exports = Partimage;