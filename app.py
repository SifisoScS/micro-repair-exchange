# app.py
import streamlit as st
from firebase_service import FirebaseService
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Micro-Repair Exchange",
    page_icon="🛠️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #424242;
        margin-top: 1rem;
    }
    .repair-card {
        background-color: #f5f5f5;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        border-left: 5px solid #1E88E5;
    }
    .status-open {
        color: #FF9800;
        font-weight: bold;
    }
    .status-assigned {
        color: #2196F3;
        font-weight: bold;
    }
    .status-resolved {
        color: #4CAF50;
        font-weight: bold;
    }
    .stButton>button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'current_user' not in st.session_state:
    st.session_state.current_user = None
if 'firebase' not in st.session_state:
    st.session_state.firebase = FirebaseService.get_instance()

def main():
    # Header
    st.markdown("<h1 class='main-header'>🛠️ Micro-Repair Exchange</h1>", unsafe_allow_html=True)
    st.markdown("### Restoring dignity through repair")
    
    # Initialize Firebase
    firebase = st.session_state.firebase
    
    # User Registration/Selection (Simplified for MVP)
    st.sidebar.title("👤 User Setup")
    
    if st.session_state.current_user is None:
        with st.sidebar.form("user_setup"):
            name = st.text_input("Your Name")
            location = st.text_input("Your Location")
            skills = st.text_input("Your Skills (comma-separated)", placeholder="e.g., electrical, sewing, carpentry")
            
            if st.form_submit_button("Register / Sign In"):
                if name and location:
                    user_data = {
                        'name': name,
                        'location': location,
                        'skills': [s.strip() for s in skills.split(',')] if skills else []
                    }
                    
                    # Check if user exists
                    all_users = firebase.get_all_users()
                    existing_user = next((u for u in all_users if u['name'].lower() == name.lower() and u['location'].lower() == location.lower()), None)
                    
                    if existing_user:
                        st.session_state.current_user = existing_user
                        st.success(f"Welcome back, {name}!")
                    else:
                        user_id = firebase.create_user(user_data)
                        if user_id:
                            user_data['id'] = user_id
                            st.session_state.current_user = user_data
                            st.success(f"Welcome to the community, {name}!")
                    st.rerun()
    
    if st.session_state.current_user:
        user = st.session_state.current_user
        st.sidebar.success(f"Logged in as: **{user['name']}**")
        st.sidebar.info(f"📍 {user['location']}")
        
        if user.get('skills'):
            st.sidebar.write("🛠️ Skills:")
            for skill in user['skills']:
                st.sidebar.write(f"• {skill}")
        
        if st.sidebar.button("Logout"):
            st.session_state.current_user = None
            st.rerun()
        
        # Show stats
        stats = firebase.get_stats()
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Repairs", stats.get('total', 0))
        with col2:
            st.metric("Open Requests", stats.get('open', 0), delta_color="off")
        with col3:
            st.metric("In Progress", stats.get('assigned', 0))
        with col4:
            st.metric("Completed", stats.get('resolved', 0))
        
        st.divider()
        
        # Navigation
        st.markdown("### Quick Actions")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📝 Log New Request", use_container_width=True):
                st.switch_page("pages/1_📝_Log_Request.py")
        
        with col2:
            if st.button("🔍 Browse Requests", use_container_width=True):
                st.switch_page("pages/2_🔍_Browse_Requests.py")
        
        with col3:
            if st.button("✅ My Repairs", use_container_width=True):
                st.switch_page("pages/4_✅_Resolve_&_Gratitude.py")
        
        # Recent requests preview
        st.markdown("### Recent Repair Requests")
        recent_requests = firebase.get_all_requests()[:5]
        
        if recent_requests:
            for req in recent_requests:
                with st.container():
                    col1, col2, col3 = st.columns([3, 1, 1])
                    with col1:
                        st.markdown(f"**{req.get('item', 'Unknown Item')}**")
                        st.caption(req.get('description', 'No description'))
                    with col2:
                        status = req.get('status', 'open')
                        status_class = f"status-{status}"
                        st.markdown(f"<span class='{status_class}'>{status.upper()}</span>", unsafe_allow_html=True)
                    with col3:
                        if st.button("View", key=f"view_{req['id']}"):
                            st.session_state.selected_request = req['id']
                            st.switch_page("pages/3_👷_Assign_Repairer.py")
                    st.divider()
        else:
            st.info("No repair requests yet. Be the first to log one!")
        
        # Mission statement
        st.markdown("---")
        st.markdown("""
        ## 🌍 Our Mission
        *Empower communities* to value repair over replacement.  
        *Make invisible skills visible*—the neighbor who can fix a plug, sew a button, or repair a chair.  
        *Create a culture of gratitude* where every fix is logged, acknowledged, and remembered.
        """)
    else:
        st.warning("👈 Please register/sign in from the sidebar to continue")
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            ### Why Repair?
            - ♻️ **Reduce waste** and environmental impact
            - 💰 **Save money** by fixing instead of replacing
            - 🤝 **Build community** connections
            - 🎉 **Celebrate skills** and knowledge sharing
            """)
        with col2:
            st.markdown("""
            ### How It Works
            1. **Log** your broken item
            2. **Connect** with skilled neighbors
            3. **Fix** together or get help
            4. **Share** gratitude and stories
            """)

if __name__ == "__main__":
    main()