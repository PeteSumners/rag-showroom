# Setup Guide

This guide will help you set up and run the RAG Showroom automation system.

## Prerequisites

- Python 3.11+
- Node.js 20+
- Git
- GitHub account with repo access
- API keys for:
  - Anthropic (Claude)
  - OpenAI (optional, for embeddings)
  - LinkedIn (for posting)

## Local Setup

### 1. Install Dependencies

```bash
# Install Python dependencies
pip install -r requirements.txt

# Install Node dependencies
npm install

# Install Playwright browser
npx playwright install chromium
```

### 2. Set Environment Variables

Create a `.env` file in the root directory:

```bash
ANTHROPIC_API_KEY=your_anthropic_key
OPENAI_API_KEY=your_openai_key  # Optional
LINKEDIN_ACCESS_TOKEN=your_linkedin_token
LINKEDIN_URN=urn:li:person:YOUR_PERSON_ID
```

### 3. Test the First Demo

The semantic-chunking demo is already built as a proof of concept.

```bash
# Run the demo
cd demos/semantic-chunking
python demo.py

# Run tests
pytest test_demo.py -v
```

You should see colorful ASCII art output showing the semantic chunking process.

## Running the Full Pipeline Locally

Test the complete automation pipeline:

```bash
# 1. Select next pattern and generate prompt
python scripts/generate_demo.py

# 2. Build demo (requires Claude Code CLI)
# Note: You may need to adjust this based on Claude Code CLI availability
./scripts/build_demo.sh

# 3. Test the demo
python scripts/test_demo.py

# 4. Capture screenshots
node scripts/capture_screenshots.js

# 5. Generate technical breakdown
python scripts/write_breakdown.py

# 6. Post to LinkedIn (dry run if no credentials)
python scripts/post_linkedin.py
```

## GitHub Actions Setup

### 1. Add Repository Secrets

Go to your GitHub repo → Settings → Secrets and variables → Actions

Add these secrets:

- `ANTHROPIC_API_KEY` - Your Anthropic API key
- `OPENAI_API_KEY` - Your OpenAI API key (optional)
- `LINKEDIN_ACCESS_TOKEN` - LinkedIn OAuth access token
- `LINKEDIN_URN` - Your LinkedIn person URN (format: `urn:li:person:YOUR_ID`)

### 2. Get LinkedIn API Credentials

Follow LinkedIn's OAuth 2.0 documentation:

1. Create a LinkedIn App at https://www.linkedin.com/developers/apps
2. Request access to the Share on LinkedIn product
3. Generate an OAuth 2.0 access token with `w_member_social` scope
4. Get your person URN from LinkedIn API: `GET https://api.linkedin.com/v2/me`

### 3. Enable GitHub Actions

The workflow is already configured in `.github/workflows/daily-showcase.yml`

It will run:
- Daily at 9 AM UTC
- Manually via workflow_dispatch (Actions tab → Daily RAG Showcase → Run workflow)

### 4. Test Manual Trigger

1. Go to Actions tab in your GitHub repo
2. Select "Daily RAG Showcase"
3. Click "Run workflow"
4. Monitor the execution

## Project Structure

```
.
├── demos/
│   └── semantic-chunking/       # First demo (proof of concept)
│       ├── demo.py              # Main implementation
│       ├── test_demo.py         # Tests
│       └── requirements.txt     # Dependencies
├── queue/
│   └── patterns.json            # Queue of RAG patterns to build
├── scripts/
│   ├── generate_demo.py         # Pattern selection
│   ├── build_demo.sh            # Claude Code invocation
│   ├── test_demo.py             # Test runner
│   ├── capture_screenshots.js   # Screenshot capture
│   ├── write_breakdown.py       # Content generation
│   └── post_linkedin.py         # LinkedIn posting
├── outputs/                     # Generated content (gitignored)
│   └── YYYY-MM-DD/
│       ├── terminal_output.txt
│       ├── screenshots/
│       ├── linkedin_post.md
│       └── technical_breakdown.md
├── .github/workflows/
│   └── daily-showcase.yml       # CI/CD automation
└── CLAUDE.md                    # Guidance for Claude Code

```

## Adding New Patterns

Edit `queue/patterns.json` to add new RAG patterns:

```json
{
  "name": "your-pattern",
  "description": "Brief description",
  "difficulty": "beginner|intermediate|advanced",
  "key_concepts": ["concept1", "concept2"],
  "status": "pending"
}
```

## Troubleshooting

### Claude Code CLI Not Found

The build script assumes Claude Code CLI is available. You may need to:
1. Install the Claude Code CLI tool
2. Adjust the invocation in `scripts/build_demo.sh`

### LinkedIn API Issues

- Verify your access token is valid
- Ensure you have `w_member_social` permission
- Check token hasn't expired (LinkedIn tokens typically expire after 60 days)

### Tests Failing

Run the demo directly to see detailed errors:

```bash
cd demos/{pattern-name}
python demo.py
```

## Next Steps

1. Verify the semantic-chunking demo works locally
2. Set up GitHub secrets
3. Run a manual workflow trigger
4. Monitor the daily automation
5. Review generated LinkedIn posts before they publish

## Need Help?

- Check CLAUDE.md for development guidance
- Review the README.md for project context
- Open an issue on GitHub
