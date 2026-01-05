import argparse
from dotenv import load_dotenv

from analyzer import analyze_logs
from llm_client import create_llm_client

def main():
    load_dotenv()  # load .env once

    parser = argparse.ArgumentParser(description="LLM-powered log analyzer")
    parser.add_argument("file", help="Path to log file")
    parser.add_argument(
        "--llm",
        choices=["openai", "ollama", "hf", "deepseek"],
        default="ollama",
        help="LLM backend to use"
    )

    args = parser.parse_args()

    llm = create_llm_client(args.llm)
    analyze_logs(args.file, llm)

if __name__ == "__main__":
    main()
