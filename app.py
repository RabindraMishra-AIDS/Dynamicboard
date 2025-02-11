import pandas as pd
import plotly.express as px 
import streamlit as st 
import emoji

st.set_page_config(page_title="Crop Dashboard",page_icon=":bar_chart:",layout="wide" )
df=pd.read_csv("static/yield.csv")


if "page" not in st.session_state:
    st.session_state["page"] = "dashboard"  # Default page

if st.sidebar.button("🏠 Home"):
    st.session_state["page"] = "home"
    st.rerun()

st.sidebar.header("Please Apply Filters Here")

country = st.sidebar.multiselect(
    "Select the  Country:",
    options=df["Country"].unique()
)

item = st.sidebar.multiselect(
    "Select Crop:",
    options=df["Item"].unique(),
    default=df["Item"].unique()
)

year = st.sidebar.multiselect(
    "Select the year:",
    options=df["Year"].unique()
)
df_selection = df.query(
    "Country==@country & Item==@item & Year==@year"
)
st.image("static/dashimg.png", width=120)


# Use st.markdown with inline CSS to position image and text in the same line
st.markdown(
    """
    <h1 style='text-align: center;'> 
        Experience Dynamic Dashboard!!
    </h1>
    """, 
    unsafe_allow_html=True
)



# Centering the dataframe using HTML and CSS in a div
st.markdown(
    """
    <style>
        .centered-dataframe {
            display: flex;
            justify-content: center;
            align-items: center;
        }
    </style>
    """, 
    unsafe_allow_html=True
)

st.markdown(
    "<div class='centered-dataframe'>{}</div>".format(df_selection.head(12).sort_values(by="Hectogram_per_Hectare", ascending=False)
.to_html(classes='dataframe', header="true", index=False)),
    unsafe_allow_html=True
)

# Replace missing values in the 'Hectogram_per_Hectare' column with 0
df_selection = df_selection.copy()
df_selection["Hectogram_per_Hectare"].fillna(0, inplace=True)

# Top KPI's
average_yield=0
average_rain = 0
total_yield=int(df_selection["Hectogram_per_Hectare"].sum())
if df_selection["Hectogram_per_Hectare"].sum()!=0:
    average_yield=int(df_selection["Hectogram_per_Hectare"].mean())
if df_selection["Rainfall"].sum()!=0:
    average_rain=int(df_selection["Rainfall"].mean())



left_column,middle_column,right_column=st.columns(3)

with left_column:
    st.subheader("Total Yield[Kiloton]:")
    st.subheader(f"{total_yield/1000:,}")
with middle_column:
    st.subheader("Average Yield[ton]:")
    st.subheader(f"{average_yield:,}")
with right_column:
    st.subheader("Average Rainfall[mm]:")
    st.subheader(f"{average_rain:,}")

st.markdown("---")
fig = px.pie(df_selection, values="Hectogram_per_Hectare", names="Item", title="<b> Crop yield by Total</b>")
fig.update_layout(title_x=0.3) 
fig1 = px.scatter_3d(
    df_selection, 
    x="Item", 
    y="Hectogram_per_Hectare", 
    z="Pesticide",
    color="Item",  # Colors data points by Item
    title="<b>3D Scatter Plot: Yield vs Pesticide</b>",
)

# Create two columns
col1, col2 = st.columns([0.5, 0.5])  # 60% for Pie Chart, 40% for Scatter Plot

with col2:
    st.plotly_chart(fig, use_container_width=True)

with col1:
    st.plotly_chart(fig1, use_container_width=True)

st.markdown("---")
fig2 = px.box(df_selection, x="Item", y="Hectogram_per_Hectare",color="Item", title="<b> Box plot: Crop by Yield </b>")
fig2.update_layout(title_x=0.45) 
st.plotly_chart(fig2, use_container_width=True)
st.markdown("---")
fig3 = px.line_3d(df_selection, x="Country", y="Item", z="Hectogram_per_Hectare", color="Country",title="<b> 3D Line: Country by Crop & Yield </b>") 
fig3.update_layout(title_x=0.45,width=1000,   # Set width (adjust as needed)
    height=700 )
st.plotly_chart(fig3, use_container_width=True) 
