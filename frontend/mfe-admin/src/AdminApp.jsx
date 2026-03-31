import React from "react";
import { Routes, Route } from "react-router-dom";
import UserCreate from "./components/UserCreate";

export default function AdminApp() {
  return (
    <Routes>
      <Route index element={<UserCreate />} />
    </Routes>
  );
}
