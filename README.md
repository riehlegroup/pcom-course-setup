# ML Competition – Student Prediction API Template

This repository provides a minimal FastAPI template for participating in an ML Competition.
During each evaluation round, the competition service calls your `/predict` endpoint with a download URL (for the test input CSV) and an upload URL (to submit your predicted CSV).

## Project Structure

- `main.py` – FastAPI server (`/health` and `/predict` endpoints) and `run_model(df)` where you integrate your trained ML model.
- `pyproject.toml` / `requirements.txt` – Python dependencies (`fastapi`, `uvicorn`, `pandas`, `requests`).
- `Dockerfile` – Container setup for easy deployment on a VM.

---

## 1. Integrate Your Model

Open `main.py` and replace the example code inside `run_model(df: pd.DataFrame)` with your trained model's inference logic.

**Important Rules:**
1. Do **not** change the row order, row count, or column names of the DataFrame.
2. Fill the empty target column(s) with your predictions (no `NaN` / empty values in target columns).
3. If your model requires additional Python libraries (e.g., `scikit-learn`, `xgboost`, `torch`, `joblib`), add them to `requirements.txt` and `pyproject.toml` (`uv add <package>`).

---

## 2. Run Locally

### Option A: Using `uv`
```bash
uv sync
uv run main.py
```

### Option B: Using `pip`
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

Verify that the health check responds at `http://localhost:8000/health`:
```bash
curl http://localhost:8000/health
# Expected response: {"health":"up"}
```

---

## 3. Deploy on Your Public VM

Make sure port `8000` (or the port you choose) is open in your VM's firewall (`sudo ufw allow 8000/tcp`).

### Option A: Run with Docker (Recommended – runs in background)
```bash
docker build -t ml-prediction-api .
docker run -d --name ml-api --restart unless-stopped -p 8000:8000 ml-prediction-api
```

### Option B: Run directly with `uv` / `uvicorn`
```bash
uv sync
nohup uv run uvicorn main:app --host 0.0.0.0 --port 8000 > server.log 2>&1 &
```

Once running, register your VM's base URL (e.g. `http://<your-vm-ip>:8000`) in the Competition Submission tab of Happy Go Lucky.
