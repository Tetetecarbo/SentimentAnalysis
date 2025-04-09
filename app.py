import streamlit as st
import sys
sys.path.append('src')

from text_analysis import process_text
from image_retrieval import retrieve_images
from utils import log_error

def display_images(images):
    """Function to display images grid layout."""
    if images:
        st.subheader("Your Mood Board")
        cols = st.columns(3)
        for index, image in enumerate(images):
            with cols[index % 3]:
                st.image(image, width=220, use_column_width=True)
    else:
        st.write("No images to display yet.")

def main():
    """Main function to run the Streamlit app with a user-friendly interface."""
    # Path to the CSS file
    css_path = 'style.css'
    with open(css_path) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    # Display the logo
    logo_path = 'logo.png'  # Ensure 'logo.png' is in the same directory as this script
    st.image(logo_path, use_column_width=True)  # Display the logo at full width

    # Description beneath the logo
    st.markdown("""
    <div style="text-align: center;">
        <p>Welcome to our app that brings your words to life! Simply enter your text, and we'll create a mood board for you. Our tool analyzes the emotions and themes in your text, then selects images to match.</p>
        <p>🎨 Try our NLP Text-to-Image Mood Board Generator and see your words take on a whole new dimension! 🎨</p>
    </div>
    """, unsafe_allow_html=True)

    # Create a spacious and attractive text input area with a placeholder
    user_input = st.text_area(
        "Input Text",  # Added a label for accessibility
        height=200,
        placeholder="E.g., I'm sad and feeling blue.",
        label_visibility="collapsed"  # Hides the label visually but keeps it for accessibility
    )

    if user_input:
        with st.spinner('Crafting your mood board...'):
            try:
                topics, emotion = process_text(user_input)  # Corrected function name and variable names
                st.success("Analysis complete!")

                # Display detected topics in a clear format
                st.subheader("Detected Topics")
                st.write(", ".join(topics))

                # Display detected emotion intuitively
                st.subheader("Detected Emotion")
                st.write(emotion)

                # Retrieve and display images with informative feedback
                with st.spinner('Finding inspiring images...'):
                    images = main(user_input, emotion)  # Pass the emotion to the main function
                    display_images(images)

            except Exception as e:
                log_error(e)
                st.error(f"An error occurred: {str(e)}. Please try again- we're working on fixing it!")

if __name__ == "__main__":
    main()