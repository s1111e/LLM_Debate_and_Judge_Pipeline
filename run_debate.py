from debate.debate_orchestrator import DebateOrchestrator
from config.config_loader import load_config

config = load_config()

question = "Did humans live at the same time as dinosaurs?"

debate = DebateOrchestrator(rounds=config["debate_rounds"])

transcript, result = debate.run_debate(question)