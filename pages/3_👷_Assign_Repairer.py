# pages/3_👷_Assign_Repairer.py
import streamlit as st
from firebase_service import FirebaseService
from datetime import datetime

st.set_page_config(page_title="Assign Repairer", page_icon="👷")

# Header
st.markdown("<h1 class='main-header'>👷 Repair Request Details</h1>", unsafe_allow_html=True)

# Check if user is logged in
if 'current_user' not in st.session_state or st.session_state.current_user is None:
    st.warning("Please register/sign in from the main page first.")
    if st.button("Go to Main Page"):
        st.switch_page("app.py")
    st.stop()

firebase = FirebaseService.get_instance()
user = st.session_state.current_user

# Get request ID from session state or URL params
request_id = st.session_state.get('selected_request')
if not request_id:
    st.error("No repair request selected. Please browse requests first.")
    if st.button("Browse Requests"):
        st.switch_page("pages/2_🔍_Browse_Requests.py")
    st.stop()

# Fetch request details
request = firebase.get_repair_request(request_id)
if not request:
    st.error("Repair request not found.")
    if st.button("Browse Requests"):
        st.switch_page("pages/2_🔍_Browse_Requests.py")
    st.stop()

# Display request details
col1, col2 = st.columns([2, 1])

with col1:
    # Status badge
    status = request.get('status', 'open')
    status_display = {
        'open': ('🟠 Open', 'Waiting for someone to help'),
        'assigned': ('🔵 In Progress', f"Being fixed by {request.get('assigned_to_name', 'a neighbor')}"),
        'resolved': ('🟢 Resolved', f"Fixed on {request.get('resolved_at', datetime.now()).strftime('%b %d') if isinstance(request.get('resolved_at'), datetime) else 'recently'}")
    }.get(status, ('⚪ Unknown', ''))
    
    st.markdown(f"## {status_display[0]}")
    st.caption(status_display[1])
    
    st.markdown(f"### {request.get('item', 'Unknown Item')}")
    st.markdown(f"**Location:** {request.get('requester_location', 'Not specified')}")
    st.markdown(f"**Urgency:** {request.get('urgency', 'Medium')}")
    
    if request.get('skill_needed'):
        st.markdown(f"**Skill needed:** {request.get('skill_needed')}")
    
    st.markdown("---")
    st.markdown("#### 📝 Description")
    st.write(request.get('description', 'No description provided'))
    
    if request.get('notes'):
        st.markdown("#### 📋 Additional Notes")
        st.write(request.get('notes'))
    
    if request.get('location_notes'):
        st.markdown("#### 📍 Location Details")
        st.write(request.get('location_notes'))

with col2:
    st.markdown("#### 👤 Requester")
    st.markdown(f"**{request.get('requester_name', 'Anonymous')}**")
    st.caption(f"📍 {request.get('requester_location', 'Unknown location')}")
    
    created_at = request.get('created_at', datetime.now())
    if isinstance(created_at, datetime):
        st.caption(f"📅 {created_at.strftime('%B %d, %Y')}")
    
    st.markdown("---")
    
    # Action section based on status
    if status == 'open':
        st.markdown("#### 🤝 Can You Help?")
        
        # Check if user has matching skills
        user_skills = user.get('skills', [])
        needed_skill = request.get('skill_needed', '').lower()
        has_matching_skill = any(skill.lower() in needed_skill or needed_skill in skill.lower() 
                               for skill in user_skills) if user_skills else False
        
        if has_matching_skill:
            st.success("✅ You have skills that match this request!")
        
        if st.button("I'll Fix This!", type="primary", use_container_width=True):
            success = firebase.assign_repairer(request_id, user['id'])
            if success:
                st.success(f"✅ You're now assigned to fix this {request.get('item', 'item')}!")
                st.balloons()
                st.info(f"**Next steps:** Contact {request.get('requester_name')} to arrange the repair.")
                
                # Update request in session
                request['status'] = 'assigned'
                request['assigned_to_id'] = user['id']
                
                st.rerun()
            else:
                st.error("Failed to assign repairer. Please try again.")
    
    elif status == 'assigned':
        assigned_to_id = request.get('assigned_to_id')
        if assigned_to_id == user['id']:
            st.success("✅ You're assigned to fix this!")
            if st.button("Mark as Resolved", type="primary", use_container_width=True):
                st.session_state.selected_request = request_id
                st.switch_page("pages/4_✅_Resolve_&_Gratitude.py")
        else:
            st.info("This request is already being handled by someone else.")
    
    elif status == 'resolved':
        st.success("✅ This repair has been completed!")
        if request.get('gratitude_note'):
            st.markdown("#### 💝 Gratitude Note")
            st.info(f'"{request.get("gratitude_note")}"')
    
    st.markdown("---")
    
    # Navigation buttons
    if st.button("Browse More Requests", use_container_width=True):
        st.switch_page("pages/2_🔍_Browse_Requests.py")
    
    if st.button("Back to Main Page", use_container_width=True):
        st.switch_page("app.py")