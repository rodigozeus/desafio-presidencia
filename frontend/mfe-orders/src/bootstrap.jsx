import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import OrdersApp from "./OrdersApp";

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <BrowserRouter>
    <Routes>
      <Route path="/" element={<Navigate to="/orders" replace />} />
      <Route path="/orders/*" element={<OrdersApp />} />
    </Routes>
  </BrowserRouter>
);
