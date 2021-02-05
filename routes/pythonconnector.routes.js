module.exports = app => {
    const PythonConnector = require("../PythonConnector/PythonConnector.js");
    var path = require('path');

    // Our prediction endpoint
    app.post('/predict', async function (req, res, next) {
        console.log(req.url);
        if (!req.body) {
            res.status(400).send({
              message: "Content can not be empty!"
            });
          }
        try {
            imagepath = path.join("/home/robert/LegoSorter/partimages/",req.body.imagepath);
            imagepath = imagepath.replace("/home/robert/LegoSorter/partimages/home/robert/LegoSorter/partimages/","/home/robert/LegoSorter/partimages/")
            console.log("imagepath: " + imagepath);

            const prediction = await PythonConnector.invoke('predict_from_img', imagepath);
            console.log(prediction)
            res.json(prediction);

            
        }
        catch (e) {
            console.log(`error in ${req.url}`, e);
            res.sendStatus(404);
        }
    });

    app.get('/test', async function (req, res, next) {
        console.log(req.url);
        try {
            var pyRes = await PythonConnector.invoke('test', 'None');
            var data = {result: pyRes}
            res.json(data);
        }
        catch (e) {
            console.log('error in /test', e);
            res.sendStatus(404);
        }
    });

    app.get('/bricksortedresponse', async function (req, res, next) {
        console.log(req.url);
        try {
            var pyRes = await PythonConnector.invoke('test', 'None');
            var data = {result: pyRes}
            res.json(data);
            //res.sendStatus(200);
        }
        catch (e) {
            console.log('error in /test', e);
            res.sendStatus(404);
        }
    });
};