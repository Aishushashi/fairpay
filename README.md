# FairPay: a private AI auditor for gig workers

IBM Z Datathon 2026 | Theme: AI Secured (Innovation Without Exposure), under AI for Good | Event code: SSF2026

## Problem
Gig workers (delivery and ride platforms) often cannot tell why their pay per km dropped, why deductions grew, or why incentives disappeared. Their payout history is sensitive, so sending it to an unknown service is risky.

## What FairPay does
A worker uploads a payout CSV. FairPay:
- validates the file and calculates earnings per trip, per km and per hour (adds up first, then divides)
- flags a drop in base pay per km, a rise in the deduction share, and a drop in the incentive share, by comparing the earlier half and the recent half of the worker's records
- compares the worker with aggregated peers (same city, platform and time slot); the comparison is hidden if fewer than 20 other workers match
- explains each flag in plain language using fixed templates (labelled "not AI-written"). A flag does not prove intentional underpayment.
- shows everything in a Flask dashboard running on IBM LinuxONE (binds to 127.0.0.1 only)

## Data (SYNTHETIC)
No real worker data is used. src/make_data.py generates 26,865 synthetic rows for 300 workers with planted problems (36 evening pay cuts, 24 deduction jumps, 24 incentive cuts, 216 normal workers) and an answer key.

## Results (honest)
On the synthetic data the detector found all planted cases (recall 36/36, 24/24, 24/24) with 0 of 216 normal workers flagged. The thresholds were chosen knowing the planted effect sizes, so this tests the pipeline only. It is NOT real-world accuracy.

## Architecture
CSV upload -> validation (src/metrics.py) -> detector (src/detect.py) -> peer benchmark (src/peers.py) -> explanations (src/explain.py) -> Flask dashboard (src/app.py, src/page.py, src/art.py)

## How it uses IBM Z / LinuxONE
- Runs on a LinuxONE Community Cloud VM (Ubuntu 24.04, s390x, Python 3.12)
- Docker runs IBM's Jupyter Lab ML image (jupyterlab-image-s390x); we ran its sample notebooks (Fraud_LSTM_Keras_TF and Churn_Scikit_PyTorch) on LinuxONE
- Being on LinuxONE does not by itself make the app secure

## How to run
    cd ~/fairpay
    source .venv/bin/activate
    python -m src.make_data      # regenerate synthetic data
    python -m src.evaluate       # evaluation on synthetic data
    python -m pytest -q tests    # 5 tests
    python -m src.app            # open http://127.0.0.1:5000

## Limitations
- Synthetic data only; no real-world accuracy is claimed
- Peer privacy is aggregation plus a minimum group size of 20. It is NOT differential privacy.
- Explanations are templates. No Granite or other LLM, no OCR, no PDF evidence report, no multilingual output yet.
- Related auditing projects already exist (UberCheats, Driver's Seat, Worker Info Exchange, Shipt Calculator). Our contribution is only the combination: personalized, privacy-conscious peer comparison, plain-language explanation, running privately on LinuxONE.

## Open-source libraries
Python (python.org), pandas (pandas.pydata.org), NumPy (numpy.org), scikit-learn (scikit-learn.org), matplotlib (matplotlib.org), Flask (flask.palletsprojects.com), pytest (pytest.org), Docker (docker.com), IBM Jupyter Lab ML image for LinuxONE.

All code was written after the hackathon kickoff.
