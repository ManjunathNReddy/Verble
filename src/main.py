from ui.cli import CLI
from game_runner import GameRunner

if __name__ == '__main__':
    runner = GameRunner(CLI())
    runner.run()