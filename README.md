# 🔍 Project Scout

> **Discover high-potential GitHub project opportunities by analyzing real user needs and market gaps.**

Stop wondering "what should I build?" — let Project Scout find validated project opportunities for you by analyzing real discussions from Reddit, Hacker News, and GitHub.

---

## 🎯 What Is This?

Project Scout is a Claude Code skill that automatically:

1. **Scrapes real user needs** from Reddit, HN, and GitHub (50-100 recent discussions)
2. **Extracts pain points** and clusters similar needs
3. **Analyzes GitHub competition** to find market gaps
4. **Calculates opportunity scores** based on demand vs. competition
5. **Recommends Top 5 projects** with detailed analysis and implementation guides

**Result:** A comprehensive report showing you exactly what to build, why it's a good opportunity, and how to execute.

---

## ✨ Why Project Scout?

### The Problem
- 😕 "I want to build something, but don't know what"
- 🤔 "Is my idea already solved?"
- 😰 "Will anyone actually use this?"
- ⏰ "I don't want to waste months on a failed project"

### The Solution
Project Scout finds opportunities with:
- ✅ **Validated demand** (real users asking for it)
- ✅ **Weak competition** (no good solution exists yet)
- ✅ **Clear market gap** (specific weaknesses to exploit)
- ✅ **Actionable plan** (what to build, how to launch)

### Real Value
- 🎯 **Skip the guessing** — build something people already want
- 🚀 **Faster validation** — 10-15 minutes vs. weeks of research
- 💡 **Data-driven decisions** — real user quotes, not assumptions
- 📊 **Quantified opportunities** — Market Gap Score (0-100)

---

## 🚀 Quick Start

### Installation

Project Scout is a Claude Code skill. Install it:

```bash
# In Claude Code CLI or Desktop App
/skill install project-scout
```

### Usage

```bash
# Discover opportunities in any area (recommended first run)
/scout

# Focus on specific domain
/scout "AI tools"
/scout "developer productivity"
/scout "data visualization"
```

**Output:** `./project-scout-report.md` with Top 5 opportunities

**Time:** 10-15 minutes

---

## 📖 Example Output

```markdown
## #1: AI-Powered Git Commit Message Generator
**Market Gap Score: ⭐⭐⭐⭐⭐ (87/100)**

📊 Demand Analysis:
- 234 mentions across Reddit, HN, GitHub
- Users saying "would pay $5/month"
- High frustration with current state

🏆 Competition:
- Only 3 existing tools
- Best has 45 stars (abandoned)
- All have poor reviews

✅ Why This Is Great:
- Validated demand with willingness to pay
- Weak competition (outdated tools)
- Easy to build (2-3 weeks MVP)
- Clear monetization path

🎯 Implementation:
- Tech stack: TypeScript + OpenAI API
- MVP: CLI tool with 3 core features
- Launch: Show HN, Reddit r/programming
- Estimated effort: 20-30 hours
```

[See full example report →](examples/sample-report.md)

---

## 🎨 How It Works

### 1. Demand Scraping (3-5 min)
Searches Reddit, Hacker News, and GitHub for:
- "wish there was a tool for..."
- "why isn't there..."
- Feature requests in popular repos

**Collects:** 50-100 discussions from last 3 months

### 2. Pain Extraction (2-3 min)
Uses AI to:
- Extract core problems users want solved
- Cluster similar needs
- Rank by urgency and market size

**Output:** 10-15 structured pain points with evidence

### 3. GitHub Analysis (3-5 min)
For each pain point:
- Searches GitHub for existing solutions
- Analyzes quality, maintenance, user sentiment
- Identifies weaknesses and gaps

**Output:** Competition strength assessment

### 4. Gap Scoring (1-2 min)
Calculates Market Gap Score:
```
Score = Demand × (1 - Competition)

Demand (0-100): mentions, engagement, urgency, market size
Competition (0-1): stars, maintenance, quality
```

**Output:** All opportunities ranked by score

### 5. Report Generation (2-3 min)
Generates detailed report for Top 5:
- User quotes validating demand
- Competition breakdown
- Implementation recommendations
- Go-to-market strategy
- Effort and monetization estimates

---

## 🔥 What Makes This Different?

### vs. ChatGPT / Claude Chat
- ❌ ChatGPT: Generic advice, no real data
- ✅ Project Scout: Real user discussions, quantified gaps

### vs. Manual Research
- ❌ Manual: Hours of Googling, subjective
- ✅ Project Scout: 10-15 minutes, data-driven

### vs. Product Planner
- ❌ Product Planner: Validates *your* ideas
- ✅ Project Scout: *Discovers* ideas for you

---

## 📊 Success Stories

> "Project Scout found me 'AI commit messages' opportunity. Built it in 2 weeks, got 200 stars in first month, now at $500 MRR."  
> — (Future success story — this is a new tool!)

**Your story could be here.** [Share your Project Scout success →](https://github.com/kobe8cong/project-scout/discussions)

---

## 🎯 Who Is This For?

### Perfect For:
- ✅ **Indie hackers** looking for their next project
- ✅ **Developers** who want to build but don't know what
- ✅ **Open source contributors** seeking high-impact projects
- ✅ **Students** building portfolio projects
- ✅ **Side project enthusiasts** validating ideas before building

### Not For:
- ❌ Non-developers (reports assume technical skills)
- ❌ People who already have a validated idea (use Product Planner instead)
- ❌ Enterprise product teams (different validation needs)

---

## 💡 Tips for Best Results

### 1. Run It Regularly
Markets evolve. New needs emerge. Run `/scout` monthly to discover fresh opportunities.

### 2. Focus Your Search
General search is great for discovery, but focused searches yield more relevant results:
```bash
/scout "AI tools"           # More relevant than /scout
/scout "React libraries"    # Specific domain
```

### 3. Read User Quotes Carefully
The quotes reveal not just *what* users want, but *why* and *how much* they care.

### 4. Pick Based on Fit, Not Just Score
- 87-score opportunity in unfamiliar domain < 72-score in your expertise
- Consider: your skills, interests, time availability, goals

### 5. Validate Further
Project Scout gives you strong leads. Before building:
- Post on Reddit: "Would you use X?"
- Talk to 3-5 potential users
- Build landing page, collect emails

### 6. Move Fast
High-score opportunities won't stay open forever. Build MVP in 2-4 weeks, not months.

---

## 🛠️ Technical Details

### Data Sources
- **Reddit:** r/SomebodyMakeThis, r/AppIdeas, r/Entrepreneur, r/programming
- **Hacker News:** Ask HN threads, Show HN comments
- **GitHub:** Feature request issues, Discussions

### Scoring Algorithm
```
Market Gap Score = Demand Score × (1 - Competition Score)

Demand Score (0-100):
├─ Evidence (0-40): Mentions across platforms
├─ Engagement (0-25): Upvotes, comments, reactions
├─ Urgency (0-25): Frustration, willingness to pay
└─ Market Size (0-10): Estimated user base

Competition Score (0-1):
├─ Stars (0-0.5): Popularity of existing solutions
├─ Maintenance (0-0.3): Active development status
└─ Quality (0-0.2): Documentation, tests, user sentiment
```

### Quality Filters
- ✅ Minimum 3 mentions across sources
- ✅ Minimum 5 upvotes/engagement per discussion
- ✅ Last 3 months only (recent = relevant)
- ✅ Filtered: spam, jokes, already-solved, too vague

---

## 🤝 Related Tools

**Project Scout + Product Planner = Complete Workflow**

1. **Project Scout** — Discover opportunities
2. **Product Planner** — Deep-dive on chosen opportunity
3. **Build** — Create MVP
4. **Launch** — Get users

```bash
# Step 1: Discover
/scout "AI tools"
# → Pick: "AI Commit Messages"

# Step 2: Plan
/product-plan validate "AI commit message generator"
# → Get full PRD with requirements, architecture, roadmap

# Step 3-4: Build and launch!
```

---

## 📚 Documentation

- [Example Report](examples/sample-report.md) — See what output looks like
- [How It Works](docs/HOW_IT_WORKS.md) — Deep dive into methodology
- [Scoring Algorithm](docs/SCORING_ALGORITHM.md) — Mathematical details
- [Data Sources](docs/DATA_SOURCES.md) — Where data comes from
- [FAQ](docs/FAQ.md) — Common questions

---

## 🐛 Known Limitations

- **Rate limits:** GitHub API has rate limits (handles gracefully with caching)
- **Data freshness:** Uses discussions from last 3 months only
- **English-only:** Currently only analyzes English discussions
- **No guarantee:** High score ≠ guaranteed success (but better odds!)

---

## 🗺️ Roadmap

### v1.1 (Next)
- [ ] Twitter/X data source integration
- [ ] Historical tracking (compare opportunities over time)
- [ ] Export to JSON/CSV
- [ ] Customizable scoring weights

### v1.2
- [ ] `/watch-opportunities` — Continuous monitoring
- [ ] Email notifications for new high-score opportunities
- [ ] Multi-language support

### v2.0
- [ ] Web dashboard
- [ ] API endpoints
- [ ] Team collaboration features

[Vote on roadmap →](https://github.com/kobe8cong/project-scout/discussions/categories/feature-requests)

---

## 🤝 Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md)

**Ways to contribute:**
- 🐛 Report bugs or data quality issues
- 💡 Suggest new data sources
- 📊 Improve scoring algorithm
- 📝 Improve documentation
- ⭐ Star the repo (helps others discover it!)

---

## 📄 License

MIT License - see [LICENSE](LICENSE)

---

## 🙏 Acknowledgments

Built with:
- [Claude Code](https://claude.ai/code) — AI development environment
- Inspired by: The pain of not knowing what to build next

**Special thanks to:**
- Early testers and feedback providers
- The indie hacker and open source communities

---

## 📬 Contact & Support

- **Issues:** [GitHub Issues](https://github.com/kobe8cong/project-scout/issues)
- **Discussions:** [GitHub Discussions](https://github.com/kobe8cong/project-scout/discussions)
- **Twitter:** [@kobe8cong](https://twitter.com/kobe8cong)

---

## ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=kobe8cong/project-scout&type=Date)](https://star-history.com/#kobe8cong/project-scout&Date)

---

**Stop guessing. Start building what people want. 🚀**

[Run `/scout` now →](#quick-start)
