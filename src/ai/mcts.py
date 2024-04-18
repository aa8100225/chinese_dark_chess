from typing import Any, Dict, List
import torch  # type: ignore
import numpy as np
from src.ai.res_net import ResNet
from src.game_state import GameState
from src.ai.node import Node


class MCTS:
    def __init__(self, args: Dict[str, Any], model: ResNet):
        self.args = args
        self.model = model

    @torch.no_grad()
    def search(self, state: GameState):
        root = Node(self.args, state, visit_count=1)

        policy, _ = self.model(
            torch.tensor(
                self.encoded_features(state.get_board_features()),
                device=self.model.device,
            ).unsqueeze(0)
        )
        policy = torch.softmax(policy, axis=1).squeeze(0).cpu().numpy()
        policy = (1 - self.args["dirichlet_epsilon"]) * policy + self.args[
            "dirichlet_epsilon"
        ] * np.random.dirichlet([self.args["dirichlet_alpha"]] * 2080)

        valid_moves = np.zeros(2080, dtype=np.uint8)
        valid_moves[state.get_legal_actions()] = 1
        policy *= valid_moves
        policy /= np.sum(policy)

        root.expand(policy)

        for _ in range(self.args["num_searches"]):
            node = root

            while node.is_fully_expanded():
                node = node.select()

            value, is_terminal = node.state.get_value_and_terminated()
            value = -value

            if not is_terminal:
                policy, values = self.model(
                    torch.tensor(
                        self.encoded_features(node.state.get_board_features()),
                        device=self.model.device,
                    ).unsqueeze(0)
                )
                policy = torch.softmax(policy, axis=1).squeeze(0).cpu().numpy()
                valid_moves = np.zeros(2080, dtype=np.uint8)
                valid_moves[node.state.get_legal_actions()] = 1

                policy *= valid_moves
                policy /= np.sum(policy)

                value = values.item()

                node.expand(policy)

            node.backpropagate(value)

        action_probs = np.zeros(2080)
        for child in root.children:
            action_probs[child.action_taken] = child.visit_count
        action_probs /= np.sum(action_probs)
        return action_probs

    def encoded_features(self, origin_features: List[int]):
        features = np.array(origin_features).reshape((4, 8))
        channels = 16
        encoded_features = np.zeros(
            (channels, features.shape[0], features.shape[1]), dtype=np.float32
        )
        # No Piece
        encoded_features[0] = (features == 0).astype(np.float32)
        # "Red pieces" and "Black pieces" each with numbers 1 to 7.
        # "The positive and negative signs are based on both sides. "From our perspective, all our pieces will be positive."
        for i in range(1, 8):
            encoded_features[i] = (features == i).astype(np.float32)
            encoded_features[i + 7] = (features == -i).astype(np.float32)
        # Covered Piece
        encoded_features[15] = (features == 100).astype(np.float32)
        return encoded_features
