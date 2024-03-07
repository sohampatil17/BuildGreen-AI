import streamlit as st
from main import LEEDComplianceChecker
from Breaam import BREEAMComplianceChecker
from energy_star import EnergyStarComplianceChecker
from green_globes import GreenGlobesComplianceChecker
from iso14001 import ISO14001ComplianceChecker

checker = LEEDComplianceChecker()
checker2 = BREEAMComplianceChecker()
checker3 = EnergyStarComplianceChecker()
checker4 = GreenGlobesComplianceChecker()
checker5 = ISO14001ComplianceChecker()

st.set_page_config(layout="wide")

def render_home():

    st.markdown("<h1 style='text-align: center; font-size: 85px; color: green;'> BuildGreen AI 🌎\n</h1>", unsafe_allow_html=True)
    st.text("")
    st.text("")
    st.text("")

    st.markdown("""
    <style>
    div.stButton > button {
        font-size: 16px !important;
        height: 50px; /* Fixed height */
        width: 200px; /* Fixed width */
        margin: 10px;
        border-radius: 5px;
    }
    </style>
    """, unsafe_allow_html=True)


    st.markdown("<h1 style='text-align: center; font-size: 30px; color:grey;'>Choose your compliance type\n</h1>", unsafe_allow_html=True)
    if 'show_checker' not in st.session_state:
        st.session_state['show_checker'] = False
        
    # Using columns to center the buttons
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        if st.button('LEED', key='1'):
            st.session_state['page'] = 'LEED'
        if st.button('BREEAM', key='2'):
            st.session_state['page'] = 'BREEAM'
        if st.button('Energy STAR', key='3'):
            st.session_state['page'] = 'Energy STAR'
        if st.button('Green Globes', key='4'):
            st.session_state['page'] = 'Green Globes'
        if st.button('ISO 14001', key='5'):
            st.session_state['page'] = 'IS0 14001'
            
if 'page' not in st.session_state:
    st.session_state['page'] = 'home'

# Main app logic
if st.session_state['page'] == 'home':
    render_home()
elif st.session_state['page'] == 'LEED':
    checker = LEEDComplianceChecker()
    checker.run()
elif st.session_state['page'] == 'BREEAM':
    st.empty()
    checker2 = BREEAMComplianceChecker()
    checker2.run()
elif st.session_state['page'] == 'Energy STAR':
    st.empty()
    checker3 = EnergyStarComplianceChecker()
    checker3.run()
elif st.session_state['page'] == 'Green Globes':
    st.empty()
    checker4 = GreenGlobesComplianceChecker()
    checker4.run()
elif st.session_state['page'] == 'ISO 14001':
    checker5 = ISO14001ComplianceChecker()
    checker5.run()