# Ticket Email Classification ML Project

## Overview

This project automates the classification of support ticket emails using machine learning. The main goal is to automatically label incoming tickets (emails) into categories such as team, priority, type, action, and estimate the time to resolve (TTR). This helps support teams respond faster and more accurately.

---

## Problem Statement

Manually sorting and labeling support tickets is slow and error-prone. This project uses machine learning to automatically classify tickets based on their content, making customer support more efficient.

---

## Features

- **Data Preprocessing:** Cleans and prepares raw ticket data for modeling.
- **Text Vectorization:** Uses TF-IDF to convert ticket text into features.
- **Multiple Classifiers:** 
  - Team (queue) classifier
  - Priority classifier
  - Type classifier
  - Action classifier
- **Regression Model:** Predicts TTR (Time To Resolve) in hours.
- **Reusable Pipeline:** Includes a function to predict all labels for new tickets.
- **Test Cases:** Demonstrates model predictions on real-world ticket examples.

---

## Project Structure

```
notebooks/
    models.ipynb         # Main notebook with all ML code and experiments
    data.ipynb           # Data exploration and cleaning
data/
    raw/                 # Raw datasets
    processed/           # Cleaned datasets
src/
    data/                # Data generation and validation scripts
    preprocessing/       # Data preparation scripts
    models/              # (Optional) Model scripts
    utils/               # (Optional) Utility functions
```

---

## How to Run

1. **Clone the repository:**
   ```
   git clone https://github.com/srinath2934/ticket-ml-project.git
   cd ticket-ml-project
   ```

2. **Install requirements:**
   ```
   pip install -r requirements.txt
   ```

3. **Open and run the main notebook:**
   - Go to `notebooks/models.ipynb`
   - Run all cells to train models and see predictions

---

## Example: Model Pipeline

The main notebook (`models.ipynb`) demonstrates:
- Loading and cleaning data
- Vectorizing ticket text
- Training classifiers for each label (team, priority, type, action)
- Training a regression model for TTR
- Predicting all labels for new tickets using a single function

---

## Results

- Achieved high accuracy in classifying ticket emails into multiple categories.
- Automated ticket labeling for faster and more consistent support.
- Example output for a new ticket:
  ```
  {
    "team": "Payments",
    "priority": "High",
    "type": "Incident",
    "action": "Investigate",
    "ttr_hours": 3.5
  }
  ```

---

## Technologies Used

- Python
- Pandas, NumPy
- Scikit-learn
- Jupyter Notebook

---

## Future Work

- Improve model accuracy with more real-world data
- Deploy as a web service for real-time ticket classification
- Add more advanced NLP models (BERT, etc.)

---

## About

**This project is part of my portfolio for internship applications. I focused on solving the ticket classification problem using machine learning, and the code is ready for further development as more data becomes available.**

---

**GitHub Repository:**  
[https://github.com/srinath2934/ticket-ml-project](https://github.com/srinath2934/ticket-ml-project)
