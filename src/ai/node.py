import copy
import math
from typing import Any, Dict, List, Optional
import numpy as np

from src.game_state import GameState


class Node:
    def __init__(
        self,
        args: Dict[str, Any],
        state: GameState,
        parent: Optional["Node"] = None,
        action_taken: Optional[int] = None,
        prior: int = 0,
        visit_count: int = 0,
    ) -> None:
        self.args = args
        self.state = state
        self.parent = parent
        self.action_taken = action_taken
        self.prior = prior

        self.children: List["Node"] = []

        self.visit_count = visit_count
        self.value_sum = 0

    def is_fully_expanded(self) -> bool:
        return len(self.children) > 0

    def select(self) -> "Node":
        best_child = self
        best_ucb = -np.inf

        for child in self.children:
            ucb = self.get_ucb(child)
            if ucb > best_ucb:
                best_child = child
                best_ucb = ucb

        return best_child

    def get_ucb(self, child: "Node") -> float:
        if child.visit_count == 0:
            q_value: float = 0
        else:
            q_value = 1 - ((child.value_sum / child.visit_count) + 1) / 2
        return (
            q_value
            + self.args["C"]
            * (math.sqrt(self.visit_count) / (child.visit_count + 1))
            * child.prior
        )

    def expand(self, policy) -> None:
        for action, prob in enumerate(policy):
            if prob > 0:
                child_state = copy.deepcopy(self.state)
                piece_action = child_state.generate_action_by_index(action)
                child_state = child_state.next_state(piece_action)

                child = Node(self.args, child_state, self, action, prob)
                self.children.append(child)

    def backpropagate(self, value):
        self.value_sum += value
        self.visit_count += 1

        value = -value
        if self.parent is not None:
            self.parent.backpropagate(value)
