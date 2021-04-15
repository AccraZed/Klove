const express = require("express");
const bodyParser = require("body-parser");
const ejs = require("ejs");
const _ = require("lodash");
//const { property } = require("lodash");
const { spawn } = require("child_process");

const app = express();

app.set('view engine', 'ejs');

app.use(express.static("public"));

app.use(bodyParser.urlencoded({
   extended: false
}));

app.use(bodyParser.json());

app.use(express.static("public"));

var property = {
    address: "1234 example st",
    price: "$100 000 000",
    school: "A-",
    crime: 1,
    walk_score: 90,
    bike_score: 94,
    transit_score: 80,
}

app.get("/", function (req, res) {
  res.render("home");
});



// search button 
app.post("/search", function (req, res) {

  const houseNumber = req.body.houseNumber;
  const streetName = req.body.streetName;
  const city = req.body.city;
  const state = req.body.state;
  const zip = req.body.zip; 
  property.address = houseNumber + " " + streetName;

  const python = spawn('python', ['src/main.py', houseNumber, streetName, city, state, zip]);
  //console.log(python);
  python.stdout.on('data', function (data) {
    console.log(data);
  });

  res.redirect("/report");
});

app.get("/report", function (req, res) {

  console.log(property.address);
  res.render("report", { property: property});
});

let port = process.env.PORT;
if (port == null || port == "")
  port = 8000;

app.listen(port, function() {
  console.log("Server started on port " + port + "...");
});
