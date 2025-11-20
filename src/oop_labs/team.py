from __future__ import annotations
from typing import Dict, Any
from loguru import logger

from src.core.base_model import BaseModel
from src.core.object_registry import ObjectRegistry


class Team(BaseModel):
    """
    Represents a team with win/loss records and computed statistics.

    Features:
    ----------
    - Inherits from BaseModel for ID, name, serialization, and LLM explain()
    - Tracks wins, losses, and derives win percentage
    - Provides summary methods suitable for MCP tools and LLM analysis
    - Automatically registers itself into ObjectRegistry
    """

    def __init__(self, name: str, wins: int = 0, losses: int = 0):
        super().__init__(name=name)
        self.wins = wins
        self.losses = losses

        ObjectRegistry.add(self)
        logger.debug(f"[Team] Created Team(name={name}, wins={wins}, losses={losses})")

    # ---------------------------------------------------------
    # Core Team Logic
    # ---------------------------------------------------------
    def record_win(self) -> None:
        """Increment the team's win count."""
        self.wins += 1
        logger.info(f"[Team] {self.name} recorded a win! Total wins: {self.wins}")

    def record_loss(self) -> None:
        """Increment the team's loss count."""
        self.losses += 1
        logger.info(f"[Team] {self.name} recorded a loss. Total losses: {self.losses}")

    @property
    def total_games(self) -> int:
        """Total games played."""
        return self.wins + self.losses

    @property
    def win_percentage(self) -> float:
        """Return win percentage (0.0–1.0)."""
        if self.total_games == 0:
            return 0.0
        return round(self.wins / self.total_games, 2)

    # ---------------------------------------------------------
    # High-level NLP summary capability (via llama_client)
    # ---------------------------------------------------------
    async def summarize(self) -> str:
        """
        Uses the LLM to summarize team performance.
        """
        try:
            from src.ai.llama_client import llama_summarize_team
            return await llama_summarize_team(self.to_dict())
        except Exception as e:
            logger.error(f"[Team] LLM summary failed: {e}")
            return "Summary unavailable."

    # ---------------------------------------------------------
    # Serialization & Representation
    # ---------------------------------------------------------
    def to_dict(self) -> Dict[str, Any]:
        base = super().to_dict()
        base.update(
            {
                "wins": self.wins,
                "losses": self.losses,
                "win_percentage": self.win_percentage,
                "total_games": self.total_games,
            }
        )
        return base

    def __str__(self) -> str:
        return (
            f"Team(name={self.name}, wins={self.wins}, losses={self.losses}, "
            f"win_percentage={self.win_percentage}, id={self.id})"
        )
