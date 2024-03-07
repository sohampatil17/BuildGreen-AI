import streamlit as st
from main import LEEDComplianceChecker

checker = LEEDComplianceChecker()

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
            st.success('You selected BREEAM')
        if st.button('Energy STAR', key='3'):
            st.success('You selected Energy STAR')
        if st.button('Green Globes', key='4'):
            st.success('You selected Green Globes')
            
if 'page' not in st.session_state:
    st.session_state['page'] = 'home'

# Main app logic
if st.session_state['page'] == 'home':
    render_home()
elif st.session_state['page'] == 'LEED':
    # Clear the page
    st.empty()
    # Create an instance of the LEEDComplianceChecker class and display its UI
    checker = LEEDComplianceChecker()
    checker.run()