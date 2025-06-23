const express = require('express');
const router = express.Router();
const urlController = require('../controller/urlController');

router.post('/shorten', urlController.shortenUrl);
router.get('/:shortId', urlController.redirectUrl);

module.exports = router;