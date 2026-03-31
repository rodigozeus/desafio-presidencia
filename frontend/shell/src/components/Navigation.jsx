import React from "react";
import { Link, useLocation } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import "./Navigation.css";

export default function Navigation() {
  const { user, logout } = useAuth();
  const location = useLocation();

  return (
    <nav className="nav">
      <div className="nav-brand">
        <span className="nav-logo">📦</span>
        <span className="nav-title">Gestão de Pedidos</span>
      </div>
      <div className="nav-links">
        <Link className={`nav-link ${location.pathname.startsWith("/orders") ? "active" : ""}`} to="/orders">
          Pedidos
        </Link>
        {user?.role === "admin" && (
          <Link className={`nav-link ${location.pathname.startsWith("/admin") ? "active" : ""}`} to="/admin">
            Usuários
          </Link>
        )}
      </div>
      <div className="nav-user">
        <span className="nav-user-name">{user?.name}</span>
        <span className="nav-user-role">{user?.role}</span>
        <button className="nav-logout" onClick={logout}>Sair</button>
      </div>
    </nav>
  );
}
