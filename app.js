var express             = require("express"),
    app                 = express(),
    moment              = require('moment'),
    bodyParser          = require("body-parser");


// sudo service mysqld start
// obiwan
// mysql -uroot -p

// parse requests of content-type: application/json
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: true}));    
app.set("view engine","ejs");


app.get("/", function(req,res){
    res.render("landing");
});



moment.locale("en");
app.locals.moment = moment;

require("./routes/collection.routes.js")(app);

app.listen(process.env.PORT, process.env.IP, function(){
    console.log("Server has started!");
});