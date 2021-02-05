const sql = require("../config/db.js");
const blApi = require("../config/bl.api.js");

// constructor
const SuperSet = function(superset) {
    this.partNo = superset.partNo;
    this.setNo = superset.setNo;
    this.color_id = superset.color_id;
    this.name = superset.name;
    this.type = superset.type;
    this.category_id = superset.category_id;
    this.quantity = superset.quantity;
    this.appears_as = superset.appears_as;
    this.created = new Date().toISOString().slice(0, 19).replace('T', ' ');
  };

SuperSet.create = (partNo, result) => {
    blApi.bricklinkClient.getItemSuperset(blApi.ItemType.Part, partNo)
       .then(function(supersetData){
           var resultSupersets = []
        supersetData.forEach(function(supersetdataEntry) {
            supersetdataEntry["entries"].forEach(function(entry){
                //console.log(JSON.stringify(supersetdataEntry))
                const superSet = new SuperSet({
                 partNo: partNo,
                 color_id: supersetdataEntry["color_id"],
                 setNo: entry["item"]["no"],
                 name: entry["item"]["name"],
                 type: entry["item"]["type"],
                 category_id: entry["item"]["category_id"],
                 quantity: entry["quantity"],
                 appears_as: entry["appears_as"]
               });
               

                sql.query("INSERT INTO SuperSets SET ? ON DUPLICATE KEY UPDATE id=id", superSet, (err, res) => {
                if (err) {
                    console.log("error while writing into Supersets: ", err);
                    result(err, null);
                    return;
                }
                resultSupersets.push(superSet)
                //console.log("created SuperSet entry: ", { id: res.insertId, ...superSet });
                });
            });
            
        });
        result(null, resultSupersets);
    });
};

SuperSet.getOrCreate = (partNo, result) => {
    sql.query(`SELECT * FROM SuperSets WHERE partNo = '${partNo}'`, (err, res) => {
        if (err) {
        console.log("error: ", err);
        result(err, null);
        return;
        }

        if (res.length) {
        //console.log("found Sets: ", res);
        result(null, res);
        return;
        }

        console.log("No supersets available in db for part " + partNo + ", I will download them!")
        SuperSet.create(partNo, (err, supersets) => {
            if (err)
            res.status(500).send({
                message:
                err.message || "Some error occurred while creating the Supersets for partno " + partNo
            });
            result(null, supersets);
        });
    });
};

SuperSet.countSuperSetbyPartNo = (partNo, result) => {
    sql.query(`SELECT COUNT(*) as count FROM SuperSets WHERE partNo = ${partNo}`, (err, res) => {
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
      
        console.log("No supersets available in db for part " + partNo + ", I will download them!")
        SuperSet.create(partNo, (err, supersets) => {
            if (err)
            res.status(500).send({
                message:
                err.message || "Some error occurred while creating the Supersets for partno " + partNo
            });
            result(null, supersets.length);
        });
    });
};

module.exports = SuperSet;