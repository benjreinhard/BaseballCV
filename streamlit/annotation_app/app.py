import streamlit as st
from app_utils.app_pages import AppPages
from app_utils.default_tools import DefaultTools
from app_utils.file_tools import FileTools
import atexit

def app():
    st.set_page_config(
        layout="wide",
        page_title="Baseball Annotation Tool",
        page_icon="⚾"
    )

    if "initialized" not in st.session_state:
        st.session_state.initialized = False
        
    default_tools = DefaultTools()
    if not st.session_state.initialized:
        default_tools.init_project_structure()
        st.session_state.initialized = True
        
        app_pages = AppPages()
        app_pages.task_manager.cleanup_incomplete_tasks()

    def cleanup():
        if "app_pages" in locals():
            app_pages.task_manager.cleanup_incomplete_tasks()
    atexit.register(cleanup)

    file_tools = FileTools()
    baseballcv_logo = file_tools.load_image_from_endpoint("https://data.balldatalab.com/index.php/s/3PnEp3yw2WQRMQs/download/baseballcvlogo.png")
    
    if 'page' not in st.session_state:
        st.session_state.page = "welcome"
    if 'selected_project' not in st.session_state:
        st.session_state.selected_project = None
    if 'project_type' not in st.session_state:
        st.session_state.project_type = None
    if 'user_id' not in st.session_state:
        st.session_state.user_id = None
    if 'current_category' not in st.session_state:
        st.session_state.current_category = None
    if 'annotations' not in st.session_state:
        st.session_state.annotations = []
    if 'bbox_start' not in st.session_state:
        st.session_state.bbox_start = None
    if 'current_image' not in st.session_state:
        st.session_state.current_image = None

    app_pages = AppPages()
    app_pages.app_style()

    if not st.session_state.user_id or not st.session_state.get('email'):
        with st.sidebar:
            st.image(baseballcv_logo, use_column_width=True)
            st.markdown("---")
            st.markdown("## User Login")
            user_id = st.text_input("Enter your username:")
            email = st.text_input("Enter your email:")
            if user_id and email:
                st.session_state.user_id = user_id
                if str(email).endswith(".com"):
                    st.session_state.email = email
                    st.rerun()
                else:
                    st.error("Invalid Email Address!")
        st.markdown("""
            <div style='text-align: center; padding: 7 rem; color: white;'>
                <h1 style='color: white; font-size: 10rem;'>BaseballCV Annotation Tool</h1>
                <p style='font-size: 2rem; color: #FF6B00;'>
                    Please enter Username and Email in the Sidebar to Continue...
                </p>
            </div>
        """, unsafe_allow_html=True)
        return

    with st.sidebar:
        st.image(baseballcv_logo, use_column_width=True)
        st.markdown(f"<h2 style='color: black; text-align: center'>User: {st.session_state.user_id}</h2>", unsafe_allow_html=True)
        st.markdown("---")
        
        if st.session_state.page != "welcome":
            if st.button("← Back to Home", key="nav_home"):
                st.session_state.page = "welcome"
                st.session_state.selected_project = None
                st.rerun()
            
            if st.session_state.selected_project:
                st.markdown(f"<h3 style='color: black; text-align: center'>Current Project: {st.session_state.selected_project}</h3>", unsafe_allow_html=True)
                st.markdown("---")
                
                if st.button("Project Dashboard", key="nav_dashboard"):
                    st.session_state.page = "project_dashboard"
                    st.rerun()
                if st.button("Upload Media", key="nav_upload"):
                    st.session_state.page = "add_media"
                    st.rerun()
                if st.button("Start Annotating", key="nav_annotate"):
                    st.session_state.page = "annotate"
                    st.rerun()
                if st.button("View Progress", key="nav_progress"):
                    st.session_state.page = "progress"
                    st.rerun()
        
        st.markdown("---")
        if st.button("Logout", key="logout"):
            st.session_state.user_id = None
            st.session_state.page = "welcome"
            st.session_state.selected_project = None
            st.rerun()

    if st.session_state.page == "welcome":
        app_pages.show_welcome_page()
    elif st.session_state.page == "create_project":
        app_pages.create_project_screen()
    elif st.session_state.page == "select_project":
        app_pages.show_project_selection()
    elif st.session_state.page == "project_dashboard":
        app_pages.show_project_dashboard()
    elif st.session_state.page == "add_media":
        app_pages.show_add_media_page()
    elif st.session_state.page == "progress":
        app_pages.show_progress_page()
    elif st.session_state.page == "annotate":
        app_pages.show_annotation_interface()

if __name__ == "__main__":
    app()
