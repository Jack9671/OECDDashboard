import re
from altair import value
import streamlit as st
from Pages.Component.summary_statistics import summary_statistics
from Component.chart_components import *
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')
# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="OECD Greenhouse Gas Analytics",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)
# ============================================================================
# DATA LOADING ( D:\Semester 4\Data Visualization\OECDDashBoard> C:/Users/xuant/AppData/Local/Microsoft/WindowsApps/python3.11.exe -m streamlit run "Pages\2_dashboard.py")
# ============================================================================
BASE_DIR = Path(__file__).parent.parent / 'DataSource'
@st.cache_data
def load_dataframe_for_subtopic(topic: str = 'Greenhouse Gas Output') -> dict[str, pd.DataFrame]:
    """Load all greenhouse gas datasets with error handling"""
    datasets: dict[str, pd.DataFrame] = {}
    topic_map = {
        'Greenhouse Gas Output': {
            'Without LULUCF':       BASE_DIR / 'GreenHouseGas' / 'GreenHouseGasWithoutLULUCF.csv',
            'From LULUCF':          BASE_DIR / 'GreenHouseGas' / 'GreenHouseGasFromLULUCF.csv',
            'With LULUCF':          BASE_DIR / 'GreenHouseGas' / 'GreenHouseGasWithLULUCF.csv',
            'Sector':           BASE_DIR / 'GreenHouseGas' / 'GreenHouseGasBySectors.csv',
            'Nature Source':    BASE_DIR / 'GreenHouseGas' / 'GreenHouseGasByNatureSources.csv',
        },
        'Nutrient Input and Output': {},
    }

    if topic == 'Greenhouse Gas':
        files_dict = topic_map['Greenhouse Gas Output']
        for subtopic, file_path in files_dict.items():
            try:
                df = pd.read_csv(file_path)
                datasets[subtopic] = df
            except Exception as e:
                st.error(f"Error loading {subtopic}: {e}")
    else:
        st.error(f"Data for '{topic}' is not yet implemented.")
    return datasets

@st.cache_data
def load_dataframe_for_interested_correlational_env_indicator(indicator: str) -> pd.DataFrame:
    """Load environmental indicator datasets for correlation analysis"""
    topic_map = {
        'Agricultural Energy Consumption (Tonnes of oil equivalent)': BASE_DIR / 'Energy' / 'AgriculturalEnergyConsumption.csv',
        'Agricultural Land Area (Hectares)': BASE_DIR / 'Land' / 'AgriculturalLand.csv',
        'Agricultural Water Use (Cubic meters)': BASE_DIR / 'WaterAbstraction' / 'AgriculturalWaterAbstraction.csv',
    }
    
    file_path = topic_map.get(indicator)
    if file_path and file_path.exists():
        try:
            df = pd.read_csv(file_path)
            return df
        except Exception as e:
            st.error(f"Error loading {indicator}: {e}")
            return pd.DataFrame()
    else:
        st.error(f"Data for '{indicator}' is not available or file not found.")
        return pd.DataFrame()

# ============================================================================
# Components
# ============================================================================
def user_config(df: pd.DataFrame)-> dict[str, list]:
    # Sidebar filters
    all_years = sorted(df['TIME_PERIOD'].dropna().unique().tolist())
    all_countries = sorted(df['REF_AREA'].dropna().unique().tolist())
    all_measures = sorted(df['MEASURE'].dropna().unique().tolist())
    year_range = st.sidebar.select_slider(
        "Select Year Range",
        options=all_years,
        value=(min(all_years), max(all_years))
    )
    selected_TIME_PERIOD = list(range(year_range[0], year_range[1] + 1))
    
    # Countries selection with Select All button
    st.sidebar.markdown("**Select Countries**")
    select_all_countries = st.sidebar.button("Select All", key="select_all_countries")
    
    # Initialize default countries or use session state, ensuring defaults are valid
    if 'selected_countries' not in st.session_state or not st.session_state.selected_countries:
        st.session_state.selected_countries = all_countries[:10]
    
    # Ensure selected countries are still valid (exist in current dataset)
    valid_selected_countries = [country for country in st.session_state.selected_countries if country in all_countries]
    if not valid_selected_countries:
        valid_selected_countries = all_countries[:10]
    
    if select_all_countries:
        st.session_state.selected_countries = all_countries
        valid_selected_countries = all_countries
    
    selected_REF_AREA = st.sidebar.multiselect(
        "",
        all_countries, 
        default=valid_selected_countries,
        key="countries_multiselect"
    )
    
    # Update session state with current selection
    st.session_state.selected_countries = selected_REF_AREA
    
    # Measures selection with Select All button
    st.sidebar.markdown("**Select Measures**")
    select_all_measures = st.sidebar.button("Select All", key="select_all_measures")
    
    # Initialize default measures or use session state, ensuring defaults are valid
    if 'selected_measures' not in st.session_state or not st.session_state.selected_measures:
        st.session_state.selected_measures = all_measures[:3]
    
    # Ensure selected measures are still valid (exist in current dataset)
    valid_selected_measures = [measure for measure in st.session_state.selected_measures if measure in all_measures]
    if not valid_selected_measures:
        valid_selected_measures = all_measures[:3]
    
    if select_all_measures:
        st.session_state.selected_measures = all_measures
        valid_selected_measures = all_measures
    
    selected_MEASURE = st.sidebar.multiselect(
        "",
        all_measures, 
        default=valid_selected_measures,
        key="measures_multiselect"
    )
    
    # Update session state with current selection
    st.session_state.selected_measures = selected_MEASURE
    
    return {
        "selected_TIME_PERIOD": selected_TIME_PERIOD,
        "selected_REF_AREA": selected_REF_AREA,
        "selected_MEASURE": selected_MEASURE
    }

def filter_data(df: pd.DataFrame, user_config: dict[str, str]) -> pd.DataFrame:
    selected_TIME_PERIOD = user_config.get("selected_TIME_PERIOD", np.arange(2012, 2021).tolist())
    selected_REF_AREA = user_config.get("selected_REF_AREA", ["USA"])
    selected_MEASURE = user_config.get("selected_MEASURE", [])
    # Filter the DataFrame for the selected TIME_PERIOD, REF_AREA, and MEASURE
    df = df[(df['TIME_PERIOD'].isin(selected_TIME_PERIOD)) & (df['REF_AREA'].isin(selected_REF_AREA)) & (df['MEASURE'].isin(selected_MEASURE))]
    return df

# ============================================================================
# initialize session state
# ============================================================================
if 'topic' not in st.session_state:
    st.session_state.topic = None
if 'subtopic' not in st.session_state:
    st.session_state.subtopic = None
if 'user_config' not in st.session_state:
    st.session_state.user_config = None
# ============================================================================
# MAIN DISPLAY
# ============================================================================
st.title("OECD Dashboard for Agricultural-Economic Data 🌍")

# Style the topic selection with larger text
st.markdown("""
<style>
    .stSelectbox > label {
        font-size: 24px !important;
        font-weight: bold !important;
        color: #fafafa !important;
    }
    .stSelectbox > div > div > div {
        font-size: 18px !important;
    }
</style>
""", unsafe_allow_html=True)
st.markdown("### 📊 Select Topic", unsafe_allow_html=True)
available_topics = ['Greenhouse Gas', 'Nutrient Input and Output']
st.session_state.topic = st.selectbox("", available_topics, key="topic_select") 
if st.session_state.topic == 'Greenhouse Gas':
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 🔍 Select Subtopic", unsafe_allow_html=True)
        st.session_state.subtopic = st.selectbox("", ['Without LULUCF', 'From LULUCF', 'With LULUCF', 'Sector', 'Nature Source'], index=0, key="subtopic_select")
        # Display styled explanation for each subtopic
        subtopic_info = {
            'Without LULUCF': {
                'icon': '🏭',
                'title': 'Greenhouse Gas Output (Excluding LULUCF)',
                'description': 'This analysis focuses on Greenhouse Gas Output excluding Land Use, Land-Use Change, and Forestry (LULUCF). It covers GHS output from industrial, energy, agriculture, and waste sectors.',
                'color': '#ff6b6b'
            },
            'From LULUCF': {
                'icon': '🌳',
                'title': 'Greenhouse Gas Output (From LULUCF)',
                'description': 'This analysis focuses on Greenhouse Gas Output specifically from Land Use, Land-Use Change, and Forestry (LULUCF). It includes GHS output and carbon sequestration from forests and land conversion.',
                'color': '#4ecdc4'
            },
            'With LULUCF': {
                'icon': '🌍',
                'title': 'Total Greenhouse Gas Output (Including LULUCF)',
                'description': 'This comprehensive analysis includes Greenhouse Gas Output from all sources, including Land Use, Land-Use Change, and Forestry (LULUCF). It provides the complete picture of net change in greenhouse gas output.',
                'color': '#45b7d1'
            },
            'Sector': {
                'icon': '🏗️',
                'title': 'Greenhouse Gas Output by Sectors',
                'description': 'This analysis breaks down Greenhouse Gas Output by economic sectors such as energy, industry, agriculture, transport, and waste. It helps identify which sectors contribute most to GHS output.',
                'color': '#f39c12'
            },
            'Nature Source': {
                'icon': '⚗️',
                'title': 'Greenhouse Gas Output by Nature Sources',
                'description': 'This analysis categorizes Greenhouse Gas Output by the natural sources such as cropland, grassland, wetlands, and other ecosystems. It helps understand the role of nature in greenhouse gas absorption and GHS output.',
                'color': '#9b59b6'
            }
        }
        current_info = subtopic_info[st.session_state.subtopic]
        st.markdown(f"""
        <div style="
            background-color: #0e1117;
            padding: 20px;
            border-radius: 10px;
            border-left: 5px solid {current_info['color']};
            margin: 20px 0;
            border: 1px solid #262730;
        ">
            <div style="display: flex; align-items: center; margin-bottom: 15px;">
                <span style="font-size: 24px; margin-right: 15px;">{current_info['icon']}</span>
                <span style="font-weight: bold; font-size: 20px; color: #fafafa;">{current_info['title']}</span>
            </div>
            <div style="color: #a3a8b8; font-size: 16px; line-height: 1.5;">
                {current_info['description']}
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(
            """
            <div style="text-align: center;">
            <h4>🌐 Overview of Subtopic</h4>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.plotly_chart(sunburst(), use_container_width=True)
    dfs_all_subtopics = load_dataframe_for_subtopic(st.session_state.topic) # contain { 'Without LULUCF': df1, 'From LULUCF': df2, 'With LULUCF': df3, 'Sector': df4, 'Nature Source': df5 }
    df_selected_subtopic = dfs_all_subtopics.get(st.session_state.subtopic)
    st.session_state.user_config = user_config(df_selected_subtopic)
    df_filtered = filter_data(df_selected_subtopic, st.session_state.user_config)
    #section 2: display summary statistics 
    summary_statistics(df_filtered)
    #section 3: display static map and animated map
    
    # Geographic View section with enhanced styling
    st.markdown("""
    <div style="text-align: center; margin: 40px 0 30px 0;">
        <h2 style="
            color: #fafafa; 
            font-size: 36px; 
            margin-bottom: 15px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            background: linear-gradient(45deg, #27ae60, #2ecc71);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        ">
            🌍 Geographic View
        </h2>
        <p style="
            color: #a3a8b8; 
            font-size: 18px; 
            margin-bottom: 20px;
            font-style: italic;
        ">
            Explore spatial patterns and global distributions with interactive maps
        </p>
        <div style="
            width: 100px; 
            height: 3px; 
            background: linear-gradient(45deg, #27ae60, #2ecc71); 
            margin: 0 auto;
            border-radius: 2px;
        "></div>
    </div>
    """, unsafe_allow_html=True)
    
    st.selectbox(
        "Select Projection Type",
        ['airy', 'aitoff', 'albers', 'albers usa', 'august', 'azimuthal equal area', 'azimuthal equidistant', 'baker', 'bertin1953', 'boggs', 'bonne', 'bottomley', 'bromley', 'collignon', 'conic conformal', 'conic equal area', 'conic equidistant', 'craig', 'craster', 'cylindrical equal area', 'cylindrical stereographic', 'eckert1', 'eckert2', 'eckert3', 'eckert4', 'eckert5', 'eckert6', 'eisenlohr', 'equal earth', 'equirectangular', 'fahey', 'foucaut', 'foucaut sinusoidal', 'ginzburg4', 'ginzburg5', 'ginzburg6', 'ginzburg8', 'ginzburg9', 'gnomonic', 'gringorten', 'gringorten quincuncial', 'guyou', 'hammer', 'hill', 'homolosine', 'hufnagel', 'hyperelliptical', 'kavrayskiy7', 'lagrange', 'larrivee', 'laskowski', 'loximuthal', 'mercator', 'miller', 'mollweide', 'mt flat polar parabolic', 'mt flat polar quartic', 'mt flat polar sinusoidal', 'natural earth', 'natural earth1', 'natural earth2', 'nell hammer', 'nicolosi', 'orthographic', 'patterson', 'peirce quincuncial', 'polyconic', 'rectangular polyconic', 'robinson', 'satellite', 'sinu mollweide', 'sinusoidal', 'stereographic', 'times', 'transverse mercator', 'van der grinten', 'van der grinten2', 'van der grinten3', 'van der grinten4', 'wagner4', 'wagner6', 'wiechel', 'winkel tripel', 'winkel3'],
        key='projection_type',
        index=63  # 'orthographic' is at index 63 in the list, set as default
    )
    st.toggle(" Accumulative View / Annual View", value=False, key="accumulated_ghs_toggle")
    if st.session_state.accumulated_ghs_toggle == False:
        st.plotly_chart(static_map(df_filtered, st.session_state.projection_type), use_container_width=True, key="static_map")
    else:
        st.plotly_chart(animated_map(df_filtered, st.session_state.projection_type), use_container_width=True, key="animated_map")
    
    # Analytical View section with enhanced styling
    st.markdown("""
    <div style="text-align: center; margin: 40px 0 30px 0;">
        <h2 style="
            color: #fafafa; 
            font-size: 36px; 
            margin-bottom: 15px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            background: linear-gradient(45deg, #4ecdc4, #45b7d1);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        ">
            🧮 Analytical View
        </h2>
        <p style="
            color: #a3a8b8; 
            font-size: 18px; 
            margin-bottom: 20px;
            font-style: italic;
        ">
            Dive deep into the data with comprehensive analytical tools and visualizations
        </p>
        <div style="
            width: 100px; 
            height: 3px; 
            background: linear-gradient(45deg, #4ecdc4, #45b7d1); 
            margin: 0 auto;
            border-radius: 2px;
        "></div>
    </div>
    """, unsafe_allow_html=True)
    
    st.write(df_filtered[['TIME_PERIOD', 'REF_AREA', 'MEASURE', 'OBS_VALUE']].sort_values(by=['TIME_PERIOD', 'REF_AREA', 'MEASURE']).reset_index(drop=True))
    # Styled chart configuration section
    st.markdown("### ⚙️ Chart Customization", unsafe_allow_html=True)     
    col_config1, col_config2, col_config3 = st.columns([4,2,4])
    
    with col_config1:
        x_axis_options = ['REF_AREA', 'MEASURE', 'TIME_PERIOD']
        
        selected_x_axis = st.selectbox("X-Axis Variable", x_axis_options, key="x_axis_select")
    with col_config2:
        y_axis_options = ['GHS Output']
        selected_y_axis = st.selectbox("Y-Axis Variable", y_axis_options, key="y_axis_select")
    with col_config3:
        # Filter out the selected x_axis option to prevent same selection
        category_options = ['MEASURE', 'REF_AREA']
        available_category_options = [opt for opt in category_options if opt != selected_x_axis]
        selected_category = st.selectbox("Category to compare", available_category_options, key="category_select")
    
    # Display category name based on selection
    category_name_map = {
        'MEASURE': 'GHS Gas Type',
        'REF_AREA': 'Country'
    }
    selected_category_name = category_name_map.get(selected_category, 'Category')
    # Toggle button with custom styling and icon
    col1, col2 = st.columns(2)
    with col1:
        toggle_button_1 = st.toggle("📈 Value-perspective view / 🔢 Percentage-perspective view", value=False, key="toggle_button_1")
        if toggle_button_1 == False:
            st.plotly_chart(bar_line(df_filtered, selected_x_axis, selected_category, selected_category_name), use_container_width=True, key="main_bar_chart")
        else:
            st.plotly_chart(percentage_bar_line(df_filtered, selected_x_axis, selected_category, selected_category_name), use_container_width=True, key="main_percentage_chart")
    with col2:
        toggle_button_2 = st.toggle("🌳 Tree Map / 🥧 Pie Chart", value=False, key="toggle_button_2")
        # Positive/Negative value filter for pie charts and tree maps
        value_filter = st.selectbox(" Additional configuration for pie charts/ tree maps",
                                   ["Show all contributors to GHS Emissions","Show all contributors to GHS Absorption"],
                                   key="value_filter_select", width=300)
        if toggle_button_2 == True:
            st.plotly_chart(tree_map(df_filtered, selected_category, selected_category_name, value_filter), use_container_width=True, key="tree_map_1")
        elif toggle_button_2 == False:
            st.plotly_chart(pie(df_filtered, selected_category, selected_category_name, value_filter), use_container_width=True, key="pie_chart_1")
    col1, col2 = st.columns(2)
    with col1:
        # Add icon to the toggle label for better visual cue
        toggle_button_3 = st.toggle("📊 Multi-Line Chart / 🟦 Area-Line Chart", value=False, key="toggle_button_3")
        chart_type = "area" if toggle_button_3 else "line"
        # Check for negative values in the OBS_VALUE column instead of categorical column
        min_obs_value = df_filtered['OBS_VALUE'].min()
        if min_obs_value < 0:
            st.warning(f"Warning: The selected data contains negative values, and thus the area chart is not applicable. Please use the multi-line chart instead.")
            st.plotly_chart(multi_line(df_filtered, selected_x_axis, selected_category, selected_category_name, "line"), use_container_width=True, key="multi_line_chart")
        else:
            st.plotly_chart(multi_line(df_filtered, selected_x_axis, selected_category, selected_category_name, chart_type), use_container_width=True, key="multi_line_chart")
    with col2:
        st.plotly_chart(animated_hor_bar(df_filtered, selected_category), use_container_width=True, key="animated_horizontal_bar_chart")
    
    # section 4: Correlational analysis with enhanced styling
    st.markdown("---")  # Add a separator line
    st.markdown("""
    <div style="text-align: center; margin: 30px 0;">
        <h2 style="color: #fafafa; font-size: 32px; margin-bottom: 10px;">
            🔗 Relationship between GHS Output and Environmental Factors
        </h2>
        <p style="color: #a3a8b8; font-size: 18px; margin-bottom: 20px;">
            Explore correlations between greenhouse gas output and key environmental indicators
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("#### 🌱 Select Environmental Factor", unsafe_allow_html=True)
    env_factor_options = [
        'Agricultural Energy Consumption (Tonnes of oil equivalent)', 
        'Agricultural Land Area (Hectares)', 
        'Agricultural Water Use (Cubic meters)'
    ]
    
    # Add descriptions for each environmental factor
    factor_descriptions = {
        'Agricultural Energy Consumption (Tonnes of oil equivalent)': {
            'icon': '⚡',
            'description': 'Energy used in agricultural production and processing',
            'color': '#f39c12'
        },
        'Agricultural Land Area (Hectares)': {
            'icon': '🌾',
            'description': 'Total area dedicated to agricultural activities',
            'color': '#27ae60'
        },
        'Agricultural Water Use (Cubic meters)': {
            'icon': '💧',
            'description': 'Water consumption for irrigation and livestock',
            'color': '#3498db'
        }
    }
    
    selected_env_factor = st.selectbox(
        "",
        env_factor_options,
        key="interested_correlational_env_factor"
    )
    
    # Display factor description
    factor_info = factor_descriptions[selected_env_factor]
    st.markdown(f"""
    <div style="
        background-color: #0e1117;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid {factor_info['color']};
        margin: 15px 0;
        border: 1px solid #262730;
    ">
        <div style="display: flex; align-items: center;">
            <span style="font-size: 20px; margin-right: 10px;">{factor_info['icon']}</span>
            <span style="color: #a3a8b8; font-size: 14px;">{factor_info['description']}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Load the environmental factor data
    df_env = load_dataframe_for_interested_correlational_env_indicator(st.session_state.interested_correlational_env_factor)

    # Main correlation visualization
    st.markdown("<br>", unsafe_allow_html=True)  # Add some spacing
    # Style the toggle with better visual representation
    view_toggle = st.toggle(
        "📊 Static View / 🎬 Animated View", 
        value=False, 
        key="accumulated_env_toggle"
    )
    
    # Add explanatory text for the toggle
    if view_toggle:
        st.markdown("""
        <div style="color: #a3a8b8; font-size: 12px; margin-top: 10px;">
            🎬 <strong>Animated Mode:</strong> Shows evolution over time
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="color: #a3a8b8; font-size: 12px; margin-top: 10px;">
            📊 <strong>Static Mode:</strong> Shows cumulative relationship
        </div>
        """, unsafe_allow_html=True)

    if st.session_state.accumulated_env_toggle == False:
        st.plotly_chart(static_bubble(df_filtered, df_env, st.session_state.interested_correlational_env_factor), use_container_width=True, key="static_bubble_chart")
    else:
        st.plotly_chart(animated_bubble(df_filtered, df_env, st.session_state.interested_correlational_env_factor), use_container_width=True, key="animated_bubble_chart")

    
    # Environmental factor breakdown section
    st.markdown("### 📋 Environmental Factor Breakdown Per Country (REF_AREA)", unsafe_allow_html=True)
    # Filter based on selected countries and time period only
    df_env = df_env[df_env['REF_AREA'].isin(df_filtered['REF_AREA']) & df_env['TIME_PERIOD'].isin(df_filtered['TIME_PERIOD'])]
    st.plotly_chart(water_fall(df_env, 'REF_AREA', 'MEASURE', st.session_state.interested_correlational_env_factor), use_container_width=True, key="waterfall_chart")


# Nutrient Inputs and Outputs section
elif st.session_state.topic == 'Nutrient Input and Output':
    st.markdown("## 🌾 Nutrient Input and Output")
    st.markdown("Key insights and trends from your selected nutrient data")
    st.markdown("---")

    # Load nutrient datasets
    nutrient_files = {
        'fertilisers': 'Fertilisers.csv',
        'livestock_manure': 'Livestock_manure_production.csv',
        'other_nutrient_inputs': 'Other_nutrient_inputs.csv',
        'forage': 'Forage.csv',
        'harvested_crops': 'Harvested_crops.csv'
    }

    all_dfs = {}
    for name, file in nutrient_files.items():
        try:
            df = pd.read_csv(BASE_DIR / 'Nutrient_inputs_and_outputs' / file)
            df.columns = [col.strip().replace(' ', '_').upper() for col in df.columns]
            if 'REF_AREA' in df.columns:
                df = df[~df['REF_AREA'].isin(['EU27', 'EU', 'EU27_2020', 'EU28'])]
            if 'UNIT_MULT' in df.columns:
                df['OBS_VALUE'] = pd.to_numeric(df['OBS_VALUE'], errors='coerce')
                df['OBS_VALUE'] *= 10 ** df['UNIT_MULT'].fillna(0)
            all_dfs[name] = df
        except Exception as e:
            st.warning(f"Failed to load {name}: {e}")

    # Manual mapping from notebook
    country_name_map = {
        'IDN': 'Indonesia', 'ISL': 'Iceland', 'NZL': 'New Zealand', 'KOR': 'South Korea',
        'MEX': 'Mexico', 'TUR': 'Turkey', 'PHL': 'Philippines', 'VNM': 'Vietnam',
        'UKR': 'Ukraine', 'RUS': 'Russia', 'ARG': 'Argentina', 'AUS': 'Australia',
        'AUT': 'Austria', 'BEL': 'Belgium', 'BGR': 'Bulgaria', 'BRA': 'Brazil',
        'CAN': 'Canada', 'CHE': 'Switzerland', 'CHN': 'China (People’s Republic of)',
        'COL': 'Colombia', 'CRI': 'Costa Rica', 'CYP': 'Cyprus', 'CZE': 'Czechia',
        'DEU': 'Germany', 'DNK': 'Denmark', 'ESP': 'Spain', 'EST': 'Estonia',
        'FIN': 'Finland', 'FRA': 'France', 'GBR': 'United Kingdom', 'GRC': 'Greece',
        'HRV': 'Croatia', 'HUN': 'Hungary', 'IND': 'India', 'IRL': 'Ireland',
        'ITA': 'Italy', 'JPN': 'Japan', 'KAZ': 'Kazakhstan', 'LTU': 'Lithuania',
        'LUX': 'Luxembourg', 'LVA': 'Latvia', 'MLT': 'Malta', 'NLD': 'Netherlands',
        'NOR': 'Norway', 'POL': 'Poland', 'PRT': 'Portugal', 'ROU': 'Romania',
        'SVK': 'Slovak Republic', 'SVN': 'Slovenia', 'SWE': 'Sweden', 'ZAF': 'South Africa'
    }

    st.markdown("### 🧶 Summary Statistics")
    combined = pd.concat(all_dfs.values())
    combined['TIME_PERIOD'] = pd.to_numeric(combined['TIME_PERIOD'], errors='coerce')
    dataset_info = {
        "records": len(combined),
        "time_min": int(combined['TIME_PERIOD'].min()),
        "time_max": int(combined['TIME_PERIOD'].max()),
        "countries": combined['REF_AREA'].nunique(),
        "country_list": combined['REF_AREA'].unique().tolist()
    }

    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.info(f"**Dataset Information**\n\n{dataset_info['records']} records")
        st.success(f"**Time Period**\n\n{dataset_info['time_min']} - {dataset_info['time_max']}")
    with col2:
        display_names = [country_name_map.get(c, c) for c in dataset_info['country_list'][:10]]
        countries_display = ', '.join(display_names) + ('...' if len(dataset_info['country_list']) > 10 else '')
        st.warning(f"**Countries Included**\n\n{dataset_info['countries']} countries: {countries_display}")
        st.error("**Sources**\n\nFertiliser, Livestock Manure, Others")

    st.markdown("---")

    # Year filter
    year_min = int(combined['TIME_PERIOD'].min())
    year_max = int(combined['TIME_PERIOD'].max())
    year_range = st.slider("Select Year Range", min_value=year_min, max_value=year_max, value=(year_min, year_max), step=1)
    full_years = pd.Index(range(year_range[0], year_range[1] + 1))

    # Nutrient input analysis
    nutrient_input_df = pd.concat([
        all_dfs['fertilisers'], all_dfs['livestock_manure'], all_dfs['other_nutrient_inputs']
    ], ignore_index=True).drop_duplicates()

    if all(col in nutrient_input_df.columns for col in ['REF_AREA', 'TIME_PERIOD', 'OBS_VALUE']):
        nutrient_summary = nutrient_input_df.groupby(['REF_AREA', 'TIME_PERIOD'], as_index=False)['OBS_VALUE'].sum()
        major_countries = nutrient_summary['REF_AREA'].value_counts().head(10).index.tolist()

        filtered_nutrient = nutrient_summary[
            (nutrient_summary['REF_AREA'].isin(major_countries)) &
            (nutrient_summary['TIME_PERIOD'].between(*year_range))
        ]
        pivot_nutrient = filtered_nutrient.pivot(index='TIME_PERIOD', columns='REF_AREA', values='OBS_VALUE')
        pivot_nutrient = pivot_nutrient.reindex(full_years, fill_value=0).reset_index().rename(columns={'index': 'Year'})
        pivot_nutrient.columns.name = None
        pivot_nutrient.rename(columns={col: country_name_map.get(col, col) for col in pivot_nutrient.columns}, inplace=True)

        st.plotly_chart(px.bar(
            pivot_nutrient,
            x='Year',
            y=pivot_nutrient.columns.drop('Year'),
            title='Total Nutrient Input by Country (Stacked)',
            template='plotly_dark',
            labels={'value': 'Total Input (Tonnes)', 'variable': 'Country'},
            width=1000, height=600
        ).update_layout(barmode='stack', xaxis=dict(tickmode='linear')), use_container_width=True)

        st.plotly_chart(px.line(
            pivot_nutrient,
            x='Year',
            y=pivot_nutrient.columns.drop('Year'),
            title='Nutrient Input Trends by Country',
            template='plotly_dark',
            width=1000, height=600,
            labels={'value': 'Total Input (Tonnes)', 'variable': 'Country'}
        ).update_traces(mode='lines+markers').update_layout(xaxis=dict(tickmode='linear')), use_container_width=True)

    # Forage chart (restored version)
    forage = all_dfs.get('forage')
    if forage is not None and all(col in forage.columns for col in ['REF_AREA', 'TIME_PERIOD', 'OBS_VALUE']):
        forage = forage[forage['TIME_PERIOD'].between(*year_range)]
        forage_grouped = forage.groupby(['TIME_PERIOD', 'REF_AREA'])['OBS_VALUE'].sum().reset_index()
        pivot_forage = forage_grouped.pivot(index='TIME_PERIOD', columns='REF_AREA', values='OBS_VALUE').fillna(0)
        pivot_forage.columns = [country_name_map.get(code, code) for code in pivot_forage.columns]
        year_ticks = sorted(pivot_forage.index.tolist())

        st.plotly_chart(px.bar(
            pivot_forage.reset_index(),
            y='TIME_PERIOD',
            x=pivot_forage.columns,
            orientation='h',
            title='Forage Production by Country (Stacked)',
            template='plotly_dark',
            width=1000, height=600,
            labels={'value': 'Forage (Tonnes)', 'TIME_PERIOD': 'Year', 'variable': 'Country'}
        ).update_layout(
            barmode='stack',
            yaxis=dict(tickmode='array', tickvals=year_ticks, ticktext=[str(y) for y in year_ticks]),
            legend_title_text='Country',
            xaxis_title='Production (Tonnes)',
            yaxis_title='Year'
        ), use_container_width=True)

    # Harvested Crops (unchanged)
    harvested = all_dfs.get('harvested_crops')
    if harvested is not None and all(col in harvested.columns for col in ['REF_AREA', 'TIME_PERIOD', 'OBS_VALUE']):
        harvested = harvested[harvested['TIME_PERIOD'].between(*year_range)]

        if not harvested.empty:
            latest_year = harvested['TIME_PERIOD'].max()
            crops_latest = harvested[harvested['TIME_PERIOD'] == latest_year]
            crop_sum = crops_latest.groupby('REF_AREA')['OBS_VALUE'].sum().reset_index()
            crop_sum['REF_AREA'] = crop_sum['REF_AREA'].map(country_name_map).fillna(crop_sum['REF_AREA'])

            st.plotly_chart(px.pie(
                crop_sum,
                names='REF_AREA',
                values='OBS_VALUE',
                title=f'Harvested Crops Distribution by Country ({latest_year})',
                template='plotly_dark',
                width=700, height=500
            ).update_traces(textinfo='percent+label', textposition='outside'), use_container_width=True)

            crops_grouped = harvested.groupby(['TIME_PERIOD', 'REF_AREA'])['OBS_VALUE'].sum().reset_index()
            pivot_crops = crops_grouped.pivot(index='TIME_PERIOD', columns='REF_AREA', values='OBS_VALUE')
            pivot_crops = pivot_crops.reindex(full_years, fill_value=0).reset_index().rename(columns={'index': 'Year'})
            pivot_crops.columns.name = None
            pivot_crops.rename(columns={col: country_name_map.get(col, col) for col in pivot_crops.columns}, inplace=True)

            st.plotly_chart(px.line(
                pivot_crops,
                x='Year',
                y=pivot_crops.columns.drop('Year'),
                title='Harvested Crops Trends by Country',
                template='plotly_dark',
                width=1000, height=600,
                labels={'value': 'Harvested (Tonnes)', 'variable': 'Country'}
            ).update_traces(mode='lines+markers').update_layout(xaxis=dict(tickmode='linear')), use_container_width=True)

    st.markdown("---")
    st.markdown("### 📊 Analytical View")
    st.dataframe(combined.head(100))
