const express = require('express');
const app = express();
const mysql = require("mysql");
const bodyParser = require("body-parser");
const cors = require("cors");
const formidable = require("formidable");
const fs = require("fs-extra");
const {spawn} = require('child_process');


const uploadPath = "D:/python/ucsc_courses_website/server/uploads/"

var mydb = mysql.createPool({
    host: "localhost",
    user: "root",
    password: "AsswordPay69",
    database: "ucsc_courses",
    connectionLimit: 10
});


app.post('/upload-avatar', async (req, res) => {
    var form = new formidable.IncomingForm();
    console.log("FORM BEF");
    console.log(form);
    form.parse(req);
    console.log("FORM AFT");
    console.log(form);

    form.on('fileBegin', function (name, file){
        file.path = __dirname + '/uploads/' + file.name;
    });

    form.on('file', function (name, file){
        console.log('Uploaded ' + file.name);
    });

});


app.post('/api/upload', (req, res, next) => {

    const form = new formidable.IncomingForm();
    form.parse(req, function(err, fields, files){
        // console.log("FORM");
        // console.log(form);
        console.log("FILES");
        console.log(files);
        // console.log("FILES 0");
        // console.log(files.file.originalFilename);


        // Source file
        const src = files.file.filepath;

        // Destination path
        const dest = uploadPath+files.file.originalFilename;

        // Function call
        // Using promises
        // Setting overwrite to true
        fs.move(src, dest, { overwrite: true }).then(() => console.log("File moved to the destination"+" folder successfully")).catch((e) => console.log(e));


        // var oldPath = files.profilePic.path;
        // var newPath = path.join(__dirname, 'uploads')
        //         + '/'+files.profilePic.name
        // var rawData = fs.readFileSync(oldPath)

        // fs.writeFile(newPath, rawData, function(err){
        //     if(err) console.log(err)
        //     return res.send("Successfully uploaded")
        // })
  })
});


app.use(bodyParser.urlencoded({extended: true}));
app.use(express.json());
app.use(cors());

app.use(function (req, res, next) {
    res.header("Access-Control-Allow-origin", "*")
    res.setHeader('Access-Control-Allow-Methods', "GET,POST,OPTIONS")
    res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept")
    next();
})

app.get("/", (req, res) =>{
    res.send("UCSC Courses Server");
})

app.post("/api/post-transcript",(req,res)=>{
    // console.log("Posting Transcript");
    
    const form = new formidable.IncomingForm();
    form.parse(req, function(err, fields, files){
        console.log("FILES");
        console.log(files);
        const src = files.file.filepath;
        const dest = uploadPath+files.file.originalFilename;
        fs.move(src, dest, { overwrite: true }).then(() => console.log("File moved to the destination"+" folder successfully"));
        var dataToSend;
        console.log("SPAWN PYTHON");
        const python = spawn('python', ['./pdfTextExtract.py', files.file.originalFilename]);
        python.stdout.on('data', function (data) {
        //  console.log('Pipe data from python script ...');
         dataToSend = data.toString();
        //  console.log("DATA BEF STR: ",data)
        //  console.log("DATA AFT STR: ", dataToSend)
        });
        console.log("CLOSE PYTHON");
        // console.log("DATA SEND: ", dataToSend)
        python.on('close', (code) => {
        // console.log(`child process close all stdio with code ${code}`);
        res.send(dataToSend);
        });
  
    })

});

app.get("/api/get-courses", (req, res) =>{
    console.log("Connected3")
    sql = "SELECT * FROM COURSES2 WHERE GE != '' ORDER BY GE, Name";
    mydb.query(sql, function (err, result, fields) {
        if (err) throw err;
        // console.log(result);
        res.send(result);
      });
})

app.listen(8080, () => {
    console.log("RUNNING");
});
