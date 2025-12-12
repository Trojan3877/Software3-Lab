import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from tools.ml_tools import train_model_tool

load_dotenv()

def run_agent():
    llm = ChatOpenAI(
        model="gpt-4",
        temperature=0
    )

    tools = [train_model_tool]

    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.OPENAI_FUNCTIONS,
        verbose=True
    )

    response = agent.run(
        "Train the model and summarize what was done."
    )

    print(response)

if __name__ == "__main__":
    run_agent()