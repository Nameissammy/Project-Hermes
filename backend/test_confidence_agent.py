"""
Project Hermes - Confidence Agent Test
-------------------------------------

This script tests just the confidence scoring agent to make sure it can
properly distinguish between travel and non-travel queries.
"""

from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import json

# Load environment variables (for API keys)
load_dotenv()


def test_confidence_agent(query):
    """Test the confidence agent with a given query."""
    print(f"Testing confidence for query: {query}")

    # Initialize the language model
    llm = ChatOpenAI(
        model="gpt-4-turbo",
        temperature=0.2,  # Lower temperature for more consistent classification
    )

    # Create the confidence agent
    confidence_agent = Agent(
        role="Travel Query Evaluator",
        goal="Evaluate whether user queries are related to travel planning and provide a confidence score",
        backstory="""You are an expert at analyzing user requests and determining if they're 
                  related to travel planning. You can distinguish between travel queries and 
                  general knowledge questions. You provide confidence scores ranging from 0 to 1, 
                  where 1 indicates a definite travel planning query and 0 indicates a non-travel query.""",
        verbose=True,
        llm=llm,
    )

    # Create the confidence evaluation task
    confidence_task = Task(
        description=f"""Evaluate whether the following query is related to travel planning:
                      "{query}"
                      
                      Analyze the query carefully and determine if it's asking for help planning a trip,
                      getting travel recommendations, or other travel-related assistance.
                      
                      Provide a confidence score between 0 and 1, where:
                      - 1.0 means definitely travel-related
                      - 0.0 means definitely not travel-related
                      
                      Return your response as a JSON with a 'confidence_score' key and a 'reasoning' key.
                      """,
        agent=confidence_agent,
    )

    # Create a simple crew with just the confidence agent
    crew = Crew(agents=[confidence_agent], tasks=[confidence_task], verbose=True)

    # Run the crew to evaluate the query
    result = crew.kickoff()

    # Parse and print the result
    try:
        parsed_result = json.loads(result)
        print(f"\nConfidence Score: {parsed_result.get('confidence_score', 'N/A')}")
        print(f"Reasoning: {parsed_result.get('reasoning', 'N/A')}")
        return parsed_result
    except Exception as e:
        print(f"\nError parsing result: {e}")
        print(f"Raw result: {result}")
        return {"error": str(e), "raw_result": result}


if __name__ == "__main__":
    # Test with various queries
    test_queries = [
        "Plan a weekend trip to Paris for a couple with a budget of $2000",
        "I want to go hiking in the Swiss Alps for a week in July",
        "What's the capital of France?",
        "How do I fix my broken refrigerator?",
        "Can you suggest some good restaurants in Tokyo?",
    ]

    results = {}
    for query in test_queries:
        print("\n" + "=" * 50)
        result = test_confidence_agent(query)
        results[query] = result
        print("=" * 50)

    # Save results to file
    with open("confidence_test_results.json", "w") as f:
        json.dump(results, f, indent=2)
