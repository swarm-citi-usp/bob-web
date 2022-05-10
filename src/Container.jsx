import React, { useState } from "react";
import axios from "axios";

function Container() {
  const [queryType, setQueryType] = useState("swarm:lamp");
  const [queryOperation, setQueryOperation] = useState("updateOperation");
  const [discoveryResult, setDiscoveryResult] = useState({ candidates: [] });
  const [loading, setLoading] = useState(false);
  const [img, setImg] = useState("");

  const clearState = () => {
    setDiscoveryResult({ candidates: [] });
    setImg("");
  };

  const discover = () => {
    clearState();
    setLoading(true);
    axios
      .post("http://localhost:5022/discovery", {
        type: queryType,
        operation: queryOperation,
      })
      .then(({ data }) => setDiscoveryResult(data))
      .finally(() => setLoading(false));
  };

  const use = (candidate, operation) => {
    axios
      .post("http://localhost:5022/use", {
        candidate: candidate,
        operation: operation,
      })
      .then(({ data }) => setImg(data.data));
  };

  return (
    <div className="container">
      <div className="row">
        <div className="input-field col s6">
          <input
            value={queryType}
            id="query_type"
            type="text"
            className="validate"
            onChange={(e) => setQueryType(e.target.value)}
          />
          <label htmlFor="query_type">Type</label>
        </div>
        <div className="input-field col s6">
          <input
            value={queryOperation}
            id="query_operation"
            type="text"
            className="validate"
            onChange={(e) => setQueryOperation(e.target.value)}
          />
          <label htmlFor="query_operation">Operation</label>
        </div>
      </div>
      <div className="row">
        <a className="waves-effect waves-light btn" onClick={discover}>
          Discover
        </a>
      </div>
      {loading && (
        <div className="row">
          <div class="progress">
            <div class="indeterminate"></div>
          </div>
        </div>
      )}
      <div className="row">
        {discoveryResult.candidates.map((candidate, index1) => (
          <div className="col s12 m6">
            <div className="card horizontal">
              <div className="card-stacked">
                <div className="card-content">
                  <h5>{candidate.remoteAgent.didDocument.id}</h5>
                </div>
                {candidate.remoteAgent.serviceDescription.operations.map(
                  (op, index2) => (
                    <div className="card-action">
                      <a
                        key={"" + index1 + index2}
                        className="waves-effect waves-light btn"
                        onClick={() => use(candidate, op)}
                      >
                        {op.returns}
                      </a>
                    </div>
                  )
                )}
              </div>
            </div>
          </div>
        ))}
      </div>
      {img !== "" && (
        <div className="row">
          <img className="col s6" src={`data:image/jpeg;base64, ${img}`}></img>
        </div>
      )}
    </div>
  );
}

export default Container;
