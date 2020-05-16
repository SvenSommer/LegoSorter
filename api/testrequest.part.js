const blApi = require("../config/bl.api.js");

    

   

    //Part Information
    blApi.bricklinkClient.getCatalogItem(blApi.ItemType.Part, '2877', 0)
    .then(function(partinfo){
        console.log(partinfo);
    });
 
    //Part Image
    blApi.bricklinkClient.getItemImage(blApi.ItemType.Part, '2877', 0)
    .then(function(partimage){
        console.log(partimage);
    });
        
   //Part PriceGuide
    blApi.bricklinkClient.getPriceGuide(blApi.ItemType.Part, '2877', {new_or_used: blApi.Condition.Used})
    .then(function(price){
        console.log(price);

    });
/*  
        //Part Superset
    blApi.bricklinkClient.getItemSuperset(blApi.ItemType.Part, '2877')
    .then(function(subsets){
       
        console.log(JSON.stringify(subsets));
    });
    */