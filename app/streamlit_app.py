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
    "Enter any research topic and ResearchPilot will generate "
    "research questions, search the web, analyze sources, and "
    "generate a structured research report."
)


# -----------------------------
# API Key Check
# -----------------------------
if not api_key:

    st.error(
        "ResearchPilot could not find the Gemini API key. "
        "Please configure GEMINI_API_KEY in the environment."
    )

    st.stop()


# -----------------------------
# Research Topic Input
# -----------------------------
topic = st.text_area(
    "Research Topic",
    placeholder=(
        "e.g. Impact of Remote Work on Employee Productivity"
    ),
    height=120
)


# -----------------------------
# Start Research
# -----------------------------
if st.button(
    "🚀 Start Research",
    type="primary",
    use_container_width=True
):

    # -----------------------------
    # Validate Input
    # -----------------------------
    if not topic.strip():

        st.warning(
            "Please enter a research topic first."
        )

        st.stop()

    # -----------------------------
    # Create Agent
    # -----------------------------
    agent = ResearchAgent(api_key)

    # -----------------------------
    # Run Research Pipeline
    # -----------------------------
    try:

        with st.status(
            "ResearchPilot is working...",
            expanded=True
        ) as status:

            # Step 1
            st.write(
                "🧠 Generating research questions..."
            )

            questions = agent.generate_research_questions(
                topic.strip()
            )

            # Step 2
            st.write(
                "🌐 Searching the web and reading sources..."
            )

            research_data = (
                agent.research_questions_to_searches(
                    questions
                )
            )

            # Check whether search returned anything
            total_sources = sum(
                len(item.get("sources", []))
                for item in research_data
            )

            if total_sources == 0:

                status.update(
                    label="Research could not continue",
                    state="error",
                    expanded=True
                )

                st.error(
                    "No web sources were found for this topic. "
                    "Please try a broader or more specific topic."
                )

                st.stop()

            # Step 3
            st.write(
                "📊 Analyzing research sources..."
            )

            analyses = agent.analyze_all_research(
                research_data
            )

            # Step 4
            st.write(
                "📝 Generating final research report..."
            )

            if not analyses:

                status.update(
                    label="Research analysis failed",
                    state="error",
                    expanded=True
                )

                st.error(
                    "The sources were found, but none could be "
                    "successfully analyzed."
                )

                st.stop()

            report = agent.generate_report(
                topic.strip(),
                analyses
            )

            if not report.strip():

                status.update(
                    label="Report generation failed",
                    state="error",
                    expanded=True
                )

                st.error(
                    "Research was completed, but no report "
                    "was generated."
                )

                st.stop()

            # Success
            status.update(
                label="Research completed successfully!",
                state="complete",
                expanded=False
            )

    except Exception:

        st.error(
            "ResearchPilot encountered an unexpected error "
            "while processing your research topic."
        )

        st.info(
            "Please try again. If the problem continues, "
            "check the terminal for technical details."
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
    total_questions = len(
        [
            q for q in question_lines
            if q.strip()
        ]
    )

    total_analyses = len(analyses)

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Questions Generated",
            total_questions
        )

    with col2:

        st.metric(
            "Sources Found",
            total_sources
        )

    with col3:

        st.metric(
            "Sources Analyzed",
            total_analyses
        )


    # -----------------------------
    # Source Details
    # -----------------------------
    st.header("🌐 Research Sources")

    for i, item in enumerate(
        research_data,
        1
    ):

        with st.expander(
            f"Research Question {i}: {item['question']}"
        ):

            sources = item.get(
                "sources",
                []
            )

            if not sources:

                st.warning(
                    "No sources were found for this question."
                )

                continue

            for j, source in enumerate(
                sources,
                1
            ):

                title = source.get(
                    "title",
                    "Unknown source"
                )

                snippet = source.get(
                    "snippet",
                    "No description available."
                )

                url = source.get(
                    "url",
                    ""
                )

                st.markdown(
                    f"**Source {j}: {title}**"
                )

                st.write(snippet)

                if url:

                    st.markdown(
                        f"[🔗 Open Source]({url})"
                    )

                st.divider()


    # -----------------------------
    # Final Research Report
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
        mime="text/markdown",
        use_container_width=True
    )