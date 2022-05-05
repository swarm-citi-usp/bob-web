import React, { useState } from "react";
import axios from "axios";

function Container() {
  const [queryType, setQueryType] = useState("swarm:lamp");
  const [queryOperation, setQueryOperation] = useState("readOperation");

  const test = () => {
    console.log(queryType);
    console.log(queryOperation);
    // axios.get('http://localhost:8975/test').then(({data})=> console.log(data));
  };

  const discover = () => {
    axios
      .post(
        "http://localhost:8975/discovery",
        { type: queryType, operation: queryOperation }
      )
      .then(({ data }) => console.log(data));
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
        <p> {test} </p>
      </div>
    </div>
  );
}

export default Container;
