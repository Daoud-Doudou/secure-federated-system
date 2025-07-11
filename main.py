import argparse
import logging
from flpeer import FLPeer
from utils.config import load_or_init_config, load_or_init_state
from utils.federation import elect_next_server

logging.basicConfig(level = logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == "__main__":

	parser = argparse.ArgumentParser()
	parser.add_argument("--peer-id", required = True, help = "Identifiant du pair (ex: client1)")
	args = parser.parse_args()

	config = load_or_init_config("config.yaml")
	state = load_or_init_state(config)

	config["peer_id"] = args.peer_id
	config["is_server"] = (args.peer_id == state["current_server"])


	if config['is_server']:
		config["host"] = '0.0.0.0'
	else:
		config["host"] = state["current_server"]


	logger.info(f"{args.peer_id} sera {'SERVER' if config['is_server'] else 'CLIENT'} pour cette session")

	try:
		peer = FLPeer(config)
		peer.run()
		if config['is_server']:
			elect_next_server(state, config)

	except Exception as e:
		logger.error(f"Erreur critique: {e}", exc_info = True)
		raise
