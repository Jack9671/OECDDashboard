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
        "📈 Dashboard": "dashboard"
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

if __name__ == "__main__":
    main()
