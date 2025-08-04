import streamlit as st
import pandas as pd
from pathlib import Path

# Page header
st.title("📖 Introduction to OECD Environmental Data")

st.markdown("""
## About This Dashboard

This interactive dashboard provides comprehensive analysis of environmental indicators from the Organisation for Economic Co-operation and Development (OECD). 
The platform focuses on key environmental metrics that are crucial for understanding sustainability trends across member countries.

## 🎯 Objectives

Our dashboard aims to:
- **Visualize** complex environmental data in an accessible format
- **Compare** environmental performance across OECD countries
- **Track** trends and changes over time
- **Identify** patterns and correlations in environmental indicators

## 📊 Data Sources

### Greenhouse Gas Emissions
- **Without LULUCF**: Direct emissions excluding Land Use, Land-Use Change, and Forestry
- **From LULUCF**: Emissions specifically from land use changes
- **With LULUCF**: Total emissions including all sources
- **By Sectors**: Breakdown by economic sectors
- **By Nature Sources**: Classification by emission source types

### Agricultural Land Data
- Land use patterns and agricultural statistics
- Changes in agricultural area over time
- Country-specific agricultural metrics

### Nutrient Input/Output
- Environmental nutrient flow analysis
- Input sources and output destinations
- Impact on environmental sustainability

## 🔍 Key Features

### Interactive Visualizations
- Dynamic charts that respond to user selections
- Multiple chart types: line plots, bar charts, heatmaps, and more
- Zoom, pan, and hover capabilities for detailed exploration

### Filtering and Customization
- Filter by country, time period, and data categories
- Customize visualizations based on your interests
- Export capabilities for further analysis

### Statistical Analysis
- Summary statistics for quick insights
- Trend analysis and percentage changes
- Cross-country comparisons

## 📈 How to Use This Dashboard

1. **Navigate** using the sidebar menu to access different sections
2. **Filter** data using the available controls to focus on specific aspects
3. **Interact** with charts by hovering, clicking, and zooming
4. **Analyze** trends and patterns in the visualizations
5. **Export** data or charts for your own analysis

## 🌍 About OECD Environmental Data

The OECD maintains comprehensive databases on environmental indicators as part of its commitment to sustainable development. 
This data helps policymakers, researchers, and citizens understand environmental challenges and track progress toward sustainability goals.

### Data Quality and Updates
- Data is regularly updated by OECD member countries
- Standardized methodologies ensure comparability
- Quality checks and validation processes maintain data integrity

---

Ready to explore? Navigate to the **Dashboard** section to start your analysis!
""")

# Add some visual elements
col1, col2 = st.columns(2)

with col1:
    st.info("💡 **Tip**: Use the sidebar navigation to move between different sections of the dashboard.")

with col2:
    st.success("🚀 **Get Started**: Head to the Dashboard to begin exploring the data!")

# Footer
st.markdown("---")
st.markdown("*This dashboard is designed for educational and research purposes. Data source: OECD Environmental Statistics.*")