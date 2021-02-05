const sql = require("../config/db.js");

// constructors
const Run = function(run) {
  this.no = run.no,
  this.collection_id = run.collection_id;
  this.sorter_id = run.sorter_id;
  this.imagefolder = run.imagefolder;
  this.created = new Date().toISOString().slice(0, 19).replace('T', ' ');
};

const RunStatus = function(runstatus) {
  this.run_id = runstatus.run_id;
  this.status = runstatus.status;
  this.reason = runstatus.reason;
  this.created = new Date().toISOString().slice(0, 19).replace('T', ' ');
};

const RunStatistic = function(runstatistic) {
  this.run_id = runstatistic.run_id;
  this.collection_id = runstatistic.collection_id;
  this.parts_unidentified = runstatistic.parts_unidentified;
  this.parts_deleted = runstatistic.parts_deleted;
  this.parts_identified = runstatistic.parts_identified;
  this.parts_identified_by_human = runstatistic.parts_identified_by_human;
  this.parts_identified_by_cnn = runstatistic.parts_identified_by_cnn;
  this.parts_uniquepartsidentified = runstatistic.parts_uniquepartsidentified;
};

Run.create = (newRun, result) => {
  sql.query("INSERT INTO Runs SET ?", newRun, (err, res) => {
    if (err) {
      console.log("error: ", err);
      result(err, null); 
      return;
    }
    var newRunStatus = new RunStatus({
      run_id : res.insertId,
      status : 10
    });
    sql.query("INSERT INTO RunStatus SET ?", newRunStatus, (err, res) => {
      if (err) {
        console.log("error with runStatus: ", err);
        result(err, null);
        return;
      }
      //console.log("created run: ", { id: res.insertId, ...newRun });
      result(null, { id: res.insertId, ...newRun });
    });
  });
};

Run.findById = (runId, result) => {
  sql.query(`SELECT *, r.no, r.id as run_id,  st.name as status_name, st.description as status_description
  FROM Runs r
  LEFT JOIN RunStatus rs ON r.id = rs.run_id
  LEFT JOIN Status st ON rs.status = st.id AND st.type = 'run'
   WHERE run_id = ${runId}
   ORDER BY rs.created desc`, (err, res) => {
    if (err) {
      console.log("error: ", err);
      result(err, null);
      return;
    }

    if (res.length) {
      //console.log("found run: ", res[0]);
      result(null, res[0]);
      return;
    }

    // not found Run with the id
    result({ kind: "not_found" }, null);
  });
};

Run.getAll = result => {
  sql.query(`SELECT *,  r.no, r.id as run_id, st.name as status_name, st.description as status_description
            FROM Runs r
            LEFT JOIN RunStatus rs ON r.id = rs.run_id
            LEFT JOIN Status st ON rs.status = st.id AND st.type = 'run'`, (err, res) => {
    if (err) {
      console.log("error: ", err);
      result(null, err);
      return;
    }

    //console.log("runs: ", res);
    result(null, res);
  });
};

Run.updateById = (id, run, result) => {
  sql.query(
    "UPDATE Runs SET no = ?, collection_id = ?, sorter_id = ?, imagefolder = ?, created = ? WHERE id = ?",
    [run.no, run.collection_id, run.sorter_id, run.imagefolder, run.created, id],
    (err, res) => {
      if (err) {
        console.log("error: ", err);
        result(null, err);
        return;
      }

      if (res.affectedRows == 0) {
        // not found run with the id
        result({ kind: "not_found" }, null);
        return;
      }

      //console.log("updated run: ", { id: id, ...run });
      result(null, { id: id, ...run });
    }
  );
};

Run.remove = (id, result) => {
  sql.query("DELETE FROM Runs WHERE id = ?", id, (err, res) => {
    if (err) {
      console.log("error: ", err);
      result(null, err);
      return;
    }

    if (res.affectedRows == 0) {
      // not found run with the id
      result({ kind: "not_found" }, null);
      return;
    }

    sql.query("DELETE FROM RunStatus WHERE run_id = ?", id, (err, res) => {
      if (err) {
        console.log("error: ", err);
        result(null, err);
        return;
      }

      if (res.affectedRows == 0) {
        // not found run with the id
        result({ kind: "not_found" }, null);
        return;
      }
    });

    console.log("deleted run with id: ", id);
    result(null, res);
  });
};

Run.removeAll = result => {
  sql.query("DELETE FROM Runs", (err, res) => {
    if (err) {
      console.log("error: ", err);
      result(null, err);
      return;
    }

    console.log(`deleted ${res.affectedRows} run`);
    result(null, res);
  });
};

Run.findAllRunsByCollectionId = (colId, result) => {
  sql.query(`SELECT *, r.id as run_id, st.name as status_name, st.description as status_description
            FROM Runs r
            LEFT JOIN RunStatus rs ON r.id = rs.run_id
            LEFT JOIN Status st ON rs.status = st.id AND st.type = 'run'
            WHERE collection_id =  ${colId}`, (err, res) => {
    if (err) {
      console.log("error: ", err);
      result(err, null);
      return;
    }

    result(null, res);
  });
};

Run.findNextRunNoforCollectionId = (colId, result) => {
    sql.query(`SELECT IFNULL(Max(no),0)+1 as no_next
    FROM Runs r
    WHERE collection_id =  ${colId}`, (err, res) => {
    if (err) {
      console.log("error: ", err);
      result(err, null);
      return;
    }
    result(null, res[0]);
    });
  };

Run.findRunStatusByRunId= (runId, result) => {
  sql.query(`SELECT * ,st.name as status_name, st.description as status_description
  FROM RunStatus rs
  LEFT JOIN Status st ON rs.status = st.id AND st.type = 'run'
  WHERE run_id =  ${runId}`, (err, res) => {
    if (err) {
      console.log("error: ", err);
      result(err, null);
      return;
    }

    result(null, res);
  });
};

Run.getRunsStatisticsByCollectionId = (colId, result) => {
  sql.query(`SELECT * FROM (
    SELECT r.id as run_id,
    st.name as status_name,
    st.description as status_description,
    r.created as created,
    SUM(IF(rp.deleted IS NULL AND rp.no IS NULL,1,0)) as parts_unidentified,
    SUM(IF(rp.deleted IS NOT NULL,1,0)) as parts_deleted,
    SUM(IF(rp.deleted IS NULL AND rp.no IS NOT NULL,1,0)) as parts_identified, 
    SUM(IF(rp.deleted IS NULL AND rp.no IS NOT NULL AND rp.identifier = 'human',1,0)) as parts_identified_by_human, 
    SUM(IF(rp.deleted IS NULL AND rp.no IS NOT NULL AND rp.identifier != 'human',1,0)) as parts_identified_by_cnn
    FROM LegoSorterDB.Recognisedparts rp
    LEFT JOIN LegoSorterDB.Runs r ON r.id = rp.run_id
    LEFT JOIN LegoSorterDB.RunStatus rs ON r.id = rs.run_id
    LEFT JOIN LegoSorterDB.Status st ON rs.status = st.id AND st.type = 'run' 
    where r.collection_id = ${colId} 
    GROUP BY r.id, status_name,status_description,created) As allparts_specific
  JOIN (SELECT COUNT(*) as parts_uniquepartsidentified , parts_uniquepartsidentified.run_id FROM (SELECT COUNT(*), r.id as run_id FROM LegoSorterDB.Recognisedparts rp
    LEFT JOIN LegoSorterDB.Runs r ON r.id = rp.run_id
    WHERE deleted IS NULL AND rp. no IS NOT NULL 
    AND collection_id = ${colId} 
    GROUP BY rp.no, run_id) as parts_uniquepartsidentified GROUP BY run_id) as uniqueparts_specific
  ON allparts_specific.run_id = uniqueparts_specific.run_id`, (err, resStatistics) => {

    if (err) {
      console.log("error: ", err);
      result(err, null);
      return;
    }
    result(null, resStatistics);

  });
};

Run.getTotalRunsStatisticsForCollectionId = (colId, result) => {
  sql.query(`SELECT 
    SUM(IF(rp.deleted IS NULL AND rp.no IS NULL,1,0)) as parts_unidentified,
    SUM(IF(rp.deleted IS NOT NULL,1,0)) as parts_deleted,
    SUM(IF(rp.deleted IS NULL AND rp.no IS NOT NULL,1,0)) as parts_identified, 
    SUM(IF(rp.deleted IS NULL AND rp.no IS NOT NULL AND rp.identifier = 'human',1,0)) as parts_identified_by_human, 
    SUM(IF(rp.deleted IS NULL AND rp.no IS NOT NULL AND rp.identifier != 'human',1,0)) as parts_identified_by_cnn
    FROM LegoSorterDB.Recognisedparts rp
    LEFT JOIN LegoSorterDB.Runs r ON r.id = rp.run_id
    where collection_id = ${colId}  `, (err, resStatistics) => {

    if (err) {
      console.log("error: ", err);
      result(err, null);
      return;
    }

    sql.query(`SELECT COUNT(*) FROM (SELECT COUNT(*) FROM LegoSorterDB.Recognisedparts rp
      LEFT JOIN LegoSorterDB.Runs r ON r.id = rp.run_id
      WHERE deleted IS NULL AND rp. no IS NOT NULL 
      AND collection_id = ${colId}  
      GROUP BY rp.no) as parts_uniquepartsidentified`, (err, parts_uniquepartsidentified) => {
        if (err) {
          console.log("error: ", err);
          result(err, null);
          return;
        }

        var runStatistic = new RunStatistic({
          run_id : runId,
          collection_id : resStatistics[0].collection_id,
          parts_unidentified : resStatistics[0].parts_unidentified,
          parts_deleted : resStatistics[0].parts_deleted,
          parts_identified : resStatistics[0].parts_identified,
          parts_identified_by_human : resStatistics[0].parts_identified_by_human,
          parts_identified_by_cnn : resStatistics[0].parts_identified_by_cnn,
          parts_uniquepartsidentified : parts_uniquepartsidentified[0].parts_uniquepartsidentified
        });
        
         result(null, runStatistic);
    });
  });
};

module.exports = Run;