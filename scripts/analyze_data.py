"""
Analyze scraped data and extract pain points

This script reads scraped_data.json and uses AI to extract structured pain points.
"""

import json
import os
from typing import List, Dict, Any
from collections import defaultdict

def load_scraped_data(file_path: str = 'scraped_data.json') -> Dict:
    """Load scraped data from file"""
    full_path = os.path.join(os.path.dirname(__file__), '..', file_path)

    if not os.path.exists(full_path):
        raise FileNotFoundError(
            f"{file_path} not found! Run scrape_data.py first."
        )

    with open(full_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def extract_keywords(discussions: List[Dict]) -> Dict[str, int]:
    """Extract and count keywords from discussions"""
    keywords = defaultdict(int)

    # Common pain point indicators
    pain_keywords = [
        'wish', 'need', 'want', 'looking for', 'missing',
        'frustrat', 'annoying', 'waste', 'hate', 'painful',
        'why isn\'t there', 'would pay', 'should exist'
    ]

    for discussion in discussions:
        title = discussion.get('title', '').lower()
        content = discussion.get('content', '').lower()
        text = title + ' ' + content

        for keyword in pain_keywords:
            if keyword in text:
                keywords[keyword] += 1

    return dict(sorted(keywords.items(), key=lambda x: x[1], reverse=True))

def cluster_discussions(discussions: List[Dict]) -> Dict[str, List[Dict]]:
    """Group discussions by topic/theme"""
    clusters = defaultdict(list)

    # Simple keyword-based clustering
    themes = {
        'validation': ['validate', 'idea', 'market', 'research'],
        'automation': ['automate', 'automatic', 'script', 'workflow'],
        'tools': ['tool', 'software', 'app', 'utility'],
        'productivity': ['productive', 'efficient', 'fast', 'quick'],
        'collaboration': ['team', 'share', 'collaborate', 'together']
    }

    for discussion in discussions:
        text = (discussion.get('title', '') + ' ' + discussion.get('content', '')).lower()

        # Assign to first matching theme
        assigned = False
        for theme, keywords in themes.items():
            if any(kw in text for kw in keywords):
                clusters[theme].append(discussion)
                assigned = True
                break

        if not assigned:
            clusters['other'].append(discussion)

    return dict(clusters)

def calculate_engagement_score(discussion: Dict) -> int:
    """Calculate engagement score for a discussion"""
    source = discussion['source']

    if source == 'reddit':
        return discussion.get('upvotes', 0) + discussion.get('comments', 0) * 2
    elif source == 'hackernews':
        return discussion.get('points', 0) + discussion.get('comments', 0) * 3
    elif source == 'github':
        return discussion.get('reactions', 0) + discussion.get('comments', 0) * 2

    return 0

def extract_pain_points(data: Dict) -> List[Dict[str, Any]]:
    """Extract pain points from scraped data"""
    print("\n🔍 Analyzing scraped data...")
    print("=" * 50)

    # Combine all discussions
    all_discussions = (
        data.get('reddit', []) +
        data.get('hackernews', []) +
        data.get('github', [])
    )

    print(f"📊 Total discussions: {len(all_discussions)}")

    # Extract keywords
    keywords = extract_keywords(all_discussions)
    print(f"\n🔑 Top pain indicators:")
    for keyword, count in list(keywords.items())[:5]:
        print(f"   '{keyword}': {count} mentions")

    # Cluster by theme
    clusters = cluster_discussions(all_discussions)
    print(f"\n📁 Discussion themes:")
    for theme, discussions in clusters.items():
        if discussions:
            print(f"   {theme.capitalize()}: {len(discussions)} discussions")

    # Extract top pain points
    pain_points = []

    for theme, discussions in clusters.items():
        if not discussions:
            continue

        # Sort by engagement
        sorted_discussions = sorted(
            discussions,
            key=calculate_engagement_score,
            reverse=True
        )

        # Take top discussion from each theme
        top = sorted_discussions[0]

        pain_points.append({
            'theme': theme,
            'title': top.get('title', 'Untitled'),
            'evidence_count': len(discussions),
            'top_discussion': {
                'source': top['source'],
                'url': top.get('url', ''),
                'engagement': calculate_engagement_score(top),
                'excerpt': top.get('content', '')[:200]
            },
            'potential_score': len(discussions) * 10 + calculate_engagement_score(top) // 10
        })

    # Sort by potential score
    pain_points.sort(key=lambda x: x['potential_score'], reverse=True)

    print(f"\n✅ Extracted {len(pain_points)} pain points")

    return pain_points

def save_analysis(pain_points: List[Dict], output_file: str = 'pain_points.json'):
    """Save analysis results"""
    output_path = os.path.join(os.path.dirname(__file__), '..', output_file)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(pain_points, f, indent=2, ensure_ascii=False)

    print(f"\n💾 Analysis saved to: {output_file}")

def print_summary(pain_points: List[Dict]):
    """Print summary of findings"""
    print("\n" + "=" * 50)
    print("📊 Top Pain Points Summary")
    print("=" * 50)

    for i, pain_point in enumerate(pain_points[:5], 1):
        print(f"\n#{i}: {pain_point['title']}")
        print(f"   Theme: {pain_point['theme'].capitalize()}")
        print(f"   Evidence: {pain_point['evidence_count']} discussions")
        print(f"   Top source: {pain_point['top_discussion']['source']}")
        print(f"   Engagement: {pain_point['top_discussion']['engagement']}")
        print(f"   Potential score: {pain_point['potential_score']}")

def main():
    try:
        # Load scraped data
        data = load_scraped_data()

        # Extract pain points
        pain_points = extract_pain_points(data)

        # Save results
        save_analysis(pain_points)

        # Print summary
        print_summary(pain_points)

        print("\n✨ Analysis complete!")
        print("\n🚀 Next: Use these pain points to generate the full report")

    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
        print("\n📝 Run these steps in order:")
        print("   1. python scripts/scrape_data.py")
        print("   2. python scripts/analyze_data.py (this script)")

    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
