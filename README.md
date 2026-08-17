# 🏎️ SpeedCar — Automotive Performance & AI Analytics Dashboard

A high-performance, interactive multi-page **Streamlit** application designed for analyzing car specifications from the UAE/DriveArabia dataset and predicting vehicle Engine Power (**Power (hp)**) using Machine Learning algorithms like **Random Forest**.

---

## ✨ Live Demo

🔗 **Explore the Interactive App:** [SpeedCar Live Dashboard]([https://your-app-name.streamlit.app](https://speedcar-automotive-analytics-ai.streamlit.app/)) *(👈 ضع رابط استريمليت هنا)*

---

## 🌟 Key Highlights

* **🏎️ Futuristic Glassmorphism UI:** Built with glowing neon aesthetics, sleek dark-mode design, and a fully responsive layout.
* **📊 Comprehensive Performance Analytics:** In-depth visual analysis covering acceleration (0-100 kph), top speed, pricing trends, and weight-to-power ratios.
* **🧹 Smart Data Engineering:** Automated text cleaning, regex-based transmission & gear extraction, and robust missing-value handling.
* **🤖 AI Horsepower Predictor:** Real-time ML inference engine using a finely tuned **Random Forest Regressor**:
  * **$R^2$ Accuracy:** `99.88%`
  * **Mean Absolute Error (MAE):** `2.06 hp`
  * **Root Mean Squared Error (RMSE):** `5.53 hp`

---

## 📁 Repository Structure

```text
├── app.py                            # Main entry point (Landing & Hero Page)
├── utils.py                          # Data caching, custom UI elements & helpers
├── requirements.txt                  # Python package dependencies
├── README.md                         # Project documentation
├── car.jpg                           # Hero banner background image
├── DriveArabia_All_uae_updated.csv   # Raw automotive dataset
├── DriveArabia_handled.csv           # Preprocessed dataset
├── models/                           # Trained ML models (.joblib binaries)
└── pages/
    ├── 1_Dashboard.py                # Visual analytics & performance KPIs
    ├── 2_Data_Description.py         # Detailed data engineering pipeline
    └── 3_Best_Model_Prediction.py    # Live AI horsepower prediction page
