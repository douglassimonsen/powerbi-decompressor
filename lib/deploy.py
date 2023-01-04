import auto_deployer
from pathlib import Path
import os


def main():
    os.environ["github_token"] = open(Path(__file__).parent / "token.txt").read()
    auto_deployer.main(Path(__file__).parent)


if __name__ == "__main__":
    main()
