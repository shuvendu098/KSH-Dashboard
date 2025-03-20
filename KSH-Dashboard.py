import streamlit as st
import pandas as pd
import plotly.express as px
import warnings
warnings.filterwarnings('ignore')


@st.cache_data
def load_data_incoming(file=None):
    if file:
        df = pd.read_csv(file)
    else:
        df = pd.read_csv("incoming.csv")  # Default file
    df['Date'] = pd.to_datetime(df['Date'])
    return df

# Streamlit App Configuration
st.set_page_config(page_title="KSH Daily Dashboard", layout="wide", initial_sidebar_state="expanded",page_icon=":chart_with_upwards_trend:")

st.sidebar.image("ksh_265.png", use_container_width=True, output_format="PNG")
st.sidebar.markdown("<h2 style = 'text-align : center; padding-top : 0rem;' >Krushi Samrudhi Helpline</h2>", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.markdown("<h5 style = 'text-align : center; padding-top : 0rem;' >Upload Inbound Data</h5>", unsafe_allow_html=True)
uploaded_file = st.sidebar.file_uploader(f"Upload Data",type=["csv","tsv","xlsx"])


filtered_data = load_data_incoming(uploaded_file)

if filtered_data is None:
    st.warning("Please upload a valid file to proceed.")
else:   
        st.markdown("<h1 style='text-align: center;'>Inbound Report</h1>", unsafe_allow_html=True)
        st.markdown('<style>div.block-container{padding-top : 1.9rem;}</style>', unsafe_allow_html=True)

     # Input for Start Date and End Date
        col1, col2 = st.columns(2)
        start_date = col1.date_input("Start Date", min_value=filtered_data["Date"].min(), max_value=filtered_data["Date"].max(), value=filtered_data["Date"].min())
        end_date = col2.date_input("End Date", min_value=filtered_data["Date"].min(), max_value=filtered_data["Date"].max(), value=filtered_data["Date"].max())

    # Filter Data Based on Selected Date Range
        selected_data = filtered_data[(filtered_data["Date"] >= pd.Timestamp(start_date)) & (filtered_data["Date"] <= pd.Timestamp(end_date))]

    # Display Cards for Offered, Answered, Abandoned Calls
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Calls Offered", selected_data["Offered"].sum())
        col2.metric("Total Calls Answered", selected_data["Answered"].sum())
        col3.metric("Total Calls Abandoned", selected_data["Abandoned"].sum())

        st.markdown("---")

        col11, col12,col13 = st.columns(3)
        fig11 = px.bar(
         selected_data, 
         x="Date", 
         y="Offered", 
         title="Date-wise Calls: Offered",
        )
        col11.plotly_chart(fig11, use_container_width=True)
    
    
        fig12 = px.bar(
         selected_data, 
         x="Date", 
         y="Answered", 
         title="Date-wise Calls: Answered",
        )
        col12.plotly_chart(fig12, use_container_width=True)
    
        fig13 = px.bar(
            selected_data, 
            x="Date", 
            y="Abandoned", 
            title="Date-wise Calls: Abandoned",
        )
        col13.plotly_chart(fig13, use_container_width=True)

        col21, col22 = st.columns(2)

        offer_sum = selected_data["Offered"].sum()
        answer_sum = selected_data["Answered"].sum()
        abandoned_sum = selected_data["Abandoned"].sum()
        pie_data = pd.DataFrame({
            "Category" : ["Offered", "Answered", "Abandoned"],
            "Values" : [offer_sum, answer_sum, abandoned_sum]
        })
        fig21 = px.pie(pie_data, names="Category", values= "Values" , title= "Total Calls")
        col21.plotly_chart(fig21, use_container_width=True)


        # Pie Chart (Distribution of Agri, AH, Fishery, LCC AHT)
        agri_sum = selected_data["Agri_AHT"].sum()
        ah_sum = selected_data["AH_AHT"].sum()
        fishery_sum = selected_data["Fishery_AHT"].sum()
        lcc_sum = selected_data["LCC_AHT"].sum()
        
        pie_data = pd.DataFrame({
            "Category": ["Agri", "AH", "Fishery", "LCC"],
            "Value": [agri_sum, ah_sum, fishery_sum, lcc_sum]
        })
        
        fig22 = px.pie(pie_data, names="Category", values="Value", title="AHT Distribution: Agri, AH, Fishery & LCC")
        col22.plotly_chart(fig22, use_container_width=True)

        # 4 Line Charts with Scatter Plots
        col4, col5 = st.columns(2)

        fig3 = px.line(
            selected_data, x="Date", y="Agri_AHT", 
            title="Agri AHT Over Time", markers=True
        )
        col4.plotly_chart(fig3, use_container_width=True)

        fig4 = px.line(
            selected_data, x="Date", y="AH_AHT", 
            title="AH AHT Over Time", markers=True
        )
        col5.plotly_chart(fig4, use_container_width=True)

        col6, col7 = st.columns(2)

        fig5 = px.line(
            selected_data, x="Date", y="Fishery_AHT", 
            title="Fishery AHT Over Time", markers=True
        )
        col6.plotly_chart(fig5, use_container_width=True)

        fig6 = px.line(
            selected_data, x="Date", y="LCC_AHT", 
            title="LCC AHT Over Time", markers=True
        )
        col7.plotly_chart(fig6, use_container_width=True)
