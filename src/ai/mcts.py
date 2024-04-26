from typing import Any, Dict
import torch  # type: ignore
import numpy as np
from src.ai.ai_game_state_transition_helper import AIGameStateTransitionHelper
from src.ai.res_net import ResNet
from src.ai.node import Node


class MCTS:
    def __init__(
        self,
        args: Dict[str, Any],
        ai_game_state_transition_helper: AIGameStateTransitionHelper,
        model: ResNet,
    ):
        self.args = args
        self.model = model
        self.ai_game_state_transition_helper = ai_game_state_transition_helper

    @torch.no_grad()
    def search(self, state: np.ndarray):
        root = Node(
            self.ai_game_state_transition_helper, self.args, state, visit_count=1
        )

        policy, _ = self.model(
            torch.tensor(
                self.ai_game_state_transition_helper.get_encoded_state(state),
                device=self.model.device,
            ).unsqueeze(0)
        )
        policy = torch.softmax(policy, axis=1).squeeze(0).cpu().numpy()
        policy = (1 - self.args["dirichlet_epsilon"]) * policy + self.args[
            "dirichlet_epsilon"
        ] * np.random.dirichlet(
            [self.args["dirichlet_alpha"]]
            * self.ai_game_state_transition_helper.action_size
        )

        valid_moves = self.ai_game_state_transition_helper.get_valid_moves(state)

        if len(np.where(valid_moves > 0)[0]) == 0:
            raise Exception("Error")

        policy *= valid_moves
        policy /= np.sum(policy)

        root.expand(policy)

        for _ in range(self.args["num_searches"]):
            node = root

            while node.is_fully_expanded():
                node = node.select()

            value, is_terminal = (
                self.ai_game_state_transition_helper.get_value_and_terminated(
                    node.state, node.action_taken, current=True
                )
            )
            value = self.ai_game_state_transition_helper.get_opponent_value(value)
            if not is_terminal:
                policy, values = self.model(
                    torch.tensor(
                        self.ai_game_state_transition_helper.get_encoded_state(
                            node.state
                        ),
                        device=self.model.device,
                    ).unsqueeze(0)
                )
                policy = torch.softmax(policy, axis=1).squeeze(0).cpu().numpy()
                valid_moves = self.ai_game_state_transition_helper.get_valid_moves(
                    node.state
                )
                if len(np.where(valid_moves > 0)[0]) == 0:
                    raise Exception("Error")
                policy *= valid_moves
                if np.sum(policy) > 0:
                    policy /= np.sum(policy)

                value = values.item()

                node.expand(policy)

            node.backpropagate(value)

        action_probs = np.zeros(self.ai_game_state_transition_helper.action_size)
        for child in root.children:
            if child is not None:
                action_probs[child.action_taken] = child.visit_count
        action_probs /= np.sum(action_probs)
        return action_probs
