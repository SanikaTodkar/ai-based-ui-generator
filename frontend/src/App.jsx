import React, { useState } from "react";
import { sendMessage, rollback, clearHistory } from "./api";

import Button from "./components/Button";
import Card from "./components/Card";
import Input from "./components/Input";
import Table from "./components/Table";
import Modal from "./components/Modal";
import Sidebar from "./components/Sidebar";
import Navbar from "./components/Navbar";
import Chart from "./components/Chart";
import "./styles.css";



const componentMap = {
  Button,
  Card,
  Input,
  Table,
  Modal,
  Sidebar,
  Navbar,
  Chart,
};



function RenderTree({ node }) {
  if (!node) return null;

  const Component = componentMap[node.type];

  if (!Component) {
    return <div style={{ color: "red" }}>Invalid Component</div>;
  }



  return (
    <Component {...node.props}>
      {node.children &&
        node.children.map((child, index) => (
        <RenderTree key={index} node={child} />
        ))}
    </Component>
  );
}


export default function App() {
  const [input, setInput] = useState("");
  const [tree, setTree] = useState(null);
  const [explanation, setExplanation] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSend = async () => {
    if(!input.trim()) return;

    try{
      setLoading(true);

      const res = await sendMessage(input);

      setTree(res.tree);
      setExplanation(res.explanation);
      setInput("");
    } catch (err) {
      console.error("Error:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleRollback = async () => {
    const res = await rollback();
    setTree(res.tree);
  };


  const handleClear = async () => {
    await clearHistory();
    setTree(null);
    setExplanation("");
  };

  return (
  <div className="app-container">

    <div className="chat-panel">
      <h2>Agent Chat</h2>

      <div className="chat-box">
        {explanation && <p>{explanation}</p>}
      </div>

      <textarea
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Type your instruction..."
      />

      <div className="button-group">
        <button onClick={handleSend} disabled={loading}>{loading ? "Generating..." : "Send"}</button>
        <button onClick={handleRollback}>Rollback</button>
        <button onClick={handleClear}>Clear</button>
      </div>
    </div>

    <div className="right-panel">

      <div className="json-viewer">
        <h3>Generated JSON</h3>
        <pre>
          {tree ? JSON.stringify(tree, null, 2) : "No UI Generated"}
        </pre>
      </div>

      <div className="preview-panel">
        <h3>Live Preview</h3>
        <div className="preview-content">
          {tree && <RenderTree node={tree} />}
        </div>
      </div>

    </div>

  </div>
);

}