import sys
import os
sys.path.insert(0, os.getcwd() + "/../swarm-lib-python")


from swarm_lib import Wallet, Agent, Candidate, ServiceOperation
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
def discovery():
    data = request.get_json()

    type_ = data.get("type", "")
    operation = data.get("operation", "")

    if operation == "":
        query = {"@type": type_, "minCandidates": 1}
    else:
        query = {"@type": type_, "operation": {"@type": operation}, "minCandidates": 1}

    discovery_result = bob.discover(query)
    print(discovery_result)
    print("Found %s results via discovery" % (len(discovery_result.candidates)))
    print(discovery_result)
    # if type_ == "swarm:camera":
    #     run_frame(discovery_result.best_remote())
    # else:
    #     run(discovery_result.remote_agents())

    return discovery_result.to_json()

@bob.flask_app.route("/use", methods=["POST"])
def use():
    data = request.get_json()

    candidate_dict = data.get("candidate")
    operation_dict = data.get("operation")

    if candidate_dict is not None:
        candidate = Candidate.from_dict(candidate_dict)
        operation = ServiceOperation.from_dict(operation_dict)

        if candidate_dict["remoteAgent"]["serviceDescription"]["@type"] == "swarm:camera":
            resp, jpg_as_text = run_frame(candidate, operation)

        else:
            resp, jpg_as_text = run(candidate, operation)

    # data = cbor2.loads(resp["payload"])["value"]
    # return jsonify({data: data}, resp["status"])
    return jsonify({data: jpg_as_text})


def run(candidate, operation):
    remote_agent = candidate.remote_agent
    ok, resp, token = bob.execute_auto_token(remote_agent, operation=operation, message=msg, token=None)

    # print("ok")
    # print(ok)
    # print("resp")
    # print(resp)
    # print("token")
    # print(token)

    return resp



def run_frame(candidate, operation):
    import cv2
    import numpy as np
    import base64

    remote_agent = candidate.remote_agent

    token = None
    ok, resp, token = bob.execute_auto_token(remote_agent, operation=operation, message=msg, token=token)
    print(">>>> Execute with ABAC + Auto Token: ", ok)
    data = cbor2.loads(resp["payload"])["value"]

    # _retval, buffer = cv2.imencode('.jpg', data)
    jpg_as_text = base64.b64encode(data).decode("utf-8") 
    # jpg_as_np = np.frombuffer(data, dtype=np.uint8)
    # img = cv2.imdecode(jpg_as_np, flags=1)
    # print(img)
    # print(type(img))
    print(jpg_as_text)
    # print(data)

    # cv2.imwrite("frame.jpg", img)
    # cv2.imshow("frame", img)
    # cv2.waitKey(1)

    return resp, jpg_as_text


# def run_frame(remote_agent):
#     import cv2
#     import numpy as np
#     token = None
#     while True:
#         ok, resp, token = bob.execute_auto_token(remote_agent, operation=remote_agent.service_description.operations[0], message=msg, token=token)
#         print(">>>> Execute with ABAC + Auto Token: ", ok)
#         data = cbor2.loads(resp["payload"])["value"]
#         jpg_as_np = np.frombuffer(data, dtype=np.uint8)
#         img = cv2.imdecode(jpg_as_np, flags=1)
#         cv2.imwrite("frame.jpg", img)
#         cv2.imshow("frame", img)
#         cv2.waitKey(1)
#         input("press enter")

if __name__ == "__main__":
    # bob.register_at_broker()
    bob.serve_with_flask(debug=True)
