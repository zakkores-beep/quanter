/* Inline gen.js and verbal.js into the page: node build.js  ->  index.html */
"use strict";
const fs = require("fs");
const src = fs.readFileSync(__dirname + "/index.src.html", "utf8");
const gen = fs.readFileSync(__dirname + "/gen.js", "utf8");
const verbal = fs.readFileSync(__dirname + "/verbal.js", "utf8");
if (!src.includes("/*GEN*/") || !src.includes("/*VERBAL*/")) throw new Error("placeholder missing");
fs.writeFileSync(__dirname + "/index.html", src.replace("/*GEN*/", () => gen).replace("/*VERBAL*/", () => verbal));
console.log("wrote index.html", fs.statSync(__dirname + "/index.html").size, "bytes");
