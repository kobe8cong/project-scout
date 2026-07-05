"""
Test configuration and API connectivity

Run this script to verify your config.json is set up correctly.
"""

import json
import os
import sys

def test_config_file():
    """Check if config.json exists and is valid"""
    print("1️⃣  Checking config.json...")

    config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')

    if not os.path.exists(config_path):
        print("   ❌ config.json not found!")
        print("   📝 Create it by copying config.example.json")
        return None

    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        print("   ✅ config.json is valid JSON")
        return config
    except json.JSONDecodeError as e:
        print(f"   ❌ config.json has invalid JSON: {e}")
        return None

def test_reddit_config(config):
    """Test Reddit API configuration"""
    print("\n2️⃣  Testing Reddit API...")

    try:
        import praw
    except ImportError:
        print("   ❌ praw not installed. Run: pip install praw")
        return False

    try:
        reddit = praw.Reddit(
            client_id=config['reddit']['client_id'],
            client_secret=config['reddit']['client_secret'],
            user_agent=config['reddit']['user_agent']
        )

        # Test by fetching a subreddit
        subreddit = reddit.subreddit('test')
        _ = subreddit.display_name

        print("   ✅ Reddit API connected successfully")
        return True
    except Exception as e:
        print(f"   ❌ Reddit API error: {e}")
        print("   📝 Check your client_id and client_secret in config.json")
        return False

def test_github_config(config):
    """Test GitHub API configuration"""
    print("\n3️⃣  Testing GitHub API...")

    try:
        from github import Github
    except ImportError:
        print("   ❌ PyGithub not installed. Run: pip install PyGithub")
        return False

    try:
        g = Github(config['github']['access_token'])
        user = g.get_user()

        # Get rate limit info
        rate_limit = g.get_rate_limit()

        print(f"   ✅ GitHub API connected successfully")
        print(f"   👤 Authenticated as: {user.login}")
        print(f"   📊 Rate limit: {rate_limit.core.remaining}/{rate_limit.core.limit}")
        return True
    except Exception as e:
        print(f"   ❌ GitHub API error: {e}")
        print("   📝 Check your access_token in config.json")
        return False

def test_hackernews_api():
    """Test Hacker News API (no auth needed)"""
    print("\n4️⃣  Testing Hacker News API...")

    try:
        import requests
    except ImportError:
        print("   ❌ requests not installed. Run: pip install requests")
        return False

    try:
        response = requests.get("https://hn.algolia.com/api/v1/search?query=test&hitsPerPage=1")

        if response.status_code == 200:
            print("   ✅ Hacker News API accessible")
            return True
        else:
            print(f"   ❌ HN API returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ HN API error: {e}")
        return False

def test_ai_config(config):
    """Test AI API configuration"""
    print("\n5️⃣  Testing AI API...")

    provider = config.get('ai', {}).get('provider', 'none')

    if provider == 'anthropic':
        try:
            import anthropic
        except ImportError:
            print("   ❌ anthropic not installed. Run: pip install anthropic")
            return False

        try:
            client = anthropic.Anthropic(api_key=config['ai']['api_key'])
            # Just test authentication, don't make an actual API call
            print("   ✅ Anthropic API key configured")
            return True
        except Exception as e:
            print(f"   ❌ Anthropic API error: {e}")
            return False

    elif provider == 'openai':
        try:
            import openai
        except ImportError:
            print("   ❌ openai not installed. Run: pip install openai")
            return False

        try:
            openai.api_key = config['ai']['api_key']
            print("   ✅ OpenAI API key configured")
            return True
        except Exception as e:
            print(f"   ❌ OpenAI API error: {e}")
            return False

    else:
        print(f"   ⚠️  Unknown AI provider: {provider}")
        print("   📝 Set provider to 'anthropic' or 'openai' in config.json")
        return False

def main():
    print("🔍 Project Scout - Configuration Test")
    print("=" * 50)

    # Test config file
    config = test_config_file()
    if not config:
        print("\n❌ Configuration test failed!")
        print("\n📝 Setup instructions:")
        print("   1. Copy config.example.json to config.json")
        print("   2. Add your API keys (see CONFIG_SETUP.md)")
        print("   3. Run this test again")
        sys.exit(1)

    # Test each API
    results = {
        'reddit': test_reddit_config(config),
        'github': test_github_config(config),
        'hackernews': test_hackernews_api(),
        'ai': test_ai_config(config)
    }

    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Summary:")
    print("=" * 50)

    for service, passed in results.items():
        status = "✅" if passed else "❌"
        print(f"   {status} {service.capitalize()}")

    all_passed = all(results.values())

    if all_passed:
        print("\n✨ All tests passed! You're ready to run /scout")
        print("\n🚀 Next steps:")
        print("   1. Run: python scripts/scrape_data.py")
        print("   2. Or use /scout in Claude Code")
        sys.exit(0)
    else:
        print("\n⚠️  Some tests failed. Fix the issues above and try again.")
        sys.exit(1)

if __name__ == "__main__":
    main()
