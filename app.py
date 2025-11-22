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
    conn.autocommit = True  # ✅ important: no stuck transactions
    try:
        with conn.cursor() as cur:
            cur.execute(query, params or ())
            rows = cur.fetchall()
        return pd.DataFrame(rows)
    finally:
        conn.close()



# -------------------------------
# 3. SIDEBAR FILTERS
# -------------------------------
st.sidebar.header("Filters")

try:
    # Just read directly from the dimension tables
    cities_df = run_query("""
        SELECT DISTINCT city
        FROM dim_customers
        WHERE city IS NOT NULL
        ORDER BY city;
    """)

    categories_df = run_query("""
        SELECT DISTINCT category
        FROM dim_products
        WHERE category IS NOT NULL
        ORDER BY category;
    """)

except Exception as e:
    st.error(f"DB error while loading filters: {e}")
    st.stop()

cities = ["All"] + cities_df["city"].dropna().tolist()
categories = ["All"] + categories_df["category"].dropna().tolist()

selected_city = st.sidebar.selectbox("Customer City", cities)
selected_category = st.sidebar.selectbox("Product Category", categories)

date_range = st.sidebar.date_input(
    "Order placement date range",
    value=[],
    help="Optional filter – leave empty to use full data range."
)


# -------------------------------
# 4. MAIN DATA QUERY
# -------------------------------

query = """
    SELECT
        f.order_id,
        f.order_placement_date,
        f.customer_id,
        f.product_id,
        f.order_qty,
        f.delivery_qty,
        f."On Time"      AS on_time,
        f."In Full"      AS in_full,
        f."On Time In Full" AS otif,
        c.customer_name,
        c.city,
        p.product_name,
        p.category
    FROM fact_order_line f
    JOIN dim_customers c ON f.customer_id = c.customer_id
    JOIN dim_products  p ON f.product_id = p.product_id
    WHERE 1=1
"""

params = []

if selected_city != "All":
    query += " AND c.city = %s"
    params.append(selected_city)

if selected_category != "All":
    query += " AND p.category = %s"
    params.append(selected_category)

if len(date_range) == 2:
    query += " AND f.order_placement_date BETWEEN %s AND %s"
    params.append(date_range[0])
    params.append(date_range[1])

query += " ORDER BY f.order_placement_date;"

try:
    df = run_query(query, params)
except Exception as e:
    st.error(f"DB error while loading main data: {e}")
    st.stop()

if df.empty:
    st.warning("No data found for the selected filters.")
    st.stop()

df["order_placement_date"] = pd.to_datetime(df["order_placement_date"])

# -------------------------------
# 5. KPI CARDS
# -------------------------------
col1, col2, col3, col4 = st.columns(4)

total_orders = df["order_id"].nunique()
total_order_qty = df["order_qty"].sum()
fill_rate = (df["delivery_qty"].sum() / df["order_qty"].sum()) * 100 if df["order_qty"].sum() > 0 else 0
otif_rate = (df["otif"].sum() / len(df)) * 100 if len(df) > 0 else 0  # assuming otif is 0/1

col1.metric("Total Orders", f"{total_orders:,}")
col2.metric("Total Ordered Qty", f"{total_order_qty:,}")
col3.metric("Fill Rate (In Full)", f"{fill_rate:.1f}%")
col4.metric("OTIF %", f"{otif_rate:.1f}%")

st.markdown("---")

# -------------------------------
# 6. TIME SERIES – OTIF & QUANTITY
# -------------------------------
st.subheader("📈 OTIF & Volume Over Time")

ts = (
    df.groupby("order_placement_date")
      .agg(
          total_order_qty=("order_qty", "sum"),
          avg_otif=("otif", "mean"),
      )
      .reset_index()
)

tab1, tab2 = st.tabs(["Order Quantity", "OTIF %"])

with tab1:
    st.line_chart(ts.set_index("order_placement_date")[["total_order_qty"]])

with tab2:
    ts_otif = ts.copy()
    ts_otif["otif_percent"] = ts_otif["avg_otif"] * 100
    st.line_chart(ts_otif.set_index("order_placement_date")[["otif_percent"]])

# -------------------------------
# 7. DETAIL TABLE
# -------------------------------
st.subheader("🔍 Detailed Orders")
st.dataframe(df, use_container_width=True)

st.download_button(
    "Download filtered data as CSV",
    data=df.to_csv(index=False).encode("utf-8"),
    file_name="supply_chain_filtered.csv",
    mime="text/csv"
)

