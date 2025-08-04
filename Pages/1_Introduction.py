import streamlit as st
import pandas as pd
from pathlib import Path

# Page header
st.title("📖 Introduction")

st.markdown("""
## About This Dashboard

The OECD Dashboard allows users to view data visualization on interested time frame, countries, and measures related to two topics and extract insights from the visuals to aid them in international policymaking.The first is topic is greenhouse gas emission, the second topic is nutrient input/output on the agriculture. 

## 🎯 Objectives

Our dashboard aims to:
- **Visualize** complex environmental data in an accessible format
- **Compare** environmental performance across OECD countries
- **Track** trends and changes over time
- **Identify** patterns and correlations in environmental indicators

## 📊 Data Sources

### Greenhouse Gas Output (GHG Output)
- **Without LULUCF**: Direct GHG Output excluding Land Use, Land-Use Change, and Forestry
- **From LULUCF**: GHG Output specifically from land use changes
- **With LULUCF**: Total GHG Output including all sources
- **By Sectors**: Breakdown by economic sectors
- **By Nature Sources**: Classification by nature source types

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
