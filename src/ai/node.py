import math
from typing import Any, Dict, List, Optional
import numpy as np

from src.ai.ai_game_state_transition_helper import AIGameStateTransitionHelper


class Node:
    def __init__(
        self,
        ai_game_state_transition_helper: AIGameStateTransitionHelper,
        args: Dict[str, Any],
        state: np.ndarray,
        parent: Optional["Node"] = None,
        action_taken: Optional[int] = None,
        prior=0,
        visit_count=0,
    ):
        self.ai_game_state_transition_helper = ai_game_state_transition_helper
        self.args = args
        self.state = state
        self.parent = parent
        self.action_taken = action_taken
        self.prior = prior

        self.children: List[Optional["Node"]] = []

        self.visit_count = visit_count
        self.value_sum = 0

    def is_fully_expanded(self):
        return len(self.children) > 0

    def select(self):
        best_child = None
        best_ucb = -np.inf

        for child in self.children:
            ucb = self.get_ucb(child)
            if ucb > best_ucb:
                best_child = child
                best_ucb = ucb

        return best_child

    def get_ucb(self, child):
        if child.visit_count == 0:
            q_value = 0
        else:
            q_value = 1 - ((child.value_sum / child.visit_count) + 1) / 2
        return (
            q_value
            + self.args["C"]
            * (math.sqrt(self.visit_count) / (child.visit_count + 1))
            * child.prior
        )

    def expand(self, policy):
        child = None
        for action, prob in enumerate(policy):
            if prob > 0:
                child_state = self.state.copy()
                child_state = self.ai_game_state_transition_helper.get_next_state(
                    child_state, action
                )
                child_state = self.ai_game_state_transition_helper.change_perspective(
                    child_state
                )
                # if action > 135:
                #     prob += (
                #         0.1
                #         * self.ai_game_state_transition_helper.count_covered_pieces_number(
                #             child_state
                #         )
                #         / 32
                #     )

                child = Node(
                    self.ai_game_state_transition_helper,
                    self.args,
                    child_state,
                    self,
                    action,
                    prob,
                )
                self.children.append(child)

        return child

    def backpropagate(self, value):
        self.value_sum += value
        self.visit_count += 1

        value = self.ai_game_state_transition_helper.get_opponent_value(value)
        if self.parent is not None:
            self.parent.backpropagate(value)
