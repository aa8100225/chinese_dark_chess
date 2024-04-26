import torch.nn as nn  # type: ignore
from src.ai.res_block import ResBlock
from src.ai.ai_game_state_transition_helper import AIGameStateTransitionHelper


class ResNet(nn.Module):  # type-ignored
    def __init__(
        self,
        ai_game_state_transition_helper: AIGameStateTransitionHelper,
        num_res_blocks,
        num_hidden,
        device,
    ):
        super().__init__()

        self.device = device
        self.ai_game_state_transition_helper = ai_game_state_transition_helper
        self.start_block = nn.Sequential(
            nn.Conv2d(16, num_hidden, kernel_size=3, padding=1),
            nn.BatchNorm2d(num_hidden),
            nn.ReLU(),
        )

        self.back_bone = nn.ModuleList(
            [ResBlock(num_hidden) for i in range(num_res_blocks)]
        )

        self.policy_head = nn.Sequential(
            nn.Conv2d(num_hidden, 32, kernel_size=3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.Flatten(),
            nn.Linear(
                32
                * self.ai_game_state_transition_helper.row_count
                * self.ai_game_state_transition_helper.column_count,
                self.ai_game_state_transition_helper.action_size,
            ),
        )

        self.value_head = nn.Sequential(
            nn.Conv2d(num_hidden, 3, kernel_size=3, padding=1),
            nn.BatchNorm2d(3),
            nn.ReLU(),
            nn.Flatten(),
            nn.Linear(
                3
                * self.ai_game_state_transition_helper.row_count
                * self.ai_game_state_transition_helper.column_count,
                1,
            ),
            nn.Tanh(),
        )

        self.to(device)

    def forward(self, x):
        x = self.start_block(x)
        for res_block in self.back_bone:
            x = res_block(x)
        policy = self.policy_head(x)
        value = self.value_head(x)
        return policy, value
