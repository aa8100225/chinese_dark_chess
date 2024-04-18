import argparse
from src.game import Game
from src.logger import setup_error_logger


def parse_args():
    parser = argparse.ArgumentParser(description="Run the Chinese Dark Chess game.")
    parser.add_argument("--ai", action="store_true", help="Enable AI opponent")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    logger = setup_error_logger(__name__)
    Game("./src/ai/model.pt", args.ai, logger).run()
