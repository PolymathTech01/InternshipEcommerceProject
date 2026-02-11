# Quick Start Guide - Streamlit E-Commerce Dashboard

## 🚀 Get Started in 2 Minutes

### Step 1: Open PowerShell

Press `Win + R`, type `powershell`, and press Enter.

### Step 2: Navigate to Your Project

```powershell
cd "c:\Users\HomePC\Documents\Projects\DataScienceInternship\Ecommerce-order"
```

### Step 3: Install Dependencies (First Time Only)

```powershell
pip install -r requirements.txt
```

### Step 4: Launch the Dashboard

```powershell
streamlit run app.py
```

A browser window will automatically open with your interactive dashboard!

---

## 📊 Dashboard Sections

### 1. **Overview** (📈)

- See all your key metrics at a glance
- Dataset statistics and date range
- Quick data preview

### 2. **Revenue Analysis** (💰)

- Detailed revenue statistics
- Beautiful distribution charts
- Understand volatility patterns
- Discount impact analysis

### 3. **Customer Segmentation** (👥)

- See your customers grouped by value
- Find Champions (best customers)
- Identify At-Risk customers
- Get specific actions for each segment

### 4. **Product & Category** (📦)

- Top-selling categories
- Return rates by category
- Quality issues highlighted
- 80/20 analysis

### 5. **Seasonal Patterns** (📅)

- Monthly revenue trends
- Best and worst sales periods
- Plan inventory accordingly
- Seasonality insights

### 6. **Strategic Recommendations** (🎯)

- Actionable insights
- Best practices
- Tactical recommendations
- KPI framework

---

## 🎯 What You Can Do

✅ **View your data** - Browse and filter your e-commerce orders
✅ **See trends** - Visualize revenue patterns and seasonality
✅ **Segment customers** - Identify high-value vs at-risk customers
✅ **Analyze returns** - Find quality issues by category
✅ **Get recommendations** - Receive strategic action items
✅ **Export insights** - Screenshots and reports

---

## 💡 Tips

- 🔄 **Switch sections** using the sidebar menu
- 📱 **Responsive design** - Works on different screen sizes
- 💾 **Data refreshes** when you restart the app
- 🎨 **Professional theme** with color-coded insights
- 📊 **Interactive charts** - Hover for details

---

## ❓ Troubleshooting

### App won't open?

1. Check that `ecommerce_orders_revenue.csv` is in the same folder
2. Make sure you're in the correct directory
3. Try: `streamlit run app.py --logger.level=debug`

### Missing packages?

```powershell
pip install -r requirements.txt
```

### Want to stop the app?

Press `Ctrl + C` in PowerShell

### Change the port?

```powershell
streamlit run streamlit_app.py --server.port 8502
```

---

## 📈 What's Included

- ✅ Complete revenue analysis
- ✅ Customer RFM segmentation
- ✅ Product & category breakdown
- ✅ Return rate analysis
- ✅ Seasonal trend analysis
- ✅ Strategic recommendations
- ✅ 20+ visualizations
- ✅ Professional styling
- ✅ Color-coded alerts
- ✅ Detailed metrics

---

## 🎨 Interface Guide

**Color Meanings:**

- 🟢 Green = Good performance
- 🟡 Yellow = Warning/Monitor
- 🔴 Red = Alert/Action needed
- 🔵 Blue = Information

**Navigation:**

- Use sidebar to switch between sections
- Expand boxes with ▶️ to see details
- Metrics cards show key numbers
- Charts are interactive

---

## Next Steps

After launching:

1. Check the **Overview** to understand your data
2. Explore **Revenue Analysis** for performance
3. Review **Customer Segmentation** for strategy
4. Analyze **Product & Category** for optimization
5. Understand **Seasonal Patterns** for planning
6. Implement **Recommendations**

---

## Need Help?

- Check README.md for detailed documentation
- Review the original Jupyter notebooks (main.ipynb, test.ipynb)
- Refer to Streamlit docs: https://docs.streamlit.io/

---

**Happy analyzing!** 🚀📊
