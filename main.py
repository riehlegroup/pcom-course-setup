from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
import requests
import pandas as pd
import io
import uvicorn


app = FastAPI(title="ML Prediction API")


class EvaluationBody(BaseModel):
    testdata_download_endpoint: str
    prediction_upload_endpoint: str


def run_model(df: pd.DataFrame) -> pd.DataFrame:
    prediction_df = df.copy()
    # ==== EXAMPLE: ADD YOUR PREDICTIONS OF TRAINED MODEL HERE ====
    # Fill empty target columns of input dataset with predictions (the example just fills every empty column  with 0)
    for col in prediction_df.columns:
        if prediction_df[col].isna().all():
            prediction_df[col] = 0
    # =============================================================

    return prediction_df


def start_prediction(download_url: str, upload_url: str):
    try:
        result = requests.get(download_url, timeout=30)
        result.raise_for_status()

        # Read input CSV
        input_data = pd.read_csv(io.StringIO(result.text))

        # ADD YOUR PREDICTION MODEL HERE TO FILL PREDICTION DATA WITHOUT CHANGING THE ORDER OF ROWS IN CSV
        # ======== Example =========
        prediction_data = run_model(input_data)
        # ======== END Example =====

        assert input_data.shape == prediction_data.shape, "Shape mismatch between input and prediction data"
        output_buffer = io.StringIO()
        prediction_data.to_csv(output_buffer, header=True, index=False)
        output_buffer.seek(0)

        file = {"predictions": ("prediction.csv", output_buffer.getvalue(), "text/csv")}

        upload_res = requests.post(upload_url, files=file, timeout=30)
        upload_res.raise_for_status()
        print("Evaluation Result:", upload_res.json())

    except Exception as e:
        print("Error:", e)


@app.post("/predict", status_code=200)
async def prediction(payload: EvaluationBody, background_tasks: BackgroundTasks):
    # Start prediction in background
    background_tasks.add_task(
        start_prediction,
        payload.testdata_download_endpoint,
        payload.prediction_upload_endpoint,
    )
    return {"status": "prediction started"}


@app.get("/health", status_code=200)
async def health():
    return {"health": "up"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
