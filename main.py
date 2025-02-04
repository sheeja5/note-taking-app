import streamlit as st
import os
import json
import base64
from io import BytesIO
from PIL import Image

# Function to load notes from a file
def load_notes():
    if os.path.exists("notes.json"):
        with open("notes.json", "r") as file:
            return json.load(file)
    return {}

# Function to save notes to a file
def save_notes(notes):
    with open("notes.json", "w") as file:
        json.dump(notes, file, indent=4)  # Added indent for better readability

# Load existing notes into session state
if "notes" not in st.session_state:
    st.session_state.notes = load_notes()
notes = st.session_state.notes

# Initialize session state for the text area and image
if "new_note" not in st.session_state:
    st.session_state.new_note = ""
if "new_image" not in st.session_state:
    st.session_state.new_image = None

# Streamlit app
st.title("Note Taking App")

# Sidebar for selecting subject/preference
st.sidebar.header("Subjects/Preferences")
subject = st.sidebar.text_input("Enter a new subject/preference:")
if st.sidebar.button("Add Subject/Preference"):
    if subject:
        if subject not in notes:
            notes[subject] = []
            save_notes(notes)
            st.sidebar.success(f"Added new subject/preference: {subject}")
        else:
            st.sidebar.error("Subject/Preference already exists!")
    else:
        st.sidebar.error("Please enter a subject/preference!")

# Dropdown to select existing subject/preference
subjects = list(notes.keys())
if subjects:
    selected_subject = st.sidebar.selectbox("Select a subject/preference:", subjects)
else:
    st.sidebar.info("No subjects available. Add one first!")
    selected_subject = None

st.write("**Supporting Noty portal as well by (Abel)**")

# Main area for adding and viewing notes
if selected_subject:
    st.header(f"Notes for {selected_subject}")

    # Text area for adding a new note
    new_note = st.text_area("Add a new note:", value=st.session_state.new_note)
    new_image = st.file_uploader("Upload an image:", type=["png", "jpg", "jpeg"])

    if st.button("Save Note"):
        if new_note or new_image:
            note_entry = {"text": new_note, "image": None}
            if new_image is not None:
                note_entry["image"] = base64.b64encode(new_image.getvalue()).decode("utf-8")
            notes[selected_subject].append(note_entry)
            save_notes(notes)
            st.success("Note saved!")

            # Clear the text area and image uploader after saving
            st.session_state.new_note = ""
            st.session_state.new_image = None
            st.experimental_rerun()
        else:
            st.error("Please enter a note or upload an image!")

    # Display existing notes with delete options
    st.subheader("Your Notes:")
    for i, note in enumerate(notes[selected_subject], 1):
        col1, col2 = st.columns([4, 1])
        with col1:
            st.write(f"{i}. {note['text']}")
            if note["image"]:
                image_data = base64.b64decode(note["image"])
                image = Image.open(BytesIO(image_data))
                st.image(image, format="JPEG")
        with col2:
            if st.button(f"Delete {i}", key=f"delete_{i}"):
                # Remove the note at index (i-1)
                notes[selected_subject].pop(i - 1)
                save_notes(notes)
                st.success(f"Note {i} deleted!")
                st.experimental_rerun()
else:
    st.info("Please add or select a subject/preference to start taking notes.")
