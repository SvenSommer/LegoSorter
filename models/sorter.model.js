const sql = require("../config/db.js");

// constructor
const Sorter = function(sorter) {
  this.name = sorter.name;
  this.separate_conveyor_mode_url = sorter.separate_conveyor_mode_url;
  this.separate_conveyor_speed_url = sorter.separate_conveyor_speed_url;
  this.separate_conveyor_status_url = sorter.separate_conveyor_status_url;
  this.vibration_motor_mode_url = sorter.vibration_motor_mode_url;
  this.vibration_motor_speed_url = sorter.vibration_motor_speed_url;
  this.vibration_motor_status_url = sorter.vibration_motor_status_url;
  this.dispense_conveyor_mode_url = sorter.dispense_conveyor_mode_url;
  this.dispense_conveyor_speed_url = sorter.dispense_conveyor_speed_url;
  this.dispense_conveyor_status_url = sorter.dispense_conveyor_status_url;
  this.pusher_count = sorter.pusher_count;
  this.pusher_status_baseurl = sorter.pusher_status_baseurl;
  this.pusher_mode_baseurl = sorter.pusher_mode_baseurl;
  this.created = new Date().toISOString().slice(0, 19).replace('T', ' ');
};

Sorter.create = (newSorter, result) => {
  sql.query("INSERT INTO Sorters SET ?", newSorter, (err, res) => {
    if (err) {
      console.log("error: ", err);
      result(err, null);
      return;
    }

    //console.log("created sorter: ", { id: res.insertId, ...newSorter });
    result(null, { id: res.insertId, ...newSorter });
  });
};

Sorter.findById = (sorterId, result) => {
  sql.query(`SELECT * FROM Sorters WHERE id = ${sorterId}`, (err, res) => {
    if (err) {
      console.log("error: ", err);
      result(err, null);
      return;
    }

    if (res.length) {
      //console.log("found sorter: ", res[0]);
      result(null, res[0]);
      return;
    }

    // not found Sorter with the id
    result({ kind: "not_found" }, null);
  });
};

Sorter.getAll = result => {
  sql.query("SELECT * FROM Sorters", (err, res) => {
    if (err) {
      console.log("error: ", err);
      result(null, err);
      return;
    }

    //console.log("sorters: ", res);
    result(null, res);
  });
};

Sorter.updateById = (id, sorter, result) => {
  sql.query(
    "UPDATE Sorters SET name = ?, separate_conveyor_mode_url = ?, separate_conveyor_speed_url = ?, separate_conveyor_status_url = ?, vibration_motor_mode_url = ?, vibration_motor_speed_url = ?, vibration_motor_status_url = ?, dispense_conveyor_mode_url = ?, dispense_conveyor_speed_url = ?, dispense_conveyor_status_url = ?, pusher_count = ?, pusher_status_baseurl = ?, pusher_mode_baseurl = ?, created = ? WHERE id = ?",
    [sorter.name, sorter.separate_conveyor_mode_url, sorter.separate_conveyor_speed_url, sorter.separate_conveyor_status_url, sorter.vibration_motor_mode_url, sorter.vibration_motor_speed_url, sorter.vibration_motor_status_url, sorter.dispense_conveyor_mode_url, sorter.dispense_conveyor_speed_url, sorter.dispense_conveyor_status_url, sorter.pusher_count, sorter.pusher_status_baseurl, sorter.pusher_mode_baseurl, sorter.created, id],
    (err, res) => {
      if (err) {
        console.log("error: ", err);
        result(null, err);
        return;
      }

      if (res.affectedRows == 0) {
        // not found sorter with the id
        result({ kind: "not_found" }, null);
        return;
      }

      //console.log("updated sorter: ", { id: id, ...sorter });
      result(null, { id: id, ...sorter });
    }
  );
};

Sorter.remove = (id, result) => {
  sql.query("DELETE FROM Sorters WHERE id = ?", id, (err, res) => {
    if (err) {
      console.log("error: ", err);
      result(null, err);
      return;
    }

    if (res.affectedRows == 0) {
      // not found sorter with the id
      result({ kind: "not_found" }, null);
      return;
    }

    console.log("deleted sorter with id: ", id);
    result(null, res);
  });
};

Sorter.removeAll = result => {
  sql.query("DELETE FROM Sorters", (err, res) => {
    if (err) {
      console.log("error: ", err);
      result(null, err);
      return;
    }

    console.log(`deleted ${res.affectedRows} sorter`);
    result(null, res);
  });
};

module.exports = Sorter;