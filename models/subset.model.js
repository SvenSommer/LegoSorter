const sql = require("../config/db.js");
const blApi = require("../config/bl.api.js");
const Part = require("./part.model.js");

// constructor
const Subset = function(subset) {
  this.setNo = subset.setNo;
  this.match_no = subset.match_no;
  this.no = subset.no;
  this.name = subset.name;
  this.type = subset.type;
  this.category_id = subset.category_id;
  this.color_id = subset.color_id;
  this.quantity = subset.quantity;
  this.extra_quantity = subset.extra_quantity;
  this.is_alternate = subset.is_alternate;
  this.is_counterpart = subset.is_counterpart;
  this.created = new Date().toISOString().slice(0, 19).replace('T', ' ');
};

Subset.create = (setNumber, result) => {
 blApi.bricklinkClient.getItemSubset(blApi.ItemType.Set, setNumber + "-1", {break_minifigs: false})
    .then(function(subsetData){
         subsetData.forEach(function(subsetdataEntry) {
           subsetdataEntry["entries"].forEach(function(entry){
                     const subset = new Subset({
                      setNo: setNumber,
                      match_no: subsetdataEntry["match_no"],
                      no: entry["item"]["no"],
                      name: entry["item"]["name"],
                      type: entry["item"]["type"],
                      category_id: entry["item"]["category_id"],
                      color_id: entry["color_id"],
                      quantity: entry["quantity"],
                      extra_quantity: entry["extra_quantity"],
                      is_alternate: entry["is_alternate"],
                      is_counterpart: entry["is_counterpart"]
                    });
      
              sql.query("INSERT INTO SubSets SET ? ON DUPLICATE KEY UPDATE id=id", subset, (err, res) => {
                if (err) {
                  console.log("error while writing into Subsets: ", err);
                  result(err, null);
                  return;
                }
            
             // console.log("created Subset entry: ", { id: res.insertId, ...subset });
              // result(null, { id: res.insertId, ...newSubset });
            });
          
            // insert
            var part = new Part({no : entry["item"]["no"]});
            
            Part.create(part, (err, data)=> {
                if (err) {
                    console.log("error while writing into Subsets: ", err);
                    result(err, null);
                    return;
                  }
                });
          }); //entry loop
        }); //subsetdata loop
        return(null, {subsetData: subsetData});
    }); // api call
};

Subset.findById = (SubsetId, result) => {
  sql.query(`SELECT * FROM SubSets WHERE id = ${SubsetId}`, (err, res) => {
    if (err) {
      console.log("error: ", err);
      result(err, null);
      return;
    }

    if (res.length) {
      //console.log("found Subset: ", res[0]);
      result(null, res[0]);
      return;
    }

    // not found Subset with the id
    result({ kind: "not_found" }, null);
  });
};

Subset.findBySetNo = (setNumber, result) => {
  sql.query(`SELECT * FROM SubSets WHERE SetNo = ${setNumber}`, (err, res) => {
    if (err) {
      console.log("error: ", err);
      result(err, null);
      return;
    }

    result(null, res);
  });
};

Subset.removeAll = result => {
  sql.query("DELETE FROM SubSets", (err, res) => {
    if (err) {
      console.log("error: ", err);
      result(null, err);
      return;
    }

    console.log(`deleted ${res.affectedRows} Subset`);
    result(null, res);
  });
};

module.exports = Subset;