const sql = require("../config/db.js");
const blApi = require("../config/bl.api.js");


// constructor
const Set = function(set) {
  this.collection_id = set.collection_id;
  this.no = set.no;
  this.comments = set.comments;
  this.instructions = set.instructions;
  this.condition = set.condition;
  this.status = 10;
  this.created = new Date().toISOString().slice(0, 19).replace('T', ' ');
};

Set.create = (newSet, result) => {
  blApi.bricklinkClient.getCatalogItem(blApi.ItemType.Set, newSet.no + '-1')
    .then(function(setinfo){
       // console.log(setinfo);
        newSet.name = setinfo.name;
        newSet.year = setinfo.year_released;
        newSet.weight_g = setinfo.weight;
        newSet.size = setinfo.dim_x + " x " + setinfo.dim_y + " x " + setinfo.dim_z + " cm";
        newSet.thumbnail_url = setinfo.thumbnail_url;
        newSet.image_url = setinfo.image_url;
        newSet.category_id = setinfo.category_id;


        blApi.bricklinkClient.getPriceGuide(blApi.ItemType.Set, newSet.no + '-1', {new_or_used: blApi.Condition.Used,  region: 'europe', guide_type: 'stock'})
        .then(function(priceinfo){
            newSet.min_price = priceinfo.min_price;
            newSet.max_price = priceinfo.max_price;
            newSet.avg_price = priceinfo.avg_price;
            newSet.qty_avg_price = priceinfo.qty_avg_price;
            newSet.unit_quantity = priceinfo.unit_quantity;
            newSet.total_quantity = priceinfo.total_quantity;

            sql.query("INSERT INTO Sets SET ?", newSet, (err, res) => {
              if (err) {
                console.log("error: ", err);
                result(err, null);
                return;
              }
          
              console.log("created Set: ", { id: res.insertId, ...newSet });
              result(null, { id: res.insertId, ...newSet });
            });
        });
    });
};

Set.findById = (SetId, result) => {
  sql.query(`SELECT * FROM Sets WHERE id = ${SetId}`, (err, res) => {
    if (err) {
      console.log("error: ", err);
      result(err, null);
      return;
    }

    if (res.length) {
      //console.log("found Set: ", res[0]);
      result(null, res[0]);
      return;
    }

    // not found Set with the id
    result({ kind: "not_found" }, null);
  });
};

Set.getAll = result => {
  sql.query(`SELECT s.* , c.category_name, st.name as status_name, st.description as status_description FROM Sets s
JOIN Categories c On c.category_id =  s.category_id
JOIN Status st ON s.status = st.id AND st.type = 'SET'`, (err, res) => {
    if (err) {
      console.log("error: ", err);
      result(null, err);
      return;
    }

    //console.log("Sets: ", res);
    result(null, res);
  });
};

Set.updateById = (id, Set, result) => {
  sql.query(
    "UPDATE `Sets` SET comments = ?, instructions = ?, condition = ? WHERE id = ?",
    [Set.comments, Set.instructions, Set.condition, id],
    (err, res) => {
      if (err) {
        console.log("error: ", err);
        result(null, err);
        return;
      }

      if (res.affectedRows == 0) {
        // not found Set with the id
        result({ kind: "not_found" }, null);
        return;
      }

      //console.log("updated Set: ", { id: id, ...Set });
      result(null, { id: id, ...Set });
    }
  );
};

Set.remove = (id, result) => {
  sql.query("DELETE FROM Sets WHERE id = ?", id, (err, res) => {
    if (err) {
      console.log("error: ", err);
      result(null, err);
      return;
    }

    if (res.affectedRows == 0) {
      // not found Set with the id
      result({ kind: "not_found" }, null);
      return;
    }

    console.log("deleted Set with id: ", id);
    result(null, res);
  });
};

Set.removeAll = result => {
  sql.query("DELETE FROM Sets", (err, res) => {
    if (err) {
      console.log("error: ", err);
      result(null, err);
      return;
    }

    console.log(`deleted ${res.affectedRows} Set`);
    result(null, res);
  });
};



module.exports = Set;