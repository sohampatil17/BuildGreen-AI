import streamlit as st
from PyPDF2 import PdfReader
from fpdf import FPDF
import openai
import os, io
import base64
import time

# Assuming your OpenAI API key is set in your environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

class LEEDComplianceChecker:
    def __init__(self):
        self.model = "gpt-4-0125-preview" 

    def read_pdf(self, file):
        try:
            # Ensure the file is in BytesIO format for PdfReader
            if not isinstance(file, io.BytesIO):
                file = io.BytesIO(file.read())

            reader = PdfReader(file)
            text = ""
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:  # Ensure page_text is not None or empty
                    text += page_text
                else:
                    st.warning("A page in the PDF did not contain any text.")
            return text.strip()  # Return the extracted text, stripped of leading/trailing whitespace
        except Exception as e:
            st.error(f"An error occurred while reading the PDF: {e}")
            return None

    def upload_pdf(self):
        uploaded_file = st.file_uploader("Upload your LEED report PDF", type=["pdf"])
        if uploaded_file is not None:
            # Display the PDF
            st.success('PDF uploaded successfully!')
            st.write('Your LEED report PDF:')
            base64_pdf = base64.b64encode(uploaded_file.getvalue()).decode('utf-8')
            pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="700" height="800" type="application/pdf">'
            st.markdown(pdf_display, unsafe_allow_html=True)

            # Extract and return the text for further analysis
            return self.read_pdf(uploaded_file)
        return None


    def analyze_compliance(self, text):
        try:
            response = openai.chat.completions.create(
                model="gpt-4-0125-preview",
                messages=[
                    {"role": "system", "content": "You are an AI trained to help with LEED compliance."},
                    {"role": "user", "content": "Help me identify compliance issues with my property in the text provided and provide recommendations in bullet points:" + text}
                ]
            )
            response_message = response.choices[0].message.content
            return response_message
        except Exception as e:
            st.error(f"An error occurred while analyzing the text: {e}")
            return "Unable to analyze compliance."
        

    def run(self):
        st.title("LEED Compliance Checker")
                
        col1, col2 = st.columns(2)

        with col1:  # This will ensure the following content is in the first column
            text = self.upload_pdf()
            if text:
                # Check if the extracted text is not just empty or whitespace
                if text.strip():
                    st.write("")
                    st.write("Analyzing document for compliance issues...")
                    words = text.split() 
                    compliance_analysis = self.analyze_compliance(text)
                    st.subheader("Compliance Analysis:")
                    st.write(compliance_analysis if compliance_analysis else "No analysis found.")
                else:
                    st.error("Extracted text is empty. Please check the PDF content.")
            else:
                st.error("Please upload your property documentation/ report.")
            
            

        with col2:  # Content for the second column (Checklist and tracker)
            st.subheader("LEED Compliance Checklist")

            criteria = [
                "Site selection criteria", "Public transportation access", "Bike storage and changing room facilities",
                "Stormwater management", "Heat island effect reduction for roof and non-roof", "Light pollution reduction",
                "Water-efficient landscaping", "Innovative wastewater technologies", "Water use reduction (fixtures and fittings)",
                "Outdoor water use reduction", "Indoor water use reduction", "Metering and water performance measurement",
                "Fundamental and enhanced commissioning of building systems", "Minimum energy performance optimization",
                "Renewable energy production", "Enhanced refrigerant management", "Building energy metering and performance optimization",
                "Building life-cycle impact reduction", "Construction and demolition waste management", "Sourcing of raw materials",
                "Material ingredient reporting and optimization", "Long-term commitment to product sustainability",
                "Minimum indoor air quality performance", "Environmental tobacco smoke control", "Low-emitting materials",
                "Indoor lighting quality", "Thermal comfort design and verification", "Acoustic performance"
            ]
            
            if 'progress' not in st.session_state:
                st.session_state.progress = {criteria_item: "Not Started" for criteria_item in criteria}

            # Calculate total progress to display at the top
            progress_values = {"Not Started": 0, "Pursuing": 0.5, "Completed": 1}
            total_progress = sum(progress_values[st.session_state.progress[criteria_item]] for criteria_item in criteria)
            progress_percentage = (total_progress / len(criteria)) * 100
            st.metric(label="Total Progress", value=f"{progress_percentage:.2f}%")
            st.progress(progress_percentage / 100)

            # Create buttons for each status and update the progress based on user interaction
            for criteria_item in criteria:
                st.markdown(f"**{criteria_item}**")  # Bolden criteria name
                col1, col2, col3 = st.columns(3)

                if st.session_state.progress[criteria_item] == "Not Started":
                    col1.button("Not Started", key=f"{criteria_item}_not_started", disabled=True)
                else:
                    if col1.button("Not Started", key=f"{criteria_item}_not_started"):
                        st.session_state.progress[criteria_item] = "Not Started"

                # Pursuing Button
                if st.session_state.progress[criteria_item] == "Pursuing":
                    col2.button("Pursuing", key=f"{criteria_item}_pursuing", disabled=True)
                else:
                    if col2.button("Pursuing", key=f"{criteria_item}_pursuing"):
                        st.session_state.progress[criteria_item] = "Pursuing"

                # Completed Button
                if st.session_state.progress[criteria_item] == "Completed":
                    col3.button("Completed", key=f"{criteria_item}_completed", disabled=True)
                else:
                    if col3.button("Completed", key=f"{criteria_item}_completed"):
                        st.session_state.progress[criteria_item] = "Completed"
    
if __name__ == "__main__":
    checker = LEEDComplianceChecker()
    checker.run()
