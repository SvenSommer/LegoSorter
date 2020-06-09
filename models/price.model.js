const sql = require("../config/db.js");
const blApi = require("../config/bl.api.js");


// constructor
const Price = function(price) {
    this.no = price.no;
    this.color_id = price.color_id;
    this.region = price.region;
    this.guide_type = price.guide_type;
    this.created = new Date().toISOString().slice(0, 19).replace('T', ' ');
};

Price.create = (part, result) => {
    var priceinfostock = new Price({no : part.no, color_id: part.color_id,  region: 'europe', guide_type: "stock"});
    var priceinfosold = new Price({no : part.no, color_id: part.color_id,  region: 'europe' , guide_type: "sold"});
           //Price PriceGuide STOCK
        blApi.bricklinkClient.getPriceGuide(part.type, part.no, 
          {new_or_used: blApi.Condition.Used,
            color_id:  part.color_id, 
            region: 'europe',  
            guide_type: 'stock'
          }).then(function(priceinfostockdata){
              
            priceinfostock.type = part.type;
            priceinfostock.new_or_used = priceinfostockdata.new_or_used;
            priceinfostock.currency_code = priceinfostockdata.currency_code;
            priceinfostock.min_price = priceinfostockdata.min_price;
            priceinfostock.max_price = priceinfostockdata.max_price;
            priceinfostock.avg_price = priceinfostockdata.avg_price;
            priceinfostock.qty_avg_price = priceinfostockdata.qty_avg_price;
            priceinfostock.unit_quantity = priceinfostockdata.unit_quantity;
            priceinfostock.total_quantity = priceinfostockdata.total_quantity;
              
            sql.query("INSERT INTO Prices SET ? ON DUPLICATE KEY UPDATE id=id", priceinfostock, (err, res) => {
              if (err) {
                console.log("error: ", err);
                result(err, null);
                return;
              }
              //console.log("created Price: ", { id: res.insertId, ...priceinfostock });
              
            blApi.bricklinkClient.getPriceGuide(part.type, part.no, 
              {new_or_used: blApi.Condition.Used,
                color_id:  part.color_id, 
                region: 'europe', 
                guide_type: 'sold'
              }).then(function(priceinfosolddata){
                  
                priceinfosold.type = part.type;
                priceinfosold.new_or_used = priceinfosolddata.new_or_used;
                priceinfosold.currency_code = priceinfosolddata.currency_code;
                priceinfosold.min_price = priceinfosolddata.min_price;
                priceinfosold.max_price = priceinfosolddata.max_price;
                priceinfosold.avg_price = priceinfosolddata.avg_price;
                priceinfosold.qty_avg_price = priceinfosolddata.qty_avg_price;
                priceinfosold.unit_quantity = priceinfosolddata.unit_quantity;
                priceinfosold.total_quantity = priceinfosolddata.total_quantity;
       
                sql.query("INSERT INTO Prices SET ? ON DUPLICATE KEY UPDATE id=id", priceinfosold, (err, res) => {
                  if (err) {
                    console.log("error: ", err);
                    result(err, null);
                    return;
                  }
               
              
                  //console.log("created Price: ", { id: res.insertId, ...priceinfosold });
                  result(null, { priceinfostock: priceinfostock, priceinfosold: priceinfosold});
                });
          });
        });
    });
};

Price.findById = (PriceId, result) => {
  sql.query(`SELECT * FROM Prices WHERE id = ${PriceId}`, (err, res) => {
    if (err) {
      console.log("error: ", err);
      result(err, null);
      return;
    }

    if (res.length) {
      //console.log("found Price: ", res[0]);
      result(null, res[0]);
      return;
    }

    // not found Price with the id
    result({ kind: "not_found" }, null);
  });
};

Price.findByNo = (PriceId, result) => {
  sql.query(`SELECT * FROM Prices WHERE no = ${PriceId}`, (err, res) => {
    if (err) {
      console.log("error: ", err);
      result(err, null);
      return;
    }

    if (res.length) {
      //console.log("found Price: ", res[0]);
      result(null, res[0]);
      return;
    }

    // not found Price with the id
    result({ kind: "not_found" }, null);
  });
};


Price.getAll = result => {
  sql.query("SELECT * FROM Prices", (err, res) => {
    if (err) {
      console.log("error: ", err);
      result(null, err);
      return;
    }

    //console.log("Prices: ", res);
    result(null, res);
  });
};

Price.updateById = (id, Price, result) => {
  sql.query(
    "UPDATE `Prices` SET comments = ?, instructions = ?, condition = ? WHERE id = ?",
    [Price.comments, Price.instructions, Price.condition, id],
    (err, res) => {
      if (err) {
        console.log("error: ", err);
        result(null, err);
        return;
      }

      if (res.affectedRows == 0) {
        // not found Price with the id
        result({ kind: "not_found" }, null);
        return;
      }

      //console.log("updated Price: ", { id: id, ...Price });
      result(null, { id: id, ...Price });
    }
  );
};

Price.remove = (id, result) => {
  sql.query("DELETE FROM Prices WHERE id = ?", id, (err, res) => {
    if (err) {
      console.log("error: ", err);
      result(null, err);
      return;
    }

    if (res.affectedRows == 0) {
      // not found Price with the id
      result({ kind: "not_found" }, null);
      return;
    }

    console.log("deleted Price with id: ", id);
    result(null, res);
  });
};

Price.removeAll = result => {
  sql.query("DELETE FROM Prices", (err, res) => {
    if (err) {
      console.log("error: ", err);
      result(null, err);
      return;
    }

    console.log(`deleted ${res.affectedRows} Price`);
    result(null, res);
  });
};

Price.findAllSuperSetsByPriceId = ({priceid:priceid,color_id: color_id }, result) => {
  blApi.bricklinkClient.getItemSuperset(blApi.ItemType.Price, priceid, color_id)
    .then(function(subpriceData){
        result(null, subpriceData);
    });
  };

module.exports = Price;