from altair import value
import streamlit as st
from Component import section_2
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path
import warnings
def summary_statistics(df: pd.DataFrame, user_config: dict[str, str]) -> pd.DataFrame:
    """Calculate summary statistics for the DataFrame."""
    # 3 columns: DESCRIPTION, START_VALUE, END_VALUE, PERCENTAGE_CHANGE
    start_year = user_config['selected_TIME_PERIOD'][0]
    end_year = user_config['selected_TIME_PERIOD'][-1]
    df_start = df[df['TIME_PERIOD'] == start_year].groupby('REF_AREA')['OBS_VALUE'].sum().reset_index()
    df_end = df[df['TIME_PERIOD'] == end_year].groupby('REF_AREA')['OBS_VALUE'].sum().reset_index()
    df_start.rename(columns={'OBS_VALUE': 'START_VALUE'}, inplace=True)
    df_end.rename(columns={'OBS_VALUE': 'END_VALUE'}, inplace=True)
    summary_df = pd.merge(df_start, df_end, on='REF_AREA', how='outer')
    summary_df['PERCENTAGE_CHANGE'] = ((summary_df['END_VALUE'] - summary_df['START_VALUE']) / summary_df['START_VALUE'].replace(0, np.nan)) * 100
    summary_df['DESCRIPTION'] = 'Greenhouse Gas Ouput'
    summary_df = summary_df[['DESCRIPTION', 'START_VALUE', 'END_VALUE', 'PERCENTAGE_CHANGE']]
    return summary_df

def section_2(df: pd.DataFrame):
    st.write("## Summary Statistics")    
    # Create styled info cards for summary information
    info_col1, info_col2 = st.columns(2)
    with info_col1:
        st.markdown(f"""
        <div style="
            background-color: #0e1117;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #00cc88;
            margin: 5px 0;
            border: 1px solid #262730;
        ">
            <div style="color: #a3a8b8; font-size: 20px; margin-bottom: 5px;">📊 Dataset Information</div>
            <div style="color: #fafafa; font-size: 15px; font-weight: bold;">
                {len(df):,} records
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style="
            background-color: #0e1117;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #ff9500;
            margin: 5px 0;
            border: 1px solid #262730;
        ">
            <div style="color: #a3a8b8; font-size: 20px; margin-bottom: 5px;">🗓️ Time Period</div>
            <div style="color: #fafafa; font-size: 15px; font-weight: bold;">
                {st.session_state.user_config['selected_TIME_PERIOD'][0]} - {st.session_state.user_config['selected_TIME_PERIOD'][-1]}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with info_col2:
        st.markdown(f"""
        <div style="
            background-color: #0e1117;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #0080ff;
            margin: 5px 0;
            border: 1px solid #262730;
        ">
            <div style="color: #a3a8b8; font-size: 20px; margin-bottom: 5px;">🌍 Selected Countries</div>
            <div style="color: #fafafa; font-size: 15px; font-weight: bold;">
                {len(st.session_state.user_config['selected_REF_AREA'])} countries: {', '.join(st.session_state.user_config['selected_REF_AREA'][:3])}{'...' if len(st.session_state.user_config['selected_REF_AREA']) > 3 else ''}
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f"""
        <div style="
            background-color: #0e1117;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #ff4b4b;
            margin: 5px 0;
            border: 1px solid #262730;
        ">
            <div style="color: #a3a8b8; font-size: 20px; margin-bottom: 5px;">🏭 Selected Gases</div>
            <div style="color: #fafafa; font-size: 15px; font-weight: bold;">
                {', '.join(st.session_state.user_config['selected_MEASURE'])}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Add a styled analysis question
    st.markdown(f"""
    <div style="
        background-color: #1a1d29;
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #9d4edd;
        margin: 20px 0;
        border: 1px solid #262730;
    ">
        <div style="color: #fafafa; font-size: 15px; font-style: italic;">
            💡Showing how much percentage Greenhouse Gas Output in the <span style="font-size: 20px; font-weight: bold;">{st.session_state.user_config['selected_TIME_PERIOD'][0]}</span> has increased or decreased relative to the greenhouse gas output in <span style="font-size: 20px; font-weight: bold;">{st.session_state.user_config['selected_TIME_PERIOD'][-1]}</span>.
        </div>
    </div>
    """, unsafe_allow_html=True)
    # Calculate summary statistics for each selected measure
    summary_stats = []
    start_year = st.session_state.user_config['selected_TIME_PERIOD'][0]
    end_year = st.session_state.user_config['selected_TIME_PERIOD'][-1]
    for measure in st.session_state.user_config['selected_MEASURE']:
        measure_df = df[df['MEASURE'] == measure]
        start_value = measure_df[measure_df['TIME_PERIOD'] == start_year]['OBS_VALUE'].sum()
        end_value = measure_df[measure_df['TIME_PERIOD'] == end_year]['OBS_VALUE'].sum()
        
        if start_value > 0:
            percentage_change = ((end_value - start_value) / start_value) * 100
        else:
            percentage_change = 0
            
        summary_stats.append({
            'measure': measure,
            'start_value': start_value,
            'end_value': end_value,
            'percentage_change': percentage_change
        })
    
    # Display metrics in columns
    if len(summary_stats) > 0:
        cols = st.columns(min(len(summary_stats), 4))  # Max 4 columns per row
        for i, stat in enumerate(summary_stats):
            col_idx = i % 4
            with cols[col_idx]:
                # Determine color based on percentage change
                if stat['percentage_change'] > 0:
                    color = "🔴"  # Red for increase (bad for emissions)
                    trend = "↗"
                    color_class = "red"
                elif stat['percentage_change'] < 0:
                    color = "🟢"  # Green for decrease (good for emissions)
                    trend = "↘"
                    color_class = "green"
                else:
                    color = "⚪"
                    trend = "→"
                    color_class = "gray"
                
                # Format the values for prefix K, M, B, display 1 significant digit
                if stat['start_value'] >= 1e9:
                    start_formatted = f"{stat['start_value'] / 1e9:.1f} B"
                    end_formatted = f"{stat['end_value'] / 1e9:.1f} B"
                elif stat['start_value'] >= 1e6:
                    start_formatted = f"{stat['start_value'] / 1e6:.1f} M"
                    end_formatted = f"{stat['end_value'] / 1e6:.1f} M"
                elif stat['start_value'] >= 1e3:
                    start_formatted = f"{stat['start_value'] / 1e3:.1f} K"
                    end_formatted = f"{stat['end_value'] / 1e3:.1f} K"
                else:
                    start_formatted = f"{stat['start_value']:.1f}"
                    end_formatted = f"{stat['end_value']:.1f}"
                # Create the metric box
                st.markdown(f"""
                <div style="
                    background-color: #0e1117;
                    padding: 20px;
                    border-radius: 10px;
                    border-left: 5px solid {'#ff4b4b' if color_class == 'red' else '#00cc88' if color_class == 'green' else '#808080'};
                    margin: 10px 0;
                    border: 5px solid #262730;
                ">
                    <div style="display: flex; align-items: center; margin-bottom: 10px;">
                        <span style="font-size: 15px; margin-right: 10px;">{color}</span>
                        <span style="font-weight: bold; font-size: 25px; color: #fafafa;">{stat['measure']} Gas</span>
                    </div>
                    <div style="color:  #a3a8b8; font-size: 15px; margin-bottom: 0px;">
                        {start_year}: <strong style="color: #fafafa;">{start_formatted}</strong> | {end_year}: <strong style="color: #fafafa;">{end_formatted}</strong>
                    </div>
                    <div style="display: flex; align-items: center; justify-content: flex-end;">
                        <span style="font-size: 30px; margin-right: 5px;">{trend}</span>
                        <span style="
                            font-size: 30px; 
                            font-weight: bold; 
                            color: {'#ff4b4b' if color_class == 'red' else '#00cc88' if color_class == 'green' else '#a3a8b8'};
                        ">{abs(stat['percentage_change']):.1f}%</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    else:
        st.warning("No data available for the selected filters.")
    