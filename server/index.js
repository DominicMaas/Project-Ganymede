const express = require("express");
const fs = require("fs");
const gphoto2 = require("gphoto2");

const app = express();
const cam = new gphoto2.GPhoto2();

// Setup logging
cam.setLogLevel(1);
cam.on("log", function (level, domain, message) {
  console.log(domain, message);
});

// Setup endpoints
app.get("/get-settings", (req, res) => {
  cam.getConfig((er, settings) => {
    res.send(settings);
  });
});

// Start listening
app.listen(3500, () => console.log("Web app started!"));
