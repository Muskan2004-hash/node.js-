
const express = require('express');
const axios = require('axios');
const multer = require('multer');
const path = require('path');

const app = express();
const upload = multer({ dest: 'uploads/' });

app.set('view engine', 'ejs');
app.use(express.static('public'));
app.use(express.urlencoded({ extended: true }));

app.get('/', (req, res) => {
  res.render('index', { info: null });
});

app.post('/upload', upload.single('file'), async (req, res) => {
  const filename = req.file.originalname;

  try {
    const response = await axios.post('http://localhost:5000/fileinfo', {
      filename
    });

    res.render('index', { info: response.data });
  } catch (error) {
    res.render('index', { info: { error: 'Failed to fetch from backend.' } });
  }
});

app.listen(3000, () => {
  console.log('Frontend running at http://localhost:3000');
});
