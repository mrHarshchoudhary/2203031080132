const { nanoid } = require('nanoid');

const createShortUrl = async (originalUrl) => {
  const shortId = nanoid(8); // generate 8-character ID
  const url = new Url({
    originalUrl,
    shortId
  });
  await url.save();
  return url;
};
