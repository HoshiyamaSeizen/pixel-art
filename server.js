const express = require('express');
const fs = require('fs');
const { spawnSync } = require('child_process');
const { v4: uuidv4 } = require('uuid');

const app = express();
app.use(express.json({ limit: '50mb' }));

app.use((req, res, next) => {
	req.file = uuidv4();
	next();
});

app.get('/', (req, res) => {
	res.sendFile(__dirname + '/index.html');
});

app.post('/', (req, res) => {
	const { image, pixelSize, colors } = req.body;
	fs.writeFileSync(req.file, `${image}\n${pixelSize}\n${colors}`);
	spawnSync('python', [__dirname + '/script.py', req.file]);

	const img = fs.readFileSync(req.file, { encoding: 'utf8', flag: 'r' });
	fs.unlinkSync(req.file);
	res.json({ img });
});

app.listen(process.env.PORT || 3000);
