# MarketPress Submission Checklist

This checklist ensures MarketPress is fully judge-ready for Hex-a-thon evaluation.

## Pre-Submission Tasks

### ✅ Completed
- [x] Public Hex project published and accessible
- [x] Public Hex URL in README.md
- [x] Public Hex URL in HEX_GUIDE.md
- [x] Single canonical path documented (hex_cells/01-08)
- [x] Legacy methods marked as deprecated
- [x] Demo data fallback implemented
- [x] Automatic API failure handling
- [x] DATA_MODE banner system
- [x] Newspaper layout dataframes standardized
- [x] All required columns present in outputs
- [x] Drill-down fact boxes and timelines
- [x] Semantic model aligned with data
- [x] Editor Desk functions (Threads)
- [x] Threads starter prompts in README
- [x] Methodology section explaining signals
- [x] Smoke tests passing
- [x] CI/CD workflow configured
- [x] GitHub Actions running

### 📸 Screenshot Tasks (Optional but Recommended)
- [ ] Capture front page screenshot
  - Open: https://app.hex.tech/wildhash/app/marketpress-prediction-markets-newspaper/latest
  - Click "Run All"
  - Take full-page screenshot (1200-1600px wide)
  - Save as `assets/frontpage.png`
  - Delete `assets/frontpage_placeholder.md`
  - Update README to reference real image

- [ ] Capture drill-down screenshot
  - Navigate to drill-down cell output
  - Capture fact box and timeline
  - Save as `assets/drilldown.png`
  - Delete `assets/drilldown_placeholder.md`
  - Update README to reference real image

- [ ] Capture Editor Desk (Threads) screenshot
  - Open Threads panel
  - Run prompt: "Write today's front page in 8 headlines"
  - Capture prompt and response
  - Save as `assets/editor_desk.png`
  - Delete `assets/editor_desk_placeholder.md`
  - Update README to reference real image

## Judge Test (5-Minute Validation)

Before submitting, perform this 5-minute test as if you were a judge:

1. **Open the public Hex link** from README
   - Link works? ☐ Yes ☐ No
   - Project title visible? ☐ Yes ☐ No

2. **Click "Run All"**
   - All cells execute? ☐ Yes ☐ No
   - Time to complete: ___ seconds
   - Any errors? ☐ Yes ☐ No

3. **Verify outputs**
   - Lead Story visible? ☐ Yes ☐ No
   - Top Stories section (5 markets)? ☐ Yes ☐ No
   - Category sections visible? ☐ Yes ☐ No
   - Developing section visible? ☐ Yes ☐ No
   - Most Read section visible? ☐ Yes ☐ No
   - Data mode banner visible? ☐ Yes ☐ No

4. **Test Threads (Editor Desk)**
   - Threads panel opens? ☐ Yes ☐ No
   - Try: "Write today's front page in 8 headlines"
   - Response generated? ☐ Yes ☐ No
   - Try: "What's the biggest belief shift since yesterday?"
   - Response generated? ☐ Yes ☐ No

5. **Test drill-down**
   - Fact box displays? ☐ Yes ☐ No
   - Timeline data visible? ☐ Yes ☐ No

## Submission Platforms

### Hex-a-thon Submission
- [ ] Public Hex project URL submitted
- [ ] Project title: "MarketPress - Prediction Markets Newspaper"
- [ ] Description includes key features
- [ ] Tags: prediction markets, data visualization, semantic model, journalism

### Devpost (if applicable)
- [ ] GitHub repository linked
- [ ] README serves as project description
- [ ] Screenshots uploaded (if available)
- [ ] Video demo (optional)
- [ ] Built with: Hex, Kalshi API, Pandas, Python

## Common Issues & Solutions

### Issue: Kalshi API returns 429 (rate limit)
**Solution**: Demo fallback activates automatically. Banner shows "Demo mode."

### Issue: Kalshi API timeout
**Solution**: Demo fallback activates automatically after 10-second timeout.

### Issue: Empty sections
**Solution**: Check `MARKET_LIMIT` in Cell 1 (should be ≥ 50 for diverse sections).

### Issue: Threads prompts don't work
**Solution**: Ensure `semantic_model.yaml` is in project root and Cell 8 ran successfully.

## Final Verification

Run these commands locally before final submission:

```bash
# Install dependencies
pip install -r requirements.txt

# Run smoke tests
python tests/smoke_test.py

# Verify example script
python example.py

# Check all hex cells exist
ls hex_cells/*.py | wc -l  # Should output 8
```

Expected results:
- ✅ Smoke tests: 6/6 passed
- ✅ Example script: completes without errors
- ✅ Hex cells: 8 files present

---

## Submission Timeline

- **Pre-deadline**: Complete all ✅ tasks
- **Optional**: Add screenshots (can be done anytime)
- **Final check**: Run 5-minute judge test
- **Submit**: Public Hex URL + GitHub repo

---

**Status**: All critical features complete. Ready for submission pending optional screenshots.
