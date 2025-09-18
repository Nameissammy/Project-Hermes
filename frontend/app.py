"""
Project Hermes Frontend App

A simple web interface for the travel planning system.
"""

import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API endpoint configuration
API_HOST = os.getenv("API_HOST", "http://localhost:8001")
TRAVEL_ENDPOINT = f"{API_HOST}/travel/plan"

# Page configuration
st.set_page_config(
    page_title="Project Hermes - Travel Planning", page_icon="✈️", layout="wide"
)

# Header
st.title("✈️ Project Hermes - AI Travel Planning")
st.markdown(
    "This app uses a team of specialized AI agents to create comprehensive travel plans."
)

st.subheader("Your query")
st.text_area(
    "",
    key="query_input",
    height=120,
    placeholder="Describe the trip you want planned (destination, duration, preferences, budget, constraints)",
)

# Sidebar: provider selection and settings
st.sidebar.header("Settings")
provider_label = "LLM Provider"
provider_choice = st.sidebar.selectbox(
    provider_label,
    ["Auto-detect", "gemini", "claude", "openai"],
    index=0,
    help="Leave as Auto-detect to use the first available provider (Gemini → Claude → OpenAI)",
)

# Custom CSS for a more compact, wide button
st.markdown(
    """
    <style>
    /* More specific selector targeting the exact button label */
    div.stButton > button[purpose="secondary"] { }
    .stButton button:contains('Generate Plan') { }
    /* Fallback: target all buttons, then narrow using size adjustments */
    .stButton button {
        padding: 0.25rem 0.6rem !important;
        font-size: 0.8rem !important;
        line-height: 1.1 !important;
        width: 100% !important;
        min-height: 30px !important;
        border-radius: 4px !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

submit_button = st.button("Generate Plan", use_container_width=True)

# Process the query when submitted
query = st.session_state.get("query_input", "").strip()
if submit_button:
    if not query:
        st.warning("Please enter a travel query.")
    else:
        try:
            # Show a spinner while processing
            with st.spinner("Generating your travel plan... This may take a minute."):
                # Call the API
                payload = {"query": query}
                if provider_choice != "Auto-detect":
                    payload["llm_provider"] = provider_choice
                response = requests.post(
                    TRAVEL_ENDPOINT,
                    json=payload,
                    headers={"Content-Type": "application/json"},
                    timeout=120,  # Longer timeout for complex queries
                )

            # Check if the request was successful
            if response.status_code == 200:
                result = response.json()

                # Display results
                if result.get("success", False):
                    st.success("Travel plan generated successfully!")

                    # Show confidence score
                    conf = result.get("confidence_score")
                    if isinstance(conf, (int, float)):
                        st.metric("Confidence Score", f"{conf * 100:.1f}%")

                    # Show provider used
                    provider_used = result.get("llm_provider")
                    if provider_used:
                        st.caption(f"Provider used: {provider_used}")

                    # Display travel plan
                    travel_plan = result.get("travel_plan", {})

                    # Create tabs for different sections
                    tabs = st.tabs(
                        ["Overview", "Itinerary", "Safety", "Budget", "Raw JSON"]
                    )

                    # Overview tab
                    with tabs[0]:
                        st.markdown("## 📋 Overview")
                        st.write(travel_plan.get("overview", "No overview available"))

                    # Itinerary tab
                    with tabs[1]:
                        st.markdown("## 🗓️ Itinerary")
                        itinerary = travel_plan.get(
                            "itinerary", "No itinerary available"
                        )
                        if isinstance(itinerary, list):
                            for day in itinerary:
                                st.subheader(f"📅 {day.get('day', 'Day')}")
                                for activity in day.get("activities", []):
                                    st.write(
                                        f"• {activity.get('time', '')} - {activity.get('description', '')}"
                                    )
                        else:
                            st.write(itinerary)

                    # Safety tab
                    with tabs[2]:
                        st.markdown("## 🛡️ Safety Information")
                        safety = travel_plan.get(
                            "safety", "No safety information available"
                        )
                        if isinstance(safety, dict):
                            for key, value in safety.items():
                                st.subheader(key.replace("_", " ").title())
                                st.write(value)
                        else:
                            st.write(safety)

                    # Budget tab
                    with tabs[3]:
                        st.markdown("## 💰 Budget")
                        finance = travel_plan.get(
                            "finance", "No budget information available"
                        )
                        if isinstance(finance, dict):
                            # Create a table for budget items
                            budget_data = []
                            for category, amount in finance.items():
                                if category != "total" and category != "summary":
                                    if isinstance(amount, (int, float)):
                                        budget_data.append(
                                            {
                                                "Category": category.replace(
                                                    "_", " "
                                                ).title(),
                                                "Amount": f"${amount:,.2f}",
                                            }
                                        )
                                    else:
                                        budget_data.append(
                                            {
                                                "Category": category.replace(
                                                    "_", " "
                                                ).title(),
                                                "Amount": str(amount),
                                            }
                                        )

                            # Show the table if we have data
                            if budget_data:
                                st.table(budget_data)

                            # Show total if available
                            if "total" in finance:
                                st.subheader("Total")
                                total = finance["total"]
                                if isinstance(total, (int, float)):
                                    st.metric("Total Budget", f"${total:,.2f}")
                                else:
                                    st.write(total)

                            # Show budget summary if available
                            if "summary" in finance:
                                st.subheader("Budget Summary")
                                st.write(finance["summary"])
                        else:
                            st.write(finance)

                    # Raw JSON tab
                    with tabs[4]:
                        st.markdown("## Raw JSON Response")
                        st.json(result)

                else:
                    st.error(f"Error: {result.get('error', 'Unknown error')}")
                    if "confidence_score" in result:
                        st.warning(
                            f"Confidence Score: {result.get('confidence_score', 0) * 100:.1f}%"
                        )
                        st.info(
                            "The query may not be specific enough or might not be travel-related."
                        )
            else:
                st.error(f"Error: HTTP {response.status_code} - {response.text}")

        except Exception as e:
            st.error(f"Error calling the travel planning API: {str(e)}")
            st.info("Make sure the API server is running at " + API_HOST)

# Minimal footer divider (retain if you want a visual end-of-page cue)
st.markdown("---")
