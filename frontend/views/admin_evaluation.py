import streamlit as st
from utils.api import get
from components.header import render_header
from components.cards import stat_card
import pandas as pd

def render_admin_evaluation():
    render_header("RAG Evaluation", "View AI system evaluation metrics and test results")
    
    eval_data = get("/admin/evaluation")
    
    if eval_data:
        if eval_data.get("message"):
            st.info(eval_data["message"])
        
        metrics = eval_data.get("metrics", {})
        
        if metrics:
            st.subheader("Evaluation Metrics")
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                val = metrics.get("retrieval_accuracy", 0)
                stat_card("Retrieval Accuracy", f"{val:.0%}" if isinstance(val, float) else str(val))
            with col2:
                val = metrics.get("answer_relevance", 0)
                stat_card("Answer Relevance", f"{val:.0%}" if isinstance(val, float) else str(val))
            with col3:
                val = metrics.get("citation_accuracy", 0)
                stat_card("Citation Accuracy", f"{val:.0%}" if isinstance(val, float) else str(val))
            with col4:
                val = metrics.get("avg_response_time", 0)
                stat_card("Avg Response Time", f"{val:.2f}s" if isinstance(val, (int, float)) else str(val))
            with col5:
                stat_card("Unanswered", metrics.get("unanswered_questions", 0))
        
        test_results = eval_data.get("test_results", [])
        if test_results:
            st.markdown("---")
            st.subheader("Test Results")
            df = pd.DataFrame(test_results)
            st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.warning("Could not load evaluation data. Make sure the backend is running.")
        st.info("Run `python -m tests.test_rag_evaluation` to generate evaluation results.")
