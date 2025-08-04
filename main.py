import streamlit as st
from pathlib import Path
import sys

# Add the Pages directory to the Python path
pages_dir = Path(__file__).parent / "Pages"
sys.path.append(str(pages_dir))

# Configure the main page
st.set_page_config(
    page_title="OECD Data Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    # Create sidebar navigation
    st.sidebar.title("📊 Navigation")
    
    # Page selection
    pages = {
        "🏠 Home": "home",
        "📖 Introduction": "introduction", 
        "📈 Dashboard": "dashboard"
    }
    
    selected_page = st.sidebar.selectbox(
        "Select a page:",
        options=list(pages.keys()),
        format_func=lambda x: x
    )
    
    # Route to different pages
    page_key = pages[selected_page]
    
    if page_key == "home":
        show_home_page()
    elif page_key == "introduction":
        show_introduction_page()
    elif page_key == "dashboard":
        show_dashboard_page()

def show_home_page():
    """Display the home page"""
    st.title("🌍 OECD Data Visualization Dashboard")
    
    st.markdown("""
    ## Welcome to the OECD Data Analytics Platform
    
    This dashboard provides comprehensive analysis of OECD environmental data including:
    
    ### 📊 Available Data Sources:
    - **Greenhouse Gas Emissions**: Analysis by sectors, nature sources, and LULUCF classifications
    - **Agricultural Land**: Land use patterns and agricultural statistics
    - **Nutrient Input/Output**: Environmental nutrient flow analysis
    
    ### 🔍 Features:
    - Interactive visualizations
    - Multi-dimensional data exploration
    - Statistical summaries and trends
    - Cross-country comparisons
    
    ### 🚀 Getting Started:
    1. Navigate to the **Introduction** page to learn more about the data
    2. Explore the **Dashboard** for interactive analytics
    3. Use the sidebar filters to customize your analysis
    
    ---
    *Use the navigation panel on the left to explore different sections of the dashboard.*
    """)
    
    # Add some statistics about the data
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Data Categories", "4", help="Greenhouse Gas, Land, Nutrients, etc.")
    
    with col2:
        st.metric("Interactive Charts", "10+", help="Various visualization types available")
    
    with col3:
        st.metric("Countries Covered", "OECD", help="All OECD member countries")

def show_introduction_page():
    """Display the introduction page"""
    try:
        # Import and run the introduction page
        import importlib.util
        spec = importlib.util.spec_from_file_location("introduction", pages_dir / "1_Introduction.py")
        introduction_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(introduction_module)
    except Exception as e:
        st.error(f"Error loading Introduction page: {e}")
        st.markdown("""
        ## 📖 Introduction
        
        Welcome to the OECD Environmental Data Dashboard. This platform provides insights into:
        
        - Environmental indicators across OECD countries
        - Greenhouse gas emission trends
        - Agricultural and land use patterns
        - Sustainable development metrics
        """)

def show_dashboard_page():
    """Display the dashboard page"""
    try:
        # Import and run the dashboard page
        import importlib.util
        spec = importlib.util.spec_from_file_location("dashboard", pages_dir / "2_dashboard.py")
        dashboard_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(dashboard_module)
    except Exception as e:
        st.error(f"Error loading Dashboard page: {e}")
        st.markdown("## Dashboard loading error. Please check the dashboard configuration.")

if __name__ == "__main__":
    main()
