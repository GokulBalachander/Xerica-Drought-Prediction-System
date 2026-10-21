# Xerica: Drought Prediction System

Xerica forecasts next week's U.S. Drought Monitor (USDM) map with a neural network trained on drought history, satellite data and climate indicators.

This repository holds the Xerica website: a single page with an interactive map of current drought across all 50 states and Puerto Rico, D0 Abnormally Dry through D4 Exceptional.

## Files

| Path | What it is |
|---|---|
| `index.html` | The whole website, with the state boundaries and the current USDM map embedded |
| `xerica-logo.svg` | The Xerica logo, also used as the favicon |
| `scripts/update_usdm.py` | Refreshes the drought map with a new weekly USDM file |
| `.nojekyll` | Tells GitHub Pages to serve the files as they are |

## Publishing with GitHub Pages

1. Open the repository on GitHub and go to **Settings → Pages**.
2. Under **Build and deployment**, set **Source** to **Deploy from a branch**.
3. Pick the branch that holds `index.html` and the **/ (root)** folder, then click **Save**.

After a minute or two the site is live at `https://gokulbalachander.github.io/Xerica-Drought-Prediction-System/`.

## Updating the drought map each week

The USDM publishes a new map every Thursday, dated the Tuesday before.

1. Download https://droughtmonitor.unl.edu/data/json/usdm_current.json
2. Run, with the date shown on the USDM site:
   ```
   python scripts/update_usdm.py usdm_current.json "Oct 20, 2026"
   ```
   The script needs Python 3 and Node.js (it runs mapshaper through `npx` to shrink the 15–20 MB file to about 160 KB).
3. Commit and push `index.html`. GitHub Pages republishes the site automatically.

The county markers, sidebar levels and landing page badge all update from the new map on their own.

## Contact form

Messages from the Contact Us form are emailed through [FormSubmit](https://formsubmit.co). The very first message sends a one-time activation email to the receiving address; click the link in it and later messages arrive directly. FormSubmit then offers a random alias for the address: replace the email in `CONTACT_ENDPOINT` inside `index.html` with that alias to keep the address out of the page source.

## Data

- Drought areas: [U.S. Drought Monitor](https://droughtmonitor.unl.edu), produced by the National Drought Mitigation Center at the University of Nebraska-Lincoln, USDA and NOAA.
- State boundaries: [us-atlas](https://github.com/topojson/us-atlas) 3.0.1, from the U.S. Census Bureau.
