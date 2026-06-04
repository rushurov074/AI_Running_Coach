import streamlit as st
from google import genai
import os
import csv

# set page configuration
st.set_page_config(
    page_title="AI Running Coach",
    layout="centered"
)

api_key = os.environ.get("GEMINI_API_KEY")

# title 
st.markdown("<h1 style='text-align: center; color: #FF4B4B;'>Ruslan's AI Running Coach</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 18px;'>Powered by Google Gemini Flash 3.5</p>", unsafe_allow_html=True)
st.write("---")

system_instructions = (
    "You are a super friendly, encouraging, elite, and nice running coach. "
    "You always celebrate the runner's effort first before giving advice. "
    "However, PLEASE be real, and don't sugarcoat ANYTHING. "
    "Eliminate the use of em dashes"
    "Refrain from using vulgar language, keep it clean. This means absolutely no swearing at all. "
    "Keep your tone lively, warm, and conversational, like a supportive friend. "
    "Analyze the runner's data, highlight a few things they did really well, "
    "and give them some insightful tips for their next run to keep improving."
)

workout_summary = ""

# input
st.subheader("Choose Your Data Entry Method (Upload or Manually enter):")
tab1, tab2 = st.tabs(["Upload Spreadsheet (CSV)", "Manual Entry Dashboard"])

# .csv upload
with tab1:
    uploaded_file = st.file_uploader("Drop your run .csv file here", type="csv", help="Supports standard automated watch exports containing Mile, Pace, and Heart_Rate columns.")
    
    if uploaded_file is not None:
        file_contents = uploaded_file.read().decode("utf-8").splitlines()
        csv_reader = csv.DictReader(file_contents)
        
        calculated_distance = 0
        splits_text = ""
        
        # expander to look inside the data
        with st.expander("View Raw Spreadsheet Rows", expanded=False):
            for row in csv_reader:
                calculated_distance += 1
                st.text(f"Mile {row['Mile']} | Pace: {row['Pace']} | HR: {row['Heart_Rate']} BPM")
                splits_text += f"- Mile {row['Mile']}: {row['Pace']} pace, {row['Heart_Rate']} BPM\n"
        
        st.metric(label="Total Distance Parsed", value=f"{calculated_distance} Miles")
        
        workout_summary = f"""
        Spreadsheet Run Data:
        - Total Distance: {calculated_distance} miles
        
        Split Breakdown:
        {splits_text}
        """

# entering manually
with tab2:
    st.write("Log your workout metrics manually to sync with the AI coach.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        distance = st.number_input("Total Distance (miles):", min_value=0.0, value=3.0, step=0.1)
    with col2:
        time = st.number_input("Total Time (minutes):", min_value=0.0, value=25.0, step=0.5)
    with col3:
        cadence = st.number_input("Average Cadence (SPM):", min_value=0, value=170, step=1)

    st.write("---")
    st.markdown("#### Split Breakdown Builder")
    total_miles_count = max(1, round(distance))
    workout_splits = []

    for i in range(total_miles_count):
        m_col1, m_col2, m_col3 = st.columns([1, 2, 2])
        with m_col1:
            st.markdown(f"<p style='margin-top: 30px;'><b>Mile {i+1}</b></p>", unsafe_allow_html=True)
        with m_col2:
            pace = st.text_input(f"Pace (H:SS):", value="8:00", key=f"pace_{i}")
        with m_col3:
            hr = st.number_input(f"Heart Rate (BPM):", min_value=40, max_value=220, value=150, key=f"hr_{i}")
        
        workout_splits.append({
            "mile": i + 1,
            "pace": pace,
            "heart_rate": hr
        })

    if uploaded_file is  None:
        splits_text = ""
        for split in workout_splits:
            splits_text += f"- Mile {split['mile']}: {split['pace']} pace, {split['heart_rate']} BPM\n"
        
        workout_summary = f"""
        Runner Manual Workout Data:
        - Total Distance: {distance} miles
        - Total Time: {time} mins
        - Avg Cadence: {cadence} steps/min
        
        Split Breakdown:
        {splits_text}
        """

# giving data to Gemini
st.write("")
if st.button("Get the AI Coach's feedback!", use_container_width=True):
    if not workout_summary:
        st.warning("Please either upload the spreadsheet or fill out the manual entry options before analyzing.")
    elif not api_key:
        st.error("Missing System Authentication.")
    else:
        with st.status("Taking Left Turns Only...", expanded=True) as status:
            try:
                client = genai.Client(api_key=api_key)
                
                response = client.models.generate_content(
                    model='gemini-3.5-flash',
                    contents=f"{system_instructions}\n\n{workout_summary}"
                )
                
                status.update(label="Analysis Complete!", state="complete", expanded=False)
                
                # answer
                st.markdown("### Coach's Assessment")
                st.info(response.text)
                
            except Exception as error:
                status.update(label="Analysis Failed", state="error")
                st.error(f"Execution Error: {error}")
