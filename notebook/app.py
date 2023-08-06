import pickle
import streamlit as st
import re

global langdetect_Model

# Load the language detection model 
with open('model.pckl', 'rb') as f:
    langdetect_Model = pickle.load(f)

# Clean Function
def clean_text(text):
    
    # Converting the text to lower case
    text = text.lower()
    
    # Removing the symbols and numbers
    text = re.sub(r'[\([{})\]!@#$,’&-_/"%^*?؟:;~`0-9\.]', ' ', text)
             
    # Removing URLs
    text = re.sub('http\S+\s*', ' ', text)
    
    # Removing RT and cc
    text = re.sub('RT|cc', ' ', text)
    
    # Removing hashtags
    text = re.sub('#\S+', '', text)
    
    # Removing mentions
    text = re.sub('@\S+', '  ', text)
    
    # Removing extra whitespace
    text = re.sub('\s+', ' ', text)
    
    return text

# Streamlit app
st.title("Language Detection Tool")
input_test = st.text_input("Enter your text input here", "Hello, how are you?")

if st.button("Detect the Language"):
    if input_test:
        # Clean the input text
        input_test_clean = clean_text(input_test)
        print(input_test_clean)
        # Check if the cleaned input is valid
        if not re.match('^[A-Za-z\s]+$', input_test_clean) and not re.match('^[\u0621-\u064A\s]+$', input_test_clean):
            st.text("The input must be a text in English or Arabic.")
        elif re.search(r'(.)\1{3,}', input_test_clean):
            st.text("Wrong input.")
        else:
            # Get a list of predictions
            predictions = langdetect_Model.predict([input_test_clean])
            # Convert each prediction to a plain string
            predictions_plain = [p[:] for p in predictions]
            # Check if the predicted language is English or Arabic
            if "Arabic" in predictions_plain or "English" in predictions_plain:
                st.text(", ".join(predictions_plain)) # Display the predicted languages as a comma-separated string
            else:
                st.text("The input must be a text in English or Arabic.")
    else:
        st.text("Please enter some text to detect the language.")
