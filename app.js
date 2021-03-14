const express = require("express");
const bodyParser = require("body-parser");
const ejs = require("ejs");
const _ = require("lodash");
const { property } = require("lodash");

const app = express();

app.set('view engine', 'ejs');

app.use(express.static("public"));

app.use(bodyParser.urlencoded({
   extended: false
}));

app.use(bodyParser.json());

app.use(express.static("public"));

app.get("/", function (req, res) {
  res.render("home");
});

// search button 
app.post("/search", function (req, res) {
  const search = req.body.search;
  console.log(search);
  res.redirect("/report");
});

app.get("/report", function (req, res) {
  var property = {
    address: "1234 example st",
    price: "price",
    school: 1,
    crime: 1,
    example: "test",
    example2: "test2"
  }
  res.render("report", { property: property});
});

let port = process.env.PORT;
if (port == null || port == "")
  port = 8000;

app.listen(port, function() {
  console.log("Server started on port " + port + "...");
});
