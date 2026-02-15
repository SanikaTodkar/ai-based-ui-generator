import Button from "../components/Button";
import Card from "../components/Card";
import Chart from "../components/Chart";
import Modal from "../components/Modal";
import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";
import Input from "../components/Input";
import Table from "../components/Table";


const componentMap = {
  Button,
  Card,
  Chart,
  Modal,
  Navbar,
  Sidebar,
  Input,
  Table
};


export default function TreeRenderer({ node }) {
  if (!node) return null;

  const Component = componentMap[node.type];

  if (!Component){
    return (
          <div>
              <div style={{color: "red"}}>Invalid Component</div>
              console.error("Invalid Component: ", node.type);
          </div>
    );
  }

  return (
    <Component {...node.props}>
      {node.children &&
        node.children.map((child, index) => (
          <TreeRenderer key={index} node={child} />
        ))}
    </Component>
  );
}