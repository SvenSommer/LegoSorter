const Partimage = require("../models/partimage.model.js");

exports.delete = (req, res) => {
  if (!req.body) {
    res.status(400).send({
      message: "Content can not be empty!"
    });
  }

  req.body.ImageIds.forEach(imageid => {
   
    Partimage.MarkAsDeletedById(imageid.split("-")[1], (err, imagedata) => {
      if (err)
        res.status(500).send({
          message:
            err.message || "Some error occurred while deleting Recognisedimage."
        });
    });

  });
  res.status(200).send();
};
