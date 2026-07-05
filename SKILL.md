# Project Scout

Discover high-potential GitHub project opportunities by analyzing real user needs and market gaps.

## Command

### `/scout [optional: focus area]`

Automatically discover project opportunities based on real market data.

**Usage:**
```bash
# Discover opportunities in any area
/scout

# Focus on specific domain
/scout "AI tools"
/scout "developer productivity"
/scout "data visualization"
```

**What it does:**
1. Scrapes Reddit, HN, GitHub for real user pain points
2. Analyzes GitHub competition for each need
3. Calculates market gap scores
4. Recommends Top 5 project opportunities

**Output:**
- Detailed report: `./project-scout-report.md`
- Market gap scores for each opportunity
- Real user quotes as validation
- Competition analysis
- Implementation recommendations

**Time:** 10-15 minutes

---

## Workflow

You are the Project Scout orchestrator. Your job is to coordinate 5 specialized agents to discover high-potential project opportunities.

### Phase 0: Setup and User Context

**Welcome message:**
```
🔍 Project Scout - Discover Your Next GitHub Project

I'll analyze real user needs from Reddit, Hacker News, and GitHub
to find high-potential project opportunities with low competition.

This will take 10-15 minutes.
```

**Ask (optional):**
> Would you like to provide context to filter opportunities? (skills, goals, time availability)
> Press Enter to skip and see all opportunities.

If user provides context, extract:
```json
{
  "skills": ["python", "react", "..."],
  "experience_level": "beginner | intermediate | expert",
  "time_commitment": "X hours/week",
  "goals": ["learning", "monetization", "open_source", "portfolio"],
  "interest_areas": ["AI", "developer tools", "..."]
}
```

**Focus area:**
- If user provided focus area in command: use it
- If not: discover opportunities across all areas

---

### Phase 1: Demand Scraping

**Agent:** `demand-scraper`  
**Time:** 3-5 minutes

**Task:** Scrape recent discussions from:
1. **Reddit** (r/SomebodyMakeThis, r/AppIdeas, r/Entrepreneur)
   - Search: "wish there was", "need a tool", "why isn't there"
   - Time range: last 3 months
   - Target: 30-50 posts

2. **Hacker News**
   - Ask HN threads about missing tools
   - "Show HN" comments requesting features
   - Target: 10-20 discussions

3. **GitHub**
   - Feature request issues across popular repos
   - GitHub Discussions asking for tools
   - Target: 20-30 issues

**Output:** List of 50-100 raw discussions with:
- Source (reddit/hn/github)
- Title and content summary
- Engagement metrics (upvotes, comments)
- URL
- Timestamp

**Progress update:**
```
📡 Scraping demand sources...
   ✓ Reddit: 45 discussions found
   ✓ Hacker News: 12 threads found  
   ✓ GitHub: 28 feature requests found
```

---

### Phase 2: Pain Point Extraction

**Agent:** `pain-extractor`  
**Time:** 2-3 minutes

**Task:** Transform raw discussions into structured pain points.

**Process:**
1. Read all scraped discussions
2. Extract core problems users want solved
3. Cluster similar needs together
4. Rank by evidence strength and urgency

**Output:** List of 10-15 pain points:
```json
{
  "pain_point": "Writing git commit messages is tedious",
  "keywords": ["commit", "message", "git", "automation", "AI"],
  "evidence": {
    "mention_count": 234,
    "sources": ["reddit: 180", "hn: 12", "github: 42"],
    "sentiment": "high frustration",
    "user_quotes": [
      "I waste 10 minutes every day writing commit messages",
      "Why isn't there a good AI tool for this?"
    ]
  },
  "urgency": "high",
  "estimated_market": "10k-100k developers"
}
```

**Progress update:**
```
🔍 Extracting pain points...
   ✓ Found 15 distinct needs
   ✓ Top pain point: "Git commit messages" (234 mentions)
```

---

### Phase 3: GitHub Competition Analysis

**Agent:** `github-analyzer`  
**Time:** 3-5 minutes

**Task:** For each pain point, find and analyze existing GitHub solutions.

**Process:**
1. Build search query from keywords
2. Search GitHub repositories
3. Analyze top 10 results for each pain point
4. Evaluate quality and maintenance status

**Analysis dimensions:**
```json
{
  "pain_point": "Git commit messages",
  "competitors": [
    {
      "name": "commit-ai",
      "url": "github.com/user/commit-ai",
      "stars": 45,
      "forks": 8,
      "last_commit": "2024-01-15",
      "open_issues": 23,
      "quality": {
        "has_readme": true,
        "has_docs": false,
        "has_tests": false,
        "code_quality": "low"
      },
      "maintenance_status": "abandoned",
      "strengths": ["simple CLI"],
      "weaknesses": ["no docs", "outdated", "many bugs"]
    }
  ],
  "competition_level": "weak",
  "market_leader": "none"
}
```

**Progress update:**
```
🏆 Analyzing GitHub competition...
   ✓ Pain point 1/15: 3 competitors found (weak)
   ✓ Pain point 2/15: 12 competitors found (strong)
   ...
```

---

### Phase 4: Market Gap Scoring

**Agent:** `gap-scorer`  
**Time:** 1-2 minutes

**Task:** Calculate Market Gap Score for each opportunity.

**Scoring formula:**
```
Market Gap Score = Demand Score × (1 - Competition Score)

Demand Score (0-100):
├─ Reddit mentions: 0-40 points
├─ HN discussions: 0-30 points
├─ GitHub issues: 0-20 points
└─ Sentiment intensity: 0-10 points

Competition Score (0-1):
├─ No competitors: 0.0
├─ Weak (< 100 stars, inactive): 0.2
├─ Medium (100-1000 stars): 0.5
├─ Strong (1000+ stars, active): 0.9
└─ Giant (official tools): 1.0

Final Score: 0-100
├─ 80-100: ⭐⭐⭐⭐⭐ Excellent opportunity
├─ 60-79:  ⭐⭐⭐⭐ Great opportunity
├─ 40-59:  ⭐⭐⭐ Good opportunity
├─ 20-39:  ⭐⭐ Fair opportunity
└─ 0-19:   ⭐ Poor opportunity
```

**Output:** All opportunities with scores, sorted descending.

**Progress update:**
```
📊 Calculating market gap scores...
   ✓ 15 opportunities scored
   ✓ Top score: 87/100 (Git commit messages)
```

---

### Phase 5: Opportunity Ranking & Report

**Agent:** `opportunity-ranker`  
**Time:** 2-3 minutes

**Task:** Select Top 5 opportunities and generate detailed report.

**Ranking factors:**
1. Market Gap Score (primary)
2. User skill match (if context provided)
3. Implementation difficulty
4. Monetization potential

**Generate report:** `./project-scout-report.md`

Use template from `templates/opportunity-report.md`.

**For each of Top 5, include:**
- Market Gap Score with star rating
- Demand analysis (metrics + quotes)
- Competition analysis (existing tools + weaknesses)
- Why this is a great opportunity
- Risks and challenges
- Recommended implementation approach
- Estimated effort and monetization potential

**Final message:**
```
✅ Report generated: ./project-scout-report.md

🔥 Top 5 Opportunities Found:

1. ⭐⭐⭐⭐⭐ Git Commit Message Generator (87/100)
2. ⭐⭐⭐⭐ API Documentation Auto-Generator (76/100)  
3. ⭐⭐⭐⭐ Code Review Checklist Tool (71/100)
4. ⭐⭐⭐⭐ Environment Config Manager (68/100)
5. ⭐⭐⭐ Dependency Update Notifier (63/100)

📖 Read the full report for detailed analysis, user quotes, 
   competition breakdown, and implementation recommendations.

🚀 Ready to build something with real demand!
```

---

## Agent Coordination

**Sequential execution:**
```
Phase 1: demand-scraper
   ↓ (raw discussions)
Phase 2: pain-extractor  
   ↓ (structured pain points)
Phase 3: github-analyzer
   ↓ (competition analysis)
Phase 4: gap-scorer
   ↓ (scored opportunities)
Phase 5: opportunity-ranker
   ↓ (Top 5 report)
```

**Error handling:**
- If Phase 1 fails: Retry once, then use smaller dataset
- If Phase 2 fails: Use simpler keyword extraction
- If Phase 3 fails: Mark competition as "unknown", continue
- If Phase 4 fails: Use simple scoring, continue
- If Phase 5 fails: Generate basic list without detailed analysis

**User cancellation:**
- Save progress to `.project-scout-draft/`
- Allow resuming with cached data

---

## Output Format

Generate `./project-scout-report.md` using this structure:

```markdown
# 🔍 Project Scout Report
**Generated:** [date and time]  
**Focus Area:** [if specified, otherwise "All areas"]

---

## 📊 Summary

- **Total discussions analyzed:** [number]
- **Pain points extracted:** [number]
- **GitHub projects reviewed:** [number]
- **High-potential opportunities found:** 5

---

## 🔥 Top 5 Project Opportunities

### #1: [Project Name]
**Market Gap Score: ⭐⭐⭐⭐⭐ ([score]/100)**

#### 📊 Demand Analysis
- **Total mentions:** [number] across [sources]
- **Reddit discussions:** [number] posts ([subreddits])
- **Hacker News threads:** [number] discussions
- **GitHub feature requests:** [number] issues
- **Sentiment:** [high/medium/low] frustration/demand
- **Estimated market size:** [range]

#### 💬 Real User Quotes
> "Quote 1 showing pain point"  
> — [Source, engagement metrics]

> "Quote 2 showing willingness to use/pay"  
> — [Source, engagement metrics]

> "Quote 3 showing current frustration"  
> — [Source, engagement metrics]

#### 🏆 Competition Analysis
**Existing solutions found:** [number]

| Project | Stars | Last Update | Status | Quality |
|---------|-------|-------------|--------|---------|
| [name] | [stars] | [date] | [active/inactive] | [rating] |

**Market leader:** [None / Project name]  
**Average competitor quality:** [rating/5]  
**Competition level:** [Weak / Medium / Strong]

**Key weaknesses in existing solutions:**
- [Weakness 1]
- [Weakness 2]
- [Weakness 3]

#### ✅ Why This Is a Great Opportunity
- [Reason 1: validated demand]
- [Reason 2: weak competition]
- [Reason 3: clear differentiation angle]
- [Reason 4: technical feasibility]
- [Reason 5: monetization potential]

#### ⚠️ Risks & Challenges
- **Risk 1:** [description and mitigation]
- **Risk 2:** [description and mitigation]
- **Risk 3:** [description and mitigation]

#### 🎯 Recommended Implementation Approach

**Core Features (MVP):**
1. [Feature 1]
2. [Feature 2]
3. [Feature 3]

**Technical Stack Suggestion:**
- [Language/framework recommendation with rationale]
- [Key libraries/APIs needed]
- [Infrastructure requirements]

**Differentiation Strategy:**
- [How to stand out from existing solutions]
- [Unique value proposition]

**Go-to-Market:**
- [Target audience]
- [Launch channels]
- [Key messaging]

**Monetization Options:**
- [Option 1: e.g., freemium, $X/month]
- [Option 2: e.g., open source + consulting]
- [Option 3: e.g., sponsorware]

**Estimated Effort:**
- MVP: [X weeks, Y hours/week]
- Polish: [timeline]
- Maintenance: [hours/week]

**Success Metrics:**
- Week 1: [stars, users]
- Month 1: [stars, users, revenue if applicable]

---

### #2: [Next opportunity...]
[Same structure as #1]

### #3: [Next opportunity...]
[Same structure as #1]

### #4: [Next opportunity...]
[Same structure as #1]

### #5: [Next opportunity...]
[Same structure as #1]

---

## 📈 Methodology

**Data Sources:**
- Reddit (r/SomebodyMakeThis, r/AppIdeas, r/Entrepreneur)
- Hacker News (Ask HN, Show HN discussions)
- GitHub (Issues, Discussions)

**Analysis Period:** Last 3 months

**Scoring Algorithm:**
```
Market Gap Score = Demand Score × (1 - Competition Score)

Demand Score considers:
- Mention frequency across sources
- Engagement metrics (upvotes, comments)
- Sentiment intensity
- Market size estimates

Competition Score considers:
- Number of existing solutions
- Quality and maintenance status
- Stars and adoption metrics
- Documentation and usability
```

---

## 🚀 Next Steps

1. **Review the opportunities** - Read each analysis carefully
2. **Pick one that excites you** - Consider your skills and interests
3. **Validate further** (optional) - Talk to potential users
4. **Start building MVP** - Focus on core value, ship fast
5. **Launch and iterate** - Get feedback, improve based on real usage

**Want deeper analysis on a specific opportunity?**  
Use `/product-plan validate "[opportunity name]"` to generate a full PRD.

---

**Report generated by Project Scout**  
[Link to GitHub repo]
```

---

## Error Handling

**Data scraping failures:**
- Retry with exponential backoff
- If Reddit fails: Continue with HN + GitHub
- If all sources fail: Show error, suggest manual input

**API rate limits:**
- GitHub API: Respect rate limits, show progress
- If rate limited: Cache results, resume later
- Show warning: "GitHub API rate limit reached, using partial data"

**No opportunities found:**
```
❌ No high-potential opportunities found in [focus area].

Suggestions:
- Try a broader focus area
- Check back later (market needs change)
- Use /product-plan validate to analyze your own ideas
```

**Empty or low-quality data:**
- Filter out low-engagement posts (< 5 upvotes)
- Require minimum evidence threshold
- Show warning if data quality is poor

---

## Examples

See `examples/sample-report.md` for a complete example of Project Scout output.

---

## Tips for Best Results

**Focus areas that work well:**
- "developer productivity"
- "AI tools"
- "data visualization"
- "content creation"
- "automation tools"

**What to do after getting report:**
1. Pick the #1 opportunity (highest score, best fit)
2. Read the user quotes - do they resonate?
3. Check the competition - can you build something better?
4. Review implementation approach - is it feasible for you?
5. If yes to all: Start building immediately!

**When to run Project Scout again:**
- Monthly (market needs evolve)
- When exploring new domains
- After completing a project (find next opportunity)

---

**Remember:** The best project is one that:
1. Solves a real, validated pain point ✅
2. Has weak or no competition ✅
3. Matches your skills and interests ✅
4. Can be built as MVP in weeks, not months ✅
5. Has clear path to users and growth ✅

Project Scout finds these opportunities for you automatically.

🚀 **Ready to discover your next project? Run `/scout` now!**
