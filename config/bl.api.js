const api = require('bricklink-api');
const blConfig = require("./bl.api.config.js");
const Client = api.Client,
    ItemType = api.ItemType,
    Condition = api.Condition,
    Category = api.Category,
    Color = api.Color;
    
var bricklinkClient = new Client({
    "consumer_key": blConfig.CONSUMERKEY,
    "consumer_secret": blConfig.CONSUMERSECRET,
    "token": blConfig.TOKEN,
    "token_secret": blConfig.TOKENSECRET
});

module.exports = {
    bricklinkClient,
    ItemType,
    Condition,
    Category,
    Color
};