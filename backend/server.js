const express = require("express");
const cors = require("cors");
const gplay = require("google-play-scraper");

const app = express();
app.use(cors());
app.use(express.json());

app.get("/api/search", async (req, res) => {
  const query = String(req.query.q || "").trim();

  if (!query) {
    return res.status(400).json({
      error: "App name enter cheyyandi"
    });
  }

  try {
    const searchFunction = gplay.search ||
      gplay.default?.search;

    if (typeof searchFunction !== "function") {
      throw new Error(
        "Google Play scraper search function unavailable"
      );
    }

    const results = await searchFunction({
      term: query,
      num: 10,
      country: "in",
      lang: "en"
    });

    res.json(results.map((item) => ({
      name: item.title,
      developer: item.developer,
      rating: item.score ?? null,
      icon: item.icon,
      url: item.url
    })));
  } catch (error) {
    console.error("Google Play error:", error);
    res.status(502).json({
      error: error.message
    });
  }
});

app.listen(5000, () => {
  console.log("Backend running at http://localhost:5000");
});