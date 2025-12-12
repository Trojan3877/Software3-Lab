from src.llm_agent import run_agent

def test_agent_runs():
    # Ensures orchestration layer executes
    run_agent()
    assert True