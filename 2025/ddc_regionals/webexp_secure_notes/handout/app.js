const express = require('express');
const ejs = require('ejs');
const app = express();

app.use(express.static('public'));
app.use(express.urlencoded({ extended: true }));
app.use(express.json());
app.set('view engine', 'ejs');

app.get('/', function (req, res) {
    res.render(__dirname + '/views/index.ejs');
});

const notes = {};

app.post('/submit', (req, res) => {
    const { id, description, property, value } = req.body;

    if (!id || !description || !property || !value) {
        return res.status(400).send('Missing note ID, description, properties, or values.');
    }

    if (!notes[id]) {
        notes[id] = { description };
    }

    for (let i = 0; i < property.length; i++) {
        notes[id][property[i]] = value[i];
    }

    res.redirect(`/view?id=${id}`);
});

app.get('/list', (req, res) => {
    res.render('list', { notes });
});

app.get('/view', (req, res) => {
    const { id } = req.query;
    res.render('view', { id, note: notes[id] });
});

app.listen(80, () => {
    console.log('Secure Notes running');
});
