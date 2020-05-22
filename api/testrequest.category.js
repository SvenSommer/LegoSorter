const blApi = require("../config/bl.api.js");


   var req = blApi.Category.get(123);
     blApi.bricklinkClient.send(req).then(category => console.log(category));
    
   var req = blApi.Category.all();
     blApi.bricklinkClient.send(req).then(category => console.log(category));

 
 