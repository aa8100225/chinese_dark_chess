import torch  # type: ignore
import numpy as np
from src.ai.mcts import MCTS
from src.models.piece_action import PieceAction, PieceActionType
from src.ai.piece_action_code import PIECE_ACTION_DECODE_ACTION
from src.ai.ai_game_state_transition_helper import AIGameStateTransitionHelper
from src.game_state import GameState
from src.ai.res_net import ResNet
from src.config.settings import AI_ARGS


class Agent:
    def __init__(self, ai_model_path: str) -> None:
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.ai_game_state_transition_helper = AIGameStateTransitionHelper()
        self.model = ResNet(self.ai_game_state_transition_helper, 9, 128, self.device)
        self.mcts: MCTS
        self.initialization(ai_model_path)

    def initialization(self, ai_model_path: str) -> None:
        self.model.load_state_dict(torch.load(ai_model_path, map_location=self.device))  # type: ignore
        self.model.eval()  # type: ignore
        self.mcts = MCTS(AI_ARGS, self.ai_game_state_transition_helper, self.model)

    def predict(self, game_state: GameState) -> PieceAction:
        state = self.ai_game_state_transition_helper.get_initial_state(game_state)
        mcts_probs = self.mcts.search(state)
        action = PIECE_ACTION_DECODE_ACTION[np.argmax(mcts_probs).astype(int)]
        match (action[1]):
            case 0:
                piece_action_type = PieceActionType.REVEAL
            case 1:
                piece_action_type = PieceActionType.MOVE
            case 2:
                piece_action_type = PieceActionType.EAT
        return PieceAction(action[0], piece_action_type, action[2])
