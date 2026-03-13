import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from PIL import Image

# 1. API Configuration
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

st.set_page_config(page_title="AI Food Analyzer", page_icon="🥗")
st.title("🥗 AI Food and Calorie Analyzer/Tracker")
st.caption("Upload a photo of your meal to get its name and estimated calories!")

# 2. Image Upload Section
uploaded_file = st.file_uploader("Choose a food photo...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Plate', use_container_width=True)
    
    analyze_button = st.button("Analyze Meal")

    if analyze_button:
        with st.spinner("Analyzing your plate..."):
            try:
                # Using Gemini 2.5 Flash for multimodal analysis
                model = genai.GenerativeModel("gemini-2.5-flash")
                
                # Concise English prompt
                prompt = """
                You are an expert dietician and chef. Examine this photo and:
                Analyze this photo and provide these two pieces of information:
                1. Name of the food or the main ingredients of food.
                2. Estimated total calories(firstly respectively for every ingredient and then totally).
                
                Be brief and concise. Do not add any extra explanations or greetings.
                """
                
                # Generate content
                response = model.generate_content([prompt, image])
                
                st.subheader("🍴 Result:")
                st.write(response.text)
                
            except Exception as e:
                st.error(f"An error occurred: {e}")
else:
    st.info("Please upload a photo to start the analysis.")