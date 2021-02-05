const sql = require("../config/db.js");
const Partimage = require("./partimage.model.js");
const SuperSet = require("./superset.model.js");

// constructor
const Recognisedparts = function(recognisedparts) {
  this.no = recognisedparts.no;
  this.run_id = recognisedparts.run_id;
  this.color_id = recognisedparts.color_id;
  this.score = recognisedparts.score;
  this.identifier = recognisedparts.identifier;
  this.created = recognisedparts.created;
  this.supersetcount = recognisedparts.supersetcount;
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

Recognisedparts.updateById = (id, recognisedparts, result) => {
  sql.query(
    "UPDATE Recognisedparts SET no = ?, run_id = ?, color_id = ?, identifier = ?, score = ?, created = ? WHERE id = ?",
    [recognisedparts.no, recognisedparts.run_id, recognisedparts.color_id, recognisedparts.identifier, recognisedparts.score, recognisedparts.created, id],
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

      //console.log("updated recognisedparts: ", { id: id, ...collection });
      result(null, { id: id, ...recognisedparts });
    }
  );
};

Recognisedparts.findById = (recognisedpartsId, result) => {
  sql.query(`SELECT * FROM Recognisedparts WHERE id = ${recognisedpartsId}`, (err, res) => {
    if (err) {
      console.log("error: ", err);
      result(null, err);
      return;
    }
    if (res.length) {
      var recPart = res[0]
      var returnPart = new Recognisedparts({
        no : recPart.no,
        run_id : recPart.run_id, 
        color_id : recPart.color_id,
        score : recPart.score,
        identifier : recPart.identifier,
        created : recPart.created,
      });
      returnPart["id"] = recPart.id;
      returnPart["images"] = [];
      returnPart["images_deleted"] = [];
          
      sql.query(`SELECT * FROM Recognisedimages ri LEFT JOIN Partimages pi ON ri.image_id = pi.id WHERE ri.score > 60 AND pi.deleted IS NULL AND ri.part_id = ${recPart.id}`, (err, recImages) => {
        if (err) {
          console.log("error: ", err);
          result(null, err);
          return;
        }

        recImages.forEach(image => {
          var tempImage = new Partimage({
            run_id : image.run_id,
            path : image.path,
            size_kb : image.size_kb,
            created : image.created,
            imported : image.imported,
            deleted : image.deleted
          })
          tempImage["id"] = image.id;
          returnPart.images.push(tempImage);
        });
       
        sql.query(`SELECT * FROM Recognisedimages ri LEFT JOIN Partimages pi ON ri.image_id = pi.id WHERE  ri.part_id = ${recPart.id} AND (ri.score IS NULL OR pi.deleted IS NOT NULL)`, (err, recImages_deleted) => {
          if (err) {
            console.log("error: ", err);
            result(null, err);
            return;
          }
          
          recImages_deleted.forEach(image => {
            var tempImage = new Partimage({
              run_id : image.run_id,
              path : image.path,
              size_kb : image.size_kb,
              created : image.created,
              imported : image.imported,
              deleted : image.deleted
            })
            tempImage["id"] = image.id;
            returnPart.images_deleted.push(tempImage);
          });
          result(null, returnPart);
        });
      });

      
    } else
      result({ kind: "not_found" }, null);
  });
};

Recognisedparts.getAllLabeledbyRunId = (runId, result) => {
  sql.query(`SELECT id, no, color_id, score, created FROM Recognisedparts WHERE run_id = ${runId} AND no IS NOT NULL AND deleted IS NULL`, (err, recParts) => {
    if (err) {
      console.log("error: ", err);
      result(null, err);
      return;
    }
    returnParts = [];
    recParts.forEach(recPart => {

        var tempPart = new Recognisedparts({
          no : recPart.no,
          run_id : runId, 
          color_id : recPart.color_id,
          score : recPart.score,
          identifier : recPart.identifier,
          created : recPart.created,
        });
        tempPart["id"] = recPart.id;
        tempPart["images"] = [];

        
        sql.query(`SELECT * FROM Recognisedimages ri LEFT JOIN Partimages pi ON ri.image_id = pi.id WHERE ri.score > 60 AND pi.deleted IS NULL AND ri.part_id = ${recPart.id}`, (err, recImages) => {
          if (err) {
            console.log("error: ", err);
            result(null, err);
            return;
          }

          recImages.forEach(image => {
            var tempImage = new Partimage({
              run_id : image.run_id,
              path : image.path,
              size_kb : image.size_kb,
              created : image.created,
              imported : image.imported,
              deleted : image.deleted
            })
            tempPart.images.push(tempImage);
          });

      });
      returnParts.push(tempPart);
    });
   
    result(null, returnParts);
  });
};

Recognisedparts.getAllUnLabeledbyRunId = (runId, result) => {
  console.log("runId:" + runId );
  sql.query(`SELECT * FROM Recognisedparts WHERE run_id = ${runId} AND no IS NULL AND deleted IS NULL`, (err, recParts) => {
    if (err) {
      console.log("error: ", err);
      result(null, err);
      return;
    }
    returnParts = [];
    recParts.forEach(recPart => {
        //console.log("id" + recPart.id)
        var tempPart = new Recognisedparts({
          no : recPart.no,
          run_id : runId, 
          color_id : recPart.color_id,
          score : recPart.score,
          identifier : recPart.identifier,
          created : recPart.created,
        });
        tempPart["images"] = [];
        tempPart["id"] = recPart.id
        
        sql.query(`SELECT *, pi.w * pi.h as dimension, pi.camera FROM Recognisedimages ri LEFT JOIN Partimages pi ON ri.image_id = pi.id WHERE pi.deleted IS NULL AND ri.part_id = ${recPart.id} ORDER BY pi.camera, dimension desc`, (err, recImages) => {
          if (err) {
            console.log("error: ", err);
            result(null, err);
            return;
          }

          recImages.forEach(image => {
            var tempImage = new Partimage({
              camera : image.camera,
              path : image.path,
              size_kb : image.size_kb,
              created : image.created,
              imported : image.imported,
              deleted : image.deleted
            })
            tempImage["id"] = image.id

            tempPart.images.push(tempImage);
          });

      });
      returnParts.push(tempPart);
    });
    //console.log("returnPartsXCXX: ", returnParts);
    result(null, returnParts);
  });
};

Recognisedparts.getAllUnsettedPartsOfCollectionId = (colId, result) => {
  sql.query(` SELECT PartNo, color_id, super_set_count FROM LegoSorterDB.unsetted_parts WHERE collection_id = ${colId}`, (err, unsettedParts) => {
    if (err) {
      console.log("error while getting unsettet Parts: ", err);
      result(err, null);
      return;
    }
    result(null, unsettedParts);
  });

};

Recognisedparts.getSuggestedSets = (colId, result) => {
  //console.log("colId:" + colId );
  sql.query(` SELECT collection_id, 
  partNos, 
  color_ids, 
  setNo, 
  count, 
  s_id, 
  no, 
  name, category_id, year, weight_g, size, complete_part_count, complete_minifigs_count, min_price, max_price, avg_price, qty_avg_price, unit_quantity, total_quantity, thumbnail_url, image_url, created, parts_existing, complete_percentage 
  FROM LegoSorterDB.suggested_sets_detail_view 
  WHERE count > ROUND((SELECT max(count) FROM LegoSorterDB.suggested_sets_detail_view)*0.7,0) 
  AND setNo IS NOT NULL 
  AND collection_id = ${colId} 
  ORDER by count desc`, (err, suggestedSets) => {
    if (err) {
      console.log("error while getting suggested Sets: ", err);
      result(err, null);
      return;
    }
    result(null, suggestedSets);
  });

};


Recognisedparts.updateById = (id, recognisedparts, result) => {
  sql.query(
    "UPDATE Recognisedparts SET no = ?, run_id = ?, color_id = ?, score = ?, identifier = ?, created = ? WHERE id = ?",
    [recognisedparts.no, recognisedparts.run_id, recognisedparts.color_id, recognisedparts.score, recognisedparts.identifier, recognisedparts.created, id],
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

Recognisedparts.MarkAsDeletedById = (recognisedpartId, result) => {
  var deleted = new Date().toISOString().slice(0, 19).replace('T', ' ');
  sql.query(
    "UPDATE Recognisedparts SET deleted = ? WHERE id = ?",
    [deleted, recognisedpartId],
    (err, res) => {
      if (err) {
        console.log("error: ", err);
        result(null, err);
        return;
      }

      if (res.affectedRows == 0) {
        // not found recognisedpartId with the id
        result({ kind: "not_found" }, null);
        return;
      }

      //console.log("updated Recognisedparts: ", { id: id, ...Recognisedparts });
      result(null, { recognisedpartId: recognisedpartId});
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