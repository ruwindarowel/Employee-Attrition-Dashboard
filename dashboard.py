import streamlit as st
import pandas as pd
import altair as alt
import numpy as np

# Set the theme to dark
st.set_page_config(page_title="Employee Attrition Dashboard", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
/* Style for individual metric boxes */
.metric-box {
    padding: 20px;
    border-radius: 8px;
    color: white;
    text-align: center;
    font-size: 16px;
    font-weight: bold;
}

.box1 { background-color: #b3d9ff;color: #000000; }
.box2 { background-color: #66b3ff;color: #000000; }
.box3 { background-color: #2eb8b8; color:#000000;}
.box4 { background-color: #71dada;color: #000000; }

.container {
    padding: 10px;  /* Reduced padding */
    border-radius: 0px;
    height: 160px; /* Adjust height to auto for flexibility */
    color: white; /* Text color */
    margin: 5px;  /* Reduced margin */
}
.donut-container {
    padding: 10px;  /* Reduced padding */
    border-radius: 0px;
    margin:10px;
}
.chart-container {
    padding: 10px;  /* Reduced padding */
    border-radius: 0px;
} 
.custom-sidebar-header {
        text-align: center;
        font-size: 24px; /* Adjust font size as needed */
        font-weight: bold;
        margin-bottom: 15px;
 }
 .selected-variable-box {
        background-color: #ff4b4b;
        color: #fff;
        padding: 10px;
        border-radius: 5px;
        text-align: center;
        font-weight: bold;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Load dataset from GitHub
data_url = "https://raw.githubusercontent.com/sithmipehara/EmployeeAttrition_Dashboard/refs/heads/main/train.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(data_url)
    df = df.iloc[:, 1:]  # Remove the first column (ID column)
    return df

# Load data
df = load_data()

# Header metrics
num_data_points = round((sum(df['Attrition']=='Left')/df.shape[0])*100,2)
num_categorical = df['Job Satisfaction'].mode()[0]
num_numerical = round(np.mean(df['Number of Promotions']))
response_variable = round(np.mean(df['Monthly Income']),2)

# Display the metrics
col1, col2, col3, col4 = st.columns(4)
col1.markdown(f"<div class='metric-box box1'>Attrition Rate<br><span style='font-size: 24px;'>{num_data_points}</span></div>", unsafe_allow_html=True)
col2.markdown(f"<div class='metric-box box2'>Average Job satisfaction<br><span style='font-size: 24px;'>{num_categorical}</span></div>", unsafe_allow_html=True)
col3.markdown(f"<div class='metric-box box3'>Average No. of Promotions<br><span style='font-size: 24px;'>{num_numerical}</span></div>", unsafe_allow_html=True)
col4.markdown(f"<div class='metric-box box4'>Average Monthly Income<br><span style='font-size: 24px;'>{response_variable}</span></div>", unsafe_allow_html=True)

st.write(" ")
st.write(" ")
st.write(" ")
st.write(" ")

st.sidebar.markdown("<div class='custom-sidebar-header'>Input Parameters</div>", unsafe_allow_html=True)
st.write(" ")
st.write(" ")
st.sidebar.header("Bar Chart & Stack Bar Chart 1 Parameters")
categorical_columns = df.select_dtypes(include='object').columns
cat_var = st.sidebar.selectbox("Select Data", options=categorical_columns, index=0)

st.sidebar.header("Histogram & Stack Bar Chart 2 Parameters")
numerical_columns = df.select_dtypes(include='number').columns
num_var = st.sidebar.selectbox("Select Data", options=numerical_columns, index=0)

st.sidebar.markdown(f"<div class='selected-variable-box'>Selected Categorical Variable:<br> {cat_var}</div>", unsafe_allow_html=True)
st.sidebar.markdown(f"<div class='selected-variable-box'>Selected Numerical variable: <br>{num_var}</div>", unsafe_allow_html=True)

st.title("Attrition Statistics")
# Create columns with different widths
col1, col2, col3 = st.columns(3)  

# Second column: Three containers for donut chart and response details
with col1:
    # Container for Donut Chart
    st.markdown("<div class='donut-container'><h5 style='text-align: center;'>Response Variable Distribution</h5>", unsafe_allow_html=True)
    
    # Calculate response variable distribution
    response_data = df["Attrition"].value_counts().reset_index()
    response_data.columns = ["Attrition", "Count"]
    response_data['Percentage'] = (response_data['Count'] / response_data['Count'].sum()) * 100

    # Donut chart base
    donut_chart = alt.Chart(response_data).mark_arc(innerRadius=60).encode(
        theta=alt.Theta(field="Count", type="quantitative"),
        color=alt.Color('Attrition:N', scale=alt.Scale(domain=['Left', 'Stayed'], range=['#FF6347', '#4682B4']),
                    legend=alt.Legend(orient="bottom", direction="horizontal")),
        tooltip=["Attrition", "Count"]
    ).properties(width=30, height=300)

    # Center text overlay (total count)
    total_count = response_data["Count"].sum()
    center_text = alt.Chart(pd.DataFrame({'text': [total_count]})).mark_text(
        text=str(total_count),
        size=28,
        color='white'
    ).encode(
        text='text:N'
    )
    
    # Combine the donut chart with center text and segment labels
    response_donut_chart = donut_chart + center_text
    
    st.altair_chart(response_donut_chart, theme=None, use_container_width=True)
    
    # Add labels for Left and Stayed categories
    response_data = df["Attrition"].value_counts().reset_index()
    response_data.columns = ["Attrition", "Count"]
    response_data['Percentage'] = (response_data['Count'] / response_data['Count'].sum()) * 100

    # Extracting details for each category
    left_count = response_data.loc[response_data['Attrition'] == 'Left', 'Count'].values[0]
    left_percentage = response_data.loc[response_data['Attrition'] == 'Left', 'Percentage'].values[0]
    
    stayed_count = response_data.loc[response_data['Attrition'] == 'Stayed', 'Count'].values[0]
    stayed_percentage = response_data.loc[response_data['Attrition'] == 'Stayed', 'Percentage'].values[0]

    # Displaying labels
    st.markdown(f"<h5 style='text-align: left;font-size: 12px;margin-top: -220px;'>Stayed<br>{stayed_count}<br>({stayed_percentage:.1f}%)</h5>", unsafe_allow_html=True)
    st.markdown(f"<h5 style='text-align: right;font-size: 12px;margin-top: -180px;'>Left<br>{left_count}<br>({left_percentage:.1f}%)</h5>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
    
# Third column of charts in one container
with col2:
    st.markdown("<div class='chart-container'><h5 style='text-align: center;'>Response vs Numerical Variables</h5>", unsafe_allow_html=True)
    
    # Calculate necessary quantiles and IQR for numerical variable
    q1 = df[num_var].quantile(0.25)
    q3 = df[num_var].quantile(0.75)
    iqr = q3 - q1

    # Filter outliers
    df_filtered = df[(df[num_var] >= (q1 - 1.5 * iqr)) & (df[num_var] <= (q3 + 1.5 * iqr))]

    # Create Box Plot with white whiskers
    box_plot = alt.Chart(df_filtered).mark_boxplot(size=40, color='white').encode(
        x=alt.X("Attrition:N", title="Attrition"),
        y=alt.Y(num_var, title=num_var),
        color=alt.Color("Attrition", scale=alt.Scale(domain=['Left', 'Stayed'], range=['#FF6347', '#4682B4']),
                    legend=alt.Legend(orient="bottom", direction="horizontal"))
    ).properties(width=300, height=300)

    st.altair_chart(box_plot, theme=None, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
# Fourth column of charts in one container
with col3:
    st.markdown("<div class='chart-container'><h5 style='text-align: center;'>Response vs Categorical Variables</h5>", unsafe_allow_html=True)

    # Response vs Categorical Variable (Stacked Bar Chart) with custom colors
    stacked_cat_chart = alt.Chart(df).mark_bar().encode(
        y=alt.Y(cat_var, title=cat_var, sort='-x'),
        x=alt.X('count()', title='Count'),
        color=alt.Color('Attrition', scale=alt.Scale(domain=['Left', 'Stayed'], range=['#FF6347', '#4682B4']),
                    legend=alt.Legend(orient="bottom", direction="horizontal")),
        tooltip=[cat_var, 'Attrition', 'count()']
    ).properties(width=300, height=300)

    st.altair_chart(stacked_cat_chart, theme=None, use_container_width=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
# Additional Row for New Graphs
st.title("Job Role Statistics")

col4, col5, col6 = st.columns(3) 

with col4:
    st.markdown("<div class='chart-container'><h5 style='text-align: center;'>Promotion Rate by Job Role</h5>", unsafe_allow_html=True)
    
    # Calculate necessary quantiles and IQR for numerical variable
    q1 = df['Number of Promotions'].quantile(0.25)
    q3 = df['Number of Promotions'].quantile(0.75)
    iqr = q3 - q1

    # Filter outliers
    df_filtered = df[(df['Number of Promotions'] >= (q1 - 1.5 * iqr)) & (df['Number of Promotions'] <= (q3 + 1.5 * iqr))]

    # Create Box Plot with white whiskers
    box_plot = alt.Chart(df_filtered).mark_boxplot(size=40, color='white').encode(
        x=alt.X("Job Level:N", title="Job Level"),
        y=alt.Y('Number of Promotions', title='Number of Promotions'),
        color=alt.Color("Job Level", scale=alt.Scale(domain=['Mid', 'Senior', 'Entry'], range=['#FF6347','#FFFFFF', '#4682B4']),
                    legend=alt.Legend(orient="bottom", direction="horizontal"))
    ).properties(width=300, height=300)

    st.altair_chart(box_plot, theme=None, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
with col5:
    st.markdown("<div class='chart-container'><h5 style='text-align: center;'>Monthly Income by Job Role</h5>", unsafe_allow_html=True)
    
    # Calculate necessary quantiles and IQR for numerical variable
    q1 = df['Monthly Income'].quantile(0.25)
    q3 = df['Monthly Income'].quantile(0.75)
    iqr = q3 - q1

    # Filter outliers
    df_filtered = df[(df['Monthly Income'] >= (q1 - 1.5 * iqr)) & (df['Monthly Income'] <= (q3 + 1.5 * iqr))]

    # Create Box Plot with white whiskers
    box_plot = alt.Chart(df_filtered).mark_boxplot(size=40, color='white').encode(
        x=alt.X("Job Level:N", title="Job Level"),
        y=alt.Y('Monthly Income', title='Monthly Income'),
        color=alt.Color("Job Level", scale=alt.Scale(domain=['Mid', 'Senior', 'Entry'], range=['#FF6347','#FFFFFF', '#4682B4']),
                    legend=alt.Legend(orient="bottom", direction="horizontal"))
    ).properties(width=300, height=300)

    st.altair_chart(box_plot, theme=None, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
with col6:
    st.markdown("<div class='chart-container'><h5 style='text-align: center;'>Job Satisfaction by Job Role</h5>", unsafe_allow_html=True)

    # Response vs Categorical Variable (Stacked Bar Chart) with custom colors
    stacked_cat_chart = alt.Chart(df).mark_bar().encode(
        y=alt.Y('Job Satisfaction', title='Job Satisfaction', sort='-x'),
        x=alt.X('count()', title='Count'),
        color=alt.Color("Job Level", scale=alt.Scale(domain=['Mid', 'Senior', 'Entry'], range=['#FF6347','#FFFFFF', '#4682B4']),
                    legend=alt.Legend(orient="bottom", direction="horizontal")),
        tooltip=["Job Level", 'Job Satisfaction', 'count()']
    ).properties(width=300, height=300)

    st.altair_chart(stacked_cat_chart, theme=None, use_container_width=True)
    
    st.markdown("</div>", unsafe_allow_html=True)