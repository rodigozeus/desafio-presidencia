import React, { Suspense, lazy } from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { AuthProvider, useAuth } from "./context/AuthContext";
import Navigation from "./components/Navigation";
import Login from "./components/Login";
import "./App.css";

const OrdersApp = lazy(() => import("mfe_orders/OrdersApp"));

function ProtectedRoute({ children }) {
  const { token } = useAuth();
  return token ? children : <Navigate to="/login" replace />;
}

function AppRoutes() {
  const { token } = useAuth();
  return (
    <>
      {token && <Navigation />}
      <main className="main-content">
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route
            path="/orders/*"
            element={
              <ProtectedRoute>
                <Suspense fallback={<div className="loading">Carregando módulo de pedidos...</div>}>
                  <OrdersApp />
                </Suspense>
              </ProtectedRoute>
            }
          />
          <Route path="/" element={<Navigate to={token ? "/orders" : "/login"} replace />} />
        </Routes>
      </main>
    </>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <AppRoutes />
      </BrowserRouter>
    </AuthProvider>
  );
}
