
const Url = require('../models/url');
const { nanoid } = require('nanoid');

const createShortUrl = async (originalUrl) => {
  const shortId = nanoid(8);
  const url = new Url({ originalUrl, shortId });
  await url.save();
  return url;
};

const getOriginalUrl = async (shortId) => {
  const url = await Url.findOneAndUpdate(
    { shortId },
    { $inc: { clicks: 1 } },
    { new: true }
  );
  return url?.originalUrl;
};


module.exports = {
  createShortUrl,
  getOriginalUrl
};
