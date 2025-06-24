
const urlService = require('../services/urlServices'); 

const shortenUrl = async (req, res) => {
  try {
    console.log('[DEBUG] Request Body:', req.body);

    const { originalUrl } = req.body;
    if (!originalUrl) {
      return res.status(400).json({ error: 'Original URL is required' });
    }

    const url = await urlService.createShortUrl(originalUrl);
    res.json({
      originalUrl: url.originalUrl,
      shortUrl: `${req.protocol}://${req.get('host')}/${url.shortId}`,
      shortId: url.shortId
    });
  } catch (error) {
    console.error('[ERROR]', error);
    res.status(500).json({ error: 'Server error' });
  }
};

const redirectUrl = async (req, res) => {
  try {
    const { shortId } = req.params;
    const originalUrl = await urlService.getOriginalUrl(shortId);

    if (!originalUrl) {
      return res.status(404).json({ error: 'URL not found' });
    }

    res.redirect(originalUrl);
  } catch (error) {
    console.error('[ERROR]', error);
    res.status(500).json({ error: 'Server error' });
  }
};

module.exports = {
  shortenUrl,
  redirectUrl
};
