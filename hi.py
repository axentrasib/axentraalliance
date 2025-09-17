import streamlit as st

# --- App Config ---
st.set_page_config(page_title="Career & Education Advisor", layout="centered")

# --- Branding ---
st.markdown(
    """
    <div style="text-align:center; margin-bottom: 20px;">
        <h1 style="color:#2E86C1;">🚀 Axentra Alliance</h1>
        <h3 style="color:#566573;">Career & Education Advisor (Prototype)</h3>
    </div>
    """,
    unsafe_allow_html=True
)

# Track step
if "step" not in st.session_state:
    st.session_state.step = 1

# --- Step 1: Profile ---
if st.session_state.step == 1:
    st.header("Step 1: Student Profile")
    st.session_state.name = st.text_input("Enter your name")
    st.session_state.class_level = st.selectbox("Select your class", ["10th", "12th"])
    if st.button("Next ➡️"):
        st.session_state.step = 2
        st.rerun()

# --- Step 2: Aptitude Quiz ---
elif st.session_state.step == 2:
    st.header("Step 2: Aptitude Quiz")
    q1 = st.radio("Do you enjoy experiments?", ["Yes", "No"])
    q2 = st.radio("Do you prefer working with numbers?", ["Yes", "No"])
    q3 = st.radio("Do you like literature or history?", ["Yes", "No"])

    if st.button("🎯 Get Suggestion"):
        if q1 == "Yes":
            st.session_state.stream = "Science"
        elif q2 == "Yes":
            st.session_state.stream = "Commerce"
        elif q3 == "Yes":
            st.session_state.stream = "Arts"
        else:
            st.session_state.stream = "Vocational"
        st.session_state.got_suggestion = True

    if st.session_state.get("got_suggestion", False):
        st.success(f"👉 Suggested Stream: {st.session_state.stream}")
        if st.button("Next ➡️"):
            st.session_state.step = 3
            st.rerun()

# --- Step 3: Career Mapping ---
elif st.session_state.step == 3:
    st.header("Step 3: Career Options")
    career_map = {
        "Science": ["Research", "Engineering", "Medical"],
        "Commerce": ["Banking", "CA", "MBA"],
        "Arts": ["Teaching", "Civil Services", "Law"],
        "Vocational": ["Skill Jobs", "Entrepreneurship"]
    }
    st.write("Based on your stream, career options are:")
    st.success(", ".join(career_map.get(st.session_state.stream, [])))
    if st.button("Next ➡️"):
        st.session_state.step = 4
        st.rerun()

# --- Step 4: Colleges ---
elif st.session_state.step == 4:
    st.header("Step 4: Nearby Colleges (Demo)")
    st.table({
        "College": ["Govt College A", "Govt College B"],
        "Courses": ["B.Sc, B.A", "B.Com, B.Sc"],
        "Location": ["Town X", "Town Y"]
    })
    if st.button("Next ➡️"):
        st.session_state.step = 5
        st.rerun()

# --- Step 5: Notifications ---
elif st.session_state.step == 5:
    st.header("Step 5: Important Dates")
    st.info("📌 Scholarship deadline: 30 Sept")
    st.info("📌 Admission counseling: 10 Oct")
    st.info("📌 Entrance test: 15 Oct")
    st.success("🎉 You're all set!")
