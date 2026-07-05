"""
Project Scout - Real Data Scraper

This script scrapes real discussions from Reddit, Hacker News, and GitHub
to find validated project opportunities.
"""

import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Any

# Load configuration
def load_config():
    """Load API credentials from config.json"""
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')

    if not os.path.exists(config_path):
        raise FileNotFoundError(
            "config.json not found! Please copy config.example.json to config.json "
            "and add your API keys. See CONFIG_SETUP.md for instructions."
        )

    with open(config_path, 'r') as f:
        return json.load(f)

# Initialize APIs
def init_reddit(config):
    """Initialize Reddit API client"""
    try:
        import praw
    except ImportError:
        raise ImportError("Please install praw: pip install praw")

    reddit = praw.Reddit(
        client_id=config['reddit']['client_id'],
        client_secret=config['reddit']['client_secret'],
        user_agent=config['reddit']['user_agent']
    )
    return reddit

def init_github(config):
    """Initialize GitHub API client"""
    try:
        from github import Github
    except ImportError:
        raise ImportError("Please install PyGithub: pip install PyGithub")

    g = Github(config['github']['access_token'])
    return g

# Reddit scraping
def scrape_reddit(config) -> List[Dict[str, Any]]:
    """Scrape Reddit for project ideas and pain points"""
    print("📡 Scraping Reddit...")

    reddit = init_reddit(config)
    discussions = []

    subreddits = config['settings']['subreddits']
    keywords = config['settings']['search_keywords']
    max_per_source = config['settings']['max_discussions_per_source']

    # Calculate date threshold (last N months)
    months = config['settings']['time_range_months']
    date_threshold = datetime.now() - timedelta(days=30 * months)

    for subreddit_name in subreddits:
        try:
            subreddit = reddit.subreddit(subreddit_name)
            print(f"  Searching r/{subreddit_name}...")

            # Search for each keyword
            for keyword in keywords:
                for post in subreddit.search(keyword, limit=max_per_source // len(keywords)):
                    post_date = datetime.fromtimestamp(post.created_utc)

                    # Skip old posts
                    if post_date < date_threshold:
                        continue

                    discussions.append({
                        'source': 'reddit',
                        'subreddit': subreddit_name,
                        'title': post.title,
                        'url': f"https://reddit.com{post.permalink}",
                        'content': post.selftext[:500],  # First 500 chars
                        'upvotes': post.score,
                        'comments': post.num_comments,
                        'created_at': post_date.isoformat(),
                        'keywords': keyword
                    })

            print(f"  ✓ Found {len([d for d in discussions if d['subreddit'] == subreddit_name])} discussions")

        except Exception as e:
            print(f"  ⚠️ Error scraping r/{subreddit_name}: {e}")
            continue

    print(f"✓ Reddit: {len(discussions)} discussions found")
    return discussions

# Hacker News scraping
def scrape_hackernews(config) -> List[Dict[str, Any]]:
    """Scrape Hacker News for Ask HN discussions"""
    print("📡 Scraping Hacker News...")

    try:
        import requests
    except ImportError:
        raise ImportError("Please install requests: pip install requests")

    discussions = []
    api_url = config['hackernews']['api_url']
    max_per_source = config['settings']['max_discussions_per_source']

    # Calculate timestamp threshold
    months = config['settings']['time_range_months']
    timestamp_threshold = int((datetime.now() - timedelta(days=30 * months)).timestamp())

    # Search queries
    queries = [
        "Ask HN why isn't there",
        "Ask HN looking for a tool",
        "Ask HN need software"
    ]

    for query in queries:
        try:
            response = requests.get(
                f"{api_url}/search",
                params={
                    'query': query,
                    'tags': 'ask_hn',
                    'numericFilters': f'created_at_i>{timestamp_threshold}',
                    'hitsPerPage': max_per_source // len(queries)
                }
            )

            if response.status_code == 200:
                data = response.json()

                for hit in data['hits']:
                    discussions.append({
                        'source': 'hackernews',
                        'title': hit.get('title', ''),
                        'url': f"https://news.ycombinator.com/item?id={hit['objectID']}",
                        'content': hit.get('story_text', '')[:500],
                        'points': hit.get('points', 0),
                        'comments': hit.get('num_comments', 0),
                        'created_at': datetime.fromtimestamp(hit['created_at_i']).isoformat(),
                        'author': hit.get('author', '')
                    })

        except Exception as e:
            print(f"  ⚠️ Error searching HN for '{query}': {e}")
            continue

    print(f"✓ Hacker News: {len(discussions)} discussions found")
    return discussions

# GitHub scraping
def scrape_github(config) -> List[Dict[str, Any]]:
    """Scrape GitHub for feature requests"""
    print("📡 Scraping GitHub...")

    github = init_github(config)
    discussions = []
    max_per_source = config['settings']['max_discussions_per_source']

    # Calculate date threshold
    months = config['settings']['time_range_months']
    date_str = (datetime.now() - timedelta(days=30 * months)).strftime('%Y-%m-%d')

    # Search queries
    queries = [
        f"label:feature-request created:>{date_str}",
        f"label:enhancement created:>{date_str}",
        f"is:issue is:open 'need a tool' created:>{date_str}"
    ]

    for query in queries:
        try:
            issues = github.search_issues(query, sort='comments', order='desc')

            count = 0
            for issue in issues:
                if count >= max_per_source // len(queries):
                    break

                discussions.append({
                    'source': 'github',
                    'title': issue.title,
                    'url': issue.html_url,
                    'content': (issue.body or '')[:500],
                    'reactions': issue.get_reactions().totalCount if hasattr(issue, 'get_reactions') else 0,
                    'comments': issue.comments,
                    'created_at': issue.created_at.isoformat(),
                    'repo': issue.repository.full_name if hasattr(issue, 'repository') else 'unknown',
                    'labels': [label.name for label in issue.labels]
                })
                count += 1

        except Exception as e:
            print(f"  ⚠️ Error searching GitHub: {e}")
            continue

    print(f"✓ GitHub: {len(discussions)} discussions found")
    return discussions

# Main scraper
def scrape_all_sources(config) -> Dict[str, List[Dict]]:
    """Scrape all data sources"""
    print("\n🔍 Project Scout - Real Data Scraper")
    print("=" * 50)

    results = {
        'metadata': {
            'scraped_at': datetime.now().isoformat(),
            'time_range_months': config['settings']['time_range_months'],
            'total_discussions': 0
        },
        'reddit': [],
        'hackernews': [],
        'github': []
    }

    # Scrape each source
    try:
        results['reddit'] = scrape_reddit(config)
    except Exception as e:
        print(f"❌ Reddit scraping failed: {e}")

    try:
        results['hackernews'] = scrape_hackernews(config)
    except Exception as e:
        print(f"❌ Hacker News scraping failed: {e}")

    try:
        results['github'] = scrape_github(config)
    except Exception as e:
        print(f"❌ GitHub scraping failed: {e}")

    # Calculate total
    results['metadata']['total_discussions'] = (
        len(results['reddit']) +
        len(results['hackernews']) +
        len(results['github'])
    )

    print("\n" + "=" * 50)
    print(f"✅ Scraping complete!")
    print(f"   Total discussions: {results['metadata']['total_discussions']}")
    print(f"   Reddit: {len(results['reddit'])}")
    print(f"   Hacker News: {len(results['hackernews'])}")
    print(f"   GitHub: {len(results['github'])}")

    return results

# Save results
def save_results(results: Dict, output_file: str = 'scraped_data.json'):
    """Save scraped data to file"""
    output_path = os.path.join(os.path.dirname(__file__), '..', output_file)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\n💾 Data saved to: {output_file}")
    return output_path

# Main entry point
if __name__ == "__main__":
    try:
        # Load config
        config = load_config()

        # Scrape all sources
        results = scrape_all_sources(config)

        # Save results
        save_results(results)

        print("\n✨ Done! Run the analysis script next to extract pain points.")

    except FileNotFoundError as e:
        print(f"\n❌ Configuration error: {e}")
        print("\n📝 Setup instructions:")
        print("   1. Copy config.example.json to config.json")
        print("   2. Add your API keys (see CONFIG_SETUP.md)")
        print("   3. Run this script again")

    except ImportError as e:
        print(f"\n❌ Missing dependency: {e}")
        print("\n📦 Install required packages:")
        print("   pip install praw requests PyGithub")

    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
