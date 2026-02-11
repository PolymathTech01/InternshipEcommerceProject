import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="E-Commerce Analytics Dashboard",
    page_icon="chart",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom styling
st.markdown("""
    <style>
    .metric-container {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .insight-box {
        background-color: #e8f4f8;
        padding: 15px;
        border-left: 4px solid #0066cc;
        border-radius: 5px;
        margin: 10px 0;
    }
    .warning-box {
        background-color: #fff3cd;
        padding: 15px;
        border-left: 4px solid #ff9800;
        border-radius: 5px;
        margin: 10px 0;
    }
    .success-box {
        background-color: #d4edda;
        padding: 15px;
        border-left: 4px solid #28a745;
        border-radius: 5px;
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Load data


@st.cache_data
def load_data():
    df = pd.read_csv('ecommerce_orders_revenue.csv')
    df["order_date"] = pd.to_datetime(df["order_date"])
    df["discount_applied"] = df["discount_applied"].fillna(0)

    # Add temporal features
    df["order_month"] = df["order_date"].dt.month
    df["order_month_name"] = df["order_date"].dt.strftime("%B")
    df["Quarter"] = df["order_date"].dt.quarter
    df["Week"] = df["order_date"].dt.isocalendar().week

    def get_season(month):
        if month in [12, 1, 2]:
            return "Winter"
        elif month in [3, 4, 5]:
            return "Spring"
        elif month in [6, 7, 8]:
            return "Summer"
        else:
            return "Fall"

    df["Season"] = df["order_month"].apply(get_season)
    return df


df = load_data()

# Sidebar
st.sidebar.title("E-Commerce Analytics")
st.sidebar.markdown("---")
page = st.sidebar.radio(
    "Select Analysis:",
    ["Overview", "Revenue Analysis", "Customer Segmentation",
     "Product & Category", "Seasonal Patterns", "Recommendations"]
)

# ==================== PAGE 1: OVERVIEW ====================
if page == "Overview":
    st.title("E-Commerce Analytics Dashboard")
    st.markdown(
        "Comprehensive analysis of e-commerce orders, revenue patterns, and customer behavior")

    st.markdown("---")
    st.subheader("Dataset Overview")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Orders", f"{len(df):,}")
    with col2:
        st.metric("Total Revenue", f"${df['order_value'].sum():,.2f}")
    with col3:
        st.metric("Unique Customers", f"{df['customer_id'].nunique():,}")
    with col4:
        st.metric(
            "Date Range", f"{df['order_date'].dt.date.min()} to {df['order_date'].dt.date.max()}")

    st.markdown("---")
    st.subheader("Quick Data Preview")
    st.dataframe(df.head(10), use_container_width=True)

    st.markdown("---")
    st.subheader("Dataset Information")
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Data Types:**")
        st.dataframe(df.dtypes)
    with col2:
        st.write("**Missing Values:**")
        st.dataframe(df.isnull().sum())

# ==================== PAGE 2: REVENUE ANALYSIS ====================
elif page == "Revenue Analysis":
    st.title("Revenue Analysis")

    st.markdown("---")
    st.subheader("Revenue Statistics")

    revenue_stats = {
        "Total Revenue": f"${df['order_value'].sum():,.2f}",
        "Average Order Value": f"${df['order_value'].mean():.2f}",
        "Median Order Value": f"${df['order_value'].median():.2f}",
        "Standard Deviation": f"${df['order_value'].std():.2f}",
        "Min Order Value": f"${df['order_value'].min():.2f}",
        "Max Order Value": f"${df['order_value'].max():.2f}",
        "Q1 (25%)": f"${df['order_value'].quantile(0.25):.2f}",
        "Q3 (75%)": f"${df['order_value'].quantile(0.75):.2f}",
        "IQR": f"${df['order_value'].quantile(0.75) - df['order_value'].quantile(0.25):.2f}"
    }

    col1, col2, col3 = st.columns(3)
    metrics = list(revenue_stats.items())
    for i, (key, value) in enumerate(metrics):
        if i % 3 == 0:
            col = col1
        elif i % 3 == 1:
            col = col2
        else:
            col = col3
        with col:
            st.metric(key, value)

    # Coefficient of Variation
    st.markdown("---")
    mean_val = df["order_value"].mean()
    std_val = df["order_value"].std()
    cov = (std_val / mean_val) * 100

    st.subheader("Revenue Volatility Analysis")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Coefficient of Variation", f"{cov:.1f}%")
    with col2:
        st.metric("Best Case Day", f"${mean_val + (cov * mean_val):.2f}")
    with col3:
        st.metric("Worst Case Day", f"${mean_val - (cov * mean_val):.2f}")

    if cov > 50:
        st.warning(
            "High volatility detected! Revenue is highly unpredictable. Consider implementing inventory buffers.")

    # Distribution Analysis
    st.markdown("---")
    st.subheader("Revenue Distribution Analysis")

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # Histogram
    axes[0, 0].hist(df["order_value"], bins=20,
                    edgecolor="black", alpha=0.7, color="#3498db")
    axes[0, 0].axvline(df["order_value"].mean(), color="orange", linestyle="--",
                       linewidth=2, label=f"Mean: ${df['order_value'].mean():.2f}")
    axes[0, 0].axvline(df["order_value"].median(), color="green", linestyle="--",
                       linewidth=2, label=f"Median: ${df['order_value'].median():.2f}")
    axes[0, 0].set_title("Distribution of Order Value",
                         fontsize=11, fontweight="bold")
    axes[0, 0].set_xlabel("Order Value [$]")
    axes[0, 0].set_ylabel("Frequency")
    axes[0, 0].legend()
    axes[0, 0].grid(alpha=0.5)

    # Box plot
    axes[0, 1].boxplot(df["order_value"], vert=True)
    axes[0, 1].set_title("Box Plot - Order Value Distribution",
                         fontsize=12, fontweight="bold")
    axes[0, 1].set_ylabel("Order Value [$]")
    axes[0, 1].grid(alpha=0.5, axis='y')

    # Cumulative revenue curve
    sorted_values = np.sort(df["order_value"])
    cumsum = np.cumsum(sorted_values)
    cumsum_pct = (cumsum / cumsum[-1]) * 100
    order_pct = np.arange(1, len(cumsum) + 1) / len(cumsum) * 100

    axes[1, 0].plot(order_pct, cumsum_pct, linewidth=2, color="#e74c3c")
    axes[1, 0].fill_between(order_pct, cumsum_pct, alpha=0.3, color="#e74c3c")
    axes[1, 0].plot([0, 100], [0, 100], "k--", alpha=0.5,
                    label="Perfect Distribution")
    axes[1, 0].set_title(
        "Cumulative Revenue Curve (Pareto Chart)", fontsize=12, fontweight="bold")
    axes[1, 0].set_xlabel('% of Orders (smallest to largest)')
    axes[1, 0].set_ylabel('% of Total Revenue')
    axes[1, 0].set_xlim(0, 100)
    axes[1, 0].set_ylim(0, 100)
    axes[1, 0].legend()
    axes[1, 0].grid(alpha=0.5)

    # Quantile distribution
    quantiles = np.arange(0, 1.05, 0.05)
    quantiles_values = np.quantile(df["order_value"], quantiles)
    axes[1, 1].bar([f"{int(q*100)}%" for q in quantiles],
                   quantiles_values, color="#9b59b6", alpha=0.7)
    axes[1, 1].set_title("Revenue by Quantiles",
                         fontsize=12, fontweight="bold")
    axes[1, 1].set_ylabel("Order Value [$]")
    axes[1, 1].grid(alpha=0.5, axis="y")
    plt.xticks(rotation=45)

    plt.tight_layout()
    st.pyplot(fig)

    # Discount Impact Analysis
    st.markdown("---")
    st.subheader("Discount Impact Analysis")

    no_discount_revenue = df[df["discount_applied"] == 0]["order_value"].sum()
    with_discount_revenue = df[df["discount_applied"] > 0]["order_value"].sum()
    no_discount_avg = df[df["discount_applied"] == 0]["order_value"].mean()
    with_discount_avg = df[df["discount_applied"] > 0]["order_value"].mean()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("No Discount Revenue", f"${no_discount_revenue:,.2f}")
    with col2:
        st.metric("Discounted Revenue", f"${with_discount_revenue:,.2f}")
    with col3:
        st.metric("Avg (No Discount)", f"${no_discount_avg:.2f}")
    with col4:
        st.metric("Avg (With Discount)", f"${with_discount_avg:.2f}")

    percentage_diff = (
        (no_discount_avg - with_discount_avg) / no_discount_avg) * 100

    if percentage_diff > 0:
        st.info(
            f"Discounted orders have {percentage_diff:.1f}% lower average value. Consider optimizing discount strategy.")

    # Visualization
    fig, ax = plt.subplots(figsize=(10, 6))
    categories = ['No Discount', 'With Discount']
    revenues = [no_discount_revenue, with_discount_revenue]
    colors = ['#2ecc71', '#e74c3c']
    bars = ax.bar(categories, revenues, color=colors, alpha=0.7, width=0.5)
    ax.set_ylabel('Total Revenue [$]', fontweight='bold')
    ax.set_title('Revenue Comparison: Discounted vs Non-Discounted Orders',
                 fontweight='bold', fontsize=12)
    ax.grid(alpha=0.3, axis='y')

    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'${height/1000:.0f}K', ha='center', va='bottom', fontweight='bold')

    st.pyplot(fig)

# ==================== PAGE 3: CUSTOMER SEGMENTATION ====================
elif page == "Customer Segmentation":
    st.title("Customer Segmentation (RFM Analysis)")

    st.markdown("""
    **RFM (Recency, Frequency, Monetary)** is a customer segmentation technique that identifies and groups customers based on:
    - **Recency (R)**: How recently did the customer make a purchase?
    - **Frequency (F)**: How often does the customer purchase?
    - **Monetary (M)**: How much has the customer spent?
    """)

    st.markdown("---")

    # Calculate RFM
    reference_date = df["order_date"].max() + pd.Timedelta(days=1)

    rfm = df.groupby("customer_id").agg({
        "order_date": lambda x: (reference_date - x.max()).days,
        "order_id": "count",
        "order_value": "sum"
    }).rename(columns={
        "order_date": "Recency",
        "order_id": "Frequency",
        "order_value": "Monetary"
    }).reset_index()

    # RFM Scoring
    rfm["R_score"] = pd.qcut(rfm["Recency"], q=5, labels=[
                             5, 4, 3, 2, 1], duplicates="drop").astype(int)
    rfm["F_score"] = pd.qcut(rfm["Frequency"].rank(method="first"), q=5, labels=[
                             1, 2, 3, 4, 5], duplicates="drop").astype(int)
    rfm["M_score"] = pd.qcut(rfm["Monetary"].rank(method="first"), q=5, labels=[
                             1, 2, 3, 4, 5], duplicates="drop").astype(int)
    rfm["RFM_Score"] = rfm["R_score"].astype(
        str) + rfm["F_score"].astype(str) + rfm["M_score"].astype(str)

    # Segmentation
    def segment_customer(row):
        r, f, m = row["R_score"], row["F_score"], row["M_score"]

        if r >= 4 and f >= 4 and m >= 4:
            return "Champions"
        elif r >= 3 and f >= 4 and m >= 4:
            return "Loyal Customers"
        elif r >= 4 and f >= 3 and m >= 4:
            return "Potential Loyalists"
        elif f >= 3 and m >= 3 and r <= 2:
            return 'At Risk'
        elif r >= 4 and (f <= 2 or m <= 2):
            return 'Need Attention'
        elif r >= 3 and (f >= 3 or m >= 3):
            return 'Promising'
        elif r <= 2 and f <= 2:
            return 'Lost'
        else:
            return 'Other'

    rfm["Segment"] = rfm.apply(segment_customer, axis=1)

    st.subheader("RFM Statistics")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Customers", f"{len(rfm):,}")
        st.write("**Recency (days since last purchase)**")
        st.write(f"Mean: {rfm['Recency'].mean():.0f} days")
        st.write(f"Median: {rfm['Recency'].median():.0f} days")

    with col2:
        st.write("")
        st.write("**Frequency (number of orders)**")
        st.write(f"Mean: {rfm['Frequency'].mean():.1f} orders")
        st.write(f"Median: {rfm['Frequency'].median():.0f} orders")

    with col3:
        st.write("")
        st.write("**Monetary (total spending)**")
        st.write(f"Mean: ${rfm['Monetary'].mean():.2f}")
        st.write(f"Median: ${rfm['Monetary'].median():.2f}")

    st.markdown("---")
    st.subheader("Customer Segments Distribution")

    segment_counts = rfm["Segment"].value_counts().sort_values(ascending=False)

    colors_segment = {
        'Champions': '#2ecc71',
        'Loyal Customers': '#3498db',
        'Potential Loyalists': '#f39c12',
        'Promising': '#9b59b6',
        'Need Attention': '#e67e22',
        'At Risk': '#e74c3c',
        'Lost': '#95a5a6',
        'Other': '#bdc3c7'
    }

    fig, ax = plt.subplots(figsize=(12, 6))
    segment_colors = [colors_segment.get(
        seg, '#95a5a6') for seg in segment_counts.index]
    bars = ax.bar(range(len(segment_counts)),
                  segment_counts.values, color=segment_colors, alpha=0.8)
    ax.set_xticks(range(len(segment_counts)))
    ax.set_xticklabels(segment_counts.index, rotation=45, ha='right')
    ax.set_ylabel("Number of Customers", fontweight='bold')
    ax.set_title("Customer Segments Distribution",
                 fontweight='bold', fontsize=12)
    ax.grid(alpha=0.5, axis='y')

    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height,
                f'{int(height)}', ha='center', va='bottom', fontweight='bold')

    plt.tight_layout()
    st.pyplot(fig)

    st.markdown("---")
    st.subheader("Segment Details & Recommendations")

    segment_info = {
        "Champions": {
            "color": "#2ecc71",
            "description": "Your best customers - recent, frequent, high-spending",
            "actions": ["VIP treatment", "Exclusive offers", "Loyalty rewards", "Request referrals"]
        },
        "Loyal Customers": {
            "color": "#3498db",
            "description": "Consistent spenders, but haven't purchased recently",
            "actions": ["Win-back campaigns", "Exclusive member perks", "Special discounts"]
        },
        "Potential Loyalists": {
            "color": "#f39c12",
            "description": "Recent big spenders, not yet proven loyal",
            "actions": ["Personalized offers", "Build loyalty programs", "Nurture engagement"]
        },
        "At Risk": {
            "color": "#e74c3c",
            "description": "Were valuable but going dormant - biggest lost revenue threat",
            "actions": ["Urgent win-back campaigns", "Exclusive comeback offers", "Phone outreach"]
        },
        "Need Attention": {
            "color": "#e67e22",
            "description": "Recent window-shoppers, small purchases",
            "actions": ["Educational content", "Product recommendations", "Onboarding"]
        },
        "Promising": {
            "color": "#9b59b6",
            "description": "Solid customers with growth potential",
            "actions": ["Engagement campaigns", "Upsell/cross-sell", "Build relationships"]
        },
        "Lost": {
            "color": "#95a5a6",
            "description": "Inactive, low-engagement customers",
            "actions": ["Minimal spend", "Selective reactivation", "Consider removal from email"]
        }
    }

    for segment, info in segment_info.items():
        if segment in segment_counts.index:
            with st.expander(f"{segment} ({segment_counts[segment]} customers)"):
                st.write(f"**Profile:** {info['description']}")
                st.write("**Recommended Actions:**")
                for action in info['actions']:
                    st.write(f"- {action}")

    st.markdown("---")
    st.subheader("RFM Score Examples")
    st.dataframe(rfm[['customer_id', 'Recency', 'Frequency', 'Monetary', 'R_score',
                 'F_score', 'M_score', 'RFM_Score', 'Segment']].head(10), use_container_width=True)

# ==================== PAGE 4: PRODUCT & CATEGORY ====================
elif page == "Product & Category":
    st.title("Product and Category Analysis")

    st.markdown("---")
    st.subheader("Best-Selling Products and Categories")

    # Category Analysis
    category_analysis = df.groupby("product_category").agg({
        "order_id": "count",
        "order_value": ["sum", "mean"],
        "customer_id": "nunique"
    }).round(2)
    category_analysis.columns = [
        "Order_count", "Total_Revenue", "Avg_Revenue_per_Order", "Unique_Customers"]
    category_analysis["Revenue[%]"] = (
        category_analysis["Total_Revenue"] / category_analysis["Total_Revenue"].sum() * 100).round(1)
    category_analysis["Order[%]"] = (
        category_analysis["Order_count"] / category_analysis["Order_count"].sum() * 100).round(1)
    category_analysis = category_analysis.sort_values(
        by="Total_Revenue", ascending=False)

    st.dataframe(category_analysis, use_container_width=True)

    # Visualizations
    col1, col2 = st.columns(2)

    with col1:
        fig, ax = plt.subplots(figsize=(10, 6))
        category_revenue_sort = category_analysis.sort_values(
            'Total_Revenue', ascending=True)
        colors = ['#2ecc71' if i == 0 else '#3498db' if i == 1 else '#e74c3c' if i >= len(category_revenue_sort)-2 else '#9b59b6'
                  for i in range(len(category_revenue_sort))]
        ax.barh(range(len(category_revenue_sort)),
                category_revenue_sort['Total_Revenue'], color=colors, alpha=0.8)
        ax.set_yticks(range(len(category_revenue_sort)))
        ax.set_yticklabels(category_revenue_sort.index)
        ax.set_xlabel('Revenue [$]', fontweight='bold')
        ax.set_title('Total Revenue by Category',
                     fontweight='bold', fontsize=12)
        ax.grid(alpha=0.3, axis='x')

        for i, (idx, row) in enumerate(category_revenue_sort.iterrows()):
            ax.text(row['Total_Revenue'], i, f" ${row['Total_Revenue']/1000:.0f}K ({row['Revenue[%]']:.1f}%)",
                    va='center', fontweight='bold', fontsize=9)

        plt.tight_layout()
        st.pyplot(fig)

    with col2:
        fig, ax = plt.subplots(figsize=(10, 6))
        category_orders_sort = category_analysis.sort_values(
            'Order_count', ascending=True)
        ax.barh(range(len(category_orders_sort)),
                category_orders_sort['Order_count'], color='#3498db', alpha=0.8)
        ax.set_yticks(range(len(category_orders_sort)))
        ax.set_yticklabels(category_orders_sort.index)
        ax.set_xlabel('Number of Orders', fontweight='bold')
        ax.set_title('Order Count by Category', fontweight='bold', fontsize=12)
        ax.grid(alpha=0.3, axis='x')

        for i, (idx, row) in enumerate(category_orders_sort.iterrows()):
            ax.text(row['Order_count'], i, f" {int(row['Order_count'])} ({row['Order[%]']:.1f}%)",
                    va='center', fontweight='bold', fontsize=9)

        plt.tight_layout()
        st.pyplot(fig)

    # 80/20 Analysis
    st.markdown("---")
    st.subheader("Pareto Analysis (80/20 Rule)")

    cumsum_revenue = category_analysis["Total_Revenue"].cumsum()
    cumsum_revenue_pct = (
        cumsum_revenue / category_analysis["Total_Revenue"].sum()) * 100

    num_categories_80 = (cumsum_revenue_pct <= 80).sum()
    num_categories_20 = len(category_analysis) - num_categories_80

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Categories for 80% Revenue", num_categories_80)
        st.write(", ".join(category_analysis.index[:num_categories_80]))

    with col2:
        st.metric("Categories for 20% Revenue", num_categories_20)
        st.write(", ".join(category_analysis.index[num_categories_80:]))

    # Return/Refund Analysis
    st.markdown("---")
    st.subheader("Return/Refund Analysis by Category")

    return_analysis = df.groupby("product_category").agg({
        "order_id": "count",
        "order_status": lambda x: ((x == "cancelled") | (x == "returned")).sum()
    }).rename(columns={
        "order_id": "Total_Orders",
        "order_status": "Returns_Refunds"
    })

    return_analysis['Return_Rate[%]'] = (
        return_analysis['Returns_Refunds'] / return_analysis['Total_Orders'] * 100).round(1)
    return_analysis['Completed_Orders'] = return_analysis['Total_Orders'] - \
        return_analysis['Returns_Refunds']
    return_analysis['Completion_Rate[%]'] = (
        return_analysis['Completed_Orders'] / return_analysis['Total_Orders'] * 100).round(1)
    return_analysis = return_analysis.sort_values(
        by="Return_Rate[%]", ascending=False)

    st.dataframe(return_analysis, use_container_width=True)

    fig, ax = plt.subplots(figsize=(12, 6))
    return_rate_sort = return_analysis.sort_values(
        'Return_Rate[%]', ascending=True)
    colors_return = ['#2ecc71' if x < 20 else '#f39c12' if x < 30 else '#e74c3c'
                     for x in return_rate_sort['Return_Rate[%]']]
    ax.barh(range(len(return_rate_sort)),
            return_rate_sort['Return_Rate[%]'], color=colors_return, alpha=0.8)
    ax.set_yticks(range(len(return_rate_sort)))
    ax.set_yticklabels(return_rate_sort.index)
    ax.set_xlabel('Return Rate [%]', fontweight='bold')
    ax.set_title('Return/Refund Rate by Category',
                 fontweight='bold', fontsize=12)
    ax.axvline(x=return_analysis['Return_Rate[%]'].mean(), color='red', linestyle='--',
               linewidth=2, label=f"Avg: {return_analysis['Return_Rate[%]'].mean():.1f}%")
    ax.grid(alpha=0.3, axis='x')
    ax.legend()

    for i, (idx, row) in enumerate(return_rate_sort.iterrows()):
        ax.text(row['Return_Rate[%]'], i, f" {row['Return_Rate[%]']:.1f}%",
                va='center', fontweight='bold', fontsize=9)

    plt.tight_layout()
    st.pyplot(fig)

    # Overall metrics
    st.markdown("---")
    st.subheader("Overall Return/Refund Metrics")

    total_orders = len(df)
    total_returns = ((df['order_status'] == 'cancelled') |
                     (df['order_status'] == 'refunded')).sum()
    overall_return_rate = (total_returns / total_orders * 100)
    total_lost_revenue = df[((df['order_status'] == 'cancelled') |
                             (df['order_status'] == 'refunded'))]['order_value'].sum()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Overall Return Rate", f"{overall_return_rate:.1f}%")
    with col2:
        st.metric("Orders at Risk", f"{total_returns:,}")
    with col3:
        st.metric("Lost Revenue", f"${total_lost_revenue:,.2f}")
    with col4:
        status = "Above Average" if overall_return_rate > 25 else "Good"
        st.metric("Status", status)

    if overall_return_rate > 30:
        st.error(
            "Return rate is above industry average (30%). Quality issue investigation recommended.")
    elif overall_return_rate > 20:
        st.warning(
            "Return rate is at high end (20-30%). Close monitoring recommended.")
    else:
        st.success(
            f"Return rate ({overall_return_rate:.1f}%) is below industry average. Good performance!")

# ==================== PAGE 5: SEASONAL PATTERNS ====================
elif page == "Seasonal Patterns":
    st.title("Seasonal Patterns and Trends")

    st.markdown("---")
    st.subheader("Monthly Revenue Trend")

    monthly_data = df.groupby("order_month_name").agg({
        "order_id": "count",
        "order_value": ["sum", "mean"],
        "customer_id": "nunique"
    }).round(2)

    month_order = ["January", "February", "March", "April", "May", "June",
                   "July", "August", "September", "October", "November", "December"]
    monthly_data = monthly_data.reindex(month_order)
    monthly_data.columns = ["Order_count", "Total_Revenue",
                            "Avg_Revenue_per_Order", "Unique_Customers"]
    monthly_data["Completion_rate[%]"] = (df.groupby("order_month_name")['order_status'].apply(
        lambda x: (x == "completed").sum()).reindex(month_order) / monthly_data["Order_count"] * 100).round(1)

    st.dataframe(monthly_data, use_container_width=True)

    # Monthly trend visualization
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    monthly_rev = df.groupby('order_month')['order_value'].sum().sort_index()
    axes[0, 0].plot(monthly_rev.index, monthly_rev.values,
                    marker='o', linewidth=2.5, markersize=8, color='#e74c3c')
    axes[0, 0].fill_between(
        monthly_rev.index, monthly_rev.values, alpha=0.3, color='#e74c3c')
    axes[0, 0].set_title('Monthly Revenue Trend',
                         fontweight='bold', fontsize=12)
    axes[0, 0].set_xlabel('Month')
    axes[0, 0].set_ylabel('Revenue [$]')
    axes[0, 0].set_xticks(range(1, 13))
    axes[0, 0].set_xticklabels(
        ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    axes[0, 0].grid(alpha=0.3)
    axes[0, 0].axhline(y=monthly_rev.mean(), color='blue', linestyle='--',
                       linewidth=2, label=f"Avg: ${monthly_rev.mean()/1000:.0f}K")
    axes[0, 0].legend()

    # Monthly orders
    monthly_orders = df.groupby('order_month')['order_id'].count().sort_index()
    axes[0, 1].plot(monthly_orders.index, monthly_orders.values,
                    marker='s', linewidth=2.5, markersize=8, color='#3498db')
    axes[0, 1].set_title('Monthly Order Count', fontweight='bold', fontsize=12)
    axes[0, 1].set_xlabel('Month')
    axes[0, 1].set_ylabel('Number of Orders')
    axes[0, 1].set_xticks(range(1, 13))
    axes[0, 1].set_xticklabels(
        ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    axes[0, 1].grid(alpha=0.3)

    # Quarterly breakdown
    quarterly_rev = df.groupby('Quarter')['order_value'].sum()
    bars = axes[1, 0].bar(['Q1', 'Q2', 'Q3', 'Q4'], quarterly_rev.values,
                          color=['#2ecc71', '#3498db', '#f39c12', '#e74c3c'], alpha=0.8)
    axes[1, 0].set_title('Quarterly Revenue', fontweight='bold', fontsize=12)
    axes[1, 0].set_ylabel('Revenue [$]')
    axes[1, 0].grid(alpha=0.3, axis='y')

    for bar in bars:
        height = bar.get_height()
        axes[1, 0].text(bar.get_x() + bar.get_width()/2., height,
                        f'${height/1000:.0f}K', ha='center', va='bottom', fontweight='bold')

    # Seasonal breakdown
    seasonal_rev = df.groupby('Season')['order_value'].sum()
    season_order = ['Winter', 'Spring', 'Summer', 'Fall']
    seasonal_rev = seasonal_rev.reindex(
        [s for s in season_order if s in seasonal_rev.index])
    colors_season = ['#4ecdc4', '#45b7d1', '#f7dc6f', '#f8b739']
    wedges, texts, autotexts = axes[1, 1].pie(seasonal_rev.values, labels=seasonal_rev.index,
                                              autopct='%1.1f%%', colors=colors_season, startangle=90)
    axes[1, 1].set_title('Revenue by Season', fontweight='bold', fontsize=12)
    for autotext in autotexts:
        autotext.set_color('black')
        autotext.set_fontweight('bold')
        autotext.set_fontsize(10)

    plt.tight_layout()
    st.pyplot(fig)

    # Key seasonal insights
    st.markdown("---")
    st.subheader("Key Seasonal Insights")

    peak_month = monthly_data["Total_Revenue"].idxmax()
    low_month = monthly_data["Total_Revenue"].idxmin()

    quarterly_data_df = df.groupby('Quarter')['order_value'].sum()
    peak_quarter = quarterly_data_df.idxmax()
    peak_season = seasonal_rev.idxmax()

    col1, col2 = st.columns(2)

    with col1:
        st.write("**Peak Periods:**")
        st.write(
            f"- Peak Month: {peak_month} (${monthly_data.loc[peak_month, 'Total_Revenue']:,.2f})")
        st.write(
            f"- Peak Quarter: Q{peak_quarter} (${quarterly_data_df.loc[peak_quarter]:,.2f})")
        st.write(
            f"- Peak Season: {peak_season} (${seasonal_rev.loc[peak_season]:,.2f})")

    with col2:
        st.write("**Low Periods:**")
        st.write(
            f"- Low Month: {low_month} (${monthly_data.loc[low_month, 'Total_Revenue']:,.2f})")
        st.write(f"- Opportunity: Plan promotions during {low_month}")

    # Volatility analysis
    monthly_revenue = monthly_data['Total_Revenue']
    revenue_std = monthly_revenue.std()
    revenue_mean = monthly_revenue.mean()
    revenue_cv = (revenue_std / revenue_mean) * 100

    st.markdown("---")
    st.subheader("Volatility Analysis")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Average Monthly Revenue", f"${revenue_mean:,.2f}")
    with col2:
        st.metric("Std Deviation", f"${revenue_std:,.2f}")
    with col3:
        st.metric("Coefficient of Variation", f"{revenue_cv:.1f}%")

    if revenue_cv > 30:
        st.warning(
            f"HIGH seasonality ({revenue_cv:.1f}%): Plan inventory carefully")
    else:
        st.success(
            f"MODERATE seasonality ({revenue_cv:.1f}%): Revenue is relatively stable")

# ==================== PAGE 6: RECOMMENDATIONS ====================
elif page == "Recommendations":
    st.title("Strategic Recommendations")

    st.markdown("""
    Based on the comprehensive analysis of your e-commerce data, here are actionable recommendations 
    organized by business priorities.
    """)

    st.markdown("---")
    st.subheader("BEST-SELLING PRODUCTS")

    with st.container():
        st.markdown("""
        **Key Finding:** Top 2-3 categories drive 80% of revenue (Pareto Principle)
        
        **Action Items:**
        """)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("""
            **Stock Prioritization**
            - Allocate 60% of inventory to top 2-3 categories
            - Monitor stock levels weekly
            - Implement automated reorder points
            """)

        with col2:
            st.markdown("""
            **Marketing Focus**
            - Spend 80% of budget on top performers
            - Create targeted campaigns
            - Highlight bestsellers prominently
            """)

        with col3:
            st.markdown("""
            **Strategic Pricing**
            - Top performers can sustain +5-10% price increases
            - Create bundles with slower-moving items
            - Test price elasticity
            """)

    st.markdown("---")
    st.subheader("HIGH-RETURN/REFUND CATEGORIES")

    # Get highest return rate category
    return_analysis = df.groupby("product_category").agg({
        "order_id": "count",
        "order_status": lambda x: ((x == "cancelled") | (x == "returned")).sum()
    })
    return_analysis['Return_Rate[%]'] = (
        return_analysis['Returns_Refunds'] / return_analysis['Total_Orders'] * 100)
    high_return_cat = return_analysis['Return_Rate[%]'].idxmax()
    high_return_rate = return_analysis.loc[high_return_cat, 'Return_Rate[%]']

    with st.container():
        if high_return_rate > 30:
            st.error(f"""
            **CRISIS - {high_return_cat}: {high_return_rate:.1f}% return rate**
            
            - Audit product sourcing/supplier immediately
            - Quality testing required before restocking
            - Consider temporary delisting until resolved
            - Offer proactive refunds before customers request
            - Root cause analysis needed
            """)
        elif high_return_rate > 20:
            st.warning(f"""
            **INVESTIGATE - {high_return_cat}: {high_return_rate:.1f}% return rate**
            
            - Analyze customer feedback and returns reasons
            - Improve product descriptions and images
            - Add size guides and material information
            - Increase review visibility
            """)
        else:
            st.success(f"""
            **GOOD - All categories below 20% return rate**
            
            - Continue current quality standards
            - Use best-in-class categories as benchmarks
            - Share best practices across teams
            """)

    st.markdown("---")
    st.subheader("SEASONAL STRATEGY")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        **Peak Season Strategy (6-8 weeks before peak)**
        
        1. **Inventory Planning**
           - Increase stock by 20-30%
           - Pre-position inventory in warehouses
           - Secure additional fulfillment capacity
        
        2. **Marketing and Demand**
           - Increase paid advertising budget
           - Plan promotional campaigns
           - Build email sequences
        
        3. **Operations**
           - Hire seasonal customer service staff
           - Optimize fulfillment processes
           - Monitor quality levels
        """)

    with col2:
        st.markdown("""
        **Low Season Strategy**
        
        1. **Promotional Activities**
           - Run flash sales and clearance events
           - Generate demand with discounts
           - Clear old inventory
        
        2. **Strategic Opportunities**
           - Launch new products (no revenue impact)
           - System upgrades and maintenance
           - Deep analysis and planning
        
        3. **Cost Optimization**
           - Reduce marketing spend slightly
           - Optimize labor scheduling
           - Negotiate better supplier terms
        """)

    st.markdown("---")
    st.subheader("CUSTOMER LIFECYCLE MANAGEMENT")

    with st.container():
        st.markdown("""
        **Champions (Best Customers)**
        - VIP treatment and exclusive access
        - Request referrals and testimonials
        - Personal account management
        - Invitation to beta tests
        
        **Loyal Customers (Risk of Loss)**
        - Win-back campaigns with special offers
        - Exclusive member perks
        - Personalized recommendations
        - Special birthday/anniversary offers
        
        **Potential Loyalists (Growth Opportunity)**
        - Nurture with personalized content
        - Build loyalty programs
        - Upsell complementary products
        - Track engagement closely
        
        **At Risk (Highest ROI Reactivation)**
        - Urgent win-back campaigns
        - Exclusive comeback discounts
        - Phone/personal outreach
        - Limited-time reactivation offers
        """)

    st.markdown("---")
    st.subheader("REVENUE OPTIMIZATION")

    with st.container():
        st.markdown("""
        **Discount Strategy Insights**
        - Discounted orders have lower average value
        - Consider loyalty programs instead of blanket discounts
        - Use discounts strategically for customer acquisition only
        - Bundle strategy more effective than discounts
        
        **Pricing Opportunities**
        - High-value segments can absorb premium pricing
        - Psychological pricing (9.99, 49.99) can improve conversion
        - Dynamic pricing based on demand seasonality
        - Volume discounts for bulk orders
        
        **Cross-Sell & Upsell**
        - Recommend complementary products
        - Bundle products for increased AOV
        - Target high-value customers with premium options
        - Personalization increases acceptance rate
        """)

    st.markdown("---")
    st.subheader("KPIs TO MONITOR")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        **Revenue Metrics**
        - Average Order Value (AOV)
        - Revenue per Customer
        - Monthly Revenue Trend
        - Return Rate by Category
        """)

    with col2:
        st.markdown("""
        **Customer Metrics**
        - Customer Acquisition Cost (CAC)
        - Customer Lifetime Value (CLV)
        - Repeat Purchase Rate
        - RFM Score Distribution
        """)

st.markdown("---")
st.sidebar.markdown("---")
st.sidebar.markdown("**Dashboard Version:** 1.0")
st.sidebar.markdown("**Last Updated:** February 2026")
st.sidebar.markdown("**Data Source:** ecommerce_orders_revenue.csv")
