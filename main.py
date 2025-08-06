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
    st.sidebar.title("Navigation")
    
    # Page selection
    pages = {
        "📖 Introduction": "introduction", 
        "📈 Dashboard": "dashboard",
        "📋 Process Book": "processbook"
    }
    
    selected_page = st.sidebar.selectbox(
        "Select a page:",
        options=list(pages.keys()),
        format_func=lambda x: x
    )
    
    # Route to different pages
    page_key = pages[selected_page]

    if page_key == "introduction":
        show_introduction_page()
    elif page_key == "dashboard":
        show_dashboard_page()
    elif page_key == "processbook":
        show_processbook_page()

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
        - Greenhouse gas output trends
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

def show_processbook_page():
    """Display the process book page"""
    try:
        # Check if file exists first
        processbook_file = pages_dir / "3_ProcessBook.py"
        if not processbook_file.exists():
            st.error(f"Process Book file not found at: {processbook_file}")
            return
            
        # Import and run the process book page
        import importlib.util
        spec = importlib.util.spec_from_file_location("processbook", processbook_file)
        if spec is None:
            st.error("Failed to create module specification")
            return
            
        processbook_module = importlib.util.module_from_spec(spec)
        if processbook_module is None:
            st.error("Failed to create module from specification")
            return
            
        # Execute the module
        spec.loader.exec_module(processbook_module)
        
    except ImportError as e:
        st.error(f"Import Error loading Process Book page: {e}")
        st.markdown("## Import Error - Process Book")
        st.markdown("Please check if all required packages are installed.")
        st.markdown(f"**Specific Error:** {str(e)}")
        
        # Show fallback content
        show_fallback_processbook()
        
    except FileNotFoundError as e:
        st.error(f"File not found: {e}")
        st.markdown("## File Not Found - Process Book")
        st.markdown("The Process Book file `3_ProcessBook.py` was not found in the Pages directory.")
        
    except Exception as e:
        st.error(f"Unexpected error loading Process Book page: {e}")
        st.markdown("## Process Book Loading Error")
        st.markdown(f"**Error Type:** {type(e).__name__}")
        st.markdown(f"**Error Details:** {str(e)}")
        
        # Show detailed traceback for debugging
        import traceback
        with st.expander("Technical Details"):
            st.code(traceback.format_exc())
        
        # Show fallback content
        show_fallback_processbook()

def show_fallback_processbook():
    """Show fallback Process Book content when the main version fails to load"""
    st.markdown("# 📋 Process Book")
    st.markdown("*Development Documentation and Analysis Report*")
    
    st.markdown("## Executive Summary")
    st.markdown("""
    This Process Book documents the development of an interactive OECD agricultural environmental data dashboard. 
    The project transforms complex environmental datasets into accessible visualizations for policy analysis and research.
    """)
    
    st.markdown("## Project Overview")
    st.markdown("""
    **Objective**: Create an interactive visualization platform for OECD agricultural environmental indicators
    
    **Data Sources**: 
    - OECD Agricultural Statistics Database
    - Greenhouse Gas Emissions Database  
    - Population and Land Use Records
    
    **Technical Stack**: Python, Streamlit, Plotly, Pandas, NumPy
    """)
    
    st.markdown("## Development Timeline")
    st.markdown("""
    1. **Data Collection & Assessment** - Identified key OECD datasets
    2. **Data Preprocessing** - Automated cleaning and standardization pipeline
    3. **Visualization Development** - Interactive charts with Plotly
    4. **Dashboard Integration** - Multi-page Streamlit application
    5. **Testing & Validation** - Cross-verification with source data
    """)
    
    st.markdown("## Key Features Implemented")
    st.markdown("""
    - **Interactive Maps**: Geographic visualizations with 80+ projection options
    - **Time Series Analysis**: Trend analysis from 1990-2022
    - **Comparative Analytics**: Country-level benchmarking tools
    - **Statistical Analysis**: Correlation and regression analysis
    - **Data Export**: Download capabilities for further analysis
    """)
    
    st.markdown("---")
    st.markdown("*This is fallback content. For the complete Process Book, please resolve any technical issues and refresh the page.*")


if __name__ == "__main__":
    main()
