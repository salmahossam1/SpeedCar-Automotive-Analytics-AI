import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

from utils import (
    setup_page,
    sidebar,
    load_data,
    load_joblib,
    chart_layout
)


# ============================================================
# PAGE SETUP
# ============================================================

setup_page(
    "Speed Car — Best Model & Prediction",
    "🤖"
)

sidebar()

df = load_data()

model = load_joblib("best_model.joblib")

fi = load_joblib("feature_importance.joblib")


# ============================================================
# MODEL RESULTS
# ============================================================

results = pd.DataFrame([
    {
        "Model": "Extra Trees",
        "Train Accuracy": 98.981923,
        "Test Accuracy": 97.009265,
        "MAE": 9.870696,
        "RMSE": 27.211889
    },
    {
        "Model": "XGBoost",
        "Train Accuracy": 98.488109,
        "Test Accuracy": 96.438114,
        "MAE": 16.309478,
        "RMSE": 29.696805
    },
    {
        "Model": "Gradient Boosting",
        "Train Accuracy": 99.017475,
        "Test Accuracy": 95.953017,
        "MAE": 13.612368,
        "RMSE": 31.654496
    },
    {
        "Model": "Random Forest",
        "Train Accuracy": 97.619877,
        "Test Accuracy": 92.584355,
        "MAE": 18.658659,
        "RMSE": 42.849344
    }
])


# ============================================================
# BEST MODEL
# ============================================================

best = results.loc[
    results["Test Accuracy"].idxmax()
]


# ============================================================
# TITLE
# ============================================================

st.title("🤖 Best Model & Prediction")

st.caption(
    "Model validation and an interactive test for engine power prediction."
)


# ============================================================
# BEST MODEL - STREAMLIT ONLY
# ============================================================

st.subheader("🏆 Selected Best Model")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        "🤖 Best Model",
        best["Model"]
    )

with c2:
    st.metric(
        "🎯 Test Accuracy",
        f"{best['Test Accuracy']:.2f}%"
    )

with c3:
    st.metric(
        "📏 MAE",
        f"{best['MAE']:.2f} hp"
    )

st.info(
    f"🏆 {best['Model']} achieved the highest "
    f"Test Accuracy of {best['Test Accuracy']:.2f}% "
    f"among the four evaluated models."
)

st.write("")


# ============================================================
# TABS
# ============================================================

info_tab, perf_tab, model_tab, pred_tab = st.tabs(
    [
        "🚗 Car Info",
        "⚙️ Performance",
        "🏆 Model Comparison",
        "🔮 Prediction"
    ]
)


# ============================================================
# CAR INFORMATION
# ============================================================

with info_tab:

    st.subheader("🚗 Car Information")

    st.write(
        "Choose a starting car. Its values are loaded "
        "from the handled dataset and can be edited "
        "in the Prediction tab."
    )

    selected = st.selectbox(
        "Starting Car",
        df.index.tolist(),
        format_func=lambda i:
        f"{df.loc[i, 'Manufacturer']} "
        f"{df.loc[i, 'Brand']} | "
        f"{df.loc[i, 'Model Year']}"
    )

    st.session_state["selected_car"] = selected

    row = df.loc[[selected]]

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Manufacturer",
        str(row.iloc[0]["Manufacturer"])
    )

    c2.metric(
        "Brand",
        str(row.iloc[0]["Brand"])
    )

    c3.metric(
        "Body Type",
        str(row.iloc[0]["Body Type"])
    )


# ============================================================
# PERFORMANCE
# ============================================================

with perf_tab:

    st.subheader("⚙️ Performance")

    selected = st.session_state.get(
        "selected_car",
        df.index[0]
    )

    row = df.loc[[selected]]

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Power",
        f"{row.iloc[0]['Power (hp)']:.0f} hp"
    )

    c2.metric(
        "Torque",
        f"{row.iloc[0]['Torque (Nm)']:.0f} Nm"
    )

    c3.metric(
        "Top Speed",
        f"{row.iloc[0]['Top speed (kph)']:.0f} kph"
    )

    c4.metric(
        "0–100",
        f"{row.iloc[0]['Performance 0-100 kph (sec)']:.1f} sec"
    )


# ============================================================
# MODEL COMPARISON
# ============================================================

with model_tab:

    st.subheader("🏆 Four-Model Comparison")

    st.write(
        "Performance comparison of the four trained "
        "regression models."
    )

    display = results.copy()

    display["Train Accuracy"] = display[
        "Train Accuracy"
    ].map(
        lambda x: f"{x:.2f}%"
    )

    display["Test Accuracy"] = display[
        "Test Accuracy"
    ].map(
        lambda x: f"{x:.2f}%"
    )

    display["MAE"] = display[
        "MAE"
    ].map(
        lambda x: f"{x:.2f} hp"
    )

    display["RMSE"] = display[
        "RMSE"
    ].map(
        lambda x: f"{x:.2f} hp"
    )

    st.dataframe(
        display,
        use_container_width=True,
        hide_index=True
    )

    st.subheader("📊 Test Accuracy")

    fig = px.bar(
        results,
        x="Model",
        y="Test Accuracy",
        text_auto=".2f",
        title="Test Accuracy — Four Models",
        color="Test Accuracy",
        color_continuous_scale="Blues"
    )

    fig.update_layout(
        xaxis_title="Model",
        yaxis_title="Test Accuracy (%)",
        showlegend=False
    )

    st.plotly_chart(
        chart_layout(
            fig,
            360,
            False
        ),
        use_container_width=True
    )

    st.success(
        f"🏆 Winner: {best['Model']} — "
        f"{best['Test Accuracy']:.2f}% Test Accuracy"
    )


# ============================================================
# PREDICTION
# ============================================================

with pred_tab:

    st.subheader("🔮 Interactive Power Prediction")

    if model is None:

        st.error(
            "best_model.joblib is missing."
        )

        st.stop()

    selected = st.session_state.get(
        "selected_car",
        df.index[0]
    )

    row = df.loc[[selected]].copy()

    edited = row.copy()

    st.info(
        "Edit the car information below and press "
        "PREDICT POWER."
    )


    # ========================================================
    # CATEGORICAL INPUTS
    # ========================================================

    left, right = st.columns(2)

    categorical = [
        ("Manufacturer", left),
        ("Brand", left),
        ("Origin Country", left),
        ("Body Type", left),
        ("Additional Type", right),
        ("gear_type", right)
    ]

    for col, container in categorical:

        if col not in df.columns:
            continue

        values = sorted(
            df[col]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        current = str(
            row.iloc[0][col]
        )

        if current not in values:
            values = [current] + values

        with container:

            new_value = st.selectbox(
                col,
                values,
                index=values.index(current),
                key=f"prediction_{col}"
            )

        edited.at[
            selected,
            col
        ] = new_value


    # ========================================================
    # NUMERIC INPUTS
    # ========================================================

    st.subheader("⚙️ Engine & Performance")

    left, right = st.columns(2)

    numeric = [
        (
            "Model Year",
            left,
            1900.0,
            2035.0,
            1.0
        ),
        (
            "Approx Cost",
            left,
            0.0,
            None,
            1000.0
        ),
        (
            "Weight",
            left,
            0.0,
            None,
            10.0
        ),
        (
            "gear_count",
            left,
            0.0,
            20.0,
            1.0
        ),
        (
            "Torque (Nm)",
            right,
            0.0,
            None,
            1.0
        ),
        (
            "Fuel Econ (L/100km)",
            right,
            0.0,
            None,
            0.1
        ),
        (
            "Fuel Econ (km/L)",
            right,
            0.0,
            None,
            0.1
        ),
        (
            "Performance 0-100 kph (sec)",
            right,
            0.0,
            None,
            0.1
        ),
        (
            "Top speed (kph)",
            right,
            0.0,
            None,
            1.0
        )
    ]

    for col, container, minimum, maximum, step in numeric:

        if col not in df.columns:
            continue

        value = pd.to_numeric(
            row.iloc[0][col],
            errors="coerce"
        )

        if pd.isna(value):
            value = 0.0

        value = float(value)

        kwargs = {
            "min_value": minimum,
            "value": value,
            "step": step,
            "format": "%.2f"
        }

        if maximum is not None:
            kwargs["max_value"] = maximum

        with container:

            new_value = st.number_input(
                col,
                **kwargs
            )

        edited.at[
            selected,
            col
        ] = new_value


    st.write("")


    # ========================================================
    # PREDICT
    # ========================================================

    if st.button(
        "🏎️ PREDICT POWER",
        type="primary",
        use_container_width=True
    ):

        try:

            prediction = float(
                model.predict(edited)[0]
            )

            actual = pd.to_numeric(
                row["Power (hp)"].iloc[0],
                errors="coerce"
            )


            # ------------------------------------------------
            # PREDICTION KPIs
            # ------------------------------------------------

            st.subheader("📊 Prediction Result")

            c1, c2, c3 = st.columns(3)

            c1.metric(
                "⚡ Predicted Power",
                f"{prediction:,.1f} hp"
            )

            c2.metric(
                "📌 Actual Power",
                f"{actual:,.1f} hp"
                if np.isfinite(actual)
                else "N/A"
            )

            if np.isfinite(actual):

                difference = prediction - actual

                c3.metric(
                    "📏 Difference",
                    f"{difference:+,.1f} hp"
                )

            else:

                c3.metric(
                    "📏 Difference",
                    "N/A"
                )


            # ------------------------------------------------
            # RESULT
            # ------------------------------------------------

            st.success(
                f"🔮 Predicted Engine Power: "
                f"{prediction:,.1f} HP"
            )

            st.caption(
                f"Model used: {best['Model']}"
            )


            # ------------------------------------------------
            # ACTUAL VS PREDICTED
            # ------------------------------------------------

            if np.isfinite(actual):

                comparison = pd.DataFrame(
                    {
                        "Type": [
                            "Actual",
                            "Predicted"
                        ],
                        "Power (hp)": [
                            actual,
                            prediction
                        ]
                    }
                )

                fig = px.bar(
                    comparison,
                    x="Type",
                    y="Power (hp)",
                    text_auto=".1f",
                    title="Actual vs Predicted Power",
                    color="Type",
                    color_discrete_sequence=[
                        "#38BDF8",
                        "#F472B6"
                    ]
                )

                st.plotly_chart(
                    chart_layout(
                        fig,
                        360,
                        False
                    ),
                    use_container_width=True
                )


        except Exception as e:

            st.error(
                f"Prediction failed: {e}"
            )


# ============================================================
# FEATURE IMPORTANCE
# ============================================================

st.divider()

st.subheader(
    "🔎 Top Features Driving Power"
)

if fi is not None:

    top = (
        fi.head(8)
        .copy()
        .sort_values("Importance")
    )

    top["Feature"] = top[
        "Feature"
    ].str.replace(
        r"^(num__|cat__)",
        "",
        regex=True
    )

    fig = px.bar(
        top,
        x="Importance",
        y="Feature",
        orientation="h",
        title="Top 8 Feature Importances",
        color="Importance",
        color_continuous_scale="Blues"
    )

    st.plotly_chart(
        chart_layout(
            fig,
            390,
            False
        ),
        use_container_width=True
    )