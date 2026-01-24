# pages/4_✅_Resolve_&_Gratitude.py
import streamlit as st
from firebase_service import FirebaseService
from datetime import datetime

st.set_page_config(page_title="Resolve & Gratitude", page_icon="✅")

# Header
st.markdown("<h1 class='main-header'>✅ Complete Repair</h1>", unsafe_allow_html=True)
st.markdown("### Mark as fixed and share gratitude")

# Check if user is logged in
if 'current_user' not in st.session_state or st.session_state.current_user is None:
    st.warning("Please register/sign in from the main page first.")
    if st.button("Go to Main Page"):
        st.switch_page("app.py")
    st.stop()

firebase = FirebaseService.get_instance()
user = st.session_state.current_user

# Get assigned repairs
assigned_requests = firebase.get_user_requests(user['id'], role='assignee')

# Get requested repairs (for showing gratitude)
my_requests = firebase.get_user_requests(user['id'], role='requester')

# Tab layout
tab1, tab2 = st.tabs(["🔧 My Assigned Repairs", "💝 My Requests"])

with tab1:
    if not assigned_requests:
        st.info("You haven't been assigned any repair requests yet.")
        if st.button("Browse requests to help", type="primary"):
            st.switch_page("pages/2_🔍_Browse_Requests.py")
    else:
        # Filter for in-progress repairs
        in_progress = [r for r in assigned_requests if r.get('status') == 'assigned']
        completed = [r for r in assigned_requests if r.get('status') == 'resolved']
        
        if in_progress:
            st.markdown(f"### In Progress ({len(in_progress)})")
            for req in in_progress:
                with st.expander(f"🛠️ {req.get('item', 'Unknown Item')}"):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.write(req.get('description', 'No description'))
                        st.caption(f"📍 {req.get('requester_location', 'Unknown')}")
                        st.caption(f"Requested by: {req.get('requester_name', 'Anonymous')}")
                    with col2:
                        if st.button("Mark Resolved", key=f"resolve_{req['id']}"):
                            st.session_state.selected_request = req['id']
                            st.rerun()
            
            st.divider()
        
        if completed:
            st.markdown(f"### Completed ({len(completed)})")
            for req in completed:
                with st.expander(f"✅ {req.get('item', 'Unknown Item')}"):
                    st.write(req.get('description', 'No description'))
                    st.caption(f"📍 {req.get('requester_location', 'Unknown')}")
                    st.caption(f"Requested by: {req.get('requester_name', 'Anonymous')}")
                    
                    if req.get('gratitude_note'):
                        st.info(f"**Gratitude:** {req.get('gratitude_note')}")
                    
                    resolved_at = req.get('resolved_at')
                    if isinstance(resolved_at, datetime):
                        st.caption(f"Resolved on: {resolved_at.strftime('%B %d, %Y')}")

with tab2:
    if not my_requests:
        st.info("You haven't requested any repairs yet.")
        if st.button("Request a repair", type="primary"):
            st.switch_page("pages/1_📝_Log_Request.py")
    else:
        # Show gratitude for resolved repairs
        resolved_requests = [r for r in my_requests if r.get('status') == 'resolved']
        
        if resolved_requests:
            st.markdown("### Thank Your Repairer")
            st.info("Share your appreciation for neighbors who helped fix your items!")
            
            for req in resolved_requests:
                with st.expander(f"✅ {req.get('item', 'Unknown Item')}"):
                    if req.get('assigned_to_id'):
                        repairer = firebase.get_user(req.get('assigned_to_id'))
                        if repairer:
                            st.markdown(f"**Fixed by:** {repairer.get('name', 'Anonymous')}")
                    
                    if req.get('gratitude_note'):
                        st.success(f"**Your gratitude note:** {req.get('gratitude_note')}")
                    else:
                        # Option to add gratitude note
                        with st.form(key=f"gratitude_form_{req['id']}"):
                            gratitude = st.text_area("Share your appreciation", 
                                                   placeholder="Thank you for your help! What did this repair mean to you?")
                            if st.form_submit_button("Send Gratitude"):
                                if gratitude:
                                    success = firebase.resolve_request(req['id'], gratitude)
                                    if success:
                                        st.success("Thank you for sharing your gratitude!")
                                        st.rerun()
        else:
            st.info("Your repair requests are still in progress. Check back when they're completed!")

# Handle resolution if a request was selected
if 'selected_request' in st.session_state:
    request_id = st.session_state.selected_request
    request = firebase.get_repair_request(request_id)
    
    if request and request.get('status') == 'assigned' and request.get('assigned_to_id') == user['id']:
        st.divider()
        st.markdown("### 🎉 Complete This Repair")
        
        with st.form("resolve_form"):
            st.markdown(f"**Item:** {request.get('item', 'Unknown Item')}")
            st.markdown(f"**Requester:** {request.get('requester_name', 'Anonymous')}")
            
            gratitude_note = st.text_area(
                "Share a gratitude note (optional)",
                placeholder="Thank the requester or share something about the repair experience...",
                help="This will be visible to the requester and community"
            )
            
            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button("✅ Mark as Resolved", type="primary", use_container_width=True):
                    success = firebase.resolve_request(request_id, gratitude_note)
                    if success:
                        st.success("Repair marked as resolved! Thank you for your contribution to the community.")
                        st.balloons()
                        st.session_state.pop('selected_request', None)
                        st.rerun()
            with col2:
                if st.form_submit_button("Cancel", use_container_width=True):
                    st.session_state.pop('selected_request', None)
                    st.rerun()

# Navigation
st.divider()
col1, col2 = st.columns(2)
with col1:
    if st.button("← Back to Main Page", use_container_width=True):
        st.switch_page("app.py")
with col2:
    if st.button("Browse More Requests", use_container_width=True):
        st.switch_page("pages/2_🔍_Browse_Requests.py")