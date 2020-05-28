var express             = require("express"),
    app                 = express(),
    moment              = require('moment'),
    bodyParser          = require("body-parser"),
    methodOverride      = require("method-override"),
    passport            = require('passport'),
    LocalStrategy       = require('passport-local').Strategy;


// sudo service mysqld start
// obiwan
// mysql -uroot -p

// parse requests of content-type: application/json
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: true}));    
app.set("view engine","ejs");
app.use(express.static(__dirname + "/public"));
app.use(methodOverride("_method"));


app.get("/", function(req,res){
    res.render("landing");
});

moment.locale("en");
app.locals.moment = moment;

require("./routes/collection.routes.js")(app);
require("./routes/set.routes.js")(app);
require("./routes/part.routes.js")(app);
require("./routes/preferences.routes.js")(app);
require("./routes/color.routes.js")(app);
require("./routes/category.routes.js")(app);

require("./routes/run.routes.js")(app);
require("./routes/sorter.routes.js")(app);

app.listen(process.env.PORT || 3000, process.env.IP || '192.168.178.67', function(){
    console.log("Server has started!");
});