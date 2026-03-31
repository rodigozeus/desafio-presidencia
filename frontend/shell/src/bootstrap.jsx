import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";

class ErrorBoundary extends React.Component {
  constructor(props) { super(props); this.state = { error: null }; }
  static getDerivedStateFromError(err) { return { error: err }; }
  render() {
    if (this.state.error) {
      return (
        <div style={{ padding: 24, fontFamily: "monospace", background: "#fee", color: "#c00", whiteSpace: "pre-wrap" }}>
          <strong>Erro de renderização:</strong>{"\n"}
          {String(this.state.error)}
        </div>
      );
    }
    return this.props.children;
  }
}

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(<ErrorBoundary><App /></ErrorBoundary>);
