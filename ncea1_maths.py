import streamlit as st

# 1. Page Config MUST go here in the master file
st.set_page_config(page_title="NCEA Level 1 Maths Revision", page_icon="🎓", layout="centered")

# 2. Import your 6 modified app files
import algebra_ncea1_module as algebra
import graphs_ncea1_module as graphs
import trig_ncea1_module as trig
import linear_ncea1_module as linear
import tables_ncea1_module as tables
import geometry3d_ncea1_module as geometry

# 3. Create a tab-reset handler
def handle_nav_change():
    # When switching topics, force the new app to generate a fresh problem
    st.session_state.generating = True 
    st.session_state.pdf_bytes = None
    st.session_state.id_feedback = ""

# 4. Create the "Fake Tabs" (Horizontal Radio)
st.markdown("""
    <style>
    /* Make the radio buttons look like a clean tab bar */
    div[role="radiogroup"] {
        justify-content: center;
        gap: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

selected_app = st.radio(
    "Navigation", 
    ["Algebra", "Graphs", "Trig", "Linear", "Tables", "3D Geometry"],
    horizontal=True,
    label_visibility="collapsed",
    on_change=handle_nav_change
)

st.markdown("<hr style='margin: 0.2em 0px 1.5em 0px; border-color: #444;'>", unsafe_allow_html=True)

# 5. Route to the correct app
if selected_app == "Algebra":
    algebra.run_app()
elif selected_app == "Graphs":
    graphs.run_app()
elif selected_app == "Trig":
    trig.run_app()
elif selected_app == "Linear":
    linear.run_app()
elif selected_app == "Tables":
    tables.run_app()
elif selected_app == "3D Geometry":
    geometry.run_app()
