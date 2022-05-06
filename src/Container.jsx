import React, { useState } from "react";
import axios from "axios";

function Container() {
  const [queryType, setQueryType] = useState("swarm:lamp");
  const [queryOperation, setQueryOperation] = useState("readOperation");
  const [discoveryResult, setDiscoveryResult] = useState({ candidates: [] });
  const [img, setImg] = useState("");

  const test = () => {
    console.log(queryType);
    console.log(queryOperation);
    // axios.get('http://localhost:8975/test').then(({data})=> console.log(data));
  };

  const discover = () => {
    axios
      .post("http://localhost:5022/discovery", {
        type: queryType,
        operation: queryOperation,
      })
      .then(({ data }) => setDiscoveryResult(data));
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
      <div className="row">
        {discoveryResult.candidates.map((candidate, index1) => (
          <div>
            {candidate.remoteAgent.serviceDescription.operations.map(
              (op, index2) => (
                <a
                  key={"" + index1 + index2}
                  className="waves-effect waves-light btn"
                  onClick={() => use(candidate, op)}
                >
                  {candidate.remoteAgent.didDocument.id + " " + op.returns}
                </a>
              )
            )}
          </div>
        ))}
      </div>
      <div className="row">
        <img className="col s6" src={`data:image/jpeg;base64, ${img}`}></img>
      </div>
    </div>
  );
}

export default Container;
