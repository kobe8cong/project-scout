# Contributing to Project Scout

Thank you for considering contributing to Project Scout! 🎉

## How to Contribute

### Reporting Bugs

Found a bug? Please [open an issue](https://github.com/kobe8cong/project-scout/issues/new) with:
- Description of the bug
- Steps to reproduce
- Expected vs actual behavior
- Your environment (OS, Claude Code version)

### Suggesting Features

Have an idea? [Start a discussion](https://github.com/kobe8cong/project-scout/discussions/new?category=ideas) with:
- Problem you're trying to solve
- Proposed solution
- Why it would be valuable

### Improving Documentation

Documentation improvements are always welcome! Areas that need help:
- Clarifying existing docs
- Adding examples
- Fixing typos
- Translating (future)

### Code Contributions

#### Before You Start
1. Check [existing issues](https://github.com/kobe8cong/project-scout/issues) to avoid duplication
2. For large changes, open an issue first to discuss
3. For small fixes, PRs are welcome directly

#### Development Setup
```bash
# Clone the repo
git clone https://github.com/kobe8cong/project-scout.git

# Project Scout is a Claude Code skill, so you'll need Claude Code to test
# Load it as a local skill in your Claude Code workspace
```

#### Making Changes
1. Create a branch: `git checkout -b feature/your-feature-name`
2. Make your changes
3. Test thoroughly
4. Commit with clear messages
5. Push and open a PR

#### Pull Request Guidelines
- Clear description of what and why
- Reference related issues
- Test your changes
- Update docs if needed
- Keep PRs focused (one feature/fix per PR)

### Improving the Scoring Algorithm

The scoring algorithm is in `agents/gap-scorer.md`. If you have ideas to improve it:
1. Explain the current limitation
2. Propose the improvement with rationale
3. Show example calculations
4. Open a discussion or PR

### Adding Data Sources

Want to add a new data source (e.g., Twitter, Discord, Dev.to)?
1. Check feasibility (API availability, rate limits, costs)
2. Open a discussion to get feedback
3. Implement in `agents/demand-scraper.md`
4. Update documentation

## Code of Conduct

- Be respectful and constructive
- Welcome newcomers
- Focus on the idea, not the person
- Assume good intentions

## Questions?

Not sure about something? Ask in [Discussions](https://github.com/kobe8cong/project-scout/discussions)!

## Recognition

Contributors will be:
- Listed in README acknowledgments
- Credited in release notes
- Mentioned in project announcements

Thank you for helping make Project Scout better! 🚀
