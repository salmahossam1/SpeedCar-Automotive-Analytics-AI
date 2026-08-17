import streamlit as st
import plotly.express as px
from utils import setup_page,sidebar,load_data,chart_layout,CHART_COLORS
setup_page("Speed Car — Dashboard","📊"); sidebar()
df=load_data()
st.title("📊 Speed Car Dashboard")
st.caption("A focused view of the most important automotive performance insights.")

k=[("🚗","Cars",f"{len(df):,}"),("🏭","Manufacturers",f"{df['Manufacturer'].nunique():,}"),("⚡","Average Power",f"{df['Power (hp)'].mean():,.0f} hp"),("🔥","Max Top Speed",f"{df['Top speed (kph)'].max():,.0f} kph")]
for col,(i,l,v) in zip(st.columns(4),k):
    with col: st.markdown(f'<div class="kpi"><div>{i}</div><div class="kpi-value">{v}</div><div class="kpi-label">{l}</div></div>',unsafe_allow_html=True)

st.markdown("### 📈 Performance Overview")
a,b=st.columns(2)
with a:
    fig=px.scatter(df,x="Power (hp)",y="Top speed (kph)",color="Body Type",hover_data=["Manufacturer","Brand","Model Year"],title="Power vs Top Speed",color_discrete_sequence=CHART_COLORS)
    st.plotly_chart(chart_layout(fig,410),use_container_width=True)
with b:
    fig=px.scatter(df,x="Torque (Nm)",y="Power (hp)",color="Body Type",hover_data=["Manufacturer","Brand"],title="Torque vs Power",color_discrete_sequence=CHART_COLORS)
    st.plotly_chart(chart_layout(fig,410),use_container_width=True)

st.markdown("### 🏆 Top Insights")
a,b=st.columns(2)
with a:
    top=df.groupby("Brand_Manufacturer")["Top speed (kph)"].mean().nlargest(10).sort_values().reset_index()
    fig=px.bar(top,x="Top speed (kph)",y="Brand_Manufacturer",orientation="h",title="Top 10 Brands by Average Top Speed",color_discrete_sequence=["#22D3EE"])
    st.plotly_chart(chart_layout(fig,410,False),use_container_width=True)
with b:
    yearly=df.groupby("Model Year")["Power (hp)"].mean().reset_index()
    fig=px.line(yearly,x="Model Year",y="Power (hp)",markers=True,title="Average Power by Model Year",color_discrete_sequence=["#F472B6"])
    st.plotly_chart(chart_layout(fig,410,False),use_container_width=True)
