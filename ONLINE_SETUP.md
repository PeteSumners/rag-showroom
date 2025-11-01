# 🌐 Online Setup - Quick Start Guide

Get your RAG Showroom running completely online with automated LinkedIn posts in under 10 minutes.

## What You'll Get

✅ **Fully automated system** running on GitHub Actions
✅ **Daily RAG pattern demos** built and tested automatically
✅ **LinkedIn posts** with screenshots and technical breakdowns
✅ **Zero local maintenance** - runs entirely in the cloud

## Prerequisites

You need:
- GitHub account
- GitHub CLI (`gh`) installed - [Get it here](https://cli.github.com/)
- LinkedIn account for posting
- Anthropic API key - [Get it here](https://console.anthropic.com/)

## One-Command Setup

Run this from your project directory:

```bash
./setup-online.sh
```

This script will guide you through:
1. Creating GitHub repository
2. Getting LinkedIn API credentials (with helper tool)
3. Configuring all secrets
4. Triggering test run

## Manual Setup (Step by Step)

If you prefer manual control:

### 1. Create GitHub Repository

```bash
./setup-github.sh
```

Answers the prompts for:
- Repository name (default: rag-showroom)
- Public or private
- Initial commit and push

### 2. Get LinkedIn Credentials

**Option A**: Interactive helper (easiest)
```bash
python scripts/linkedin_oauth.py
```

**Option B**: Manual process
Follow detailed guide in `LINKEDIN_SETUP.md`

You'll get:
- `LINKEDIN_ACCESS_TOKEN` - Your OAuth token
- `LINKEDIN_URN` - Your person URN (format: `urn:li:person:YOUR_ID`)

### 3. Configure GitHub Secrets

```bash
./setup-secrets.sh
```

Sets up:
- `ANTHROPIC_API_KEY` (required) - For Claude API
- `OPENAI_API_KEY` (optional) - For embeddings
- `LINKEDIN_ACCESS_TOKEN` (required) - For posting
- `LINKEDIN_URN` (required) - Your LinkedIn ID

### 4. Trigger Test Run

```bash
gh workflow run daily-showcase.yml
```

Monitor it:
```bash
gh run watch
```

Or view in browser:
```bash
gh workflow view daily-showcase.yml --web
```

## Verification Checklist

After setup, verify:

- [ ] Repository created on GitHub
- [ ] All secrets configured (check with `gh secret list`)
- [ ] Workflow triggered successfully
- [ ] Demo files created in `demos/` directory
- [ ] Post appeared on your LinkedIn profile
- [ ] Pattern queue updated in `queue/patterns.json`

## Monitoring & Management

### Check Status

```bash
./scripts/check_workflow.sh
```

Shows:
- Recent workflow runs
- Configured secrets
- Pattern queue status
- Next scheduled run

### View Workflow Logs

```bash
gh run list
gh run view <run-id>
```

### Manually Trigger Run

```bash
gh workflow run daily-showcase.yml
```

## How It Works

Once set up, the system runs automatically:

### Daily at 9 AM UTC:

1. **Pattern Selection** - Picks next RAG pattern from queue
2. **Demo Building** - Uses Claude API to generate implementation
3. **Testing** - Runs pytest tests and captures output
4. **Screenshots** - Captures colored terminal output as images
5. **Content Generation** - Writes technical breakdown with Claude
6. **LinkedIn Post** - Posts demo with screenshot to LinkedIn
7. **Commit** - Saves demo back to repository

### Each demo includes:

- ✅ Working Python implementation
- ✅ Comprehensive tests
- ✅ Rich ASCII art visualization
- ✅ Technical explanation
- ✅ LinkedIn post content

## Troubleshooting

### "Workflow failed at build step"

Check Claude API key is valid:
```bash
gh secret set ANTHROPIC_API_KEY
```

### "LinkedIn post failed"

1. Verify token hasn't expired (60-day lifetime)
2. Check token has `w_member_social` scope
3. Verify URN format: `urn:li:person:YOUR_ID`
4. Re-run OAuth: `python scripts/linkedin_oauth.py`

### "No demos being created"

1. Check workflow is enabled: GitHub → Actions → Enable workflows
2. Verify schedule: Should run daily at 9 AM UTC
3. Manual trigger: `gh workflow run daily-showcase.yml`

### "Tests failing"

1. View logs: `gh run view`
2. Check demo requirements.txt has all dependencies
3. Pattern might need adjustment in `queue/patterns.json`

## Pattern Queue Management

View queue status:
```bash
cat queue/patterns.json | python -m json.tool
```

Add new pattern:
```json
{
  "name": "your-pattern-name",
  "description": "Brief description",
  "difficulty": "beginner|intermediate|advanced",
  "key_concepts": ["concept1", "concept2"],
  "status": "pending"
}
```

## Cost Estimates

### GitHub Actions
- Free tier: 2,000 minutes/month
- This workflow: ~5-10 minutes/run
- Daily runs: ~300 minutes/month
- **Cost: FREE** (well within limits)

### Anthropic API
- Claude API calls: ~2 per run (build + breakdown)
- Cost: ~$0.10-0.20 per demo
- Monthly (30 demos): ~$3-6
- **Cost: $3-6/month**

### LinkedIn API
- Completely free
- No rate limit issues at 1 post/day

**Total: ~$3-6/month** (mostly Claude API)

## Next Steps

1. ✅ Complete setup with `./setup-online.sh`
2. 📊 Monitor first workflow run
3. 👀 Check LinkedIn for your first post
4. 🎉 Watch daily automation work its magic
5. 🔄 Optionally customize patterns in queue
6. 📅 Set reminder for token refresh (50 days)

## Support

- **Setup issues**: Review SETUP.md for details
- **LinkedIn API**: See LINKEDIN_SETUP.md
- **Development**: Check CLAUDE.md
- **Pattern ideas**: Open GitHub issue

---

**Ready to run completely online? Execute:**
```bash
./setup-online.sh
```

The script will guide you through everything! 🚀
