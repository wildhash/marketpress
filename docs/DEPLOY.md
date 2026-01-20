# GitHub Pages Deployment Guide

This guide explains how to enable GitHub Pages deployment for the MarketPress landing page.

## Enable GitHub Pages

1. Go to your repository on GitHub
2. Click **Settings** (in the repository navigation)
3. In the left sidebar, click **Pages** (under "Code and automation")
4. Under **Build and deployment**:
   - Set **Source** to **GitHub Actions**
5. That's it! The workflow is already configured.

## How It Works

The `.github/workflows/pages.yml` workflow automatically deploys the `/docs` folder to GitHub Pages when you push to the `main` branch.

### Workflow Details

- **Trigger**: Push to `main` branch or manual workflow dispatch
- **Content**: Deploys everything in the `/docs` folder
- **URL**: Your site will be available at `https://wildhash.github.io/marketpress/`

## Updating Content

To update the landing page:

1. Edit files in the `/docs` folder
2. Commit and push to `main`
3. Wait 1-2 minutes for the workflow to complete
4. Visit your site to see the changes

## Placeholder Links

In `docs/index.html`, the demo video button is currently disabled:

### Demo Video Link
```html
<a href="#" class="btn btn-secondary btn-disabled" title="Demo video coming soon">Watch Demo Video (Coming Soon)</a>
```

To enable the demo video button, replace this line with:
```html
<a href="YOUR_DEMO_VIDEO_URL" class="btn btn-secondary">Watch Demo Video</a>
```

Replace `YOUR_DEMO_VIDEO_URL` with your actual demo video URL (YouTube, Loom, etc.) and remove the `btn-disabled` class.

### Public Hex Project Link
The public Hex project link is already configured and working:
```html
<a href="https://app.hex.tech/wildhash/app/marketpress-prediction-markets-newspaper/latest" class="btn btn-primary">Open Public Hex Project</a>
```

## Troubleshooting

### Site Not Loading
- Check that GitHub Actions is enabled in repository settings
- Verify the workflow completed successfully in the **Actions** tab
- Ensure Pages is set to "GitHub Actions" source

### Images Not Showing
- Verify image files exist in `/docs/assets/`
- Check that image paths in HTML are relative (e.g., `assets/marketpress-hero.png`)
- Clear browser cache and reload

### CSS Not Applied
- Verify `style.css` exists in `/docs/`
- Check that the CSS link in HTML is correct: `<link rel="stylesheet" href="style.css">`
- Clear browser cache and reload

## Manual Deployment

If you need to manually trigger deployment:

1. Go to the **Actions** tab in your repository
2. Click **Deploy Pages** workflow
3. Click **Run workflow** button
4. Select the `main` branch
5. Click **Run workflow**

## First-Time Setup Checklist

- [x] `/docs` folder created
- [x] `index.html` created with landing page content
- [x] `style.css` created with styling
- [x] Placeholder images created in `/docs/assets/`
- [x] `.github/workflows/pages.yml` created
- [ ] Repository Settings → Pages → Source set to "GitHub Actions"
- [ ] Push to `main` branch
- [ ] Wait for workflow to complete
- [ ] Visit `https://wildhash.github.io/marketpress/`

After completing the checklist, your MarketPress landing page should be live!
