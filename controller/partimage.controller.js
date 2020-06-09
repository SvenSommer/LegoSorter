const fs = require('fs');
const path = require( 'path' );
const Run = require("../models/run.model.js");
const Partimage = require("../models/partimage.model.js");



exports.importImagesFromFolder = (req, res) => {
    Run.findById(req.params.Id, (err, run) => {
        if (err) {
          if (err.kind === "not_found") {
            res.status(404).send({
              message: `Not found ImageFolder with Runid ${req.params.Id}.`
            });
          } else {
            res.status(500).send({
              message: "Error retrieving ImageFolder with Runid " + req.params.Id
            });
          }
        } else {
            (async ()=>{
            try {

                const images = await fs.promises.readdir(run.imagefolder)
                for( const image of images ) {
                    const imagepath = path.join( run.imagefolder, image );
                    const stat = await fs.promises.stat( imagepath );

                    if( stat.isFile() ) {

                       // if(image.substring(0,2) == "i_")
                       //   continue;
                       // var newname =  path.join( run.imagefolder, 'i_' + image );
                        var newname =  path.join( run.imagefolder, image );
                        await fs.promises.rename( imagepath, newname );
                        
                    }
                    console.log( "renamed to '%s'", newname );
                        var partimage = new Partimage({
                            run_id : run.id,
                            path :  newname.replace("/home/robert/LegoSorter/public",""),
                            size_kb : stat.size,
                            created : stat.birthtime
                        });
                        Partimage.create(partimage,(err, data) => {
                            if (err)
                              res.status(500).send({
                                message:
                                  err.message || "Some error occurred while creating the Collection."
                              });
                        });
                } // End for...of

            }
            catch( e ) {
            // Catch anything bad that happens
            console.error( "We've thrown! Whoops!", e );
            }
            })(); 
        }
    })
    res.redirect("/runs/"+ req.params.Id);  
};