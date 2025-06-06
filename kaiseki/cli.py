import argparse
from stats import Analyzer
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Compute statistics of Japanese text.")
    parser.add_argument("path", type=Path, help="Path to .txt or .epub file")
    args = parser.parse_args()

    analyzer = Analyzer(args.path)
    analyzer.display_stats()


if __name__ == "__main__":
    main()
