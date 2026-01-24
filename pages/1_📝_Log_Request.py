# pages/1_📝_Log_Request.py
import streamlit as st
from firebase_service import FirebaseService
from datetime import datetime

st.set_page_config(page_title="Log Repair Request", page_icon="📝")

# Header
st.markdown("<h1 class='main-header'>📝 Log Repair Request</h1>", unsafe_allow_html=True)
st.markdown("### Share what needs fixing in your community")

# Check if user is logged in
if 'current_user' not in st.session_state or st.session_state.current_user is None:
    st.warning("Please register/sign in from the main page first.")
    if st.button("Go to Main Page"):
        st.switch_page("app.py")
    st.stop()

firebase = FirebaseService.get_instance()
user = st.session_state.current_user

# Log request form
with st.form("log_request_form"):
    st.markdown(f"**Requester:** {user['name']} ({user['location']})")
    
    item = st.text_input("What needs repair?*", placeholder="e.g., Kettle, Chair, Jacket zipper")
    description = st.text_area("Describe the issue*", placeholder="What's wrong? What have you tried? What materials might be needed?")
    
    col1, col2 = st.columns(2)
    with col1:
        urgency = st.selectbox("Urgency", ["Low", "Medium", "High"], help="How soon do you need this fixed?")
    with col2:
        location_notes = st.text_input("Location for repair", placeholder="e.g., My place, Community center, Can transport")
    
    skill_category = st.selectbox(
        "What skill is needed?",
        ["", "Electrical", "Carpentry/Woodwork", "Sewing/Textiles", "Plumbing", 
         "Mechanical", "Electronics", "General Handyman", "Other"]
    )
    
    other_skill = ""
    if skill_category == "Other":
        other_skill = st.text_input("Please specify the skill needed")
    
    notes = st.text_area("Additional notes", placeholder="Any specific tools needed? Best times to meet?")
    
    submitted = st.form_submit_button("Submit Repair Request", use_container_width=True)
    
    if submitted:
        if not item or not description:
            st.error("Please fill in all required fields (marked with *)")
        else:
            request_data = {
                'item': item,
                'description': description,
                'urgency': urgency,
                'location_notes': location_notes,
                'skill_needed': other_skill if skill_category == "Other" else skill_category,
                'notes': notes,
                'requester_id': user['id'],
                'requester_name': user['name'],
                'requester_location': user['location'],
                'status': 'open'
            }
            
            request_id = firebase.create_repair_request(request_data)
            if request_id:
                st.success("✅ Repair request logged successfully!")
                st.balloons()
                st.info("Your request is now visible to the community. Someone with the right skills will offer to help!")
                
                # Show next steps
                st.markdown("### What happens next?")
                st.markdown("""
                1. **Community sees your request** - Neighbors can browse open requests
                2. **Skill match** - Someone with the right skills will offer to help
                3. **Connect** - Arrange a time/place for the repair
                4. **Fix & celebrate** - Complete the repair and share gratitude
                """)
                
                if st.button("Browse other requests"):
                    st.switch_page("pages/2_🔍_Browse_Requests.py")
            else:
                st.error("Failed to create repair request. Please try again.")

# Back button
st.divider()
if st.button("← Back to Main Page"):
    st.switch_page("app.py")