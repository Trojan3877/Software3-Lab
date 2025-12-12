from langchain.tools import tool
from src.train import train

@tool
def train_model_tool() -> str:
    """
    Triggers ML model training and logs metrics to MLflow.
    """
    train()
    return "Model training completed and logged to MLflow."