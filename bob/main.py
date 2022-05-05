import sys
import os
sys.path.insert(0, os.getcwd() + "/../swarm-lib-python")


from swarm_lib import Wallet, Agent
import cbor2, logging, sys
from flask import jsonify, request
from flask_cors import CORS

# import time
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument(
    "-c", "--consumer", default="bob", type=str, help="consumer to execute"
)
args = parser.parse_args()

Wallet.init(os.environ.get("SWARM_BASE_DIR"))

bob = Agent.from_config("bob", load_upnp=False)
bob.enable_flask_app(__name__)

CORS(bob.flask_app)

msg = cbor2.dumps({"value": 75})

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s {%(pathname)s:%(lineno)d} %(levelname)s %(message)s')


@bob.flask_app.route("/test", methods=["GET"])
def test(type: str = "swarm:lamp", operation: str = "readOperation"):
    return jsonify({"abc": 222})

@bob.flask_app.route("/discovery", methods=["POST"])
def discovery(type: str = "swarm:lamp", operation: str = "readOperation"):
    data = request.get_json()

    type_ = data.get("type", type)
    operation = data.get("operation", operation)

    discovery_result = bob.discover({"@type": type_, "operation": {"@type": operation}, "minCandidates": 1})
    print(discovery_result)
    print("Found %s results via discovery" % (len(discovery_result.candidates)))
    print(discovery_result)
    input("Discovery done. Press enter to continue with service execution.")
    if type_ == "swarm:camera":
        run_frame(discovery_result.best_remote())
    else:
        run(discovery_result.remote_agents())

def run(remote_agents):
    print(">>>>>>>>", remote_agents)
    tokens = [None, None]
    while True:
        for i, remote_agent in enumerate(remote_agents):
            ok, resp, token = bob.execute_auto_token(remote_agent, operation=remote_agent.service_description.operations[0], message=msg, token=tokens[i])
            tokens[i] = token
            print(">>>> Execute with ABAC + Auto Token: ", ok)
        input("press enter")

def run_frame(remote_agent):
    import cv2
    import numpy as np
    token = None
    while True:
        ok, resp, token = bob.execute_auto_token(remote_agent, operation=remote_agent.service_description.operations[0], message=msg, token=token)
        print(">>>> Execute with ABAC + Auto Token: ", ok)
        data = cbor2.loads(resp["payload"])["value"]
        jpg_as_np = np.frombuffer(data, dtype=np.uint8)
        img = cv2.imdecode(jpg_as_np, flags=1)
        cv2.imwrite("frame.jpg", img)
        cv2.imshow("frame", img)
        cv2.waitKey(1)
        input("press enter")

if __name__ == "__main__":
    # bob.register_at_broker()
    bob.serve_with_flask(debug=True)
