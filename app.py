import streamlit as st

# Password protection
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    password = st.text_input("Enter password to access the app", type="password")
    if password == st.secrets["auth"]["password"]:
        st.session_state.authenticated = True
        st.rerun()
    else:
        st.stop()


import pandas as pd
import math

# Config
st.set_page_config(layout="wide")
st.title("Video Pair Comparison")

# Mapping for easier selection
csv_options = {
    "MotionSmoothness-Wrong": "vbench_motion_smoothness_none_captions_all3_agree_failures_50.csv",
    "VGGSfM-Wrong": "vggsfm_theta_consistency_none_captions_all3_agree_failures_50.csv",
    "Monst3r-Wrong": "monst3r_theta_consistency_none_captions_all3_agree_failures_50.csv",
    "Monst3r-Wrong | MotionSmoothness-Correct": "monst3r_theta_consistency_vbench_motion_smoothness_captions_all3_agree_failures_50.csv",
}

# Load CSV
csv_choice = st.sidebar.selectbox("Select CSV File", list(csv_options.keys()))
selected_file = f"{csv_options[csv_choice]}"
df_data = pd.read_csv(selected_file)

# Pagination
entries_per_page = 8
total_pages = math.ceil(len(df_data) / entries_per_page)
page = st.sidebar.number_input("Page", min_value=1, max_value=total_pages, value=1, step=1)

# Get subset of rows for this page
start_idx = (page - 1) * entries_per_page
end_idx = start_idx + entries_per_page
df_page = df_data.iloc[start_idx:end_idx]

# Function to convert path to URL
def convert_to_url(path):
    # 'model_000/video_001_02.mp4' -> 'https://github.com/genai-ncb/gen-vid-m0/raw/main/video_061_02.mp4'
    model_id = int(path.split('/')[0].split('_')[1])
    prompt_id = int(path.split('/')[1].split('_')[1])
    instance_id = int(path.split('/')[1].split('_')[2].split('.')[0])
    return f"https://github.com/genai-ncb/gen-vid-m{model_id}/raw/main/video_{prompt_id:03d}_{instance_id:02d}.mp4"

# Display videos
for idx, row in df_page.iterrows():
    v1_url = convert_to_url(row['v1'])
    v2_url = convert_to_url(row['v2'])
    caption = row['caption']

    st.subheader(f"Comparison {start_idx + idx + 1}")
    col1, col2 = st.columns(2)

    with col1:
        st.video(v1_url)

    with col2:
        st.video(v2_url)

    for line in caption.split('\n'):
        st.write(f"<p style='text-align: center;'>{line}</p>", unsafe_allow_html=True)

    st.markdown("---")
