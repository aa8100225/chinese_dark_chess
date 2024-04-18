from typing import List
import torch  # type: ignore
import numpy as np
from src.ai.mcts import MCTS
from src.game_state import GameState
from src.ai.res_net import ResNet
from src.config.settings import AI_ARGS


class Agent:
    def __init__(self, ai_model_path: str) -> None:
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = ResNet(4, 8, 2080, 4, 64, self.device)
        self.mcts: MCTS
        self.initialization(ai_model_path)

    def initialization(self, ai_model_path: str) -> None:
        self.model.load_state_dict(torch.load(ai_model_path, map_location=self.device))  # type: ignore
        self.model.eval()  # type: ignore
        self.mcts = MCTS(AI_ARGS, self.model)

    def predict(self, state: GameState) -> int:
        mcts_probs = self.mcts.search(state)
        return np.argmax(mcts_probs).astype(int)

    def _predict(self, origin_features: List[int], leagal_actions: List[int]) -> int:
        valid_moves = np.zeros(2080, dtype=np.uint8)
        valid_moves[leagal_actions] = 1
        tensor_state = torch.tensor(
            self.encoded_features(origin_features), device=self.device
        ).unsqueeze(0)
        with torch.no_grad():
            policy, value = self.model(tensor_state)
        policy = torch.softmax(policy, axis=1).squeeze(0).detach().cpu().numpy()
        value = value.item()
        policy *= valid_moves
        if policy.sum() > 0:
            policy /= policy.sum()
            # Randomly select one based on probabilities
            return np.random.choice(len(policy), p=policy)
        # If there are no valid moves predicted, randomly choose one to escape
        print("Unable to predict")
        return np.random.choice(np.where(valid_moves > 0)[0])

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
