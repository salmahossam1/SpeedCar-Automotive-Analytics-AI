import streamlit as st
import pandas as pd
from utils import setup_page,sidebar,load_data
setup_page("Speed Car — Data Description","🧹"); sidebar()
df=load_data()

st.title("🧹 Data Description")
st.caption("Cleaning, feature engineering and the final handled dataset used by the project.")

steps=[
("1","Loaded the dataset","Started from the DriveArabia UAE car dataset: 7,647 records and 18 original columns."),
("2","Cleaned numeric fields","Removed text, units, symbols and AED formatting from numeric variables."),
("3","Converted ranges","For fields stored as ranges, the midpoint was used to obtain a numeric value."),
("4","Handled missing values","The target Power (hp) missing record was excluded from training. Feature missing values are handled by the preprocessing pipeline using imputation."),
("5","Created gearbox features","Extracted gear_count and derived gear_type from Gear box."),
("6","Created Brand_Manufacturer","Combined Manufacturer and Brand into one modeling feature."),
("7","Encoded categorical features","Categorical variables are encoded inside the trained preprocessing pipeline."),
("8","Prepared ML data","Power (hp) was defined as the target and the data was split 80/20 with random_state=42."),
]
for n,t,d in steps:
    st.markdown(f'<div class="card" style="margin-bottom:10px"><b style="color:#67e8f9">{n}. {t}</b><div class="small-muted" style="margin-top:6px">{d}</div></div>',unsafe_allow_html=True)

st.markdown("### 📦 Final Handled Dataset")
summary=pd.DataFrame({
    "Metric":["Rows","Columns","Target","Missing cells","Average Power (hp)","Average Top Speed (kph)"],
    "Value":[len(df),len(df.columns),"Power (hp)",int(df.isna().sum().sum()),f"{df['Power (hp)'].mean():.1f}",f"{df['Top speed (kph)'].mean():.1f}"]
})
st.dataframe(summary,use_container_width=True,hide_index=True)

st.markdown("#### 🔎 Data after handling")
# Show the modeling-relevant columns first so the user sees the handled numeric/feature-engineered data.
priority=[c for c in ["Approx Cost","Origin Country","Manufacturer","Brand","Model Year","Body Type","Weight","Power (hp)","Torque (Nm)","Fuel Econ (L/100km)","Fuel Econ (km/L)","Performance 0-100 kph (sec)","Top speed (kph)","gear_count","gear_type","Brand_Manufacturer"] if c in df.columns]
preview=df[priority].head(20).copy()
st.dataframe(preview,use_container_width=True,hide_index=True)

st.download_button("⬇️ Download Handled Dataset",data=df.to_csv(index=False).encode("utf-8"),file_name="DriveArabia_handled.csv",mime="text/csv",use_container_width=True)
