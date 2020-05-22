const blApi = require("../config/bl.api.js");
/*
    //SET Information
    blApi.bricklinkClient.getCatalogItem(blApi.ItemType.Set, '9526-1')
    .then(function(setinfo){
        console.log(setinfo);
    });
   
    //SET ItemImage
    blApi.bricklinkClient.getItemImage(blApi.ItemType.Set, '9526-1')
    .then(function(setimage){
        console.log(setimage);
    });
    
      //SET Subset
        blApi.bricklinkClient.getItemSubset(blApi.ItemType.Set, '9479-1', {break_minifigs: true})
    .then(function(subsets){
       
        console.log(JSON.stringify(subsets));
    });

    
   

   */ 
   
    //SET PriceGuide
    blApi.bricklinkClient.getPriceGuide(blApi.ItemType.Set, '8880-1', {new_or_used: blApi.Condition.Used, country_code: 'DE', guide_type: 'stock'})
    .then(function(price){
        console.log(price);
    });

 