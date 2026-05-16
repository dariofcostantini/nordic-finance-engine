# Nordic Loan Lifecycle Engine 🏦

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://nordic-finance-engine.streamlit.app)

A professional-grade financial engine designed to model, calculate, and visualize loan amortization schedules using European banking standards. 

## 🚀 Live Demo
**[Try the Interactive Dashboard Here](https://nordic-finance-engine.streamlit.app)**

## 📌 Features
- **Domain-Driven Design:** Clean separation of financial mathematics (`loan_math.py`), data models (`loan_models.py`), and the core schedule generator (`loan_schedule.py`).
- **Multiple Amortization Systems:**
  - **French System (Annuitetslån):** Constant total payment schedule.
  - **German System (Serielån):** Constant principal payment schedule.
  - **American System (Bullet):** Interest-only payments with full principal repayment at maturity.
- **High Precision Math:** Utilizes Python's `Decimal` module with strict `ROUND_HALF_UP` banking conventions to prevent floating-point calculation errors.
- **Premium Visualization:** Dynamic, fully responsive stacked bar charts and metric dashboards using Plotly Express and Streamlit.

## 🛠️ Technology Stack
- **Backend:** Python
- **Frontend/UI:** Streamlit
- **Data Manipulation:** Pandas
- **Visualization:** Plotly

## 🧠 Usage (Local)
To run this project locally:

```bash
pip install -r requirements.txt
python -m streamlit run app.py
```
