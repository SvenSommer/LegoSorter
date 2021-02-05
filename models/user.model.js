const sql = require("../config/db.js");

const User = function(user) {
  this.username = user.username;
  this.password = user.password;
};


module.exports = User;