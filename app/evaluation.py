def evaluate_research_result(result):
    """
    Evaluate the quality and completeness of a ResearchPilot run.
    """

    evaluation = {}

    # -----------------------------
    # Basic Pipeline Checks
    # -----------------------------

    evaluation["topic_provided"] = bool(
        result.get("topic", "").strip()
    )

    evaluation["questions_generated"] = len(
        [
            q for q in result.get("questions", "").splitlines()
            if q.strip()
        ]
    )

    evaluation["research_questions_searched"] = len(
        result.get("research_data", [])
    )

    evaluation["analyses_completed"] = len(
        result.get("analyses", [])
    )

    evaluation["report_generated"] = bool(
        result.get("report", "").strip()
    )

    # -----------------------------
    # Source Statistics
    # -----------------------------

    total_sources = 0

    for item in result.get("research_data", []):

        total_sources += len(
            item.get("sources", [])
        )

    evaluation["total_sources"] = total_sources

    # -----------------------------
    # Success Checks
    # -----------------------------

    evaluation["question_generation_success"] = (
        evaluation["questions_generated"] >= 5
    )

    evaluation["search_success"] = (
        evaluation["research_questions_searched"] > 0
    )

    evaluation["analysis_success"] = (
        evaluation["analyses_completed"] > 0
    )

    evaluation["report_success"] = (
        evaluation["report_generated"]
    )

    # -----------------------------
    # Overall Pipeline Status
    # -----------------------------

    evaluation["pipeline_success"] = all([
        evaluation["topic_provided"],
        evaluation["question_generation_success"],
        evaluation["search_success"],
        evaluation["analysis_success"],
        evaluation["report_success"]
    ])

    return evaluation


def print_evaluation(evaluation):
    """
    Display evaluation results in a readable format.
    """

    print("\n")
    print("=" * 60)
    print("RESEARCHPILOT EVALUATION")
    print("=" * 60)

    print(
        f"Topic provided: "
        f"{'✓' if evaluation['topic_provided'] else '✗'}"
    )

    print(
        f"Questions generated: "
        f"{evaluation['questions_generated']}"
    )

    print(
        f"Research questions searched: "
        f"{evaluation['research_questions_searched']}"
    )

    print(
        f"Total sources found: "
        f"{evaluation['total_sources']}"
    )

    print(
        f"Analyses completed: "
        f"{evaluation['analyses_completed']}"
    )

    print(
        f"Report generated: "
        f"{'✓' if evaluation['report_generated'] else '✗'}"
    )

    print("-" * 60)

    print(
        f"Overall pipeline: "
        f"{'SUCCESS ✓' if evaluation['pipeline_success'] else 'FAILED ✗'}"
    )

    print("=" * 60)