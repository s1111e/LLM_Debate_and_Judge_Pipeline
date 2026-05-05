import argparse
import json

from debate.debate_orchestrator import DebateOrchestrator
from utils.config_loader import load_config


def main():
    parser = argparse.ArgumentParser(description="Run one LLM debate.")
    parser.add_argument(
        "--question",
        default="Did humans live at the same time as dinosaurs?",
        help="Yes/no reasoning question to debate."
    )
    parser.add_argument(
        "--no-log",
        action="store_true",
        help="Run without appending to logs/debate_logs.json."
    )
    args = parser.parse_args()

    config = load_config()
    debate = DebateOrchestrator(config=config)
    _, result = debate.run_debate(args.question, save_log=not args.no_log)

    print("\n=== STRUCTURED RESULT ===")
    print(json.dumps({
        "prediction": result["prediction"],
        "confidence": result["confidence"],
        "stopped_early": result["stopped_early"],
        "stop_reason": result["stop_reason"]
    }, indent=2))


if __name__ == "__main__":
    main()
