import streamlit as st
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io

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

# --- Initialize Session State ---
if "step" not in st.session_state:
    st.session_state.step = 1
if "profile" not in st.session_state:
    st.session_state.profile = {}

# --- Step 1: Profile ---
if st.session_state.step == 1:
    st.header("Step 1: Student Profile")
    name = st.text_input("Enter your name", st.session_state.profile.get("name", ""))
    class_level = st.selectbox("Select your class", ["10th", "12th"],
                               index=["10th", "12th"].index(st.session_state.profile.get("class_level", "10th")))
    interests = st.multiselect("Select your interests",
                               ["Science", "Math", "Arts", "Commerce", "Technology", "Languages"],
                               default=st.session_state.profile.get("interests", []))

    if st.button("💾 Save Profile"):
        st.session_state.profile["name"] = name
        st.session_state.profile["class_level"] = class_level
        st.session_state.profile["interests"] = interests
        st.success(f"Profile saved ✅ ({name}, Class {class_level}, Interests: {', '.join(interests)})")

    if st.button("Next ➡️"):
        if name:
            st.session_state.step = 2
            st.rerun()
        else:
            st.warning("Please enter your name before continuing.")

# --- Step 2: Aptitude Quiz ---
elif st.session_state.step == 2:
    st.header("Step 2: Aptitude Quiz (7 Questions)")
    q1 = st.radio("Do you enjoy experiments and labs?", ["Yes", "No"])
    q2 = st.radio("Do you prefer working with numbers & accounts?", ["Yes", "No"])
    q3 = st.radio("Do you like literature, history, or politics?", ["Yes", "No"])
    q4 = st.radio("Do you enjoy solving puzzles or coding?", ["Yes", "No"])
    q5 = st.radio("Would you like to start your own business someday?", ["Yes", "No"])
    q6 = st.radio("Do you enjoy helping others learn or teaching?", ["Yes", "No"])
    q7 = st.radio("Are you interested in arts, design, or creativity?", ["Yes", "No"])

    if st.button("🎯 Get Suggestion"):
        # Simple scoring system
        scores = {"Science": 0, "Commerce": 0, "Arts": 0, "Vocational": 0}
        if q1 == "Yes": scores["Science"] += 1
        if q2 == "Yes": scores["Commerce"] += 1
        if q3 == "Yes": scores["Arts"] += 1
        if q4 == "Yes": scores["Science"] += 1
        if q5 == "Yes": scores["Commerce"] += 1
        if q6 == "Yes": scores["Arts"] += 1
        if q7 == "Yes": scores["Arts"] += 1

        # Boost score if interests match
        if "Science" in st.session_state.profile.get("interests", []): scores["Science"] += 1
        if "Commerce" in st.session_state.profile.get("interests", []): scores["Commerce"] += 1
        if "Arts" in st.session_state.profile.get("interests", []): scores["Arts"] += 1
        if "Technology" in st.session_state.profile.get("interests", []): scores["Science"] += 1

        # Pick best stream
        st.session_state.stream = max(scores, key=scores.get)
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
    st.session_state.career_options = career_map.get(st.session_state.stream, [])
    st.success(", ".join(st.session_state.career_options))
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

# --- Step 5: Notifications & Report ---
# --- Step 5: Notifications & Report ---
elif st.session_state.step == 5:
    st.header("Step 5: Important Dates")
    st.info("📌 Scholarship deadline: 30 Sept")
    st.info("📌 Admission counseling: 10 Oct")
    st.info("📌 Entrance test: 15 Oct")

    st.subheader("👤 Profile Summary")
    st.write(f"**Name:** {st.session_state.profile.get('name','N/A')}")
    st.write(f"**Class:** {st.session_state.profile.get('class_level','N/A')}")
    st.write(f"**Interests:** {', '.join(st.session_state.profile.get('interests', []))}")
    st.write(f"**Suggested Stream:** {st.session_state.get('stream','Not Chosen')}")
    st.write(f"**Career Options:** {', '.join(st.session_state.get('career_options', []))}")

    # --- Generate PDF function ---
    def generate_pdf(profile, stream, careers):
        buf = io.BytesIO()
        c = canvas.Canvas(buf, pagesize=letter)
        c.setFont("Helvetica-Bold", 16)
        c.drawString(180, 750, "Career & Education Report")
        c.setFont("Helvetica", 12)
        c.drawString(50, 700, f"Name: {profile.get('name', 'N/A')}")
        c.drawString(50, 680, f"Class: {profile.get('class_level', 'N/A')}")
        c.drawString(50, 660, f"Interests: {', '.join(profile.get('interests', []))}")
        c.drawString(50, 640, f"Suggested Stream: {stream}")
        c.drawString(50, 620, "Career Options:")
        y = 600
        for career in careers:
            c.drawString(70, y, f"- {career}")
            y -= 20
        c.drawString(50, y-10, "Important Dates:")
        c.drawString(70, y-30, "📌 Scholarship: 30 Sept")
        c.drawString(70, y-50, "📌 Counseling: 10 Oct")
        c.drawString(70, y-70, "📌 Entrance: 15 Oct")
        c.save(); buf.seek(0)
        return buf

    if st.button("📥 Download PDF Report"):
        pdf = generate_pdf(st.session_state.profile,
                           st.session_state.get("stream", "Not Chosen"),
                           st.session_state.get("career_options", []))
        st.download_button("⬇️ Save Report", pdf, "career_report.pdf", "application/pdf")

    st.success("🎉 You're all set!")

