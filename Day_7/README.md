# Day 7 - Deploy ML Model as an API (Remote Internship Task)

This folder contains my Day 7 practical task submission for the remote internship.
It deploys the Logistic Regression model (our best-performing model from Day 4-6)
as a REST API using FastAPI.

## 📁 Project Structure

```
day7-ml-api/
├── model/
│   ├── logistic_regression_model.joblib   # trained model
│   ├── scaler.joblib                       # fitted StandardScaler
│   └── feature_order.joblib                # exact feature column order
├── api/
│   └── main.py                             # FastAPI app + /predict endpoint
├── students.csv                            # dataset (same as Day 3-6)
├── train_and_save_model.py                 # script that trains & saves the model
├── requirements.txt
├── POSTMAN_TESTING_GUIDE.md                # exact requests to test in Postman
└── README.md
```

## 🧠 What Model Is Being Served

**Logistic Regression** — the best-performing model across Day 4, 5, and 6
(100% accuracy, 100% precision/recall/F1, and 1.00 ROC-AUC on our test set).
See the Day 6 repository folder for the full comparison against a Decision
Tree that justified this choice.

The model predicts Pass/Fail using 4 features: Attendance, Assignment Score,
Midterm Score, and Final Score — the same features and the same weighted
Overall Score target (20% Assignment + 30% Midterm + 50% Final, Pass if ≥ 40)
used throughout this project since Day 4.

## ▶️ How to Install Dependencies

```bash
pip install -r requirements.txt
```

(Tip: it's good practice to do this inside a virtual environment —
`python -m venv venv` then activate it before installing.)

## ▶️ How to Run the API

The model is already trained and saved in `model/`, so you don't need to
retrain it. Just start the server:

```bash
cd api
uvicorn main:app --reload
```

The API will be running at: **http://127.0.0.1:8000**

You can also visit **http://127.0.0.1:8000/docs** for FastAPI's automatic
interactive documentation, where you can test the endpoint directly in
your browser without Postman.

(If you ever want to retrain the model yourself, run
`python train_and_save_model.py` from the project root — this regenerates
the files inside `model/`.)

## 🔌 Endpoint

### `POST /predict`

Predicts whether a student will Pass or Fail, given their attendance and scores.

**Request format:**

```json
{
    "attendance": 90,
    "assignment_score": 85,
    "midterm_score": 80,
    "final_score": 88
}
```

All four fields are required and must be numbers between 0 and 100.

**Response format (success):**

```json
{
    "prediction": "Pass",
    "confidence": 0.9918
}
```

- `prediction` — either `"Pass"` or `"Fail"`
- `confidence` — the model's confidence in that specific prediction (0 to 1)

**Response format (invalid input):**

If a field is missing, out of range (below 0 or above 100), or the wrong
type, the API returns a `422 Unprocessable Entity` status with details
about exactly what was wrong:

```json
{
    "detail": [
        {
            "type": "less_than_equal",
            "loc": ["body", "attendance"],
            "msg": "Input should be less than or equal to 100",
            "input": 150,
            "ctx": {"le": 100.0}
        }
    ]
}
```

See `POSTMAN_TESTING_GUIDE.md` for the exact requests used to test both
valid and invalid inputs, with their expected responses.

## 🛠️ Requirements
See `requirements.txt`. Key packages: fastapi, uvicorn, pydantic,
scikit-learn, pandas, numpy, joblib.

## 👤 Author
Abbas Raza
- GitHub: [AbbasRaza5055](https://github.com/AbbasRaza5055)

---
*Day 7 task — deploying a trained Scikit-learn model as a REST API with FastAPI,
including input validation and error handling.*
