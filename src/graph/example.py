import logging
from pprint import pprint
from src.graph.workflow import create_career_graph

# Setup basic logging to see node transitions
logging.basicConfig(level=logging.INFO)

def run_example():
    """
    Runnable example showcasing the CareerPilot overall workflow 
    powered by LangGraph.
    """
    
    # 1. Provide an LLM client
    # For this example, we'll pass None and watch the agents return their standard fallbacks.
    # In a real environment, you'd configure a DeepSeek LangChain chat model here.
    llm_client = None
    
    # 2. Compile the Graph
    # We use an in-memory SQLite database for demonstration purposes.
    app = create_career_graph(llm_client=llm_client, db_path=":memory:")

    # 3. Define User Inputs (CareerState)
    initial_state = {
        "resume_text": "Experienced Python software engineer with FastAPI knowledge and SQL experience.",
        "job_description": "Looking for a Senior Backend Developer. Requirements: Python, Docker, Kubernetes.",
        "user_id": 1  # Will attach memory processes to user #1
    }

    print("--- Starting CareerPilot Workflow ---")
    
    # 4. Invoke the workflow
    final_state = app.invoke(initial_state)

    # 5. Display the final output
    print("\n--- Workflow Execution Completed ---\n")
    print("Final State Results:")
    
    print("\n1. Resume Info Extracted:")
    pprint(final_state.get("resume_info"))
    
    print("\n2. Job Info Extracted:")
    pprint(final_state.get("job_info"))
    
    print("\n3. Gap Report:")
    pprint(final_state.get("gap_report"))
    
    print("\n4. Learning Plan:")
    pprint(final_state.get("learning_plan"))
    
    print("\n5. Interview Questions Prepared:")
    pprint(final_state.get("interview_questions"))
    
    print("\n6. Memory Operation Details:")
    pprint(final_state.get("memory"))

if __name__ == "__main__":
    run_example()
