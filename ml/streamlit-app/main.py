import os
import json
import requests
import base64
from typing import Dict, Any

import streamlit as st

API_ENDPOINT = os.getenv("API_ENDPOINT", "http://localhost:8080/generate_course")


def upload_image_and_get_course(image_file) -> Dict[str, Any]:
    """Send image to API and get course JSON response."""
    try:
        # Read file content as bytes
        image_bytes = image_file.getvalue()
        image_base64 = base64.b64encode(image_bytes).decode("utf-8")

        payload = {"image": image_base64}

        response = requests.post(
            API_ENDPOINT, json=payload, headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Error: {e}")
        return None


def display_exercise_card(exercise: Dict[str, str]):
    """Display individual exercise in a card format."""
    with st.container():
        st.markdown(
            f"""
        <div style="
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 10px;
            border-left: 4px solid #007bff;
            margin: 10px 0;
        ">
            <h4 style="margin: 0 0 10px 0; color: #333;">{exercise.get('exercise', '')}</h4>
            <div style="display: flex; gap: 20px; margin-bottom: 10px;">
                <span><strong>Sets:</strong> {exercise.get('sets', '')}</span>
                <span><strong>Reps:</strong> {exercise.get('repeats', '')}</span>
                <span><strong>Duration:</strong> {exercise.get('duration', '')}</span>
                <span><strong>Rest:</strong> {exercise.get('rest', '')}</span>
            </div>
            <p style="margin: 0; color: #666; font-style: italic;">{exercise.get('description', '')}</p>
        </div>
        """,
            unsafe_allow_html=True,
        )


def display_course_card(course_data: Dict[str, Any]):
    """Display the complete course card."""
    st.markdown(
        f"""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        margin: 20px 0;
    ">
        <h1 style="margin: 0 0 10px 0;">{course_data.get('course_title', '')}</h1>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Program description
    st.markdown("### 📝 Program description")
    st.markdown(course_data.get("program_description", ""))

    # Training plan
    st.markdown("### 🏋️ Training plan")

    for day_plan in course_data.get("training_plan", []):
        st.markdown(f"#### {day_plan.get('title', '')}")

        for exercise in day_plan.get("exercises", []):
            display_exercise_card(exercise)

        st.markdown("---")


def main():
    st.set_page_config(page_title="Course generator", page_icon="🏋️", layout="wide")

    st.title("🏋️ Course generator")
    st.markdown("Upload an image and get a personalized training course!")

    # File upload
    uploaded_file = st.file_uploader(
        "Select an image",
        type=["png", "jpg", "jpeg"],
        help="Upload an image to generate a course",
    )

    if uploaded_file is not None:
        # Display uploaded image
        col1, col2 = st.columns([1, 2])

        with col1:
            st.image(uploaded_file, caption="Uploaded image", use_column_width=True)

        with col2:
            if st.button("🚀 Generate course", type="primary"):
                with st.spinner("Generating course..."):
                    course_data = upload_image_and_get_course(uploaded_file)
                    try:
                        course_data = json.loads(course_data["response"])
                    except Exception:
                        st.error("LLM failed to generate correct JSON.")
                        return

                    if course_data:
                        st.success("Course generated successfully!")
                        display_course_card(course_data)
                    else:
                        st.error("Failed to generate course. Please try again.")


if __name__ == "__main__":
    main()
