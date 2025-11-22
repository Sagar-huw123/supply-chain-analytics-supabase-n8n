# 📦 Supply Chain Analytics Dashboard

Cloud-Native ETL + Analytics using n8n → Supabase → Streamlit

This project is a fully automated, cloud-based supply chain analytics solution.

## 🚀 Live Dashboard

**Streamlit App:** 
https://supply-chain-analytics-supabase-n8n-bxdk8w8lhw65c7wt3aitpy.streamlit.app/

## 🧠 Project Architecture
n8n (workflow automation)
↓
Supabase (PostgreSQL data warehouse)
↓
Google Colab (ETL + modelling)
↓
GitHub (version control)
↓
Streamlit Cloud (live dashboard)


## 🎯 Key Features

### 1. Automated ETL Pipeline (n8n → Supabase)
- Order-level data automatically captured via n8n
- Cleaned, transformed, and loaded into Supabase tables
- Supports incremental/event-driven updates

### 2. Interactive Supply Chain Dashboard
- Built using Streamlit + PostgreSQL
- **KPIs:**
  - Total Orders
  - Total Ordered Quantity
  - Fill Rate (In Full %)
  - OTIF % (On Time In Full)
  - Revenue (INR)
- **Visualizations:**
  - Order Quantity Trend
  - OTIF Trend
  - Customer Segmentation Treemap (Revenue × OTIF)
  - OTIF by City
  - OTIF by Product Category
  - Detailed data explorer + CSV export
- **Filters:**
  - City
  - Product Category
  - Date Range

## 🗄️ Database Schema (Supabase)

**Fact Tables:**
- `fact_order_line`
- `fact_aggregate`

**Dimension Tables:**
- `dim_customers`
- `dim_products`
- `dim_targets_orders`

## 📁 Repository Structure

supply-chain-analytics-supabase-n8n/
│── app.py
│── requirements.txt
│── SUPPLY_CHAIN_ANALYTICS_USING_SUPABASE_AND_N8N.ipynb
│── README.md


## 🔌 Streamlit → Supabase Connection

**`.streamlit/secrets.toml`** (Stored in Streamlit Cloud, not in GitHub)

```toml
[db]
host = "YOUR_SUPABASE_HOST"
database = "postgres"
user = "YOUR_DB_USER"
password = "YOUR_DB_PASSWORD"
port = "5432"

```

Streamlit usage:

python
st.secrets["db"]["host"]
🛠️ Run Locally
Clone the repo

bash
git clone https://github.com/Sagar-huw123/supply-chain-analytics-supabase-n8n.git
cd supply-chain-analytics-supabase-n8n
Install dependencies

bash
pip install -r requirements.txt
Run the dashboard

bash
streamlit run app.py
☁️ Deployment (Streamlit Cloud)
Connect your GitHub repository

Choose app.py as the entry file

Add secrets in Settings → Secrets

Deploy

📈 Future Enhancements
Multi-page Streamlit app

Forecasting models (ARIMA / Prophet)

Inventory & safety stock analytics

Customer drilldown

Route optimization metrics

## 👨‍💻 Author
Sagar Panja
PGDM — Business Analytics
Supply Chain Analytics • ETL Pipelines • Cloud Systems

⭐ Support
If you like this project, please ⭐ star the repository!
