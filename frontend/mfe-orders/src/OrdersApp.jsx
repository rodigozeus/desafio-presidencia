import React from "react";
import { Routes, Route } from "react-router-dom";
import OrdersList from "./components/OrdersList";
import OrderCreate from "./components/OrderCreate";
import OrderDetail from "./components/OrderDetail";

export default function OrdersApp() {
  return (
    <Routes>
      <Route index element={<OrdersList />} />
      <Route path="new" element={<OrderCreate />} />
      <Route path=":id" element={<OrderDetail />} />
    </Routes>
  );
}
