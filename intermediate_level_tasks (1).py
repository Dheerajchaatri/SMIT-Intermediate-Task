# streamlit_app.py
import streamlit as st
import os

# ------------------- Hospital System -------------------
class Patient:
    def __init__(self, name, age, disease, patient_id):
        self.name = name
        self.age = age
        self.disease = disease
        self.patient_id = patient_id

    def display(self):
        return f"ID: {self.patient_id}\nName: {self.name}\nAge: {self.age}\nDisease: {self.disease}"


class Hospital:
    def __init__(self):
        self.patients = {}   # key = patient_id, value = Patient object

    def register_patient(self, name, age, disease, patient_id):
        if patient_id in self.patients:
            return "❌ Patient ID already exists!"
        else:
            self.patients[patient_id] = Patient(name, age, disease, patient_id)
            return "✅ Patient registered successfully"

    def search_patient(self, patient_id):
        if patient_id in self.patients:
            return f"🔍 Patient Found:\n{self.patients[patient_id].display()}"
        else:
            return "❌ Patient Not Found"

# ------------------- Diary System -------------------
class Diary:
    def __init__(self, username, password_file="users.txt", diary_file="diary.txt"):
        self.username = username
        self.password_file = password_file
        self.diary_file = diary_file

    def login(self, password):
        if not os.path.exists(self.password_file):
            return False
        with open(self.password_file, "r") as f:
            for line in f:
                user, pw = line.strip().split(":")
                if user == self.username and pw == password:
                    return True
        return False

    def _scramble(self, text):
        return "".join([chr((ord(c)+3) % 256) for c in text])

    def _unscramble(self, text):
        return "".join([chr((ord(c)-3) % 256) for c in text])

    def write_entry(self, text):
        scrambled = self._scramble(text)
        with open(self.diary_file, "a") as f:
            f.write(scrambled + "\n")
        return "✅ Entry saved securely!"

    def read_entries(self):
        if not os.path.exists(self.diary_file):
            return "No diary entries yet."
        entries = []
        with open(self.diary_file, "r") as f:
            for line in f:
                entries.append(self._unscramble(line.strip()))
        return "\n\n".join(entries)

# ------------------- Streamlit Interface -------------------
st.title("Intermediate Level Tasks - Streamlit Version")

task = st.sidebar.selectbox("Choose Task", ["Hospital Management", "Secure Digital Diary"])

# ------------------- Hospital Management -------------------
if task == "Hospital Management":
    st.header("🏥 Hospital Patient Management System")
    
    hospital = st.session_state.get("hospital", Hospital())
    st.session_state["hospital"] = hospital
    
    option = st.radio("Choose Action", ["Register Patient", "Search Patient"])

    if option == "Register Patient":
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=0)
        disease = st.text_input("Disease")
        pid = st.text_input("Patient ID")
        if st.button("Register"):
            result = hospital.register_patient(name, age, disease, pid)
            st.write(result)

    elif option == "Search Patient":
        pid = st.text_input("Enter Patient ID to search")
        if st.button("Search"):
            result = hospital.search_patient(pid)
            st.text(result.replace("\n", "  \n"))

# ------------------- Secure Digital Diary -------------------
elif task == "Secure Digital Diary":
    st.header("📓 Secure Digital Diary")
    
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        diary = Diary(username)
        if diary.login(password):
            st.success("Login successful!")
            diary_action = st.radio("Choose Action", ["Write Entry", "Read Entries"])
            
            if diary_action == "Write Entry":
                entry = st.text_area("Write your diary entry:")
                if st.button("Save Entry"):
                    st.success(diary.write_entry(entry))
            elif diary_action == "Read Entries":
                entries = diary.read_entries()
                st.text(entries)
        else:
            st.error("❌ Login failed!")
