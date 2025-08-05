# 🌍 OECD Data Visualization Dashboard

An interactive web-based dashboard for analyzing OECD environmental data, built with Streamlit and Python.

## 📊 Overview

This dashboard provides comprehensive visualization and analysis of OECD environmental indicators, focusing on:
- **Greenhouse Gas Emissions** (with/without LULUCF, by sectors, by nature sources)
- **Agricultural Land** usage patterns
- **Nutrient Input/Output** environmental flows

## 🚀 Features

- **Multi-page Navigation**: Seamless navigation between Home, Introduction, and Dashboard sections
- **Interactive Visualizations**: Dynamic charts with filtering and customization options
- **Real-time Analysis**: Statistical summaries and trend analysis
- **Cross-country Comparisons**: Compare environmental metrics across OECD countries
- **Export Capabilities**: Download data and visualizations for further analysis

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **Data Processing**: Pandas, NumPy
- **Visualizations**: Plotly
- **Backend**: Python 3.11+

## 📁 Project Structure

```
OECDDashBoard/
├── main.py                           # Main application entry point
├── requirements.txt                  # Python dependencies
├── Pages/
│   ├── 1_Introduction.py            # Introduction page
│   ├── 2_dashboard.py               # Main dashboard page
│   └── Component/
│       └── section_2.py             # Dashboard components
├── DataSource/
│   ├── GreenHouseGas/               # Greenhouse gas emission data
│   ├── Land/                        # Agricultural land data
│   └── NutrientInputOutput/         # Nutrient flow data
├── exploration_AgriLand.ipynb       # Agricultural data exploration
└── exploration_GHS.ipynb            # Greenhouse gas data exploration
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
- Use the **sidebar menu** to switch between different pages
- **Home**: Overview and quick statistics
- **Introduction**: Detailed information about the data and features
- **Dashboard**: Interactive data visualization and analysis

### Data Exploration
- Select different data categories from the dropdown menus
- Use filters to focus on specific countries or time periods
- Hover over charts for detailed information
- Export visualizations and data for external use

## 📊 Data Sources

All data is sourced from the Organisation for Economic Co-operation and Development (OECD):
- OECD Environmental Statistics
- OECD Agriculture and Fisheries Statistics
- OECD Green Growth Indicators

## 👥 Contributors

### 🌿 Nguyen Xuan Duy Thai
**Responsibility**: Greenhouse Gas Topic
- Developed comprehensive greenhouse gas emission analysis features
- Implemented visualization for emissions with/without LULUCF data
- Created sector-based and nature source emission categorizations
- Designed interactive charts and filtering systems for GHS data

### 🌱 Nguyen Minh Dang  
**Responsibility**: Nutrient Input/Output Topic
- Developed agricultural nutrient flow analysis components
- Implemented environmental sustainability metrics visualization
- Created correlation analysis between environmental factors
- Designed data processing pipelines for nutrient input/output data

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

## 🎯 Future Enhancements

- [ ] Add more OECD datasets
- [ ] Implement advanced statistical analysis
- [ ] Add data download functionality
- [ ] Create custom visualization templates
- [ ] Implement user authentication
- [ ] Add real-time data updates

---

*This dashboard is designed for educational and research purposes. Data accuracy depends on OECD data quality and updates.*
