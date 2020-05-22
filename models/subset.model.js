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

            sql.query("INSERT INTO Subsets SET ? ON DUPLICATE KEY UPDATE id=id", subset, (err, res) => {
              if (err) {
                console.log("error while writing into Subsets: ", err);
                result(err, null);
                return;
              }
          
           // console.log("created Subset entry: ", { id: res.insertId, ...subset });
            // result(null, { id: res.insertId, ...newSubset });
             });
  
            // insert
            var part = new Part({no : entry["item"]["no"],
              color_id : entry["color_id"],
              type : entry["item"]["type"]
            });
            
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
  sql.query(`SELECT * FROM Subsets WHERE id = ${SubsetId}`, (err, res) => {
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
  sql.query(`SELECT 
            Subsets.match_no as match_no, 
            p.thumbnail_url as thumbnail_url,
            p.no as part_no,
            Subsets.name as name,
            Subsets.type as type,
            Subsets.category_id as category_id,
            Subsets.color_id as color_id,
            c.color_name as color_name,
            Subsets.quantity as quantity,
            p.qty_avg_price_stock as qty_avg_price_stock,
            p.qty_avg_price_sold as qty_avg_price_sold,
            Subsets.extra_quantity as extra_quantity,
            Subsets.is_alternate as is_alternate,
            Subsets.is_counterpart as is_counterpart,
            st.name as status_name, 
            st.description as status_description 
            FROM Subsets  
            LEFT JOIN Colors c ON c.color_id = Subsets.color_id
            LEFT JOIN Parts p ON Subsets.no = p.no AND Subsets.color_id = p.color_id
            LEFT JOIN Status st ON p.status = st.id AND st.type = 'Part'
            WHERE Subsets.SetNo = ${setNumber} 
            ORDER BY CONCAT (c.color_name, ' ',Subsets.name) `, (err, res) => {
    if (err) {
      console.log("error: ", err);
      result(err, null);
      return;
    }

    result(null, res);
  });
};

Subset.CountPartsBySetNo = (setNumber, result) => {
  sql.query(`SELECT SUM(quantity) as parts_count,
            SUM(extra_quantity) as extra_quantity_count,
            SUM(is_alternate) as alternate_count, 
            SUM(is_counterpart) as counterpart_count,
            SUM(p.qty_avg_price_stock) as part_stock_price_sum,
            SUM(p.qty_avg_price_sold) as part_sold_price_sum
            FROM Subsets 
            JOIN Parts p ON Subsets.no = p.no AND Subsets.color_id = p.color_id
            WHERE p.type = 'PART'
            AND setNo = ${setNumber}`, (err, res) => {
    if (err) {
      console.log("error: ", err);
      result(err, null);
      return;
    }
    
   sql.query(
        "UPDATE `Sets` SET complete_part_count = ? WHERE no = ?",
        [res[0].parts_count, setNumber],
        (err, res) => {
          if (err) {
            console.log("error: ", err);
            result(null, err);
            return;}

      if (res.affectedRows == 0) {
        // not found Set with the id
        result({ kind: "not_found" }, null);
        return;
    }});

    result(null, res);
  });
};

Subset.CountMinifigsBySetNo = (setNumber, result) => {
  sql.query(`SELECT SUM(quantity) as minifigs_count,
            SUM(p.qty_avg_price_stock) as part_stock_price_sum,
            SUM(p.qty_avg_price_sold) as part_sold_price_sum
            FROM Subsets 
            JOIN Parts p ON Subsets.no = p.no AND Subsets.color_id = p.color_id
            WHERE p.type = 'MINIFIG'
            AND setNo = ${setNumber}`, (err, res) => {
    if (err) {
      console.log("error: ", err);
      result(err, null);
      return;
    }
    
     sql.query(
              "UPDATE `Sets` SET complete_minifigs_count = ? WHERE no = ?",
              [res[0].minifigs_count, setNumber],
              (err, res) => {
                if (err) {
                  console.log("error: ", err);
                  result(null, err);
                  return;}

            if (res.affectedRows == 0) {
              // not found Set with the id
              result({ kind: "not_found" }, null);
              return;
          }});

    result(null, res);
  });
};

Subset.getAll = result => {
  sql.query(`SELECT 
            Subsets.match_no as match_no, 
            sets.collection_id as collection_id,
            p.thumbnail_url as thumbnail_url,
            p.no as part_no,
            Subsets.setNo as setNo,
            Subsets.name as name,
            Subsets.type as type,
            Subsets.category_id as category_id,
            Subsets.color_id as color_id,
            c.color_name as color_name,
            Subsets.quantity as quantity,
            p.qty_avg_price_stock as qty_avg_price_stock,
            p.qty_avg_price_sold as qty_avg_price_sold,
            Subsets.extra_quantity as extra_quantity,
            Subsets.is_alternate as is_alternate,
            Subsets.is_counterpart as is_counterpart,
            st.name as status_name, 
            st.description as status_description 
            FROM Subsets  
            LEFT JOIN Sets sets On sets.no = Subsets.setNo
            LEFT JOIN Colors c ON c.color_id = Subsets.color_id
            LEFT JOIN Parts p ON Subsets.no = p.no AND Subsets.color_id = p.color_id
            LEFT JOIN Status st ON p.status = st.id AND st.type = 'Part'
            ORDER BY CONCAT (c.color_name, ' ',Subsets.name) `, (err, res) => {
    if (err) {
      console.log("error: ", err);
      result(err, null);
      return;
    }

    result(null, res);
  });
};

Subset.removeAll = result => {
  sql.query("DELETE FROM Subsets", (err, res) => {
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