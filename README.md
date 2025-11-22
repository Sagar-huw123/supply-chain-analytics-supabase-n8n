📦 Supply Chain Analytics Dashboard
Cloud-Native ETL + Analytics using n8n → Supabase (PostgreSQL) → Streamlit

This project is a fully automated, cloud-based supply chain analytics system built using:

n8n for workflow automation

Supabase PostgreSQL as the cloud data warehouse

Google Colab for ETL and data modelling

Streamlit for dashboarding

Plotly for interactive visualizations

🚀 Live Streamlit App

🔗 https://supply-chain-analytics-supabase-n8n-bxdk8w8lhw65c7wt3aitpy.streamlit.app/

🧠 Project Architecture
n8n (workflow automation)
        ↓
Supabase (PostgreSQL Data Warehouse)
        ↓
Google Colab (ETL, Cleaning, Modelling)
        ↓
GitHub (Version Control)
        ↓
Streamlit Cloud (Live Analytics Dashboard)

🎯 Key Features
1️⃣ Automated ETL Pipeline (n8n → Supabase)

Automatically extracts incoming order-level data

Cleans, formats, and loads it into Supabase tables

Supports incremental updates

2️⃣ Real-time Analytics Dashboard

Built on Streamlit with direct PostgreSQL queries.

Includes:

🔹 KPIs

Total Orders

Total Ordered Quantity

Fill Rate (In Full %)

OTIF % (On Time In Full)

Revenue (INR)

🔹 Visualizations

Line charts for Order Quantity & OTIF% over time

Treemap: Customer Segmentation (Revenue vs OTIF)

Bar chart: OTIF by City

Bar chart: OTIF by Product Category

Downloadable filtered dataset

🔹 Filters

Customer City

Product Category

Date Range

🗄️ Database Schema (Supabase)
Fact Tables

fact_order_line

fact_aggregate

Dimension Tables

dim_customers

dim_products

dim_targets_orders

📁 Repository Structure
supply-chain-analytics-supabase-n8n/
│── app.py
│── requirements.txt
│── SUPPLY_CHAIN_ANALYTICS_USING_SUPABASE_AND_N8N.ipynb
│── README.md

🔌 Streamlit → Supabase Connection
.streamlit/secrets.toml

(Stored in Streamlit Cloud, NOT in GitHub)

[db]
host = "YOUR_SUPABASE_HOST"
database = "postgres"
user = "YOUR_DB_USER"
password = "YOUR_DB_PASSWORD"
port = "5432"


Accessed in code via:

st.secrets["db"]["host"]

🛠️ Run the Project Locally
1️⃣ Clone the repo
git clone https://github.com/Sagar-huw123/supply-chain-analytics-supabase-n8n.git
cd supply-chain-analytics-supabase-n8n

2️⃣ Install dependencies
pip install -r requirements.txt

3️⃣ Run Streamlit app
streamlit run app.py

☁️ Deployment (Streamlit Cloud)

Connect GitHub repository

Select app.py

Add secrets under Settings → Secrets

Deploy

📈 Future Enhancements

Multi-page Streamlit app

Forecasting module (ARIMA / Prophet)

Inventory analytics

Customer-level drilldown

Route optimization

👨‍💻 Author

Sagar Panja
PGDM – Business Analytics
Focused on Supply Chain Analytics, Data Engineering, and Cloud Systems.

⭐ Support

If you found this project helpful, please star ⭐ the repository!
