import re
from altair import value
import streamlit as st
from Component.section_2 import section_2
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
BASE_DIR = Path(__file__).parent.parent / 'DataSource' / 'GreenHouseGas'
@st.cache_data
def load_dataframe_for_subtopic(topic: str = 'Greenhouse Gas Output') -> dict[str, pd.DataFrame]:
    """Load all greenhouse gas datasets with error handling"""
    datasets: dict[str, pd.DataFrame] = {}
    topic_map = {
        'Greenhouse Gas Output': {
            'Without LULUCF':       BASE_DIR / 'GreenHouseGasWithoutLULUCF.csv',
            'From LULUCF':          BASE_DIR / 'GreenHouseGasFromLULUCF.csv',
            'With LULUCF':          BASE_DIR / 'GreenHouseGasWithLULUCF.csv',
            'Sector':           BASE_DIR / 'GreenHouseGasBySectors.csv',
            'Nature Source':    BASE_DIR / 'GreenHouseGasByNatureSources.csv',
        },
        'Nutrient Input and Output': {},
        'Land': {},
        'Livestock': {}
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
    
    selected_REF_AREA = st.sidebar.multiselect("Select Countries", all_countries, default=all_countries[:10])
    selected_MEASURE = st.sidebar.multiselect("Select Gases", all_measures, default=all_measures[:3])
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

def sunburst(): # used for the sunburst chart
    data = {
        'level1': [
            # Without LULUCF (6 items)
            'GHS', 'GHS', 'GHS', 'GHS', 'GHS', 'GHS',
            # From LULUCF (3 items)
            'GHS', 'GHS', 'GHS',
            # With LULUCF (6 items)
            'GHS', 'GHS', 'GHS', 'GHS', 'GHS', 'GHS',
            # By Sector (8 items)
            'GHS', 'GHS', 'GHS', 'GHS', 'GHS', 'GHS', 'GHS', 'GHS',
            # By Nature Source (22 items)
            'GHS', 'GHS', 'GHS', 'GHS', 'GHS', 'GHS', 'GHS', 'GHS', 'GHS', 'GHS', 'GHS', 'GHS', 'GHS', 'GHS', 'GHS', 'GHS', 'GHS', 'GHS', 'GHS', 'GHS', 'GHS', 'GHS'
        ],
        'level2': [
            # Without LULUCF (6 items)
            'Without LULUCF', 'Without LULUCF', 'Without LULUCF', 'Without LULUCF', 'Without LULUCF', 'Without LULUCF',
            # From LULUCF (3 items)
            'From LULUCF', 'From LULUCF', 'From LULUCF',
            # With LULUCF (6 items)
            'With LULUCF', 'With LULUCF', 'With LULUCF', 'With LULUCF', 'With LULUCF', 'With LULUCF',
            # Sector (8 items)
            'Sector', 'Sector', 'Sector', 'Sector', 'Sector', 'Sector', 'Sector', 'Sector',
            # Nature Source (22 items)
            'Nature Source', 'Nature Source', 'Nature Source', 'Nature Source', 'Nature Source', 'Nature Source', 'Nature Source', 'Nature Source', 'Nature Source', 'Nature Source', 'Nature Source', 'Nature Source', 'Nature Source', 'Nature Source', 'Nature Source', 'Nature Source', 'Nature Source', 'Nature Source', 'Nature Source', 'Nature Source', 'Nature Source', 'Nature Source'
            ],
            'level3': [
            # Without LULUCF (6 items)
            'CH4', 'CO2', 'HFC', 'N2O', 'PFC', 'SF',
            # From LULUCF (3 items)
            'CH4_LULUCF', 'CO2_LULUCF', 'N2O_LULUCF',
            # With LULUCF (6 items)
            'CH4', 'CO2', 'HFC', 'N2O', 'PFC', 'SF',
            # By Sector (8 items)
            'TR', 'IPP', 'EI', 'AGR', 'OTH_SECTOR', 'MIC', 'WASTE', 'OTH',
            # By Nature Source (22 items)
            'SETT_CO2', 'CL_CH4', 'CL_CO2', 'OT_N2O', 'GL_N2O', 'GL_CO2', 'GL_CH4', 'F_N2O', 'WET_N2O', 'HWP_CO2', 'F_CH4', 'F_CO2', 'SETT_N2O', 'SETT_CH4', 'CL_N2O', 'WET_CH4', 'OTHER_CO2', 'OTHER_N2O', 'OT_CO2', 'OTHER_CH4', 'OT_CH4', 'WET_CO2'
        ]
    }
    # Create DataFrame and sunburst chart
    df = pd.DataFrame(data)
    #dark theme
    fig = px.sunburst(df, path=['level1', 'level2', 'level3'], template='plotly_dark')
    #increase the radius of the sunburst chart
    fig.update_layout(margin=dict(t=0, l=0, r=0, b=0), font = dict(size=20))
    return fig

def static_map(df: pd.DataFrame, projection_type: str = 'mercator') -> go.Figure:
    df_sum = df.groupby('REF_AREA')['OBS_VALUE'].sum().reset_index()
    fig = px.choropleth(
        df_sum,
        locations='REF_AREA',
        locationmode='ISO-3',
        color='OBS_VALUE',
        color_continuous_scale=px.colors.sequential.Viridis_r,
        title="GHS output by country",
        labels={'OBS_VALUE':'Total Gas Output (tonnes)', 'REF_AREA':'Country'},
        range_color=[0, df_sum['OBS_VALUE'].max()],
        template='plotly_dark',
        width=500,
        height=500
    )
    fig.update_layout(
        geo=dict(
            showframe=False,
            showcoastlines=True,
            oceancolor='LightBlue',
            landcolor='White',
            projection_type= projection_type,
            showocean=True
        ),
    )
    return fig

def animated_map(df: pd.DataFrame, projection_type: str = 'mercator'):
    df_map_animated = df.groupby(['REF_AREA', 'TIME_PERIOD'])['OBS_VALUE'].sum().reset_index()
    # Create animated choropleth map
    fig_animated = px.choropleth(df_map_animated,
                                locations='REF_AREA',
                                locationmode='ISO-3',
                                color='OBS_VALUE',
                                color_continuous_scale=px.colors.sequential.Viridis_r,
                                animation_frame='TIME_PERIOD',
                                title=f"Evolution of GHS Distribution per Year",
                                labels={'OBS_VALUE': 'Total Gas Output (in tonnes)',
                                    'REF_AREA': 'Country Code',
                                    'TIME_PERIOD': 'Year'},
                                range_color=[0, df_map_animated['OBS_VALUE'].max()],
                                template='plotly_dark',
                                width=600,
                                height=600
    )
    fig_animated.update_layout(
        geo=dict(
            showframe=False,
            showcoastlines=True,
            oceancolor='LightBlue',
            landcolor='White',
            projection_type= projection_type,
            showocean=True
        ),
    )
    return fig_animated

def bar_line(df: pd.DataFrame, x_axis_variable: str, category_to_stack: str, category_name: str) -> go.Figure:
    df_pivoted = df.pivot_table(index=x_axis_variable, columns=category_to_stack, values='OBS_VALUE', aggfunc='sum').reset_index()
    # Add 'total' column for total greenhouse gas output using only available measures
    df_pivoted['total'] = df_pivoted.iloc[:, 1:].sum(axis=1)

    # Create a stacked bar chart using Plotly Express
    fig_stacked = px.bar(df_pivoted, x=x_axis_variable, y=df_pivoted.columns[1:-1],  # Exclude 'total' column
                        title=f"GHS output of accumulated sum of all {category_name} per {x_axis_variable}",
                        labels= {'value': 'Gas Output (in tonnes)', 'variable': category_name},
                        template='plotly_dark', width=700, height=600, barmode ='relative')

    fig_stacked.update_traces(marker=dict(line=dict(width=1, color='DarkSlateGrey')))

    # Update the layout to stack the bars properly
    fig_stacked.update_layout(barmode='stack')

    # Function to format large numbers
    def format_number(value):
        if pd.isna(value) or value == 0:
            return "0"
        elif abs(value) >= 1e9:
            return f"{value/1e9:.1f}B"
        elif abs(value) >= 1e6:
            return f"{value/1e6:.1f}M"
        elif abs(value) >= 1e3:
            return f"{value/1e3:.1f}k"
        else:
            return f"{value:.0f}"

    # Enhanced Percentage Calculation with Negative Value Handling
    # Calculate percentages for each year with negative value support
    df_percentage = df_pivoted.copy()
    measure_columns_for_text = df_pivoted.columns[1:-1]  # Exclude TIME_PERIOD and total

    # Calculate absolute total for each row (for proper percentage calculation including negatives)
    df_percentage['abs_total'] = df_pivoted[measure_columns_for_text].abs().sum(axis=1)

    # Calculate percentages based on absolute values while preserving sign
    for col in measure_columns_for_text:
        df_percentage[col] = (df_pivoted[col].abs() / df_percentage['abs_total']) * 100 * np.sign(df_pivoted[col])
    # Update each trace individually with custom text formatting (both value and percentage)
    for i, trace in enumerate(fig_stacked.data):
        if i < len(measure_columns_for_text):  
            # Get the column name for this trace
            col_name = measure_columns_for_text[i]
            # Create custom text for this trace combining formatted number and percentage
            custom_text = []
            custom_hover = []
            for j, (val, pct) in enumerate(zip(df_pivoted[col_name], df_percentage[col_name])):
                formatted_val = format_number(val)
                formatted_pct = f"{abs(pct):.1f}%" 
                custom_text.append(f"{formatted_val}<br>({formatted_pct})")                
                # Create custom hover text for each data point
                x_value = df_pivoted.iloc[j][x_axis_variable]
                formatted_val_hover = format_number(val) if not pd.isna(val) else "0"
                pct_hover = f"{abs(pct):.2f}%" if not pd.isna(pct) else "0%"
                custom_hover.append(
                    f"<b>{x_axis_variable}:</b> {x_value}<br>"
                    f"<b>{category_name}:</b> {col_name}<br>"
                    f"<b>Value:</b> {formatted_val_hover} tons<br>"
                    f"<b>Percentage:</b> {pct_hover}<extra></extra>"
                )
            
            # Update the trace with custom text and hover template
            fig_stacked.data[i].update(
                text=custom_text,
                textposition='inside',
                textfont_size=15,  # Reduced font size slightly to fit both lines
                textfont_color='white',
                hovertemplate=custom_hover,
                customdata=list(zip(df_pivoted[col_name], df_percentage[col_name]))
            )

    # Function to calculate font size based on bar width
    def calculate_font_size(text_length, bar_width_px, min_font_size=8, max_font_size=16):
        """
        Calculate font size based on text length and available bar width
        Assumes average character width is about 0.6 times the font size
        """
        # Estimated character width ratio (varies by font, but ~0.6 is reasonable for most fonts)
        char_width_ratio = 0.6
        
        # Calculate maximum font size that would fit
        max_possible_font_size = bar_width_px / (text_length * char_width_ratio)
        
        # Constrain between min and max font sizes
        font_size = max(min_font_size, min(max_possible_font_size, max_font_size))
        
        return int(font_size)

    # Calculate bar width in pixels
    plot_width = 700
    num_bars = len(df_pivoted)
    # Estimate available width for bars (accounting for margins, axes, etc.)
    available_width = plot_width * 0.8  # 80% of plot width for actual bars
    bar_width_px = available_width / num_bars * 0.8  # 80% of available space per bar (for gaps)

    # Find the maximum text length across all bars
    max_text_length = 0
    formatted_texts = []

    for i, row in df_pivoted.iterrows():
        formatted_text = format_number(row['total'])
        formatted_texts.append(formatted_text)
        text_length = len(formatted_text)
        max_text_length = max(max_text_length, text_length)

    # Calculate font size based on the maximum text length
    uniform_font_size = calculate_font_size(max_text_length, bar_width_px)

    # Add total value annotations on top of each stacked bar with uniform font sizing
    for i, row in df_pivoted.iterrows():
        fig_stacked.add_annotation(
            x=row[x_axis_variable],
            y=row['total'],
            text=formatted_texts[i],
            showarrow=False,
            yshift=10,
            font=dict(size=uniform_font_size, color="white", family="Arial")
        )
    # Add line trace for totals (net sum)
    fig_stacked.add_trace(go.Scatter(
        x=df_pivoted[x_axis_variable],
        y=df_pivoted['total'],
        mode='lines+markers',
        name='net accumulative sum',
        line=dict(color='yellow', width=3, shape='linear'),
        marker=dict(size=7, color='yellow', symbol='circle'),
        yaxis='y',
        hovertemplate=f'<b>{x_axis_variable}:</b> %{{x}}<br><b>Total:</b> %{{y:,.0f}} tonnes<extra></extra>'
    ))
    return fig_stacked

def percentage_bar_line(df: pd.DataFrame, x_axis_variable: str, category_to_stack: str, category_name: str) -> go.Figure:
    # Create the pivot table for percentage calculations
    df_pivoted_for_percentage = df.pivot_table(index=x_axis_variable, columns=category_to_stack, values='OBS_VALUE', aggfunc='sum').reset_index()

    # Calculate percentages 
    df_percentage = df_pivoted_for_percentage.copy()
    measure_columns = df_percentage.columns[1:]  

    # Store original values for display
    df_original = df_pivoted_for_percentage.copy()

    # Calculate absolute total for each row (for proper percentage calculation)
    df_percentage['abs_total'] = df_percentage[measure_columns].abs().sum(axis=1)
    # Calculate percentage for each segment within each bar
    for col in measure_columns:
        df_percentage[col] = (df_pivoted_for_percentage[col].abs() / df_percentage['abs_total']) * 100 * np.sign(df_pivoted_for_percentage[col])
    # Fill NaN values with 0
    df_percentage = df_percentage.fillna(0)
    # Function to format large numbers
    def format_number(value):
        if pd.isna(value) or value == 0:
            return "0"
        elif abs(value) >= 1e9:
            return f"{value/1e9:.1f}B"
        elif abs(value) >= 1e6:
            return f"{value/1e6:.1f}M"
        elif abs(value) >= 1e3:
            return f"{value/1e3:.1f}k"
        else:
            return f"{value:.0f}"
    # Create the enhanced stacked bar chart
    fig_detailed = px.bar(df_percentage, 
                        x=x_axis_variable,
                        y=measure_columns,
                        title=f"GHS output of accumulated sum of all {category_name} per {x_axis_variable}",
                        labels={
                            x_axis_variable: x_axis_variable,
                            'value': 'Percentage (%)',
                            'variable': category_name
                        },
                        template='plotly_dark',
                        width=800, height=600)

    fig_detailed.update_traces(marker=dict(line=dict(width=1, color='DarkSlateGrey')))

    # Update layout for proper negative/positive handling
    fig_detailed.update_layout(
        barmode='relative',  # This enables proper stacking with positive/negative separation
        yaxis=dict(
            ticksuffix='%',
            title='Percentage (%)',
            zeroline=True,
            zerolinewidth=3,
            zerolinecolor='white'
        )
    )

    # Add a prominent horizontal line at y=0 for better visual separation
    fig_detailed.add_hline(y=0, line_dash="solid", line_color="white", line_width=3)
    # Update each trace with both values and percentages in text and hover for percentage chart
    for i, trace in enumerate(fig_detailed.data):
        if i < len(measure_columns):
            col_name = measure_columns[i]
            
            # Create custom text and hover for each data point
            custom_text = []
            custom_hover = []
            
            for j, row in df_percentage.iterrows():
                x_value = row[x_axis_variable]
                percentage = row[col_name]
                original_value = df_original.loc[j, col_name]
                
                formatted_val = format_number(original_value)
                pct_display = f"{abs(percentage):.1f}%"  
                custom_text.append(f"{formatted_val}<br>({pct_display})")

                # Hover information (always show both)
                custom_hover.append(
                    f"<b>{x_axis_variable}:</b> {x_value}<br>"
                    f"<b>{category_name}:</b> {col_name}<br>"
                    f"<b>Value:</b> {formatted_val} tons<br>"
                    f"<b>Percentage:</b> {pct_display}<extra></extra>"
                )
            
            # Update the trace with custom text and hover
            fig_detailed.data[i].update(
                text=custom_text,
                textposition='inside',
                textfont_size=8,
                textfont_color='white',
                hovertemplate=custom_hover
            )
    # Hide the y-axis ticks for cleaner appearance
    fig_detailed.update_yaxes(ticks="", showticklabels=False)
    return fig_detailed

def get_color_mapping(df: pd.DataFrame, column_name: str = 'MEASURE') -> dict:
    """Create consistent color mapping for specified column"""
    # Check if the column exists in the dataframe
    if column_name not in df.columns:
        # If the specified column doesn't exist, create a simple color mapping based on unique values in the first non-numeric column
        text_columns = df.select_dtypes(include=['object', 'string']).columns
        if len(text_columns) > 0:
            column_name = text_columns[0]
        else:
            # Fallback: return empty dict if no suitable column found
            return {}
    
    # Get unique values and sort them for consistent ordering
    unique_values = sorted(df[column_name].unique())
    default_colors = px.colors.qualitative.Plotly
    
    color_map = {}
    for i, value in enumerate(unique_values):
        color_map[value] = default_colors[i % len(default_colors)]
    
    return color_map

def multi_line(df: pd.DataFrame, x_axis_variable: str, variable_for_category: str, category_name: str, chart_type: str = "line") -> go.Figure:
    df_pivoted = df.pivot_table(index='TIME_PERIOD', columns=variable_for_category, values='OBS_VALUE', aggfunc='sum').reset_index()
    # Add 'total' column for total greenhouse gas output using only available measures
    df_pivoted['total'] = df_pivoted.iloc[:, 1:].sum(axis=1)
    # sort column order of df_pivoted by alphabetical order of measures
    df_pivoted = df_pivoted[['TIME_PERIOD'] + sorted(df_pivoted.columns[1:-1].tolist()) + ['total']]
    # Get consistent color mapping
    color_map = get_color_mapping(df, 'MEASURE')
    if chart_type == "area":
        fig_line = px.area(df_pivoted, x='TIME_PERIOD', y=df_pivoted.columns[1:-1],  # Exclude 'total' column
                          title=f"Accumulative GHS output for each {category_name} of each {x_axis_variable} per Year",
                          labels={'TIME_PERIOD': 'Year', 'value': 'Gas Output (in tonnes)', 'variable': category_name},
                          template='plotly_dark', width=700, height=600,
                          color_discrete_map=color_map)
        fig_line.update_traces(
            line=dict(width=0),  # No line border
        )
        # Add border lines to separate areas
        fig_line.update_traces(marker=dict(line=dict(width=1, color='DarkSlateGrey')))
        
        # Calculate definite integral (area under curve) for each measure
        measure_columns = df_pivoted.columns[1:-1]  # Exclude TIME_PERIOD and total
        areas = {}
        total_area = 0
        
        # Function to format large numbers
        def format_area_number(value):
            if pd.isna(value) or value == 0:
                return "0"
            elif abs(value) >= 1e12:
                return f"{value/1e12:.1f}T"
            elif abs(value) >= 1e9:
                return f"{value/1e9:.1f}B"
            elif abs(value) >= 1e6:
                return f"{value/1e6:.1f}M"
            elif abs(value) >= 1e3:
                return f"{value/1e3:.1f}K"
            else:
                return f"{value:.0f}"
        
        # Calculate area using trapezoidal rule for each measure
        for measure in measure_columns:
            # Get the y-values for this measure
            y_values = df_pivoted[measure].fillna(0)
            x_values = df_pivoted['TIME_PERIOD']
            
            # Calculate area using trapezoidal integration
            if len(y_values) > 1:
                area = np.trapz(y_values, x_values)
                areas[measure] = abs(area)  # Use absolute value for area calculation
                total_area += abs(area)
            else:
                areas[measure] = 0
        
        # Calculate percentages and add annotations
        if total_area > 0:
            for i, measure in enumerate(measure_columns):
                area_value = areas[measure]
                percentage = (area_value / total_area) * 100

                font_size = max(1, int(12 * (area_value / total_area)))  # Ensure font size is at least 1

                # Find the middle position for annotation placement
                middle_year_idx = len(df_pivoted) // 2
                middle_year = df_pivoted.iloc[middle_year_idx]['TIME_PERIOD']
                
                # Calculate the y-position for annotation (middle of the layer)
                cumulative_sum = df_pivoted[measure_columns[:i+1]].sum(axis=1)
                previous_sum = df_pivoted[measure_columns[:i]].sum(axis=1) if i > 0 else 0
                y_position = (cumulative_sum.iloc[middle_year_idx] + previous_sum.iloc[middle_year_idx]) / 2 if i > 0 else cumulative_sum.iloc[middle_year_idx] / 2
                
                # Format the area value
                formatted_area = format_area_number(area_value)
                
                # Add annotation with area and percentage
                fig_line.add_annotation(
                    x=middle_year,
                    y=y_position,
                    text=f"{measure}<br>Area: {formatted_area}<br>{percentage:.1f}%",
                    showarrow=False,
                    font=dict(size=font_size, color="white", family="Arial Black"),
                    bgcolor="rgba(0,0,0,0.7)",
                    bordercolor="white",
                    borderwidth=1,
                    borderpad=1,
                    xanchor="center",
                    yanchor="middle"
                )
    else:
        # Create a normal line chart using Plotly Express with explicit color mapping
        fig_line = px.line(df_pivoted, x='TIME_PERIOD', y=df_pivoted.columns[1:-1],  # Exclude 'total' column
                          title=f"GHS output for each {category_name} per Year",
                          labels={'TIME_PERIOD': 'Year', 'value': 'Gas Output (in tonnes)', 'variable': category_name},
                          template='plotly_dark', width=700, height=600,
                          color_discrete_map=color_map)
        fig_line.update_traces(mode='lines+markers', marker=dict(size=7), line=dict(width=3))
    
    return fig_line


def animated_hor_bar(df: pd.DataFrame, col_to_rank: str) -> go.Figure:
    groupby_var = [col_to_rank, 'TIME_PERIOD']
    columns_to_count = ['OBS_VALUE']
    
    # Group the DataFrame by the specified variable and sum the OBS_VALUE
    df_grouped = df.groupby(groupby_var)[columns_to_count].sum().reset_index()

    # Sort by TIME_PERIOD first, then by OBS_VALUE in descending order for proper animation
    # This ensures highest bars appear on top in each frame
    df_sorted = df_grouped.sort_values(['TIME_PERIOD', 'OBS_VALUE'], ascending=[True, False])

    # Use the same consistent color mapping as the line chart
    color_map = get_color_mapping(df, col_to_rank)

    # Create animated horizontal bar chart
    fig = px.bar(df_sorted,
                x='OBS_VALUE', y= col_to_rank,
                title=f"Evolution of GHS output for each {col_to_rank} per year",
                labels={'OBS_VALUE': 'Gas Output (in tonnes)'},
                color_discrete_map=color_map,
                color= col_to_rank,
                animation_frame='TIME_PERIOD',
                animation_group= col_to_rank,
                template='plotly_dark',
                width=800, height=700,
                # Add range for consistent x-axis across all frames
                range_x=[0, df_grouped['OBS_VALUE'].max() * 1.1])

    # Add text labels and border styling
    fig.update_traces(
        texttemplate='%{x:.2s}', 
        textposition='outside',
        marker=dict(line=dict(width=1, color='DarkSlateGrey')),
        # Add hover template for better interactivity
        hovertemplate='<b>%{y}</b><br>' +
                     'Gas Output: %{x:,.0f} tonnes<br>' +
                     'Year: %{customdata}<br>' +
                     '<extra></extra>'
    )

    # Configure animation settings for smooth transitions
    fig.update_layout(
        # Animation configuration
        updatemenus=[{
            'type': 'buttons',
            'showactive': False,
            'buttons': [
                {
                    'label': '▶️ Play',
                    'method': 'animate',
                    'args': [None, {
                        'frame': {'duration': 800, 'redraw': True},
                        'transition': {'duration': 300, 'easing': 'cubic-in-out'},
                        'fromcurrent': True
                    }]
                },
                {
                    'label': '⏸️ Pause',
                    'method': 'animate',
                    'args': [[None], {
                        'frame': {'duration': 0, 'redraw': False},
                        'mode': 'immediate',
                        'transition': {'duration': 0}
                    }]
                }
            ],
            'x': 0.1, 'y': 0, 'xanchor': 'right', 'yanchor': 'top'
        }],
        # Ensure y-axis ordering is maintained
        yaxis=dict(
            categoryorder='total ascending',  # This ensures dynamic sorting by value
            title= col_to_rank.replace('_', ' ').title(),
        ),
        xaxis=dict(
            title='Gas Output (in tonnes)'
        ),
        # Add slider for manual frame control
        sliders=[{
            'steps': [
                {
                    'args': [[f], {
                        'frame': {'duration': 300, 'redraw': True},
                        'mode': 'immediate',
                        'transition': {'duration': 300}
                    }],
                    'label': str(f),
                    'method': 'animate'
                } for f in sorted(df_grouped['TIME_PERIOD'].unique())
            ],
            'active': 0,
            'currentvalue': {'prefix': 'Year: '},
            'len': 0.9,
            'x': 0.1,
            'xanchor': 'left',
            'y': 0,
            'yanchor': 'top'
        }]
    )

    # Add custom data for hover information
    for frame in fig.frames:
        for trace in frame.data:
            # Add year information to hover
            trace.customdata = [frame.name] * len(trace.x)
    return fig

def pie(df: pd.DataFrame, groupby_var: str, category_name: str, value_filter: str = "All Values") -> go.Figure:
    columns_to_count = ['OBS_VALUE']
    # Group the DataFrame by the specified variable and sum the OBS_VALUE
    df_grouped = df.groupby(groupby_var)[columns_to_count].sum().reset_index()
    # Apply value filtering for positive/negative values
    if value_filter == "Show all contributors to GHS Emissions":
        df_grouped = df_grouped[df_grouped['OBS_VALUE'] >= 0]
        title_suffix = " (Positive Values)"
    elif value_filter == "Show all contributors to GHS Absorption":
        df_grouped = df_grouped[df_grouped['OBS_VALUE'] < 0]
        # Convert negative values to positive for display purposes
        #df_grouped['OBS_VALUE'] = df_grouped['OBS_VALUE'].abs()
        title_suffix = " (Negative Values - Absolute)"
    else:
        title_suffix = ""
    # Check if we have data after filtering
    if df_grouped.empty or df_grouped['OBS_VALUE'].sum() == 0:
        # Create empty figure with message
        fig = go.Figure()
        fig.add_annotation(
            text=f"No {value_filter.lower()} found in the selected data",
            xref="paper", yref="paper",
            x=0.5, y=0.5, xanchor='center', yanchor='middle',
            showarrow=False, font=dict(size=16, color='white')
        )
        fig.update_layout(
            template='plotly_dark',
            title=f"Proportion of {category_name}",
            width=700, height=600
        )
        return fig
    
    # Ensure the OBS_VALUE is in percentage format
    df_grouped['OBS_VALUE'] = (df_grouped['OBS_VALUE'] / df_grouped['OBS_VALUE'].sum()) * 100
    # Get consistent color mapping based on the groupby variable
    color_map = get_color_mapping(df_grouped, groupby_var)
    fig = px.pie(df_grouped, values='OBS_VALUE', names=groupby_var,
                 title=f"Proportion of {category_name}",
                 color=groupby_var,
                 color_discrete_map=color_map,
                 labels={groupby_var: category_name, 'OBS_VALUE': 'Percentage (%)'},
                 template='plotly_dark', width=700, height=600)
    fig.update_traces(marker=dict(line=dict(width=1, color='DarkSlateGrey')),
                      textposition='inside', textinfo='label+percent')
    fig.update_layout(showlegend=True, title_x=0.5, font=dict(size=25))
    return fig

def tree_map(df: pd.DataFrame, groupby_var: str, category_name: str, value_filter: str = "All Values") -> go.Figure:
    columns_to_count = ['OBS_VALUE']
    # Group the DataFrame by the specified variable and sum the OBS_VALUE
    df_grouped = df.groupby(groupby_var)[columns_to_count].sum().reset_index()
    
    # Apply value filtering for positive/negative values
    if value_filter == "Show all contributors to GHS Emissions":
        df_grouped = df_grouped[df_grouped['OBS_VALUE'] >= 0]
        title_suffix = " (Positive Values)"
    elif value_filter == "Show all contributors to GHS Absorption":
        df_grouped = df_grouped[df_grouped['OBS_VALUE'] < 0]
        # Convert negative values to positive for display purposes
        df_grouped['OBS_VALUE'] = df_grouped['OBS_VALUE'].abs()
        title_suffix = " (Negative Values - Absolute)"
    else:
        title_suffix = ""
    
    # Check if we have data after filtering
    if df_grouped.empty or df_grouped['OBS_VALUE'].sum() == 0:
        # Create empty figure with message
        fig = go.Figure()
        fig.add_annotation(
            text=f"No {value_filter.lower()} found in the selected data",
            xref="paper", yref="paper",
            x=0.5, y=0.5, xanchor='center', yanchor='middle',
            showarrow=False, font=dict(size=16, color='white')
        )
        fig.update_layout(
            template='plotly_dark',
            title=f"Tree Map of {category_name}",
            width=700, height=600, font=dict(size=25)
        )
        return fig
    
    # Calculate percentage for each category
    df_grouped['percentage'] = (df_grouped['OBS_VALUE'] / df_grouped['OBS_VALUE'].sum()) * 100
    # Create custom text with gas type and percentage
    df_grouped['custom_text'] = df_grouped.apply(
        lambda row: f"{row[groupby_var]}<br>{row['percentage']:.1f}%", axis=1
    )

    # Get consistent color mapping based on the groupby variable
    color_map = get_color_mapping(df_grouped, groupby_var)

    # Create the treemap with custom text
    fig = px.treemap(df_grouped, 
                     path=[groupby_var], 
                     values='OBS_VALUE',
                     title=f"Tree Map of {category_name}",
                     color=groupby_var,
                     color_discrete_map=color_map,
                     labels={groupby_var: category_name, 'OBS_VALUE': 'Value'},
                     template='plotly_dark', 
                     width=700, 
                     height=600)
    
    # Update traces with centered text and dynamic font sizing
    fig.update_traces(
        textposition='middle center',
        textfont=dict(
            color='white',
            family='Arial Black'
        ),
        texttemplate='%{customdata[0]}',
        marker=dict(line=dict(width=2, color='DarkSlateGrey'))
    )
    # Set customdata to use the custom_text column for texttemplate
    fig.data[0].customdata = np.array(df_grouped[['custom_text']])
    # Update layout
    fig.update_layout(
        title_x=0.5,
        font=dict(size=25)
    )
    
    return fig
# ============================================================================
# initialize session state
# ============================================================================
if 'topic' not in st.session_state:
    st.session_state.topic = None
if 'subtopic' not in st.session_state:
    st.session_state.subtopic = None
if 'user_config' not in st.session_state:
    st.session_state.user_config = None
if 'projection_type' not in st.session_state:
    st.session_state.projection_type = 'orthographic'  # Default projection type



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
                'title': 'Greenhouse Gas Emissions (Excluding LULUCF)',
                'description': 'This analysis focuses on Greenhouse Gas Output excluding Land Use, Land-Use Change, and Forestry (LULUCF). It covers emissions from industrial, energy, agriculture, and waste sectors.',
                'color': '#ff6b6b'
            },
            'From LULUCF': {
                'icon': '🌳',
                'title': 'Greenhouse Gas Emissions (From LULUCF)',
                'description': 'This analysis focuses on Greenhouse Gas Output specifically from Land Use, Land-Use Change, and Forestry (LULUCF). It includes emissions and carbon sequestration from forests and land conversion.',
                'color': '#4ecdc4'
            },
            'With LULUCF': {
                'icon': '🌍',
                'title': 'Total Greenhouse Gas Emissions (Including LULUCF)',
                'description': 'This comprehensive analysis includes Greenhouse Gas Output from all sources, including Land Use, Land-Use Change, and Forestry (LULUCF). It provides the complete picture of net change in greenhouse gas output.',
                'color': '#45b7d1'
            },
            'Sector': {
                'icon': '🏗️',
                'title': 'Greenhouse Gas Emissions by Sectors',
                'description': 'This analysis breaks down Greenhouse Gas Output by economic sectors such as energy, industry, agriculture, transport, and waste. It helps identify which sectors contribute most to emissions.',
                'color': '#f39c12'
            },
            'Nature Source': {
                'icon': '⚗️',
                'title': 'Greenhouse Gas Emissions by Nature Sources',
                'description': 'This analysis categorizes Greenhouse Gas Output by the natural sources such as cropland, grassland, wetlands, and other ecosystems. It helps understand the role of nature in greenhouse gas absorption and emissions.',
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
    section_2(df_filtered)
    #section 3: display static map and animated map
    st.write(f"## Geographic View")
    st.selectbox("Select Projection Type", ['airy', 'aitoff', 'albers', 'albers usa', 'august', 'azimuthal equal area', 'azimuthal equidistant', 'baker', 'bertin1953', 'boggs', 'bonne', 'bottomley', 'bromley', 'collignon', 'conic conformal', 'conic equal area', 'conic equidistant', 'craig', 'craster', 'cylindrical equal area', 'cylindrical stereographic', 'eckert1', 'eckert2', 'eckert3', 'eckert4', 'eckert5', 'eckert6', 'eisenlohr', 'equal earth', 'equirectangular', 'fahey', 'foucaut', 'foucaut sinusoidal', 'ginzburg4', 'ginzburg5', 'ginzburg6', 'ginzburg8', 'ginzburg9', 'gnomonic', 'gringorten', 'gringorten quincuncial', 'guyou', 'hammer', 'hill', 'homolosine', 'hufnagel', 'hyperelliptical', 'kavrayskiy7', 'lagrange', 'larrivee', 'laskowski', 'loximuthal', 'mercator', 'miller', 'mollweide', 'mt flat polar parabolic', 'mt flat polar quartic', 'mt flat polar sinusoidal', 'natural earth', 'natural earth1', 'natural earth2', 'nell hammer', 'nicolosi', 'orthographic', 'patterson', 'peirce quincuncial', 'polyconic', 'rectangular polyconic', 'robinson', 'satellite', 'sinu mollweide', 'sinusoidal', 'stereographic', 'times', 'transverse mercator', 'van der grinten', 'van der grinten2', 'van der grinten3', 'van der grinten4', 'wagner4', 'wagner6', 'wiechel', 'winkel tripel', 'winkel3'], key='projection_type')
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(static_map(df_filtered, st.session_state.projection_type), use_container_width=True, key="static_map")
    with col2:
        st.plotly_chart(animated_map(df_filtered, st.session_state.projection_type), use_container_width=True, key="animated_map")
    st.write("## Analytical View")
    st.write(df_filtered[['TIME_PERIOD', 'REF_AREA', 'MEASURE', 'OBS_VALUE']].sort_values(by=['TIME_PERIOD', 'REF_AREA', 'MEASURE']).reset_index(drop=True))
    # Styled chart configuration section
    st.markdown("### ⚙️ Chart Customization", unsafe_allow_html=True)     
    col_config1, col_config2 = st.columns(2)
    
    with col_config1:
        x_axis_options = ['REF_AREA', 'MEASURE', 'TIME_PERIOD']
        
        selected_x_axis = st.selectbox("X-Axis Variable", x_axis_options, key="x_axis_select")
    
    with col_config2:
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
        else:
            st.plotly_chart(multi_line(df_filtered, selected_x_axis, selected_category, selected_category_name, chart_type), use_container_width=True, key="multi_line_chart")
    with col2:
        st.plotly_chart(animated_hor_bar(df_filtered, selected_category), use_container_width=True, key="animated_horizontal_bar_chart")

elif st.session_state.topic == 'Nutrient Input and Output':
    st.write("This topic is not yet implemented.")



