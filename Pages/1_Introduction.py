import streamlit as st
import pandas as pd
from pathlib import Path

# Page header with enhanced styling
st.title("📖 Introduction to OECD Environmental Dashboard")

st.markdown("""
<div style="background-color: #0e1117; padding: 20px; border-radius: 10px; border-left: 5px solid #4CAF50; margin: 20px 0; border: 1px solid #262730;">
    <h3 style="color: #4CAF50; margin-top: 0;">🌍 Welcome to the Enhanced OECD Environmental Analytics Platform</h3>
    <p style="color: #a3a8b8; font-size: 16px; line-height: 1.6;">
        Our advanced dashboard provides comprehensive visualization and analysis of OECD environmental data with cutting-edge features including dynamic font sizing, country-specific color coding, and interactive correlation analysis. Explore complex environmental relationships through intuitive, responsive visualizations.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
## 🎯 Dashboard Objectives

Our enhanced platform aims to:
- **📊 Visualize** complex environmental data with advanced, responsive chart types
- **🌍 Compare** environmental performance across OECD countries with consistent color coding
- **📈 Track** trends and correlations between different environmental indicators over time
- **🔍 Analyze** relationships between greenhouse gas emissions and agricultural factors
- **🎨 Provide** professional-grade visualizations with dynamic sizing and optimal readability

## ✨ New & Enhanced Features (v2.0)

### 🎨 Advanced Waterfall Charts
- **Country-Specific Colors**: Each country maintains consistent colors across all visualizations
- **Dynamic Font Sizing**: Text automatically adjusts (8px-18px) to fit within chart elements
- **Smart Text Positioning**: Country names inside bars, values and percentages outside
- **Professional Styling**: Enhanced borders, spacing, and visual hierarchy

### � Geographic Visualization Enhancements  
- **80+ Projection Types**: Choose from orthographic, mercator, natural earth, and many more
- **Interactive Maps**: Both static accumulative and animated annual views
- **Responsive Design**: Maps adapt to different screen sizes and data densities

### 📊 Correlation Analysis Platform
- **Multi-variable Analysis**: Explore relationships between GHS emissions and environmental factors
- **Bubble Chart Visualizations**: Size represents population, colors represent countries
- **Temporal Analysis**: Both static cumulative and animated time-series views

## 📊 Comprehensive Data Sources

### 🌿 Greenhouse Gas Output (GHG Output)
- **Without LULUCF**: Direct GHG Output excluding Land Use, Land-Use Change, and Forestry
- **From LULUCF**: GHG Output specifically from land use changes  
- **With LULUCF**: Total GHG Output including all sources
- **By Sectors**: Breakdown by economic sectors (Transport, Energy, Agriculture, etc.)
- **By Nature Sources**: Classification by natural ecosystem types (Cropland, Grassland, Forest, etc.)

### 🌱 Agricultural Environmental Indicators
- **Energy Consumption**: Agricultural energy use in tonnes of oil equivalent
- **Land Area**: Agricultural land usage in hectares
- **Water Abstraction**: Agricultural water consumption in cubic meters
- **Population Data**: Demographic context for correlation analysis

### 🔗 Cross-correlation Analysis
- **Multi-variable Relationships**: Explore connections between different environmental factors
- **Temporal Trends**: Analyze how relationships change over time
- **Geographic Patterns**: Compare environmental performance across countries

## 🔍 Enhanced Key Features

### 🎨 Advanced Interactive Visualizations
- **Dynamic Font Sizing**: Text automatically adjusts for optimal readability (8px-18px range)
- **Country-Specific Colors**: Consistent color coding across all chart types
- **Multiple Chart Types**: Waterfall, line, area, bar, pie, tree map, bubble, and geographic charts
- **Professional Styling**: Enhanced borders, spacing, and visual hierarchy
- **Zoom, Pan & Hover**: Detailed exploration capabilities with responsive interactions

### ⚙️ Smart Filtering and Customization
- **Intelligent Controls**: "Select All" buttons for quick filter management
- **Year Range Sliders**: Flexible time period selection
- **Multi-perspective Views**: Toggle between value and percentage perspectives
- **Geographic Projections**: Choose from 80+ map projection types
- **Animation Controls**: Play/pause temporal visualizations

### 📊 Professional Data Analysis
- **Statistical Summaries**: Automated trend analysis and data insights
- **Correlation Analysis**: Explore relationships between environmental indicators
- **Export Capabilities**: Download visualizations and filtered datasets
- **Responsive Design**: Optimal viewing across different screen sizes

## 🌍 About OECD Environmental Data

The Organisation for Economic Co-operation and Development (OECD) maintains comprehensive databases on environmental indicators as part of its commitment to sustainable development. This enhanced dashboard leverages this authoritative data to provide insights for policymakers, researchers, and citizens.

### 🎯 Data Quality and Standards
- **Regular Updates**: Data is systematically updated by OECD member countries
- **Standardized Methodologies**: Ensures cross-country comparability and reliability
- **Quality Assurance**: Rigorous validation processes maintain data integrity
- **Comprehensive Coverage**: Includes emissions, land use, energy, and water data

### 🚀 Technical Innovations
- **Modular Architecture**: Refactored codebase with 900+ lines organized into reusable components
- **Performance Optimization**: Enhanced data processing and chart rendering speed
- **User Experience**: Intuitive interface with professional-grade visualizations
- **Accessibility**: Improved contrast, readable fonts, and responsive design

---

## 🎮 Ready to Explore?

Navigate to the **Dashboard** section to start your comprehensive environmental data analysis journey!
""")

# Enhanced visual elements with better styling
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div style="background-color: #1f4e79; padding: 15px; border-radius: 8px; border-left: 4px solid #3498db;">
        <h4 style="color: #3498db; margin-top: 0;">💡 Pro Tips</h4>
        <ul style="color: #a3a8b8; margin-bottom: 0;">
            <li>Use <strong>Select All</strong> buttons for quick filtering</li>
            <li>Try different <strong>map projections</strong> for geographic data</li>
            <li>Toggle between <strong>static and animated</strong> views</li>
            <li>Explore <strong>correlation analysis</strong> for insights</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="background-color: #1e5631; padding: 15px; border-radius: 8px; border-left: 4px solid #27ae60;">
        <h4 style="color: #27ae60; margin-top: 0;">🚀 Get Started</h4>
        <p style="color: #a3a8b8; margin-bottom: 0;">
            Head to the <strong>Dashboard</strong> to begin exploring environmental data with our enhanced visualization tools!
        </p>
    </div>
    """, unsafe_allow_html=True)

# Enhanced Contributors Section
st.markdown("---")
st.markdown("""
<div style="text-align: center; margin: 30px 0;">
    <h2 style="color: #fafafa; font-size: 28px;">👥 Development Team</h2>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div style="background-color: #0e1117; padding: 20px; border-radius: 10px; border-left: 5px solid #ff6b6b; border: 1px solid #262730;">
        <h3 style="color: #ff6b6b; margin-top: 0;">🌿 Nguyen Xuan Duy Thai</h3>
        <p style="color: #fafafa; font-weight: bold;">Lead Developer - Greenhouse Gas Topic</p>
        <ul style="color: #a3a8b8;">
            <li>Enhanced waterfall charts with dynamic font sizing</li>
            <li>Country-specific color coding system</li>
            <li>Advanced chart refactoring and optimization</li>
            <li>Geographic visualization enhancements</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="background-color: #0e1117; padding: 20px; border-radius: 10px; border-left: 5px solid #4ecdc4; border: 1px solid #262730;">
        <h3 style="color: #4ecdc4; margin-top: 0;">🌱 Nguyen Minh Dang</h3>
        <p style="color: #fafafa; font-weight: bold;">Developer - Nutrient Input/Output Topic</p>
    </div>
    """, unsafe_allow_html=True)

# Enhanced Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #a3a8b8; font-style: italic; padding: 20px;">
    <p><strong>OECD Environmental Analytics Dashboard v2.0</strong></p>
    <p>This enhanced dashboard is designed for educational and research purposes.<br>
    Data source: OECD Environmental Statistics | Built with love using Streamlit & Plotly</p>
</div>
""", unsafe_allow_html=True)
