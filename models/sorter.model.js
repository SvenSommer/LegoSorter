const sql = require("../config/db.js");
const request = require('request');


class Sorter {
  constructor(sorter) {
    this.name = sorter.name;
    this.lifter_status_url = sorter.lifter_status_url;
    this.lifter_update_url = sorter.lifter_update_url;
    this.lifter_alterspeed_url = sorter.lifter_alterspeed_url;
    this.vfeeder_status_url = sorter.vfeeder_status_url;
    this.vfeeder_update_url = sorter.vfeeder_update_url;
    this.vfeeder_alterspeed_url = sorter.vfeeder_alterspeed_url;
    this.conveyor_status_url = sorter.conveyor_status_url;
    this.conveyor_update_url = sorter.conveyor_update_url;
    this.conveyor_alterspeed_url = sorter.conveyor_alterspeed_url;
    this.pusher_count = sorter.pusher_count;
    this.pusher_status_baseurl = sorter.pusher_status_baseurl;
    this.pusher_mode_baseurl = sorter.pusher_mode_baseurl;
    this.created = new Date().toISOString().slice(0, 19).replace('T', ' ');
    this.status = null;
  }
  static create(newSorter, result) {
    sql.query("INSERT INTO Sorters SET ?", newSorter, (err, res) => {
      if (err) {
        console.log("error: ", err);
        result(err, null);
        return;
      }
      //console.log("created sorter: ", { id: res.insertId, ...newSorter });
      result(null, { id: res.insertId, ...newSorter });
    });
  }
  static findById(sorterId, result) {
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
  }
  static getAll(result) {
    sql.query("SELECT * FROM Sorters", (err, res) => {
      if (err) {
        console.log("error: ", err);
        result(null, err);
        return;
      }
      
      result(null, res);
    });
  }
  static updateById(id, sorter, result) {
    sql.query("UPDATE Sorters SET name = ?, lifter_motormode_url = ?, lifter_motorspeed_url = ?, lifter_clientstatus_url = ?, vfeeder_motormode_url = ?, vfeeder_motorspeed_url = ?, vfeeder_clientstatus_url = ?, conveyor_motormode_url = ?, conveyor_motorspeed_url = ?, conveyor_clientstatus_url = ?, pusher_count = ?, pusher_status_baseurl = ?, pusher_mode_baseurl = ?, created = ? WHERE id = ?", [sorter.name, sorter.lifter_motormode_url, sorter.lifter_motorspeed_url, sorter.lifter_clientstatus_url, sorter.vfeeder_motormode_url, sorter.vfeeder_motorspeed_url, sorter.vfeeder_clientstatus_url, sorter.conveyor_motormode_url, sorter.conveyor_motorspeed_url, sorter.conveyor_clientstatus_url, sorter.pusher_count, sorter.pusher_status_baseurl, sorter.pusher_mode_baseurl, sorter.created, id], (err, res) => {
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
    });
  }
  static remove(id, result) {
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
  }
  static removeAll(result) {
    sql.query("DELETE FROM Sorters", (err, res) => {
      if (err) {
        console.log("error: ", err);
        result(null, err);
        return;
      }
      console.log(`deleted ${res.affectedRows} sorter`);
      result(null, res);
    });
  }
  static addStatus(status){
    this.status = status;
  }
}
module.exports = Sorter;