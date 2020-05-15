const blApi = require("../config/bl.api.js");




    //SET Information
    blApi.bricklinkClient.getCatalogItem(blApi.ItemType.Set, '9526-1')
    .then(function(setinfo){
        console.log(setinfo);
    });
/*    
    //SET ItemImage
    blApi.bricklinkClient.getItemImage(blApi.ItemType.Set, '9526-1')
    .then(function(setimage){
        console.log(setimage);
    });
    
    //SET Subset
    blApi.bricklinkClient.getItemSubset(blApi.ItemType.Set, '9526-1', {break_minifigs: true})
    .then(function(subsets){
       
        console.log(JSON.stringify(subsets));
    });
    
    //SET PriceGuide
    blApi.bricklinkClient.getPriceGuide(blApi.ItemType.Set, '9526-1', {new_or_used: blApi.Condition.Used})
    .then(function(price){
        console.log(price);
    });
    
    //Part Information
    blApi.bricklinkClient.getCatalogItem(blApi.ItemType.Part, '3001', 0)
    .then(function(partinfo){
        console.log(partinfo);
    });
 
    //Part Image
    blApi.bricklinkClient.getItemImage(blApi.ItemType.Part, '3001', 0)
    .then(function(partimage){
        console.log(partimage);
    });
*/