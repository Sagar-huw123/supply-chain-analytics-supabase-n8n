📦 Supply Chain Analytics Dashboard
Cloud-Native ETL + Analytics using n8n → Supabase (PostgreSQL) → Streamlit

This project is a fully automated supply chain analytics system built using:

n8n – Automated ETL workflows

Supabase (PostgreSQL) – Cloud data warehouse

Google Colab – Data processing & modelling

Streamlit – Interactive dashboard

Plotly – Visual analytics

It performs real-time supply chain performance monitoring, OTIF reporting, customer segmentation, and product/category-level insights.

🚀 Live Dashboard

🔗 Streamlit App:
👉 https://supply-chain-analytics-supabase-n8n-bxdk8w8lhw65c7wt3aitpy.streamlit.app/

🧠 Project Architecture
n8n (workflow automation)
        ↓
Supabase (PostgreSQL Data Warehouse)
        ↓
Google Colab (ETL, cleaning, modelling)
        ↓
GitHub (version control)
        ↓
Streamlit Cloud (live analytics dashboard)

🎯 Key Features
1️⃣ Automated ETL Pipeline

n8n fetches/receives order-level data

Cleans + formats data

Pushes into Supabase PostgreSQL in real-time

2️⃣ Analytical Dataset

Stored in the following tables:

fact_order_line

dim_customers

dim_products

dim_targets_orders

fact_aggregate

These tables provide a 360° view of customer, product, and order-level performance.

📊 Dashboard Highlights (Streamlit)
✔️ KPIs

Total Orders

Total Ordered Quantity

Fill Rate (In Full %)

OTIF % (On Time In Full)

Revenue (INR)

✔️ Visualizations

Order Quantity Trend

OTIF % Trend

Treemap: Customer Segmentation (Revenue vs OTIF)

OTIF by City (Bar Chart)

OTIF by Product Category (Bar Chart)

Detailed Order Table + CSV Export

✔️ Filters

Customer City

Product Category

Date Range

🛠️ Technologies Used
Layer	Technology
Data Automation	n8n
Database	Supabase PostgreSQL
Backend Query Layer	psycopg2
Frontend Dashboard	Streamlit
Visualizations	Plotly, Streamlit charts
Version Control	Git + GitHub
Development	Google Colab, Python
📁 Repository Structure
supply-chain-analytics-supabase-n8n/
│── app.py                # Streamlit application
│── requirements.txt      # Python dependencies
│── SUPPLY_CHAIN_ANALYTICS_USING_SUPABASE_AND_N8N.ipynb  # Colab ETL notebook
│── README.md             # Project documentation

🔌 Connecting Streamlit to Supabase

The app uses Streamlit Secrets for secure DB credentials.

.streamlit/secrets.toml
[db]
host = "YOUR_SUPABASE_HOST"
database = "postgres"
user = "YOUR_DB_USER"
password = "YOUR_DB_PASSWORD"
port = "5432"


Streamlit loads values using:

st.secrets["db"]["host"]

⚙️ Running the Project Locally
1️⃣ Clone the Repo
git clone https://github.com/Sagar-huw123/supply-chain-analytics-supabase-n8n.git
cd supply-chain-analytics-supabase-n8n
