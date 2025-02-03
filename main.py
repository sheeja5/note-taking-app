import streamlit as st
import os
import json

# Function to load notes from a file
def load_notes():
    if os.path.exists("notes.json"):
        with open("notes.json", "r") as file:
            return json.load(file)
    return {}
notes = load_notes()
#Function to save notes to a file
def save_notes(notes):
    with open("notes.json", "w") as file:
        json.dump(notes, file, indent=4)  # Added indent for better readability

# Load existing notes
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
        else:
            st.error("Please enter a note!")

    # Display existing notes
    st.subheader("Your Notes:")
    for i, note in enumerate(notes[selected_subject], 1):
        st.write(f"{i}. {note}")
else:
    st.info("Please add or select a subject/preference to start taking notes.")