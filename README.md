# E-Commerce Analytics Dashboard

A comprehensive Streamlit web application for analyzing e-commerce orders, revenue patterns, customer behavior, and seasonal trends.

## Features

### 📈 Overview

- Dataset summary with key metrics
- Quick data preview
- Data type and missing value information

### 💰 Revenue Analysis

- Revenue statistics (mean, median, std, quartiles)
- Revenue volatility analysis
- Distribution visualization (histogram, box plot, Pareto chart)
- Discount impact analysis

### 👥 Customer Segmentation (RFM Analysis)

- Recency, Frequency, Monetary scoring
- Customer segment distribution
- 8 customer segments with actionable recommendations:
  - Champions
  - Loyal Customers
  - Potential Loyalists
  - Promising
  - Need Attention
  - At Risk
  - Lost
  - Other

### 📦 Product & Category Analysis

- Best-selling products and categories
- Revenue and order distribution by category
- Pareto analysis (80/20 rule)
- Return/refund rate analysis
- Quality assessment per category

### 📅 Seasonal Patterns

- Monthly revenue trends
- Quarterly breakdown
- Seasonal distribution
- Volatility analysis
- Peak and low period identification

### 🎯 Strategic Recommendations

- Best-selling product strategies
- Return rate mitigation
- Seasonal planning
- Customer lifecycle management
- Revenue optimization tactics
- KPI monitoring framework

## Installation

### Prerequisites

- Python 3.8+
- pip (Python package manager)

### Setup Steps

1. **Navigate to the project directory:**

   ```powershell
   cd "c:\Users\HomePC\Documents\Projects\DataScienceInternship\Ecommerce-order"
   ```

2. **Install required packages:**

   ```powershell
   pip install -r requirements.txt
   ```

3. **Ensure your CSV file is in the same directory:**
   - The app expects `ecommerce_orders_revenue.csv` in the same folder as `streamlit_app.py`

## Running the Application

1. **Launch the Streamlit app:**

   ```powershell
   streamlit run app.py
   ```

2. **Access the dashboard:**
   - Streamlit will automatically open your browser to `http://localhost:8501`
   - If not, manually navigate to that URL

3. **Navigation:**
   - Use the sidebar menu to switch between different analysis sections
   - All visualizations are interactive and update in real-time

## File Structure

```
Ecommerce-order/
├── ecommerce_orders_revenue.csv    # Your data file
├── streamlit_app.py                # Main Streamlit application
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── main.ipynb                      # Original Jupyter notebook
└── test.ipynb                      # Test notebook
```

## Features Overview

### Dashboard Navigation

**📈 Overview**

- Dataset statistics
- Record count and date range
- Revenue summary
- Data quality check

**💰 Revenue Analysis**

- Statistical measures
- Distribution analysis with visualizations
- Volatility assessment
- Discount impact evaluation

**👥 Customer Segmentation**

- RFM scoring methodology
- Customer segment distribution
- Detailed segment profiles
- Actionable recommendations for each segment

**📦 Product & Category**

- Category performance ranking
- Revenue and order distribution
- 80/20 concentration analysis
- Return rate assessment by category
- Quality issues identification

**📅 Seasonal Patterns**

- Monthly and quarterly trends
- Seasonal distribution
- Peak and low period identification
- Volatility metrics

**🎯 Recommendations**

- Strategic action items
- Best practice guidelines
- Seasonal strategies
- Customer lifecycle tactics
- Revenue optimization tips

## Data Requirements

Your CSV file should contain the following columns:

- `customer_id`: Unique customer identifier
- `order_id`: Unique order identifier
- `order_date`: Date of the order (will be converted to datetime)
- `order_value`: Amount of the order
- `product_category`: Category of the product
- `order_status`: Status of the order (completed, cancelled, refunded, etc.)
- `discount_applied`: Discount amount (can have null values)

## Performance Tips

- **Large datasets:** The app uses `@st.cache_data` for efficient data loading
- **Refresh data:** Restart the Streamlit app to reload the CSV file
- **Filtering:** Use Streamlit's sidebar controls for interactive filtering

## Troubleshooting

### Issue: CSV file not found

- **Solution:** Ensure `ecommerce_orders_revenue.csv` is in the same directory as `streamlit_app.py`

### Issue: Missing dependencies

- **Solution:** Run `pip install -r requirements.txt` again

### Issue: Port 8501 already in use

- **Solution:** Run `streamlit run streamlit_app.py --server.port 8502`

### Issue: Data not updating

- **Solution:** The app caches data. Clear cache with Ctrl+R in the browser or restart Streamlit

## Customization

### Change colors

Edit the color codes in the visualization sections (e.g., `color='#2ecc71'`)

### Modify segments

Update the `segment_customer()` function in the RFM analysis section

### Add new analyses

- Follow the existing structure in the `streamlit_app.py` file
- Use `st.subheader()` for section titles
- Use `st.dataframe()` for tables
- Use `st.pyplot()` for matplotlib charts

## Browser Compatibility

- Chrome (recommended)
- Firefox
- Safari
- Edge

## Support & Documentation

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Matplotlib Documentation](https://matplotlib.org/stable/contents.html)

## Version History

**Version 1.0** (February 2026)

- Initial release
- Complete analysis dashboard
- All visualizations and recommendations

## License

Internal use only

## Notes

- All visualizations are generated on-the-fly for data freshness
- The dashboard is responsive and works on different screen sizes
- Export visualizations using Streamlit's built-in screenshot feature
- Share reports using Streamlit's sharing feature (requires Streamlit Cloud account)
