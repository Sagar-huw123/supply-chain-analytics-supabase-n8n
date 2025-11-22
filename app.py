import streamlit as st
import pandas as pd
import psycopg2
from psycopg2.extras import RealDictCursor

# -------------------------------
# 1. PAGE CONFIG
# -------------------------------
st.set_page_config(
    page_title="Supply Chain Analytics – Supabase",
    page_icon="📦",
    layout="wide"
)

st.title("📦 Supply Chain Analytics Dashboard")
st.caption("Powered by n8n → Supabase (PostgreSQL) → Streamlit")

# -------------------------------
# 2. DB CONNECTION (Supabase)
# -------------------------------
@st.cache_resource
def get_connection():
    conn = psycopg2.connect(
        host=st.secrets["db"]["host"],
        database=st.secrets["db"]["database"],
        user=st.secrets["db"]["user"],
        password=st.secrets["db"]["password"],
        port=st.secrets["db"]["port"],
        cursor_factory=RealDictCursor,
    )
    return conn

@st.cache_data
def run_query(query, params=None):
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute(query, params or ())
        rows = cur.fetchall()
    return pd.DataFrame(rows)


# -------------------------------
# 3. SIDEBAR FILTERS
# -------------------------------
st.sidebar.header("Filters")

# ⚠️ Change table/column names as per your DB schema
# Example assumes a table: supply_chain_orders
# with columns: order_date, region, product_sku, quantity, lead_time_days, cost

# Load basic dimensions for filters
try:
    regions_df = run_query("SELECT DISTINCT region FROM supply_chain_orders ORDER BY region;")
    skus_df = run_query("SELECT DISTINCT product_sku FROM supply_chain_orders ORDER BY product_sku;")
except Exception as e:
    st.error("Error connecting to database. Please check your credentials and table names.")
    st.stop()

regions = ["All"] + regions_df["region"].dropna().tolist()
skus = ["All"] + skus_df["product_sku"].dropna().tolist()

selected_region = st.sidebar.selectbox("Region", regions)
selected_sku = st.sidebar.selectbox("Product / SKU", skus)

date_range = st.sidebar.date_input(
    "Date range",
    value=[],
    help="Optional filter – leave empty to use full data range."
)

# -------------------------------
# 4. BUILD FILTERED DATA QUERY
# -------------------------------
query = """
    SELECT
        order_date,
        region,
        product_sku,
        quantity,
        lead_time_days,
        cost
    FROM supply_chain_orders
    WHERE 1=1
"""

params = []

if selected_region != "All":
    query += " AND region = %s"
    params.append(selected_region)

if selected_sku != "All":
    query += " AND product_sku = %s"
    params.append(selected_sku)

if len(date_range) == 2:
    query += " AND order_date BETWEEN %s AND %s"
    params.append(date_range[0])
    params.append(date_range[1])

query += " ORDER BY order_date;"

df = run_query(query, params)

if df.empty:
    st.warning("No data found for the selected filters.")
    st.stop()

# Convert date column
df["order_date"] = pd.to_datetime(df["order_date"])

# -------------------------------
# 5. KPI CARDS
# -------------------------------
col1, col2, col3, col4 = st.columns(4)

total_orders = len(df)
total_qty = df["quantity"].sum()
avg_lead_time = df["lead_time_days"].mean()
total_cost = df["cost"].sum()

col1.metric("Total Orders", f"{total_orders:,}")
col2.metric("Total Quantity", f"{total_qty:,}")
col3.metric("Avg Lead Time (days)", f"{avg_lead_time:.2f}")
col4.metric("Total Cost", f"₹{total_cost:,.0f}")

st.markdown("---")

# -------------------------------
# 6. TIME-SERIES CHARTS
# -------------------------------
st.subheader("📈 Trends Over Time")

ts = (
    df.groupby("order_date")
      .agg(
          total_quantity=("quantity", "sum"),
          avg_lead_time=("lead_time_days", "mean"),
          total_cost=("cost", "sum"),
      )
      .reset_index()
)

tab1, tab2, tab3 = st.tabs(["Quantity", "Lead Time", "Cost"])

with tab1:
    st.line_chart(ts.set_index("order_date")[["total_quantity"]])

with tab2:
    st.line_chart(ts.set_index("order_date")[["avg_lead_time"]])

with tab3:
    st.line_chart(ts.set_index("order_date")[["total_cost"]])

# -------------------------------
# 7. DRILL DOWN TABLE
# -------------------------------
st.subheader("🔍 Detailed Records")
st.dataframe(df, use_container_width=True)

st.download_button(
    "Download filtered data as CSV",
    data=df.to_csv(index=False).encode("utf-8"),
    file_name="supply_chain_filtered.csv",
    mime="text/csv"
)
