// app.js
const express = require("express")
const path = require('path')

const app = express();

app.use('/css', express.static(path.join(__dirname, 'node_modules/bootstrap/dist/css')))
app.use('/js', express.static(path.join(__dirname, 'node_modules/bootstrap/dist/js')))
app.use('/js', express.static(path.join(__dirname, 'node_modules/jquery/dist')))
app.use('/js', express.static(path.join(__dirname, 'node_modules/popper/dist')))
app.use('/js', express.static(path.join(__dirname, 'js')))
app.use('/css', express.static(path.join(__dirname, 'css')))
app.use('/images', express.static(path.join(__dirname, 'images')))

app.get("/", (req, res) => {
    res.sendFile(path.join(__dirname, 'views/index.html'))
});

app.listen(5000, () => {
    console.log('Listening on port ' + 5000);
});