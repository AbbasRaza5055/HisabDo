# Postman Testing Guide

This file contains the exact requests to test in Postman, and what response
you should get back for each one. Take a screenshot of each request/response
pair and include them in your submission.

**Before testing:** make sure the API is running first (see README.md for
how to start it). It should be running at `http://127.0.0.1:8000`.

---

## Test 1: Root endpoint (sanity check)

- **Method:** GET
- **URL:** `http://127.0.0.1:8000/`

**Expected response (Status 200):**
```json
{
    "message": "Student Performance Prediction API is running.",
    "docs": "Visit /docs for interactive API documentation.",
    "endpoint": "POST /predict"
}
```

---

## Test 2: Valid input — strong student (expect "Pass")

- **Method:** POST
- **URL:** `http://127.0.0.1:8000/predict`
- **Headers:** `Content-Type: application/json`
- **Body (raw, JSON):**
```json
{
    "attendance": 90,
    "assignment_score": 85,
    "midterm_score": 80,
    "final_score": 88
}
```

**Expected response (Status 200):**
```json
{
    "prediction": "Pass",
    "confidence": 0.9918
}
```

---

## Test 3: Valid input — weak student (expect "Fail")

- **Method:** POST
- **URL:** `http://127.0.0.1:8000/predict`
- **Body (raw, JSON):**
```json
{
    "attendance": 55,
    "assignment_score": 30,
    "midterm_score": 25,
    "final_score": 20
}
```

**Expected response (Status 200):**
```json
{
    "prediction": "Fail",
    "confidence": 0.7344
}
```

---

## Test 4: Invalid input — attendance over 100 (should be rejected)

- **Method:** POST
- **URL:** `http://127.0.0.1:8000/predict`
- **Body (raw, JSON):**
```json
{
    "attendance": 150,
    "assignment_score": 85,
    "midterm_score": 80,
    "final_score": 88
}
```

**Expected response (Status 422 Unprocessable Entity):**
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

---

## Test 5: Invalid input — missing field (should be rejected)

- **Method:** POST
- **URL:** `http://127.0.0.1:8000/predict`
- **Body (raw, JSON):** (notice `final_score` is missing)
```json
{
    "attendance": 90,
    "assignment_score": 85,
    "midterm_score": 80
}
```

**Expected response (Status 422 Unprocessable Entity):**
```json
{
    "detail": [
        {
            "type": "missing",
            "loc": ["body", "final_score"],
            "msg": "Field required",
            "input": {"attendance": 90, "assignment_score": 85, "midterm_score": 80}
        }
    ]
}
```

---

## Test 6: Invalid input — wrong data type (should be rejected)

- **Method:** POST
- **URL:** `http://127.0.0.1:8000/predict`
- **Body (raw, JSON):** (notice `attendance` is a word, not a number)
```json
{
    "attendance": "high",
    "assignment_score": 85,
    "midterm_score": 80,
    "final_score": 88
}
```

**Expected response (Status 422 Unprocessable Entity):**
```json
{
    "detail": [
        {
            "type": "float_parsing",
            "loc": ["body", "attendance"],
            "msg": "Input should be a valid number, unable to parse string as a number",
            "input": "high"
        }
    ]
}
```

---

## Test 7: Invalid input — negative number (should be rejected)

- **Method:** POST
- **URL:** `http://127.0.0.1:8000/predict`
- **Body (raw, JSON):**
```json
{
    "attendance": -5,
    "assignment_score": 85,
    "midterm_score": 80,
    "final_score": 88
}
```

**Expected response (Status 422 Unprocessable Entity):**
```json
{
    "detail": [
        {
            "type": "greater_than_equal",
            "loc": ["body", "attendance"],
            "msg": "Input should be greater than or equal to 0",
            "input": -5,
            "ctx": {"ge": 0.0}
        }
    ]
}
```

---

## What to screenshot

For your submission, take a screenshot of Postman for each test showing:
- The request (method, URL, and body)
- The response (status code and JSON body)

At minimum, include Tests 2, 3, and one of the invalid-input tests (4, 5, 6, or 7)
so your screenshots show both a successful prediction AND proper error handling.

## Note on exact numbers

The confidence values above (0.9918, 0.7344) were verified against the actual
trained model included in this repository. As long as you're using the
`model/` folder from this repo without retraining, your results should match
exactly.
