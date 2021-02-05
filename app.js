var express             = require("express"),
    app                 = express(),
    moment              = require('moment'),
    bodyParser          = require("body-parser"),
    methodOverride      = require("method-override")

const PythonConnector = require('./PythonConnector/PythonConnector.js');

// sudo service mysqld start
// obiwan
// mysql -uroot -p LegoSorterDB

// parse requests of content-type: application/json
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: true}));    
app.set("view engine","ejs");
app.use(express.static(__dirname + "/public"));
app.use(express.static(__dirname + "/partimages/"));
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
require("./routes/superset.routes.js")(app);
require("./routes/recognisedpart.routes.js")(app);
require("./routes/recognisedset.routes.js")(app);
require("./routes/partimage.routes.js")(app);
require("./routes/sorter.routes.js")(app);
require("./routes/pythonconnector.routes.js")(app);



const PORT = process.env.PORT || 3000;
const IP = process.env.IP || '192.168.178.46' || 'localhost'
//const IP = process.env.IP 

app.listen(PORT, IP, async () => {
    console.log(`Server has started on ${IP}:${PORT}`);
    await PythonConnector.invoke('listen');
});