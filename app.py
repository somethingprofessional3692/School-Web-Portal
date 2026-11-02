import streamlit as st
import pandas as pd
import random
import io

# Page Configuration
st.set_page_config(
    page_title="Apex International School & College - SIS",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        padding: 2rem;
        border-radius: 12px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .main-header h1 {
        margin: 0;
        font-weight: 700;
        color: #ffffff;
    }
    .main-header p {
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
        font-size: 1.1rem;
    }
    .metric-card {
        background-color: #f8fafc;
        border-left: 5px solid #2563eb;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .student-card {
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 1.25rem;
        background-color: #ffffff;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin-bottom: 1rem;
    }
    .badge-primary {
        background-color: #e0e7ff;
        color: #3730a3;
        padding: 0.2rem 0.6rem;
        border-radius: 9999px;
        font-size: 0.85rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Generator for 600 unique student records (50 per class across 12 classes)
@st.cache_data
def generate_student_database():
    first_names = [
        "Aarav", "Muhammad", "Aanya", "Zayan", "Ananya", "Rohan", "Fatima", "Vihaan", "Ali", "Saanvi",
        "Aditya", "Ibrahim", "Diya", "Reyansh", "Zainab", "Ishaan", "Ayesha", "Dhruv", "Hamza", "Kabir",
        "Sara", "Arjun", "Khadija", "Sai", "Omar", "Anushka", "Mustafa", "Riya", "Aryan", "Mariam",
        "Kian", "Bilal", "Avani", "Yash", "Ayra", "Atharva", "Usman", "Tara", "Kush", "Hassan",
        "Priya", "Shaurya", "Esha", "Dev", "Alisha", "Samarth", "Hiba", "Pranav", "Zoya", "Ahaan"
    ]
    
    last_names = [
        "Sharma", "Khan", "Patel", "Ahmed", "Verma", "Malik", "Gupta", "Hussain", "Singh", "Qureshi",
        "Joshi", "Siddiqui", "Mehta", "Raza", "Kumar", "Chaudhary", "Shah", "Baig", "Agarwal", "Mirza"
    ]
    
    father_first_names = [
        "Tariq", "Rajesh", "Sanjay", "Kamran", "Vikram", "Imran", "Sunil", "Naveed", "Anand", "Rashid",
        "Ramesh", "Farhan", "Deepak", "Asif", "Suresh", "Bilal", "Alok", "Yasir", "Manoj", "Zubair"
    ]
    
    student_records = {}
    used_roll_numbers = set()
    used_phone_numbers = set()
    
    for grade in range(1, 13):
        class_key = f"Class {grade}"
        student_records[class_key] = []
        
        for idx in range(1, 51):
            # Unique Roll Number generation (e.g., C01-01 to C12-50)
            roll_no = f"C{grade:02d}-{idx:02d}"
            
            # Non-duplicate Names
            fn = first_names[(grade * 3 + idx) % len(first_names)]
            ln = last_names[(grade * 5 + idx) % len(last_names)]
            student_name = f"{fn} {ln}"
            
            ffn = father_first_names[(grade * 2 + idx) % len(father_first_names)]
            father_name = f"{ffn} {ln}"
            
            # Non-duplicate contact details
            phone_num = f"+1 (555) {grade:02d}{idx:02d}-{(grade*7 + idx*13)%9000 + 1000}"
            
            student_records[class_key].append({
                "Roll No": roll_no,
                "Student Name": student_name,
                "Father Name": father_name,
                "Contact No": phone_num,
                "Class": class_key,
                "Gender": "Male" if idx % 2 == 0 else "Female",
                "Attendance Rate": f"{random.randint(88, 99)}%",
                "Grade Performance": random.choice(["A+", "A", "B+", "B"])
            })
            
    return student_records

# Load data
database = generate_student_database()

# Header Section
st.markdown("""
<div class="main-header">
    <h1>🎓 Apex International School & College</h1>
    <p>Official Student Information System & Academic Directory | Grades 1 to 12</p>
</div>
""", unsafe_allow_html=True)

# Sidebar Controls
st.sidebar.title("🏫 Navigation & Controls")
selected_class = st.sidebar.selectbox(
    "Select Class / Grade",
    options=[f"Class {i}" for i in range(1, 13)]
)

st.sidebar.markdown("---")
st.sidebar.subheader("🔍 Quick Search")
search_query = st.sidebar.text_input("Search student by name or roll no:")

# Overview Metrics
total_students = sum(len(students) for students in database.values())
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Enrolled Students", f"{total_students}")
with col2:
    st.metric("Total Classes", "12 Grades")
with col3:
    st.metric("Students per Class", "50 Students")
with col4:
    st.metric("Selected Class", selected_class)

st.markdown("---")

# Main Content Area
class_data = database[selected_class]

# Filter logic for search
if search_query:
    filtered_data = [
        s for s in class_data 
        if search_query.lower() in s["Student Name"].lower() or search_query.lower() in s["Roll No"].lower()
    ]
else:
    filtered_data = class_data

st.subheader(f"📋 Roster for {selected_class} ({len(filtered_data)} Students Shown)")

# Tabs view: Interactive Directory vs Tabular View
tab1, tab2 = st.tabs(["🎴 Interactive Student Cards", "📊 Class Roster Table"])

with tab1:
    st.write("Click on any student card to view full details.")
    
    # Display students in grid format
    grid_cols = st.columns(3)
    for index, student in enumerate(filtered_data):
        col = grid_cols[index % 3]
        with col:
            with st.expander(f"👤 {student['Student Name']} ({student['Roll No']})"):
                st.markdown(f"**Roll Number:** `{student['Roll No']}`")
                st.markdown(f"**Father's Name:** {student['Father Name']}")
                st.markdown(f"**Contact:** {student['Contact No']}")
                st.markdown(f"**Gender:** {student['Gender']}")
                st.markdown(f"**Performance:** `{student['Grade Performance']}`")
                st.markdown(f"**Attendance:** {student['Attendance Rate']}")

with tab2:
    df = pd.DataFrame(filtered_data)
    st.dataframe(
        df[["Roll No", "Student Name", "Father Name", "Contact No", "Gender", "Grade Performance", "Attendance Rate"]],
        use_container_width=True,
        hide_index=True
    )
    
    # CSV Export Functionality
    csv_data = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label=f"📥 Export {selected_class} Roster (CSV)",
        data=csv_data,
        file_name=f"{selected_class.replace(' ', '_')}_Roster.csv",
        mime="text/csv"
    )

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #64748b; font-size: 0.9rem;'>"
    "Apex International School & College Management Portal | Campus Address: 123 Education Boulevard, Academic City"
    "</div>", 
    unsafe_allow_html=True
)