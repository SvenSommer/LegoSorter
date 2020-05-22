const sql = require("../config/db.js");

// constructor
const Collection = function(collection) {
  this.name = collection.name;
  this.weight_kg = collection.weight_kg;
  this.origin = collection.origin;
  this.origin_url = collection.origin_url;
  this.seller = collection.seller;
  this.description = collection.description;
  this.purchase_date = collection.purchase_date;
  this.cost = collection.cost;
  this.porto = collection.porto;
  this.thumbnail_url = collection.thumbnail_url;
  this.status = 10;
  this.created = new Date().toISOString().slice(0, 19).replace('T', ' ');
};

Collection.create = (newCollection, result) => {
  sql.query("INSERT INTO Collections SET ?", newCollection, (err, res) => {
    if (err) {
      console.log("error: ", err);
      result(err, null);
      return;
    }

    //console.log("created collection: ", { id: res.insertId, ...newCollection });
    result(null, { id: res.insertId, ...newCollection });
  });
};

Collection.findById = (collectionId, result) => {
  sql.query(`SELECT * FROM Collections WHERE id = ${collectionId}`, (err, res) => {
    if (err) {
      console.log("error: ", err);
      result(err, null);
      return;
    }

    if (res.length) {
      //console.log("found collection: ", res[0]);
      result(null, res[0]);
      return;
    }

    // not found Collection with the id
    result({ kind: "not_found" }, null);
  });
};

Collection.getAll = result => {
  sql.query("SELECT * FROM Collections", (err, res) => {
    if (err) {
      console.log("error: ", err);
      result(null, err);
      return;
    }

    //console.log("collections: ", res);
    result(null, res);
  });
};

Collection.updateById = (id, collection, result) => {
  sql.query(
    "UPDATE Collections SET name = ?, weight_kg = ?, origin = ?, origin_url = ?, seller = ?, description = ?, purchase_date = ?, cost = ?, porto = ?, thumbnail_url = ?, status = ?, created = ? WHERE id = ?",
    [collection.name, collection.weight_kg, collection.origin, collection.origin_url, collection.seller, collection.description, collection.purchase_date, collection.cost, collection.porto, collection.thumbnail_url, collection.status, collection.created, id],
    (err, res) => {
      if (err) {
        console.log("error: ", err);
        result(null, err);
        return;
      }

      if (res.affectedRows == 0) {
        // not found collection with the id
        result({ kind: "not_found" }, null);
        return;
      }

      //console.log("updated collection: ", { id: id, ...collection });
      result(null, { id: id, ...collection });
    }
  );
};

Collection.remove = (id, result) => {
  sql.query("DELETE FROM Collections WHERE id = ?", id, (err, res) => {
    if (err) {
      console.log("error: ", err);
      result(null, err);
      return;
    }

    if (res.affectedRows == 0) {
      // not found collection with the id
      result({ kind: "not_found" }, null);
      return;
    }

    console.log("deleted collection with id: ", id);
    result(null, res);
  });
};

Collection.removeAll = result => {
  sql.query("DELETE FROM Collections", (err, res) => {
    if (err) {
      console.log("error: ", err);
      result(null, err);
      return;
    }

    console.log(`deleted ${res.affectedRows} collection`);
    result(null, res);
  });
};

Collection.findAllSetsByCollectionId = (collectionId, result) => {
  sql.query(`SELECT s.* , c.category_name, st.name as status_name, st.description as status_description FROM Sets s
JOIN Categories c On c.category_id =  s.category_id
JOIN Status st ON s.status = st.id AND st.type = 'SET'
WHERE collection_id = ${collectionId}`, (err, res) => {
    if (err) {
      console.log("error: ", err);
      result(err, null);
      return;
    }

    result(null, res);
  });
};

Collection.SumallSetInfosByCollectionId = (collectionId, result) => {
  sql.query(`SELECT 
            COUNT(no) as allSets_count,
            SUM(weight_g) as allSets_weight, 
            SUM(complete_part_count) as allSets_part_count,
            SUM(complete_minifigs_count) as allSets_minifigs_count,
            SUM(min_price) as AllSets_minPrice,
            SUM(avg_price) as AllSets_avgPrice
            FROM Sets s
            WHERE collection_id = ${collectionId}`, (err, res) => {
    if (err) {
      console.log("error: ", err);
      result(err, null);
      return;
    }

    result(null, res);
  });
};
  

module.exports = Collection;