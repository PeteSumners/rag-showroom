# Deploying to GitHub Pages

This guide shows you how to deploy the RAG Patterns Guide as a beautiful GitHub Pages website.

## Prerequisites

- GitHub account
- `gh` CLI installed (you mentioned you have this!)
- Repository pushed to GitHub

## Quick Deploy

### 1. Create/Update Repository

If you haven't already:

```bash
# Initialize git (if not already done)
git init
git add .
git commit -m "feat: RAG patterns guide with GitHub Pages"

# Create GitHub repository
gh repo create rag-patterns-guide --public --source=. --remote=origin --push
```

Or if repo exists:

```bash
git add .
git commit -m "feat: add GitHub Pages documentation"
git push
```

### 2. Enable GitHub Pages

```bash
# Enable GitHub Pages with Actions
gh api \
  --method POST \
  -H "Accept: application/vnd.github+json" \
  /repos/OWNER/rag-patterns-guide/pages \
  -f build_type='workflow'
```

Or do it manually:
1. Go to your repository on GitHub
2. Click **Settings** → **Pages**
3. Under "Build and deployment", select **GitHub Actions**

### 3. Push and Deploy

The GitHub Actions workflow (`.github/workflows/deploy-docs.yml`) will automatically:
- Build the MkDocs site
- Deploy to GitHub Pages

Just push any changes:

```bash
git push
```

Wait 1-2 minutes, then visit:
```
https://YOUR-USERNAME.github.io/rag-patterns-guide/
```

## Local Preview

Want to see the site locally before deploying?

### Install MkDocs

```bash
pip install mkdocs-material mkdocs-glightbox
```

### Serve Locally

```bash
mkdocs serve
```

Visit http://localhost:8000 to preview!

## Customization

### Update Site URL

Edit `mkdocs.yml`:

```yaml
site_url: https://YOUR-USERNAME.github.io/rag-patterns-guide
repo_name: YOUR-USERNAME/rag-patterns-guide
repo_url: https://github.com/YOUR-USERNAME/rag-patterns-guide
```

### Update Social Links

Edit `mkdocs.yml` under `extra`:

```yaml
extra:
  social:
    - icon: fontawesome/brands/github
      link: https://github.com/YOUR-USERNAME
    - icon: fontawesome/brands/linkedin
      link: https://linkedin.com/in/YOUR-PROFILE
```

## Troubleshooting

### Pages Not Deploying

Check the Actions tab:
```bash
gh run list --workflow="deploy-docs.yml"
```

View latest run:
```bash
gh run view
```

### Build Errors

Run locally to debug:
```bash
mkdocs build --strict
```

This will show any errors in your markdown files.

### Custom Domain

Want a custom domain? Add `CNAME` file:

```bash
echo "your-domain.com" > docs/CNAME
git add docs/CNAME
git commit -m "Add custom domain"
git push
```

Then configure DNS:
- Add CNAME record pointing to `YOUR-USERNAME.github.io`

## What's Deployed?

Your site includes:
- ✅ Beautiful Material Design theme
- ✅ Dark/light mode toggle
- ✅ Search functionality
- ✅ Code syntax highlighting
- ✅ Mermaid diagram rendering
- ✅ All pattern documentation with terminal outputs
- ✅ Getting started guides
- ✅ Pattern comparison tables
- ✅ Mobile responsive

## Next Steps

After deployment:
1. Share the URL on LinkedIn!
2. Add the URL to your repository description
3. Tweet about it / share on social media
4. Add patterns to your resume/portfolio

---

**Questions?** Open an issue or check [MkDocs Material docs](https://squidfunk.github.io/mkdocs-material/)
