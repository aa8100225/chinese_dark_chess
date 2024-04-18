import torch.nn as nn  # type: ignore
from src.ai.res_block import ResBlock


class ResNet(nn.Module):  # type-ignored
    def __init__(
        self, row: int, col: int, action_size: int, num_res_blocks, num_hidden, device
    ):
        super().__init__()

        self.device = device
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
            nn.Linear(32 * row * col, action_size),
        )

        self.value_head = nn.Sequential(
            nn.Conv2d(num_hidden, 3, kernel_size=3, padding=1),
            nn.BatchNorm2d(3),
            nn.ReLU(),
            nn.Flatten(),
            nn.Linear(3 * row * col, 1),
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
