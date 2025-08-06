# 🌍 OECD Environmental Data Visualization Dashboard

An advanced interactive web-based dashboard for comprehensive analysis of OECD environmental data, built with Streamlit and Python. Features enhanced chart customization, dynamic font sizing, and modular architecture.

## 📊 Overview

This dashboard provides comprehensive visualization and analysis of OECD environmental indicators, focusing on:
- **Greenhouse Gas Emissions** (with/without LULUCF, by sectors, by nature sources)
- **Agricultural Environmental Indicators** (Energy, Land, Water consumption)
- **Cross-correlation Analysis** between environmental factors
- **Geographic Visualizations** with multiple projection types

## 🚀 Key Features

### 🎨 Advanced Visualizations
- **Enhanced Waterfall Charts** with country-specific colors and dynamic font sizing
- **Interactive Geographic Maps** with 80+ projection types  
- **Correlation Analysis** between greenhouse gas and environmental factors
- **Animated Charts** showing evolution over time
- **Multi-perspective Views** (value vs percentage perspectives)

### ⚙️ Smart Customization
- **Dynamic Font Sizing** for optimal text readability across different chart sizes
- **Responsive Design** that adapts to various screen sizes
- **Color-coded Countries** for consistent visual identification
- **Flexible Chart Types** (line, area, bar, pie, tree map, bubble charts)

### 🔧 Enhanced User Experience
- **Multi-page Navigation** with intuitive sidebar controls
- **Real-time Filtering** by country, time period, and measures
- **Statistical Summaries** with trend analysis
- **Export Capabilities** for data and visualizations
- **Select All** buttons for quick filter management

## 🛠️ Technology Stack

- **Frontend**: Streamlit (Latest)
- **Data Processing**: Pandas, NumPy
- **Visualizations**: Plotly (with advanced customization)
- **Backend**: Python 3.11+
- **Architecture**: Modular component-based design


## 📁 Project Structure

```
OECDDashBoard/
├── main.py                           # Main application entry point
├── requirements.txt                  # Python dependencies
├── README.md                         # Project documentation and setup guide
├── data_preprocessing.ipynb          # Data cleaning and preprocessing notebook
├── Process Book.docx                # Project documentation
├── Pages/
│   ├── 1_Introduction.py            # introduction page
│   ├── 2_dashboard.py               # Main dashboard 
│   └── Component/
│       ├── section_2.py             # summary statistics
│       └── chart_components.py      # All chart functions (modularized)
└── DataSource/
    ├── Energy/                      # Agricultural energy consumption data
    │   ├── AgriculturalEnergyConsumption.csv
    │   └── AgriculturalEnergyConsumption.csv.backup  # Original data backup
    ├── GreenHouseGas/               # Greenhouse gas emission data
    │   ├── GreenHouseGasWithoutLULUCF.csv
    │   ├── GreenHouseGasWithoutLULUCF.csv.backup     # Original data backup
    │   ├── GreenHouseGasFromLULUCF.csv
    │   ├── GreenHouseGasFromLULUCF.csv.backup        # Original data backup
    │   ├── GreenHouseGasWithLULUCF.csv
    │   ├── GreenHouseGasWithLULUCF.csv.backup        # Original data backup
    │   ├── GreenHouseGasBySectors.csv
    │   ├── GreenHouseGasBySectors.csv.backup         # Original data backup
    │   ├── GreenHouseGasByNatureSources.csv
    │   └── GreenHouseGasByNatureSources.csv.backup   # Original data backup
    ├── Land/                        # Agricultural land area data
    │   ├── AgriculturalLand.csv
    │   └── AgriculturalLand.csv.backup               # Original data backup
    ├── NutrientInputOutput/         # Nutrient flow data (placeholder)
    ├── Population/                  # Population data for correlation analysis
    │   ├── AnnualPopulationOECDCountry.csv
    │   └── AnnualPopulationOECDCountry.csv.backup    # Original data backup
    └── WaterAbstraction/            # Agricultural water usage data
        ├── AgriculturalWaterAbstraction.csv
        └── AgriculturalWaterAbstraction.csv.backup   # Original data backup
```

## 🔧 Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Jack9671/OECDDashBoard.git
   cd OECDDashBoard
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   streamlit run main.py
   ```

4. **Access the dashboard**:
   Open your browser and navigate to `http://localhost:8501`

## 📈 Usage

### Navigation
- **Sidebar Menu**: Switch between Introduction and Dashboard pages
- **Topic Selection**: Choose between Greenhouse Gas and Nutrient Input/Output analysis
- **Subtopic Filtering**: Focus on specific emission categories or environmental factors

### Enhanced Chart Features
- **Waterfall Charts**: View country contributions with dynamic text sizing
- **Geographic Maps**: Choose from 80+ projection types for global visualization  
- **Correlation Analysis**: Explore relationships between environmental indicators
- **Multi-view Charts**: Toggle between value and percentage perspectives
- **Animation Controls**: Play/pause animations to see trends over time

### Data Interaction
- **Smart Filtering**: Use "Select All" buttons for quick country/measure selection
- **Year Range Selection**: Analyze specific time periods with range sliders
- **Hover Information**: Get detailed data points by hovering over charts
- **Responsive Design**: Charts automatically adjust font sizes for optimal readability

### Data Management & Safety
- **Automatic Backup System**: Original CSV files are automatically backed up before preprocessing
- **Data Recovery**: Easy restoration from `.backup` files if needed
- **Safe Data Processing**: Non-destructive data cleaning with original preservation
- **Version Control**: Track data modifications with backup timestamps

### Export & Analysis
- Export visualizations in various formats
- Download filtered datasets for external analysis
- Statistical summaries with trend indicators

## 📊 Data Sources

All data is sourced from the Organisation for Economic Co-operation and Development (OECD):
- **OECD Environmental Statistics** - Greenhouse gas emissions and environmental indicators
- **OECD Agriculture Statistics** - Agricultural land, energy, and water consumption data  
- **OECD Green Growth Indicators** - Sustainable development metrics
- **OECD Population Statistics** - Demographic data for correlation analysis

### Supported Data Categories
- **Greenhouse Gas Emissions**: Without/From/With LULUCF, by sectors, by nature sources
- **Agricultural Energy**: Energy consumption in tonnes of oil equivalent
- **Agricultural Land**: Land area usage in hectares
- **Water Abstraction**: Agricultural water consumption in cubic meters
- **Population Data**: Annual population statistics for OECD countries
## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 📧 Contact

- **Author**: Jack9671
- **Repository**: [https://github.com/Jack9671/OECDDashBoard](https://github.com/Jack9671/OECDDashBoard)

## 🎯 Recent Enhancements (v2.0)

### ✨ Enhanced Waterfall Charts
- **Country-specific Colors**: Each country has a unique, consistent color across all charts
- **Dynamic Font Sizing**: Text automatically adjusts to fit within bar widths (8px-18px range)
- **Smart Text Positioning**: Country names inside bars, values/percentages outside
- **Improved Readability**: Better spacing and professional appearance

### 🎨 Advanced Chart Customization  
- **Multiple Projection Types**: 80+ geographic projections for global data visualization
- **Responsive Design**: Charts adapt to different screen sizes and data volumes
- **Enhanced Color Mapping**: Consistent color schemes across all visualization types
- **Professional Styling**: Improved fonts, borders, and visual hierarchy

### 🏗️ Code Architecture Improvements
- **Modular Design**: Chart functions moved to separate `chart_components.py` module
- **Better Maintainability**: Cleaner code organization with 900+ lines refactored
- **Reusable Components**: Chart functions can be imported by other modules
- **Enhanced Documentation**: Comprehensive code documentation and type hints

### 📱 User Experience Enhancements
- **Intuitive Controls**: Better toggle buttons and selection interfaces
- **Performance Optimization**: Faster chart rendering and data processing
- **Error Handling**: Improved error messages and data validation
- **Accessibility**: Better contrast and readable font sizes

## 🎯 Future Enhancements

- [ ] **Machine Learning Integration**: Predictive modeling for environmental trends
- [ ] **Advanced Statistical Analysis**: Correlation matrices and regression analysis  
- [ ] **Custom Dashboard Creation**: User-defined dashboard layouts
- [ ] **Data Download API**: Programmatic access to filtered datasets
- [ ] **Multi-language Support**: Internationalization for global users
- [ ] **Real-time Data Updates**: Live data feeds from OECD APIs
- [ ] **Mobile Optimization**: Enhanced mobile device support
- [ ] **Collaborative Features**: Share and annotate visualizations

---

*This dashboard is designed for educational and research purposes. Data accuracy depends on OECD data quality and updates.*
