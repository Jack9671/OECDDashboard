"""
Chart Components Module
Contains all chart visualization functions for the OECD Dashboard
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# Base directory for data files
BASE_DIR = Path(__file__).parent.parent.parent / 'DataSource'

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

def sunburst():
    """Create sunburst chart with hard-coded data for GHS categories"""
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
    # Dark theme
    fig = px.sunburst(df, path=['level1', 'level2', 'level3'], template='plotly_dark')
    # Increase the radius of the sunburst chart
    fig.update_layout(margin=dict(t=0, l=0, r=0, b=0), font=dict(size=20))
    return fig

def static_map(df: pd.DataFrame, projection_type: str = 'mercator') -> go.Figure:
    """Create static choropleth map showing GHS output by country"""
    df_sum = df.groupby('REF_AREA')['OBS_VALUE'].sum().reset_index()
    fig = px.choropleth(
        df_sum,
        locations='REF_AREA',
        locationmode='ISO-3',
        color='OBS_VALUE',
        color_continuous_scale=px.colors.sequential.Viridis_r,
        title="GHS output by country",
        labels={'OBS_VALUE':'Gas Output (Tonnes of CO2-equivalent)', 'REF_AREA':'Country'},
        range_color=[0, df_sum['OBS_VALUE'].max()],
        template='plotly_dark',
        width=1000,
        height=1000
    )
    fig.update_layout(
        geo=dict(
            showframe=False,
            showcoastlines=True,
            oceancolor='LightBlue',
            landcolor='White',
            projection_type=projection_type,
            showocean=True
        ), title_font=dict(size=30), title_x=0.3
    )
    return fig

def animated_map(df: pd.DataFrame, projection_type: str = 'mercator'):
    """Create animated choropleth map showing GHS evolution over time"""
    df_map_animated = df.groupby(['REF_AREA', 'TIME_PERIOD'])['OBS_VALUE'].sum().reset_index()
    # Create animated choropleth map
    fig_animated = px.choropleth(df_map_animated,
                                locations='REF_AREA',
                                locationmode='ISO-3',
                                color='OBS_VALUE',
                                color_continuous_scale=px.colors.sequential.Viridis_r,
                                animation_frame='TIME_PERIOD',
                                title=f"Evolution of GHS Distribution per Year",
                                labels={'OBS_VALUE': 'Gas Output (Tonnes of CO2-equivalent)',
                                        'REF_AREA': 'Country Code',
                                        'TIME_PERIOD': 'Year'},
                                range_color=[0, df_map_animated['OBS_VALUE'].max()],
                                template='plotly_dark',
                                width=1000,
                                height=1000
    )
    fig_animated.update_layout(
        geo=dict(
            showframe=False,
            showcoastlines=True,
            oceancolor='LightBlue',
            landcolor='White',
            projection_type=projection_type,
            showocean=True
        ),title_font=dict(size=30), title_x=0.3
    )
    return fig_animated

def multi_line(df: pd.DataFrame, x_axis_variable: str, variable_for_category: str, category_name: str, chart_type: str = "line") -> go.Figure:
    """Create multi-line or area chart showing trends over time"""
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
                          labels={'TIME_PERIOD': 'Year', 'value': 'Gas Output (Tonnes of CO2-equivalent)', 'variable': category_name},
                          template='plotly_dark', width=700, height=600,
                          color_discrete_map=color_map)
        fig_line.update_traces(
            line=dict(width=0),  # No line border
        )
        fig_line.update_layout(title_font=dict(size=20), title_x=0.1)
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
                          labels={'TIME_PERIOD': 'Year', 'value': 'Gas Output (Tonnes of CO2-equivalent)', 'variable': category_name},
                          template='plotly_dark', width=700, height=600,
                          color_discrete_map=color_map)
        fig_line.update_traces(mode='lines+markers', marker=dict(size=7), line=dict(width=3))
        fig_line.update_layout(title_font=dict(size=20), title_x=0.2)
    return fig_line

def animated_hor_bar(df: pd.DataFrame, col_to_rank: str) -> go.Figure:
    """Create animated horizontal bar chart showing evolution over time"""
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
                x='OBS_VALUE', y=col_to_rank,
                title=f"Evolution of GHS output for each {col_to_rank} per year",
                labels={'OBS_VALUE': 'Gas Output (Tonnes of CO2-equivalent)'},
                color_discrete_map=color_map,
                color=col_to_rank,
                animation_frame='TIME_PERIOD',
                animation_group=col_to_rank,
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
                     'Gas Output: %{x:,.0f} Tonnes of CO2-equivalent<br>' +
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
            title=col_to_rank.replace('_', ' ').title(),
        ),
        xaxis=dict(
            title='Gas Output (Tonnes of CO2-equivalent)'
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
        }], title_font=dict(size=20), title_x=0.2, title_y=0.88 
    )

    # Add custom data for hover information
    for frame in fig.frames:
        for trace in frame.data:
            # Add year information to hover
            trace.customdata = [frame.name] * len(trace.x)
    return fig

def pie(df: pd.DataFrame, groupby_var: str, category_name: str, value_filter: str = "All Values") -> go.Figure:
    """Create pie chart showing proportions"""
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
            width=700, height=600,
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
    fig.update_layout(showlegend=True, font=dict(size=25), title_font=dict(size=25), title_x=0.3)
    return fig

def tree_map(df: pd.DataFrame, groupby_var: str, category_name: str, value_filter: str = "All Values") -> go.Figure:
    """Create tree map visualization"""
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
        title_suffix = "(Negative Values - Absolute)"
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
            showarrow=False, font=dict(size=16), color='white')
        fig.update_layout(
            template='plotly_dark',
            title=f"Tree Map of {category_name}",
            width=700, height=600, font=dict(size=25), title_font=dict(size=25), title_x=0.3
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
        font=dict(size=25),title_font=dict(size=25), title_x=0.3
    )
    return fig

def static_bubble(df_ghs: pd.DataFrame, df_x: pd.DataFrame, x_axis_label: str) -> go.Figure:
    """Create static bubble chart showing relationship between variables"""
    df_pop = pd.read_csv(BASE_DIR / 'Population' / 'AnnualPopulationOECDCountry.csv')
    df_pop.rename(columns={"OBS_VALUE": "POPULATION"}, inplace=True)
    df_ghs = df_ghs.groupby(['REF_AREA'])['OBS_VALUE'].sum().reset_index()
    df_x = pd.merge(df_x, df_pop, on=["REF_AREA"], how='inner')
    df_x = df_x.groupby(['REF_AREA', 'POPULATION'])['OBS_VALUE'].sum().reset_index()
    df_for_static_scatter_plot = pd.merge(df_x, df_ghs, on=["REF_AREA"], how='inner')
    fig = px.scatter(
        df_for_static_scatter_plot, 
        x='OBS_VALUE_x', 
        y='OBS_VALUE_y',
        size='POPULATION', 
        color='REF_AREA',
        hover_name='REF_AREA',
        text='REF_AREA',  # Add text labels with each scatter point
        labels={
            'OBS_VALUE_x': x_axis_label,
            'OBS_VALUE_y': 'GHS output (Tonnes of CO2-equivalent)'
        },
        title=f"The relationship between {x_axis_label}, Population, and GHS Output",
        width=1000, 
        height=800,
        size_max=50,  # Remove upper limit by setting very high value
        template='plotly_dark',
    )
    # Set a minimum marker size for visibility
    fig.update_traces(marker=dict(sizemin=1))
    fig.add_annotation(
    text="output of 3 variables of each country is accumulated over time except for the population being the median",
    xref="paper", yref="paper",
    x=0.5, y=0,  # Position below the plot
    showarrow=False, font=dict(size=15, color="red"))
    fig.update_layout(title_font=dict(size=30), title_x=0.08, font=dict(size=20))
    return fig

def animated_bubble(df_ghs: pd.DataFrame, df_x: pd.DataFrame, x_axis_label: str) -> go.Figure:
    """Create animated bubble chart showing evolution over time"""
    df_pop = pd.read_csv(BASE_DIR / 'Population' / 'AnnualPopulationOECDCountry.csv')
    df_pop.rename(columns={"OBS_VALUE": "POPULATION"}, inplace=True)
    df_ghs = df_ghs.groupby(['REF_AREA', 'TIME_PERIOD'])['OBS_VALUE'].sum().reset_index()
    df_x = pd.merge(df_x, df_pop, on=["REF_AREA", "TIME_PERIOD"], how='inner')
    df_x = df_x.groupby(['REF_AREA', 'TIME_PERIOD', 'POPULATION'])['OBS_VALUE'].sum().reset_index()
    df_for_animated_scatter_plot = pd.merge(df_x, df_ghs, on=["REF_AREA", "TIME_PERIOD"], how='inner')
    fig = px.scatter(
        df_for_animated_scatter_plot, 
        x='OBS_VALUE_x', 
        y='OBS_VALUE_y',
        animation_frame='TIME_PERIOD',
        size='POPULATION', 
        color='REF_AREA',
        hover_name='REF_AREA',
        text='REF_AREA',  # Add text labels with each scatter point
        labels={
            'OBS_VALUE_x': x_axis_label,
            'OBS_VALUE_y': 'Total Greenhouse Gas Output (Tonnes of CO2-equivalent)'},
        title=f"Evolution of the relationship between {x_axis_label}, Population, and GHS Output per year",
        width=1000, 
        height=800,
        size_max=50,  # Remove upper limit by setting very high value
        template='plotly_dark',
    )
    fig.update_layout(font=dict(size=20), title_font=dict(size=25), title_x=0.08)
    # Set a minimum marker size for visibility
    fig.update_traces(marker=dict(sizemin=1))
    return fig

def bar_line(df: pd.DataFrame, x_axis_variable: str, category_to_stack: str, category_name: str) -> go.Figure:
    """Create combined bar and line chart"""
    df_pivoted = df.pivot_table(index=x_axis_variable, columns=category_to_stack, values='OBS_VALUE', aggfunc='sum').reset_index()
    # Add 'total' column for total greenhouse gas output using only available measures
    df_pivoted['total'] = df_pivoted.iloc[:, 1:].sum(axis=1)
    #sort descending by total only if x_axis_variable is not 'TIME_PERIOD'
    if x_axis_variable != 'TIME_PERIOD':
        df_pivoted = df_pivoted.sort_values(by='total', ascending=False) 
    # Create a stacked bar chart using Plotly Express
    fig_stacked = px.bar(df_pivoted, x=x_axis_variable, y=df_pivoted.columns[1:-1],  # Exclude 'total' column
                        title=f"GHS output of accumulated sum of all {category_name} per {x_axis_variable}",
                        labels= {'value': 'Gas Output (Tonnes of CO2-equivalent)', 'variable': category_name},
                        template='plotly_dark', width=700, height=600, barmode ='relative')

    fig_stacked.update_traces(marker=dict(line=dict(width=1, color='DarkSlateGrey')))

    # Update the layout to stack the bars properly
    fig_stacked.update_layout(barmode='relative',title_font=dict(size=20), title_x = 0.1)

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
        hovertemplate=f'<b>{x_axis_variable}:</b> %{{x}}<br><b>Total:</b> %{{y:,.0f}} Tonnes of CO2-equivalent<extra></extra>'
    ))
    st.write(df_pivoted[x_axis_variable])
    st.write(df_pivoted['total'])
    return fig_stacked

def percentage_bar_line(df: pd.DataFrame, x_axis_variable: str, category_to_stack: str, category_name: str) -> go.Figure:
    """Create percentage-based bar and line chart"""
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
    #sort descending by total only if x_axis_variable is not 'TIME_PERIOD'
    if x_axis_variable != 'TIME_PERIOD':
        df_percentage = df_percentage.sort_values(by='abs_total', ascending=False)

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
        ),title_font=dict(size=20), title_x = 0.1
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

def water_fall(df: pd.DataFrame, x_axis_variable: str, category_to_stack: str, category_name: str) -> go.Figure:
    """Create waterfall chart with enhanced customization"""
    df_pivoted = df.pivot_table(index=x_axis_variable, columns=category_to_stack, values='OBS_VALUE', aggfunc='sum').reset_index()
    # Add 'total' column for total greenhouse gas output using only available measures
    df_pivoted['total'] = df_pivoted.iloc[:, 1:].sum(axis=1)
    #sort descending by total
    df_pivoted = df_pivoted.sort_values(by='total', ascending=False)
    
    color_map = get_color_mapping(df, x_axis_variable) if x_axis_variable == 'REF_AREA' else {}
    
    # Create waterfall chart with individual values and total
    x_values = df_pivoted[x_axis_variable].tolist()
    y_values = df_pivoted['total'].tolist()
    total_sum = sum(y_values)
    
    # Function to format large numbers for better readability
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

    # Calculate percentages for each value
    percentages = [(val / total_sum) * 100 for val in y_values]
    
    # Function to calculate appropriate font size based on text length and bar width
    def calculate_font_size_for_bar(text, bar_width_estimate, min_font_size=8, max_font_size=18):
        """
        Calculate font size to ensure text fits within bar width while maximizing readability
        """
        text_length = len(text)
        # Use a more accurate character width ratio (0.55 for better fit)
        char_width_ratio = 0.55
        
        # Calculate maximum font size that would fit with 90% of bar width (leaving 10% margin)
        usable_width = bar_width_estimate * 0.9
        max_possible_font_size = usable_width / (text_length * char_width_ratio)
        
        # Constrain between min and max font sizes
        font_size = max(min_font_size, min(max_possible_font_size, max_font_size))
        
        return int(font_size)
    
    # Estimate bar width based on figure width and number of bars
    figure_width = 800  # Chart width
    plot_area_width = figure_width * 0.8  # Approximate usable plot area (excluding margins)
    total_bars = len(x_values) + 1  # +1 for total bar
    # Account for spacing between bars (approximately 20% of total width for gaps)
    effective_width_for_bars = plot_area_width * 0.8
    estimated_bar_width = effective_width_for_bars / total_bars
    
    # Create the figure
    fig_simple = go.Figure()
    
    # Add individual bars for each country/category with custom colors
    cumulative = 0
    for i, (x_val, y_val, pct) in enumerate(zip(x_values, y_values, percentages)):
        # Determine color for this bar
        if x_axis_variable == 'REF_AREA' and x_val in color_map:
            bar_color = color_map[x_val]
        elif y_val >= 0:
            bar_color = "green"
        else:
            bar_color = "red"
        
        # Create text labels - show country name inside bar and value/percentage outside
        formatted_val = format_number(y_val)
        
        # Text inside the bar (country name)
        inside_text = str(x_val)
        
        # Text outside the bar (value and percentage)
        outside_text = f"{formatted_val}<br>({pct:.1f}%)"
        
        # Add bar trace with inside text (country name)
        fig_simple.add_trace(go.Bar(
            x=[x_val],
            y=[y_val],
            base=[cumulative],
            name=str(x_val),
            marker_color=bar_color,
            marker_line=dict(color="white", width=1),
            text=[inside_text],
            textposition="inside",
            textfont=dict(color="white", size=14, family="Arial Black"),
            hovertemplate=f"<b>{x_axis_variable}:</b> {x_val}<br>" +
                         f"<b>Value:</b> {formatted_val}<br>" +
                         f"<b>Percentage:</b> {pct:.1f}%<extra></extra>",
            showlegend=False,
        ))
        
        # Add separate annotation for value and percentage outside the bar
        # Calculate appropriate font size for this annotation
        annotation_font_size = calculate_font_size_for_bar(outside_text.replace('<br>', ''), estimated_bar_width)
        # Ensure minimum readability for annotations
        annotation_font_size = max(annotation_font_size, 10)
        
        fig_simple.add_annotation(
            x=x_val,
            y=cumulative + y_val,
            text=outside_text,
            showarrow=False,
            yshift=10,
            font=dict(size=annotation_font_size, color="white", family="Arial"),
            xanchor="center",
            yanchor="bottom"
        )
        
        # Update cumulative for next bar
        cumulative += y_val
    
    # Add total bar
    total_formatted = format_number(total_sum)
    fig_simple.add_trace(go.Bar(
        x=['TOTAL'],
        y=[total_sum],
        name='Total',
        marker_color="blue",
        marker_line=dict(color="white", width=2),
        text=['TOTAL'],
        textposition="inside",
        textfont=dict(color="white", size=16, family="Arial Black"),
        hovertemplate=f"<b>Total:</b> {total_formatted}<br>" +
                     f"<b>Percentage:</b> 100%<extra></extra>",
        showlegend=False
    ))
    
    # Add annotation for total value and percentage
    total_annotation_text = f"{total_formatted}<br>(100%)"
    total_annotation_font_size = calculate_font_size_for_bar(total_annotation_text.replace('<br>', ''), estimated_bar_width)
    # Ensure minimum readability for total annotation
    total_annotation_font_size = max(total_annotation_font_size, 10)
    
    fig_simple.add_annotation(
        x='TOTAL',
        y=total_sum,
        text=total_annotation_text,
        showarrow=False,
        yshift=10,
        font=dict(size=total_annotation_font_size, color="white", family="Arial"),
        xanchor="center",
        yanchor="bottom"
    )
    
    # Add connector lines between bars
    for i in range(len(x_values)):
        if i < len(x_values) - 1:
            # Calculate positions for connector lines
            x_start = i + 0.4  # End of current bar
            x_end = i + 1 - 0.4  # Start of next bar
            y_level = sum(y_values[:i+1])  # Cumulative sum up to current bar
            
            fig_simple.add_shape(
                type="line",
                x0=x_start, y0=y_level,
                x1=x_end, y1=y_level,
                line=dict(color="rgb(63, 63, 63)", width=1, dash="dot"),
            )
    
    fig_simple.update_layout(
        title=f"{category_name} Contributions by {x_axis_variable}",
        showlegend=False,
        template='plotly_dark',
        width=800, 
        height=800,
        title_font=dict(size=30),
        font=dict(size=20), 
        title_x=0.1,
        barmode='relative',
        xaxis=dict(title=x_axis_variable),
        yaxis=dict(title="Gas Output (Tonnes of CO2-equivalent)")
    )
    
    #increase max range of y-axis
    max_y_value = max(max(y_values), total_sum) * 1.25  # Increase by 25% for better visibility
    fig_simple.update_yaxes(range=[0, max_y_value])
    #hide x-axis labels
    return fig_simple
