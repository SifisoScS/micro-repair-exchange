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
    /* Hide default Streamlit sidebar "app" text */
    [data-testid="stSidebarNav"] li:first-child {
        display: none;
    }
    
    /* Main styling */
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
    
    /* Custom sidebar styling */
    .sidebar-header {
        text-align: center;
        padding: 1.5rem 0;
        background: linear-gradient(135deg, #1E88E5 0%, #0D47A1 100%);
        border-radius: 0 0 15px 15px;
        margin: -1rem -1rem 1.5rem -1rem;
        color: white;
    }
    .sidebar-title {
        font-size: 1.8rem;
        font-weight: bold;
        margin: 0.5rem 0;
    }
    .sidebar-tagline {
        font-size: 0.9rem;
        opacity: 0.9;
        font-style: italic;
    }
    .user-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        margin: 1rem 0;
    }
    .skill-badge {
        display: inline-block;
        background: #E3F2FD;
        color: #1565C0;
        padding: 0.25rem 0.75rem;
        border-radius: 15px;
        margin: 0.25rem;
        font-size: 0.85rem;
    }
    .nav-btn {
        width: 100%;
        margin: 0.5rem 0;
        padding: 0.75rem;
        border-radius: 10px;
        border: 2px solid #E3F2FD;
        background: white;
        color: #1E88E5;
        font-weight: bold;
        text-align: left;
        transition: all 0.3s ease;
    }
    .nav-btn:hover {
        background: #1E88E5;
        color: white;
        border-color: #1E88E5;
        transform: translateY(-2px);
    }
    .stats-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        text-align: center;
        margin: 0.5rem 0;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: bold;
        color: #1E88E5;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #666;
    }
    
    /* Main content buttons */
    .action-btn {
        padding: 1rem;
        border-radius: 10px;
        border: none;
        background: linear-gradient(135deg, #1E88E5 0%, #0D47A1 100%);
        color: white;
        font-weight: bold;
        font-size: 1.1rem;
        transition: all 0.3s ease;
    }
    .action-btn:hover {
        transform: translateY(-3px);
        box-shadow: 0 5px 15px rgba(30, 136, 229, 0.3);
    }
    
    /* Request cards */
    .request-card {
        background: white;
        padding: 1.25rem;
        border-radius: 10px;
        border-left: 5px solid #1E88E5;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    .request-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'current_user' not in st.session_state:
    st.session_state.current_user = None
if 'firebase' not in st.session_state:
    st.session_state.firebase = FirebaseService.get_instance()

def main():
    # Custom Sidebar Header (replaces default "app" text)
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-header">
            <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🛠️</div>
            <div class="sidebar-title">Micro-Repair Exchange</div>
            <div class="sidebar-tagline">Fix, don't replace</div>
        </div>
        """, unsafe_allow_html=True)

    # Initialize Firebase
    firebase = st.session_state.firebase

    # User Registration/Selection in Sidebar
    with st.sidebar:
        if st.session_state.current_user is None:
            st.markdown("### 👋 Welcome to Our Community")
            st.markdown("*Join neighbors helping neighbors*")

            with st.form("user_setup"):
                _extracted_from_main_22(firebase)
        # If user is logged in
        if st.session_state.current_user:
            _extracted_from_main_74(firebase)
    # Main Content Area
    # Header
    st.markdown("<h1 class='main-header'>🛠️ Welcome to Micro-Repair Exchange</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #666; margin-bottom: 2rem;'>Restoring dignity through repair • Building community through skills</h3>", unsafe_allow_html=True)

    if st.session_state.current_user:
        _extracted_from_main_170(firebase)
    else:
        _extracted_from_main_35(firebase)


# TODO Rename this here and in `main`
def _extracted_from_main_35(firebase):
    # Landing page for non-logged in users
    st.markdown("""
        <div style="text-align: center; padding: 3rem 1rem; background: linear-gradient(135deg, #E3F2FD 0%, #BBDEFB 100%); 
                    border-radius: 20px; margin: 2rem 0;">
            <h1 style="color: #0D47A1;">Join the Repair Revolution!</h1>
            <p style="font-size: 1.2rem; color: #1565C0; max-width: 800px; margin: 0 auto 2rem auto;">
                Every year, millions of items are thrown away that could be easily fixed. 
                Join a community that believes in repair, not replacement.
            </p>
            <div style="font-size: 3rem; margin: 2rem 0;">🛠️ ♻️ 🤝</div>
        </div>
        """, unsafe_allow_html=True)

    # Why Join Section
    st.markdown("### 💚 Why Join Our Community?")
    reasons_cols = st.columns(3)

    with reasons_cols[0]:
        st.markdown("""
            <div style="text-align: center; padding: 1.5rem;">
                <div style="font-size: 2.5rem; color: #4CAF50;">♻️</div>
                <h4>Save the Planet</h4>
                <p>Reduce waste and carbon footprint by fixing instead of buying new</p>
            </div>
            """, unsafe_allow_html=True)

    with reasons_cols[1]:
        st.markdown("""
            <div style="text-align: center; padding: 1.5rem;">
                <div style="font-size: 2.5rem; color: #2196F3;">💰</div>
                <h4>Save Money</h4>
                <p>Repairs cost a fraction of replacement and last longer</p>
            </div>
            """, unsafe_allow_html=True)

    with reasons_cols[2]:
        st.markdown("""
            <div style="text-align: center; padding: 1.5rem;">
                <div style="font-size: 2.5rem; color: #FF9800;">🤝</div>
                <h4>Build Connections</h4>
                <p>Meet neighbors, share skills, and strengthen community bonds</p>
            </div>
            """, unsafe_allow_html=True)

    steps_cols = _extracted_from_main_192(st, "### 🚀 How It Works", 4)
    steps = [
        ("1", "📝", "Log Repair", "Describe what needs fixing"),
        ("2", "🔍", "Find Help", "Connect with skilled neighbors"),
        ("3", "👷", "Fix Together", "Arrange repair meetup"),
        ("4", "🎉", "Share Gratitude", "Celebrate the successful repair")
    ]

    for idx, (num, icon, title, desc) in enumerate(steps):
        with steps_cols[idx]:
            st.markdown(f"""
                <div style="text-align: center; padding: 1rem; background: white; border-radius: 10px; 
                            border: 2px solid #E3F2FD; height: 100%;">
                    <div style="font-size: 2rem; margin-bottom: 0.5rem;">{icon}</div>
                    <h4 style="margin: 0.5rem 0;">{title}</h4>
                    <p style="color: #666; font-size: 0.9rem; margin: 0;">{desc}</p>
                </div>
                """, unsafe_allow_html=True)

    # Call to Action
    st.markdown("""
        <div style="text-align: center; margin: 3rem 0;">
            <h3>Ready to make a difference in your community?</h3>
            <p style="color: #666; margin-bottom: 2rem;">👈 Register in the sidebar to get started!</p>
        </div>
        """, unsafe_allow_html=True)

    # Community Stats Preview
    st.divider()
    stats = firebase.get_stats()
    st.markdown("### 📊 Community Impact So Far")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Repairs", stats.get('total', 0))
    with col2:
        st.metric("Items Saved", "0", "+0 this month", delta_color="off")
    with col3:
        st.metric("Community Members", len(firebase.get_all_users()))
    with col4:
        st.metric("Skills Shared", "15+", "and counting")


# TODO Rename this here and in `main`
def _extracted_from_main_170(firebase):
    user = st.session_state.current_user

    # Welcome message
    st.markdown(f"### 👋 Welcome back, {user['name']}!")
    st.markdown(f"**📍 Based in {user['location']}** • 🛠️ {len(user.get('skills', []))} skills registered")

    # Hero section with call to action
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
            <div style="background: linear-gradient(135deg, #E3F2FD 0%, #BBDEFB 100%); 
                        padding: 2rem; border-radius: 15px; margin: 1rem 0;">
                <h3 style="color: #0D47A1; margin-top: 0;">Ready to Make a Difference?</h3>
                <p style="color: #1565C0;">Every repair saves items from landfills, saves money, 
                and brings neighbors closer together. What will you fix today?</p>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        if st.button("🚀 Start New Repair", use_container_width=True, type="primary"):
            st.switch_page("pages/1_📝_Log_Request.py")

    action_cols = _extracted_from_main_192(
        st, "### 📋 What Would You Like to Do?", 3
    )
    with action_cols[0]:
        st.markdown("""
            <div style="text-align: center; padding: 1.5rem;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">📝</div>
                <h4>Log a Repair</h4>
                <p>Something broken? Let the community help fix it!</p>
            </div>
            """, unsafe_allow_html=True)
        if st.button("Log Repair Request", key="action_log", use_container_width=True):
            st.switch_page("pages/1_📝_Log_Request.py")

    with action_cols[1]:
        st.markdown("""
            <div style="text-align: center; padding: 1.5rem;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">🔍</div>
                <h4>Browse Requests</h4>
                <p>Find items you can fix with your skills</p>
            </div>
            """, unsafe_allow_html=True)
        if st.button("View Open Requests", key="action_browse", use_container_width=True):
            st.switch_page("pages/2_🔍_Browse_Requests.py")

    with action_cols[2]:
        st.markdown("""
            <div style="text-align: center; padding: 1.5rem;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">👷</div>
                <h4>My Repairs</h4>
                <p>Track repairs you're working on</p>
            </div>
            """, unsafe_allow_html=True)
        if st.button("View My Tasks", key="action_my", use_container_width=True):
            st.switch_page("pages/3_👷_Assign_Repairer.py")

    st.divider()

    # Recent Activity
    st.markdown("### 🔥 Recent Community Activity")
    if recent_requests := firebase.get_all_requests()[:4]:
        cols = st.columns(2)
        for idx, req in enumerate(recent_requests):
            with cols[idx % 2]:
                status_color = {
                    'open': '#FF9800',
                    'assigned': '#2196F3',
                    'resolved': '#4CAF50'
                }.get(req.get('status', 'open'), '#666')

                st.markdown(f"""
                    <div class="request-card">
                        <div style="display: flex; justify-content: space-between; align-items: start;">
                            <h4 style="margin: 0;">{req.get('item', 'Unknown Item')}</h4>
                            <span style="background: {status_color}; color: white; padding: 0.25rem 0.75rem; 
                                    border-radius: 12px; font-size: 0.8rem; font-weight: bold;">
                                {req.get('status', 'open').upper()}
                            </span>
                        </div>
                        <p style="color: #666; margin: 0.75rem 0; font-size: 0.9rem;">
                            {req.get('description', 'No description')[:80]}...
                        </p>
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <span style="color: #1E88E5; font-size: 0.85rem;">
                                📍 {req.get('requester_location', 'Unknown')}
                            </span>
                            <button onclick="window.location.href='/pages/3_👷_Assign_Repairer.py?request={req['id']}'" 
                                    style="background: #1E88E5; color: white; border: none; padding: 0.5rem 1rem; 
                                           border-radius: 5px; cursor: pointer; font-size: 0.85rem;">
                                View Details
                            </button>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
    else:
        st.info("No repair requests yet. Be the first to log one and inspire your community!")

    st.divider()

    # Community Impact
    st.markdown("### 🌍 Your Community Impact")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Items Saved", "0", "Start repairing!", delta_color="off")
    with col2:
        st.metric("Community Helpers", str(len(firebase.get_all_users())), "neighbors")
    with col3:
        st.metric("Waste Reduced", "0 kg", "Start your first repair!")

    # Mission statement
    st.markdown("---")
    st.markdown("""
        <div style="background: #F5F5F5; padding: 2rem; border-radius: 10px; margin-top: 2rem;">
            <h3 style="color: #1E88E5; text-align: center;">🌟 Our Mission</h3>
            <div style="display: flex; justify-content: space-between; text-align: center; margin-top: 1.5rem;">
                <div style="flex: 1; padding: 0 1rem;">
                    <div style="font-size: 2rem;">♻️</div>
                    <h4>Reduce Waste</h4>
                    <p>Give items a second life instead of sending them to landfills</p>
                </div>
                <div style="flex: 1; padding: 0 1rem; border-left: 1px solid #E0E0E0; border-right: 1px solid #E0E0E0;">
                    <div style="font-size: 2rem;">🤝</div>
                    <h4>Build Community</h4>
                    <p>Connect neighbors through shared skills and mutual help</p>
                </div>
                <div style="flex: 1; padding: 0 1rem;">
                    <div style="font-size: 2rem;">🎉</div>
                    <h4>Celebrate Skills</h4>
                    <p>Make invisible repair skills visible and valued</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)


# TODO Rename this here and in `main`
def _extracted_from_main_74(firebase):
    user = st.session_state.current_user

    st.markdown("### 👤 Your Profile")
    with st.container():
        st.markdown(f"""
                <div class="user-card">
                    <div style="font-size: 1.2rem; font-weight: bold; color: #1E88E5;">{user['name']}</div>
                    <div style="color: #666; margin: 0.5rem 0;">📍 {user['location']}</div>
                """, unsafe_allow_html=True)

        if user.get('skills'):
            st.markdown("**Your Skills:**")
            for skill in user['skills'][:3]:  # Show first 3 skills
                st.markdown(f'<span class="skill-badge">{skill}</span>', unsafe_allow_html=True)
            if len(user['skills']) > 3:
                st.caption(f"+ {len(user['skills']) - 3} more skills")
        st.markdown("</div>", unsafe_allow_html=True)

    # Logout button
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.current_user = None
        st.rerun()

    st.divider()

    # Quick Navigation
    st.markdown("### 🧭 Quick Actions")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("📝 Log Repair", use_container_width=True):
            st.switch_page("pages/1_📝_Log_Request.py")
    with col2:
        if st.button("🔍 Browse", use_container_width=True):
            st.switch_page("pages/2_🔍_Browse_Requests.py")

    col3, col4 = st.columns(2)
    with col3:
        if st.button("👷 My Tasks", use_container_width=True):
            st.switch_page("pages/3_👷_Assign_Repairer.py")
    with col4:
        if st.button("✅ Complete", use_container_width=True):
            st.switch_page("pages/4_✅_Resolve_&_Gratitude.py")

    st.divider()

    # Community Stats in Sidebar
    st.markdown("### 📊 Community Stats")
    stats = firebase.get_stats()

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
                <div class="stats-card">
                    <div class="metric-value">{stats.get('total', 0)}</div>
                    <div class="metric-label">Total Repairs</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown(f"""
                <div class="stats-card">
                    <div class="metric-value" style="color: #FF9800;">{stats.get('open', 0)}</div>
                    <div class="metric-label">Need Help</div>
                </div>
                """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
                <div class="stats-card">
                    <div class="metric-value" style="color: #2196F3;">{stats.get('assigned', 0)}</div>
                    <div class="metric-label">In Progress</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown(f"""
                <div class="stats-card">
                    <div class="metric-value" style="color: #4CAF50;">{stats.get('resolved', 0)}</div>
                    <div class="metric-label">Completed</div>
                </div>
                """, unsafe_allow_html=True)

    st.divider()

    # Quick tip
    st.markdown("""
            ### 💡 Tip of the Day
            *"The most sustainable item is the one you already own. 
            Repairing saves money, builds skills, and strengthens community bonds."*
            """)


# TODO Rename this here and in `main`
def _extracted_from_main_22(firebase):
    name = st.text_input("Your Name", placeholder="John Doe")
    location = st.text_input("Your Location", placeholder="Neighborhood, City")
    skills = st.text_input("Your Skills (comma-separated)", 
                         placeholder="electrical, sewing, carpentry, plumbing")

    col1, col2 = st.columns(2)
    with col1:
        submit = st.form_submit_button("🚀 Join Community", use_container_width=True)
    with col2:
        demo = st.form_submit_button("👀 Try Demo", use_container_width=True)

    if submit:
        if name and location:
            user_data = {
                'name': name,
                'location': location,
                'skills': [s.strip() for s in skills.split(',')] if skills else []
            }

            # Check if user exists
            all_users = firebase.get_all_users()
            if existing_user := next(
                (
                    u
                    for u in all_users
                    if u['name'].lower() == name.lower()
                    and u['location'].lower() == location.lower()
                ),
                None,
            ):
                st.session_state.current_user = existing_user
                st.success(f"Welcome back, {name}!")
            elif user_id := firebase.create_user(user_data):
                user_data['id'] = user_id
                st.session_state.current_user = user_data
                st.success(f"Welcome to the community, {name}!")
            st.rerun()
        else:
            st.error("Please enter your name and location")

    if demo:
        # Create demo user
        demo_user = {
            'id': 'demo_user_123',
            'name': 'Demo User',
            'location': 'Community Center',
            'skills': ['electrical', 'general handyman']
        }
        st.session_state.current_user = demo_user
        st.success("Demo mode activated! Explore the app.")
        st.rerun()


# TODO Rename this here and in `main`
def _extracted_from_main_192(st, arg1, arg2):
    st.divider()

        # Action Cards
    st.markdown(arg1)
    return st.columns(arg2)

if __name__ == "__main__":
    main()