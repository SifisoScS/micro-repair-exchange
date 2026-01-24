# pages/2_🔍_Browse_Requests.py
import streamlit as st
from firebase_service import FirebaseService
from datetime import datetime

st.set_page_config(page_title="Browse Repair Requests", page_icon="🔍")

# Header
st.markdown("<h1 class='main-header'>🔍 Browse Repair Requests</h1>", unsafe_allow_html=True)
st.markdown("### Find items that need fixing in your community")

# Check if user is logged in
if 'current_user' not in st.session_state or st.session_state.current_user is None:
    st.warning("Please register/sign in from the main page first.")
    if st.button("Go to Main Page"):
        st.switch_page("app.py")
    st.stop()

firebase = FirebaseService.get_instance()
user = st.session_state.current_user

# Filters
st.sidebar.header("🔍 Filters")
status_filter = st.sidebar.multiselect(
    "Status",
    ["open", "assigned", "resolved"],
    default=["open", "assigned"]
)

skill_filter = st.sidebar.selectbox(
    "Skill Needed",
    ["All", "Electrical", "Carpentry/Woodwork", "Sewing/Textiles", 
     "Plumbing", "Mechanical", "Electronics", "General Handyman"]
)

location_filter = st.sidebar.text_input("Location (optional)")

urgency_filter = st.sidebar.multiselect(
    "Urgency",
    ["High", "Medium", "Low"],
    default=["High", "Medium", "Low"]
)

# Get all requests
all_requests = firebase.get_all_requests()

# Apply filters
filtered_requests = []
for req in all_requests:
    if req.get('status') not in status_filter:
        continue
    if skill_filter != "All" and req.get('skill_needed') != skill_filter:
        continue
    if location_filter and location_filter.lower() not in req.get('requester_location', '').lower():
        continue
    if req.get('urgency') not in urgency_filter:
        continue
    filtered_requests.append(req)

# Display results
if not filtered_requests:
    st.info("No repair requests match your filters. Try adjusting them or check back later!")
else:
    st.success(f"Found {len(filtered_requests)} repair request(s)")
    
    for req in filtered_requests:
        with st.container():
            col1, col2 = st.columns([3, 1])
            
            with col1:
                # Status badge
                status = req.get('status', 'open')
                status_color = {
                    'open': '🟠',
                    'assigned': '🔵', 
                    'resolved': '🟢'
                }.get(status, '⚪')
                
                st.markdown(f"**{status_color} {req.get('item', 'Unknown Item')}**")
                st.caption(f"📍 {req.get('requester_location', 'Unknown location')} | "
                          f"⏱️ {req.get('urgency', 'Medium')} urgency")
                
                st.markdown(f"*{req.get('description', 'No description')}*")
                
                # Skill needed
                skill = req.get('skill_needed')
                if skill:
                    st.markdown(f"**Skill needed:** {skill}")
                
                # Requester info
                st.caption(f"Requested by {req.get('requester_name', 'Anonymous')} • "
                          f"{req.get('created_at', datetime.now()).strftime('%b %d, %Y') if isinstance(req.get('created_at'), datetime) else 'Recently'}")
            
            with col2:
                # Action buttons based on status
                if status == 'open':
                    if st.button("Offer to Fix", key=f"offer_{req['id']}", type="primary"):
                        st.session_state.selected_request = req['id']
                        st.switch_page("pages/3_👷_Assign_Repairer.py")
                elif status == 'assigned':
                    assigned_to = req.get('assigned_to_id')
                    if assigned_to == user['id']:
                        if st.button("Mark Resolved", key=f"resolve_{req['id']}"):
                            st.session_state.selected_request = req['id']
                            st.switch_page("pages/4_✅_Resolve_&_Gratitude.py")
                    else:
                        st.info("Assigned")
                elif status == 'resolved':
                    st.success("✅ Resolved")
                
                # View details button
                if st.button("View Details", key=f"details_{req['id']}"):
                    st.session_state.selected_request = req['id']
                    st.switch_page("pages/3_👷_Assign_Repairer.py")
            
            st.divider()

# Back button
st.divider()
if st.button("← Back to Main Page"):
    st.switch_page("app.py")