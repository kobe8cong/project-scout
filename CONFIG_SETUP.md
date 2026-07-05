# Project Scout Configuration

## Required API Keys and Setup

To use Project Scout with real data, you need to configure API access for data sources.

### 1. Reddit API (Required)

**Why:** Access Reddit discussions from r/SomebodyMakeThis, r/AppIdeas, etc.

**Setup:**
1. Go to https://www.reddit.com/prefs/apps
2. Click "Create App" or "Create Another App"
3. Fill in:
   - **Name:** Project Scout
   - **App type:** Select "script"
   - **Description:** Discover project opportunities
   - **Redirect URI:** http://localhost:8080
4. Click "Create app"
5. Note your credentials:
   - **Client ID:** (under app name, looks like: `abc123xyz`)
   - **Client Secret:** (longer string)

**Add to config:**
```bash
# Create config file
cp config.example.json config.json

# Edit config.json and add:
{
  "reddit": {
    "client_id": "YOUR_CLIENT_ID",
    "client_secret": "YOUR_CLIENT_SECRET",
    "user_agent": "ProjectScout/1.0"
  }
}
```

---

### 2. GitHub API (Required)

**Why:** Search for feature requests and analyze competitor projects.

**Setup:**
1. You already have a token: `YOUR_GITHUB_TOKEN_HERE`
2. Or create a new one at https://github.com/settings/tokens
3. Required permissions:
   - ✅ `public_repo` (read public repositories)
   - ✅ `read:org` (optional, for org repos)

**Add to config:**
```json
{
  "github": {
    "access_token": "YOUR_GITHUB_TOKEN_HERE"
  }
}
```

---

### 3. Hacker News API (No setup needed!)

**Why:** Search Ask HN discussions.

**Setup:** None! HN provides a free public API via Algolia:
- https://hn.algolia.com/api

---

### 4. OpenAI or Anthropic API (Required for AI analysis)

**Why:** Analyze discussions and extract pain points using AI.

**Option A: Anthropic Claude API (Recommended)**
1. Get API key from https://console.anthropic.com/
2. Pricing: ~$0.01 per analysis (cheap!)

**Option B: OpenAI API**
1. Get API key from https://platform.openai.com/
2. Pricing: Similar to Claude

**Add to config:**
```json
{
  "ai": {
    "provider": "anthropic",  // or "openai"
    "api_key": "YOUR_API_KEY"
  }
}
```

---

## Complete config.json Example

```json
{
  "reddit": {
    "client_id": "abc123xyz",
    "client_secret": "your_secret_here",
    "user_agent": "ProjectScout/1.0 by /u/yourusername"
  },
  "github": {
    "access_token": "YOUR_GITHUB_TOKEN_HERE"
  },
  "hackernews": {
    "api_url": "https://hn.algolia.com/api/v1"
  },
  "ai": {
    "provider": "anthropic",
    "api_key": "sk-ant-your-key-here"
  },
  "settings": {
    "max_discussions_per_source": 50,
    "time_range_months": 3,
    "cache_enabled": true,
    "cache_duration_hours": 24
  }
}
```

---

## Security Notes

⚠️ **NEVER commit config.json to git!**

The `.gitignore` already includes it:
```
config.json
config.local.json
.env
```

---

## Installation

### Prerequisites

```bash
# Python 3.8+ required
python --version

# Install dependencies
pip install praw requests anthropic PyGithub markdown
```

### Setup

```bash
# 1. Clone the repo
git clone https://github.com/kobe8cong/project-scout.git
cd project-scout

# 2. Copy config template
cp config.example.json config.json

# 3. Edit config.json with your API keys
nano config.json  # or use your editor

# 4. Test configuration
python scripts/test_config.py
```

---

## Usage

Once configured:

```bash
# In Claude Code
/scout

# Or with focus area
/scout "AI tools"
```

The tool will:
1. ✅ Read your config.json
2. ✅ Connect to Reddit, GitHub, HN APIs
3. ✅ Scrape real discussions (last 3 months)
4. ✅ Use AI to analyze and extract pain points
5. ✅ Generate report with real data

---

## Troubleshooting

### "Reddit API authentication failed"
- Check your client_id and client_secret
- Make sure user_agent is unique
- Verify app type is "script" not "web app"

### "GitHub API rate limit exceeded"
- You get 5,000 requests/hour with token
- Enable caching in config.json
- Wait an hour for rate limit reset

### "AI API key invalid"
- Check your API key is correct
- Verify you have credits/billing enabled
- Try switching provider (anthropic ↔ openai)

---

## Cost Estimates

**Per /scout run:**
- Reddit API: Free (60 requests/minute limit)
- GitHub API: Free (5,000 requests/hour)
- Hacker News API: Free (no limits)
- AI API: ~$0.05-0.15 (depending on provider)

**Total cost per report:** ~$0.05-0.15

---

## Privacy & Data

**What we collect:**
- Public discussions from Reddit, HN, GitHub
- No personal data
- No login required (read-only access)

**What we store:**
- Cached API responses (24 hours)
- Generated reports (local only)

**What we DON'T do:**
- Post or comment on your behalf
- Access private data
- Share your API keys

---

## Next Steps

1. **Get your API keys** (Reddit, GitHub, AI provider)
2. **Create config.json** with your credentials
3. **Run /scout** and get real data!

Need help? [Open an issue](https://github.com/kobe8cong/project-scout/issues)
