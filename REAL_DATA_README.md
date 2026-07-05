# 🔍 Project Scout - Real Data Implementation

**✨ This version uses REAL data scraped from Reddit, Hacker News, and GitHub!**

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Install Python packages
pip install -r requirements.txt
```

### 2. Configure API Keys

```bash
# Copy config template
cp config.example.json config.json

# Edit config.json and add your API keys
nano config.json
```

**Required API keys:**
- **Reddit API** - Free, get from https://www.reddit.com/prefs/apps
- **GitHub Token** - Free, get from https://github.com/settings/tokens
- **Anthropic or OpenAI API** - Paid (~$0.05 per report)

See [CONFIG_SETUP.md](CONFIG_SETUP.md) for detailed setup instructions.

### 3. Test Configuration

```bash
# Verify everything is set up correctly
python scripts/test_config.py
```

Should show all ✅ green checkmarks.

### 4. Run Project Scout

#### Option A: Use in Claude Code (Recommended)

```bash
/scout
# or with focus area
/scout "AI tools"
```

#### Option B: Run standalone scripts

```bash
# Step 1: Scrape real data
python scripts/scrape_data.py

# Step 2: Analyze data
python scripts/analyze_data.py

# Step 3: Generate report (in Claude Code)
/scout
```

---

## 📊 What You Get

### Real Data Scraping

The tool scrapes **real, recent discussions** from:

✅ **Reddit** (r/SomebodyMakeThis, r/AppIdeas, r/Entrepreneur, r/SideProject)
- Posts with "wish there was", "need a tool", etc.
- Upvotes, comments, timestamps
- Last 3 months by default

✅ **Hacker News**
- "Ask HN" threads about missing tools
- Points, comments, discussion threads
- High-quality developer feedback

✅ **GitHub**
- Feature request issues
- Enhancement requests
- Validation from actual repo discussions

### Analysis Output

**scraped_data.json** - Raw data:
```json
{
  "metadata": {
    "scraped_at": "2026-07-05T18:30:00",
    "total_discussions": 145
  },
  "reddit": [...],
  "hackernews": [...],
  "github": [...]
}
```

**project-scout-report.md** - Final report:
- Top 5 opportunities with real user quotes
- Actual upvote/comment counts
- Links to source discussions
- Market gap scores based on real data

---

## 🔧 Configuration

### Adjust Time Range

Edit `config.json`:
```json
{
  "settings": {
    "time_range_months": 6  // Change from 3 to 6 months
  }
}
```

### More Discussions

```json
{
  "settings": {
    "max_discussions_per_source": 100  // Change from 50
  }
}
```

### Additional Subreddits

```json
{
  "settings": {
    "subreddits": [
      "SomebodyMakeThis",
      "AppIdeas",
      "Entrepreneur",
      "SideProject",
      "startups",        // Add more
      "indiehackers"
    ]
  }
}
```

---

## 💰 Cost Estimates

**Per /scout run:**
- Reddit API: **Free** (60 requests/min limit)
- GitHub API: **Free** (5,000 requests/hour)  
- Hacker News API: **Free** (unlimited)
- AI analysis: **~$0.05-0.15** (Anthropic/OpenAI)

**Total: ~$0.05-0.15 per report**

---

## 🛠️ Troubleshooting

### "config.json not found"
```bash
cp config.example.json config.json
# Then edit config.json with your API keys
```

### "Module not found" errors
```bash
pip install -r requirements.txt
```

### Reddit API fails
- Check client_id and client_secret
- Make sure you created a "script" app (not "web app")
- Verify user_agent is unique

### GitHub rate limit exceeded
- You get 5,000 requests/hour with a token
- Wait for reset (check with `python scripts/test_config.py`)

### No discussions found
- Extend time range to 6 months
- Add more subreddits
- Check your search keywords

---

## 📁 Project Structure

```
project-scout/
├── config.example.json       # Config template
├── config.json              # Your config (gitignored)
├── CONFIG_SETUP.md          # Detailed setup guide
├── requirements.txt         # Python dependencies
├── SKILL.md                 # Claude Code skill definition
├── README.md                # This file
├── scripts/
│   ├── test_config.py      # Test your configuration
│   ├── scrape_data.py      # Scrape real data
│   ├── analyze_data.py     # Extract pain points
│   └── README.md           # Scripts documentation
├── agents/                  # AI agent definitions
│   ├── demand-scraper.md
│   ├── pain-extractor.md
│   ├── github-analyzer.md
│   ├── gap-scorer.md
│   └── opportunity-ranker.md
└── examples/
    └── sample-report.md    # Example output
```

---

## 🔐 Security & Privacy

### What We Access
- ✅ **Public data only** (no private repos/posts)
- ✅ **Read-only access** (never post/comment)
- ✅ **Local storage** (data saved on your machine)

### What We Don't Do
- ❌ Store data on remote servers
- ❌ Share your API keys
- ❌ Access private information
- ❌ Post or comment on your behalf

### API Keys Safety
- `config.json` is in `.gitignore` (never committed)
- Keys are only used for API authentication
- No keys are sent anywhere except their official APIs

---

## 🎯 Demo vs Real Data

### ❌ Demo Version (what I showed earlier)
- Simulated data for demonstration
- Estimated numbers
- Generic user quotes

### ✅ Real Version (this implementation)
- **Actual Reddit posts** with real upvotes/comments
- **Real HN discussions** with links to threads
- **Actual GitHub issues** from real repos
- **Verifiable sources** - every quote has a URL

---

## 📖 Documentation

- [CONFIG_SETUP.md](CONFIG_SETUP.md) - Detailed API setup guide
- [scripts/README.md](scripts/README.md) - Python scripts documentation
- [SKILL.md](SKILL.md) - How the /scout command works
- [examples/sample-report.md](examples/sample-report.md) - Example output

---

## 🤝 Contributing

Found a bug? Have an idea?
- Open an issue on GitHub
- Submit a pull request
- Star the repo if you find it useful!

---

## 📄 License

MIT License - See [LICENSE](LICENSE)

---

## 🙏 Acknowledgments

Built with:
- [praw](https://github.com/praw-dev/praw) - Reddit API wrapper
- [PyGithub](https://github.com/PyGithub/PyGithub) - GitHub API wrapper
- [Anthropic Claude](https://anthropic.com) - AI analysis

---

**Ready to discover real project opportunities? 🚀**

```bash
# 1. Set up config
cp config.example.json config.json
nano config.json

# 2. Test
python scripts/test_config.py

# 3. Run
/scout
```
