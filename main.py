import streamlit as st
import os
import json

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

# Load existing notes
notes = load_notes()

# Initialize session state for the text area
if "new_note" not in st.session_state:
    st.session_state.new_note = ""

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
selected_subject = st.sidebar.selectbox("Select a subject/preference:", list(notes.keys()))
st.write("**Supporting Noty portal as well  by (abel and devansh)**")
# Main area for adding and viewing notes
if selected_subject:
    st.header(f"Notes for {selected_subject}")
    
    # Text area for adding a new note
    new_note = st.text_area("Add a new note:")
    if st.button("Save Note"):
        if new_note:
            notes[selected_subject].append(new_note)
            save_notes(notes)
            st.success("Note saved!")
            # Clear the text area after saving
            st.session_state.new_note = ""
            # Refresh the app to reflect changes
        else:
            st.error("Please enter a note!")

    # Display existing notes with delete options
    st.subheader("Your Notes:")
    for i, note in enumerate(notes[selected_subject], 1):
        col1, col2 = st.columns([4, 1])
        with col1:
            st.write(f"{i}. {note}")
        with col2:
            if st.button(f"Delete {i}", key=f"delete_{i}"):
                # Remove the note at index (i-1)
                notes[selected_subject].pop(i - 1)
                save_notes(notes)
                st.success(f"Note {i} deleted!")
                st.experimental_rerun()  # Refresh the app to reflect changes
else:
    st.info("Please add or select a subject/preference to start taking notes.")
