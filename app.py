import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from PIL import Image

# 1. API Configuration
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Page settings
st.set_page_config(page_title="AI Food Analyzer", page_icon="🥗")

st.title("🥗 AI Food and Calorie Analyzer / Tracker")
st.caption("Upload or take a photo of your meal to analyze calories and macronutrients.")

# Prompt for AI
prompt = """
You are an expert nutritionist and chef.

Analyze the food in this image and return:

1. Food name
2. Ingredients detected
3. Estimated calories for each ingredient and total calories
4. Estimated macronutrients:
   - Protein (grams)
   - Carbohydrates (grams)
   - Fat (grams)

Format the result clearly like this:

Food: ...
Ingredients: ...

Calories:
- ingredient 1: ...
- ingredient 2: ...

Total: ...

Macronutrients:
Protein: ... g
Carbs: ... g
Fat: ... g

Be concise and do not add extra commentary.
"""

# Image source selection
option = st.radio("Choose image source:", ["Upload Photo", "Take Photo"])

if option == "Upload Photo":
    uploaded_file = st.file_uploader("Choose a food photo...", type=["jpg", "jpeg", "png"])
else:
    uploaded_file = st.camera_input("Take a photo of your meal")

# If image exists
if uploaded_file is not None:

    image = Image.open(uploaded_file)

    st.image(image, caption="Your Meal", use_container_width=True)

    analyze_button = st.button("Analyze Meal")

    if analyze_button:

        with st.spinner("Analyzing your plate..."):

            try:
                model = genai.GenerativeModel("gemini-2.5-flash")

                response = model.generate_content([prompt, image])

                st.markdown("### 🍽 Analysis")
                st.markdown(response.text)

            except Exception as e:
                st.error(f"An error occurred: {e}")

else:
    st.info("Please upload or take a photo to start the analysis.")
