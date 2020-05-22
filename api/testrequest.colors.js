const blApi = require("../config/bl.api.js");


   var req = blApi.Color.get(10);
     blApi.bricklinkClient.send(req).then(color => console.log(color));
    
   var req = blApi.Color.all();
     blApi.bricklinkClient.send(req).then(colors => console.log(colors));

 
 