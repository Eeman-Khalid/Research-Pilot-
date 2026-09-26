import os

import streamlit as st
from dotenv import load_dotenv

from research_agent import ResearchAgent


# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="ResearchPilot",
    page_icon="🔎",
    layout="wide"
)


# -----------------------------
# Load Environment Variables
# -----------------------------
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")


# -----------------------------
# Page Header
# -----------------------------
st.title("🔎 ResearchPilot")
st.subheader("AI-Powered Autonomous Research Agent")

st.write(
    "Enter a research topic and ResearchPilot will generate research "
    "questions, search the web, analyze sources, and generate a structured report."
)


# -----------------------------
# API Key Check
# -----------------------------
if not api_key:
    st.error(
        "GEMINI_API_KEY not found. "
        "Please add it to your .env file."
    )
    st.stop()


# -----------------------------
# Research Topic Input
# -----------------------------
topic = st.text_area(
    "Research Topic",
    placeholder="e.g. Impact of Artificial Intelligence on Healthcare",
    height=100
)


# -----------------------------
# Start Research
# -----------------------------
if st.button(
    "🚀 Start Research",
    type="primary"
):

    if not topic.strip():

        st.warning(
            "Please enter a research topic first."
        )

        st.stop()

    agent = ResearchAgent(api_key)

    # -----------------------------
    # Run Research Agent
    # -----------------------------
    with st.status(
        "ResearchPilot is working...",
        expanded=True
    ) as status:

        st.write("🧠 Generating research questions...")

        try:

            questions = agent.generate_research_questions(
                topic
            )

            st.write("🌐 Searching the web and reading sources...")

            research_data = agent.research_questions_to_searches(
                questions
            )

            st.write("📊 Analyzing research sources...")

            analyses = agent.analyze_all_research(
                research_data
            )

            st.write("📝 Generating final research report...")

            report = agent.generate_report(
                topic,
                analyses
            )

            status.update(
                label="Research completed successfully!",
                state="complete",
                expanded=False
            )

        except Exception as e:

            status.update(
                label="Research failed",
                state="error",
                expanded=True
            )

            st.error(
                f"An error occurred: {e}"
            )

            st.stop()


    # -----------------------------
    # Research Questions
    # -----------------------------
    st.header("📋 Research Questions")

    question_lines = questions.split("\n")

    for question in question_lines:

        question = question.strip()

        if question:

            st.markdown(
                f"✓ {question}"
            )


    # -----------------------------
    # Research Statistics
    # -----------------------------
    total_sources = sum(
        len(item["sources"])
        for item in research_data
    )

    total_analyses = len(analyses)


    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Sources Found",
            total_sources
        )

    with col2:

        st.metric(
            "Sources Analyzed",
            total_analyses
        )


    # -----------------------------
    # Source Details
    # -----------------------------
    st.header("🌐 Sources")

    for i, item in enumerate(
        research_data,
        1
    ):

        with st.expander(
            f"Research Question {i}: {item['question']}"
        ):

            for j, source in enumerate(
                item["sources"],
                1
            ):

                st.markdown(
                    f"**Source {j}: {source['title']}**"
                )

                st.write(
                    source["snippet"]
                )

                st.markdown(
                    f"[Open Source]({source['url']})"
                )


    # -----------------------------
    # Final Report
    # -----------------------------
    st.header("📄 Final Research Report")

    st.markdown(report)


    # -----------------------------
    # Download Report
    # -----------------------------
    st.download_button(
        label="⬇️ Download Research Report",
        data=report,
        file_name="research_report.md",
        mime="text/markdown"
    )