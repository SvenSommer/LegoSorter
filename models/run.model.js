const sql = require("../config/db.js");

// constructors
const Run = function(run) {
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
  sql.query(`SELECT *, r.id as run_id,  st.name as status_name, st.description as status_description
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
  sql.query(`SELECT *, r.id as run_id, st.name as status_name, st.description as status_description
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
    "UPDATE Runs SET collection_id = ?, sorter_id = ?, imagefolder = ?, created = ? WHERE id = ?",
    [run.collection_id, run.sorter_id, run.imagefolder, run.created, id],
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


module.exports = Run;