"""
Project Hermes Frontend App

A simple web interface for the travel planning system.
"""

import streamlit as st
import requests
import json
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
st.markdown("""
This app uses a team of specialized AI agents to create comprehensive travel plans.
Each agent contributes their expertise to different aspects of your trip.
""")

# Example queries
example_queries = [
    "Plan a weekend trip to Paris for a couple with a budget of $2000",
    "I want to go hiking in the Swiss Alps for a week in July",
    "Suggest a 5-day family vacation in Tokyo with kids",
    "Plan a backpacking trip through Southeast Asia for 2 weeks",
]

# Query input
with st.form("travel_form"):
    # Query input
    query_option = st.radio(
        "Choose an option:", ["Use an example query", "Enter your own query"]
    )

    if query_option == "Use an example query":
        query = st.selectbox("Select an example query:", example_queries)
    else:
        query = st.text_area(
            "Enter your travel query:",
            height=100,
            placeholder="e.g., Plan a weekend trip to Paris for a couple with a budget of $2000",
        )

    # Submit button
    submit_button = st.form_submit_button("Generate Travel Plan")

# Process the query when submitted
if submit_button and query:
    try:
        # Show a spinner while processing
        with st.spinner("Generating your travel plan... This may take a minute."):
            # Call the API
            response = requests.post(
                TRAVEL_ENDPOINT,
                json={"query": query},
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
                    st.metric(
                        "Confidence Score",
                        f"{result.get('confidence_score', 0) * 100:.1f}%",
                    )

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
                        st.json(travel_plan)

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

# Footer
st.markdown("---")
st.markdown("### About Project Hermes")
st.markdown("""
Project Hermes is a multi-agent AI system built with CrewAI. 
Each agent specializes in different aspects of travel planning:
- **Confidence Agent**: Evaluates if your query is travel-related
- **Orchestrator Agent**: Coordinates the overall planning process
- **Information Agent**: Provides detailed information about destinations
- **Safety Agent**: Provides safety recommendations
- **Experience Agent**: Suggests activities and experiences
- **Logistic Agent**: Plans transportation and accommodation
- **Finance Agent**: Creates budget breakdowns and offers cost-saving tips
""")

# GitHub link
st.markdown("[View on GitHub](https://github.com/your-username/Project-Hermes)")
