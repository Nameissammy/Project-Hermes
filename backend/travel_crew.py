"""
Project Hermes - Travel Planning Multi-Agent System
--------------------------------------------------

This module implements a CrewAI-based travel planning system with specialized agents
that work together to create comprehensive travel plans.

It uses the latest CrewAI API to organize agents and their tasks.
"""

from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import json

# Load environment variables (for API keys)
load_dotenv()


class TravelCrew:
    """
    TravelCrew coordinates specialized travel agents to create comprehensive travel plans.
    """

    def __init__(self, model_name="gpt-4-turbo"):
        """Initialize the crew with a specified language model."""
        # Initialize the language model
        self.llm = ChatOpenAI(model=model_name, temperature=0.7)

        # Create the specialized agents
        self.destination_expert = self._create_destination_expert()
        self.itinerary_planner = self._create_itinerary_planner()
        self.safety_advisor = self._create_safety_advisor()
        self.budget_analyst = self._create_budget_analyst()
        self.confidence_agent = self._create_confidence_agent()

    def _create_destination_expert(self):
        """Create the destination expert agent."""
        return Agent(
            role="Travel Destination Expert",
            goal="Provide detailed information about travel destinations and recommend appropriate places based on user preferences",
            backstory="""You are a highly knowledgeable travel destination expert with decades of experience 
                      exploring different countries and cities around the world. You have in-depth knowledge 
                      of popular tourist attractions, local customs, best times to visit, and hidden gems 
                      that most tourists miss.""",
            verbose=True,
            llm=self.llm,
        )

    def _create_itinerary_planner(self):
        """Create the itinerary planner agent."""
        return Agent(
            role="Travel Itinerary Planner",
            goal="Create detailed day-by-day travel itineraries that maximize enjoyment while respecting time constraints",
            backstory="""You are an expert travel itinerary planner who specializes in creating perfectly 
                      balanced schedules. You know how to pace activities to avoid exhaustion, how to 
                      group nearby attractions efficiently, and how to allow for downtime. You understand 
                      travel logistics and how long it takes to move between locations.""",
            verbose=True,
            llm=self.llm,
        )

    def _create_safety_advisor(self):
        """Create the safety advisor agent."""
        return Agent(
            role="Travel Safety Advisor",
            goal="Provide safety information and recommendations specific to the travel destination",
            backstory="""You are a former security consultant who now specializes in travel safety. 
                      You stay updated on global safety conditions, health advisories, common scams, 
                      and best practices for staying safe while traveling. You provide practical 
                      safety advice without causing unnecessary alarm.""",
            verbose=True,
            llm=self.llm,
        )

    def _create_budget_analyst(self):
        """Create the budget analyst agent."""
        return Agent(
            role="Travel Budget Analyst",
            goal="Create realistic travel budgets and find ways to optimize costs without sacrificing experience quality",
            backstory="""You are a financial advisor specializing in travel budgeting. You have 
                      extensive knowledge of costs in various destinations, from accommodation and 
                      food to activities and transportation. You know the best times for deals, 
                      money-saving tips, and how to allocate budgets to maximize experiences.""",
            verbose=True,
            llm=self.llm,
        )

    def _create_confidence_agent(self):
        """Create the confidence scoring agent that determines if a query is travel-related."""
        return Agent(
            role="Travel Query Evaluator",
            goal="Evaluate whether user queries are related to travel planning and provide a confidence score",
            backstory="""You are an expert at analyzing user requests and determining if they're 
                      related to travel planning. You can distinguish between travel queries and 
                      general knowledge questions. You provide confidence scores ranging from 0 to 1, 
                      where 1 indicates a definite travel planning query and 0 indicates a non-travel query.""",
            verbose=True,
            llm=self.llm,
        )

    def create_travel_plan(self, query):
        """
        Generate a comprehensive travel plan based on the user query.

        Args:
            query (str): The user's travel planning query

        Returns:
            dict: A travel plan with itinerary, safety info, and budget
        """
        # First, check if this is a travel-related query
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
            agent=self.confidence_agent,
        )

        # If the query is travel-related (confidence > 0.6), proceed with planning
        # Create the destination research task
        destination_task = Task(
            description=f"""Research the travel destination(s) mentioned in this query: "{query}"
                          
                          If no specific destination is mentioned, recommend suitable destinations based on the 
                          preferences and requirements stated in the query.
                          
                          Provide detailed information about:
                          1. Key attractions and points of interest
                          2. Local culture and customs
                          3. Best time to visit
                          4. Travel requirements (visas, vaccinations, etc.)
                          5. General transportation options
                          
                          Format your response in a clear, organized manner.
                          """,
            agent=self.destination_expert,
        )

        # Create the itinerary planning task
        itinerary_task = Task(
            description=f"""Create a detailed day-by-day itinerary based on this query: "{query}"
                          
                          Use the destination research to plan activities that match the user's interests.
                          Consider:
                          1. The trip duration (if specified)
                          2. A balanced pace with reasonable travel times between activities
                          3. Variety of experiences (culture, food, relaxation, adventure, etc.)
                          4. Logical grouping of nearby attractions
                          5. Meal and rest breaks
                          
                          Format the itinerary by day with timings and brief descriptions.
                          """,
            agent=self.itinerary_planner,
            context=[destination_task],  # This task depends on destination research
        )

        # Create the safety advisory task
        safety_task = Task(
            description=f"""Provide safety information and recommendations for the trip described in: "{query}"
                          
                          Based on the destination research and itinerary, advise on:
                          1. Current safety situations or travel advisories
                          2. Health recommendations and medical facilities
                          3. Common scams or dangers to be aware of
                          4. Emergency contact information
                          5. Safe transportation options
                          
                          Format your response as a concise safety guide with practical tips.
                          """,
            agent=self.safety_advisor,
            context=[
                destination_task,
                itinerary_task,
            ],  # This task depends on previous research
        )

        # Create the budget analysis task
        budget_task = Task(
            description=f"""Create a detailed budget for the trip described in: "{query}"
                          
                          Based on the destination, itinerary and safety information, estimate costs for:
                          1. Accommodation (options at different price points if appropriate)
                          2. Transportation (international and local)
                          3. Food and dining
                          4. Activities and entrance fees
                          5. Miscellaneous expenses (souvenirs, tips, etc.)
                          
                          If a budget is mentioned in the query, optimize your recommendations to fit within it.
                          If no budget is mentioned, provide options for budget, mid-range, and luxury travelers.
                          
                          Format your response as a detailed budget breakdown with approximate costs.
                          """,
            agent=self.budget_analyst,
            context=[
                destination_task,
                itinerary_task,
                safety_task,
            ],  # This task depends on all previous research
        )

        # Create the crew with the defined agents and tasks
        crew = Crew(
            agents=[
                self.confidence_agent,
                self.destination_expert,
                self.itinerary_planner,
                self.safety_advisor,
                self.budget_analyst,
            ],
            tasks=[
                confidence_task,
                destination_task,
                itinerary_task,
                safety_task,
                budget_task,
            ],
            verbose=True,
            process=Process.sequential,  # Tasks will run in the order defined
        )

        # Execute the crew workflow
        result = crew.kickoff(inputs={"query": query})

        # Parse and format results
        try:
            # Try to parse confidence score result
            confidence_result = json.loads(crew.tasks[0].output)
            confidence_score = confidence_result.get("confidence_score", 0)

            # If confidence is too low, return early with just the confidence score
            if confidence_score < 0.6:
                return {
                    "success": False,
                    "confidence_score": confidence_score,
                    "error": "Query does not appear to be related to travel planning",
                    "travel_plan": None,
                }

            # Otherwise, process the full travel plan
            return {
                "success": True,
                "confidence_score": confidence_score,
                "travel_plan": {
                    "overview": crew.tasks[1].output,  # Destination research
                    "itinerary": crew.tasks[2].output,  # Itinerary
                    "safety": crew.tasks[3].output,  # Safety info
                    "finance": crew.tasks[4].output,  # Budget
                },
            }
        except Exception as e:
            # Handle any parsing errors
            return {
                "success": False,
                "error": f"Error processing travel plan: {str(e)}",
                "raw_output": result,
            }


# Example usage
if __name__ == "__main__":
    # Create the travel planning crew
    travel_crew = TravelCrew()

    # Example query
    query = "Plan a weekend trip to Paris for a couple with a budget of $2000"

    # Generate the travel plan
    plan = travel_crew.create_travel_plan(query)

    # Print the results
    import json

    print(json.dumps(plan, indent=2))
