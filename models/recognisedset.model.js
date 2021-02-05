const sql = require("../config/db.js");

// constructor
const Recognisedset = function(recognisedset) {
  this.collection_id = recognisedset.collection_id;
  this.setNo = recognisedset.setNo;
  this.comments = recognisedset.comments;
  this.instructions = recognisedset.instructions;
  this.condition  = recognisedset.condition;
  this.status = 10;
  this.created = new Date().toISOString().slice(0, 19).replace('T', ' ');
};

Recognisedset.create = (newRecognisedset, result) => {
  sql.query("INSERT INTO Recognisedsets SET ?", newRecognisedset, (err, res) => {
    if (err) {
      console.log("error: ", err);
      result(err, null);
      return;
    }

    console.log("created newRecognisedset: ", { id: res.insertId, ...newRecognisedset });
    result(null, { id: res.insertId, ...newRecognisedset });
  });
};

Recognisedset.findById = (RecognisedsetId, result) => {
  sql.query(`SELECT * FROM Recognisedsets WHERE id = ${RecognisedsetId}`, (err, res) => {
    if (err) {
      console.log("error: ", err);
      result(err, null);
      return;
    }

    if (res.length) {
      console.log("found Recognisedset: ", res[0]);
      result(null, res[0]);
      return;
    }

    // not found Recognisedset with the id
    result({ kind: "not_found" }, null);
  });
};

Recognisedset.findAllSetsByCollectionId = (collectionId, result) => {
  sql.query(`SELECT * FROM LegoSorterDB.sets_overview WHERE collection_id = ${collectionId}`, (err, res) => {
            if (err) {
              console.log("error: ", err);
              result(err, null);
              return;
            }

    result(null, res);
  });
};

Recognisedset.getAll = result => {
  sql.query("SELECT * FROM Recognisedsets", (err, res) => {
    if (err) {
      console.log("error: ", err);
      result(null, err);
      return;
    }

    //console.log("recognisedimagess: ", res);
    result(null, res);
  });
};

Recognisedset.getAllbyCollectionId = (collection_id, result) => {
    sql.query(`SELECT * FROM Recognisedsets WHERE collection_id = ${collection_id}`, (err, res) => {
      if (err) {
        console.log("error: ", err);
        result(null, err);
        return;
      }
  
      console.log("Recognisedsets for collection_id " + collection_id + ":", res);
      result(null, res);
    });
  };

Recognisedset.updateById = (id, recognisedset, result) => {
  sql.query(
    "UPDATE Recognisedsets SET collection_id = ?, setNo = ?, comments = ?, instructions = ?, Recognisedsets.condition = ?,status = ?, created = ? WHERE (`id` = ?);",
    [recognisedset.collection_id, recognisedset.setNo, recognisedset.comments, recognisedset.instructions, recognisedset.condition, recognisedset.status, recognisedset.created, id],
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

      console.log("updated recognisedset: ", { id: id, ...recognisedset });
      result(null, { id: id, ...recognisedset});
    }
  );
};


Recognisedset.remove = (id, result) => {
  sql.query("DELETE FROM Recognisedsets WHERE id = ?", id, (err, res) => {
    if (err) {
      console.log("error: ", err);
      result(null, err);
      return;
    }

    if (res.affectedRows == 0) {
      // not found Recognisedsets with the id
      result({ kind: "not_found" }, null);
      return;
    }

    console.log("deleted Recognisedsets with id: ", id);
    result(null, res);
  });
};

Recognisedset.removeAll = result => {
  sql.query("DELETE FROM Recognisedsets", (err, res) => {
    if (err) {
      console.log("error: ", err);
      result(null, err);
      return;
    }

    console.log(`deleted ${res.affectedRows} Recognisedsets`);
    result(null, res);
  });
};

module.exports = Recognisedset;