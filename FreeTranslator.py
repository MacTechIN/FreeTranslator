import streamlit as st
import requests
from gtts import gTTS
from io import BytesIO
import base64


# Define the translation function using an OpenAPI
def translate(text, source_language, target_language):
    # Define your translation API endpoint
    TRANSLATION_API_URL = 'https://libretranslate.de/translate'
    response = requests.post(
        TRANSLATION_API_URL,
        data={'q': text, 'source': source_language, 'target': target_language},
        headers={'Content-Type': 'application/x-www-form-urlencoded'}
    )
    # Check if the request was successful
    if response.status_code == 200:
        return response.json().get('translatedText', 'Translation Error')
    else:
        return 'Error: The translation service failed.'

# Streamlit application layout
def main():
    st.title("Teacher Sam's Free Language Translator")
    st.write("This is my Multi Language translator, you can choose SL,TL by your self and click the button. ")
    st.write("Please contact me wooriszhome@gmail.com if you have any questions !!")

    # Language selection
    source_language = st.selectbox('Select source language', ('en', 'es', 'ko', 'fr', 'it'))
    target_language = st.selectbox('Select target language', ('en', 'es', 'ko', 'fr', 'it'))

    # Text area for user input
    text_to_translate = st.text_area('Enter the text to translate')

    # Translate button
    if st.button('Translate'):
        if text_to_translate:
            # Perform the translation
            translation = translate(text_to_translate, source_language, target_language)
            # Display the translation
            st.text_area('Translation', translation, height=150)

            if translation:
                tts = gTTS(translation, lang=target_language)
                tts_file = BytesIO()
                tts.write_to_fp(tts_file)
                tts_file.seek(0)
                b64 = base64.b64encode(tts_file.read()).decode()
                href = f'<a href="data:audio/mp3;base64,{b64}" download="translation.mp3">Download Translation Voice</a>'
                st.markdown(href, unsafe_allow_html=True)
        else:
            st.error('Please enter some text to translate.')

if __name__ == "__main__":
    main()