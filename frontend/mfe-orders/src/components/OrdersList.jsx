import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { fetchOrders } from "../api";
import "./OrdersList.css";

const STATUS_LABELS = {
  pending: "Pendente",
  processing: "Processando",
  shipped: "Enviado",
  delivered: "Entregue",
  cancelled: "Cancelado",
};

const PRIORITY_LABELS = { low: "Baixa", medium: "Média", high: "Alta" };

const STATUS_OPTIONS = ["", "pending", "processing", "shipped", "delivered", "cancelled"];

export default function OrdersList() {
  const navigate = useNavigate();
  const [orders, setOrders] = useState([]);
  const [filter, setFilter] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    setLoading(true);
    fetchOrders(filter)
      .then(setOrders)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, [filter]);

  return (
    <div className="orders-page">
      <div className="orders-header">
        <div>
          <h1>Pedidos</h1>
          <p className="orders-count">{orders.length} pedido{orders.length !== 1 ? "s" : ""} encontrado{orders.length !== 1 ? "s" : ""}</p>
        </div>
        <button className="btn-primary" onClick={() => navigate("/orders/new")}>
          + Novo Pedido
        </button>
      </div>

      <div className="orders-filters">
        <label>Filtrar por status:</label>
        <div className="filter-buttons">
          {STATUS_OPTIONS.map((s) => (
            <button
              key={s || "all"}
              className={`filter-btn ${filter === s ? "active" : ""}`}
              onClick={() => setFilter(s)}
            >
              {s ? STATUS_LABELS[s] : "Todos"}
            </button>
          ))}
        </div>
      </div>

      {error && <div className="error-box">{error}</div>}

      {loading ? (
        <div className="loading-box">Carregando pedidos...</div>
      ) : orders.length === 0 ? (
        <div className="empty-box">
          <span>📭</span>
          <p>Nenhum pedido encontrado</p>
          <button className="btn-primary" onClick={() => navigate("/orders/new")}>Criar primeiro pedido</button>
        </div>
      ) : (
        <div className="orders-table-wrap">
          <table className="orders-table">
            <thead>
              <tr>
                <th>Cliente</th>
                <th>Itens</th>
                <th>Total</th>
                <th>Status</th>
                <th>Prioridade</th>
                <th>Criado em</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {orders.map((order) => (
                <tr key={order.id} onClick={() => navigate(`/orders/${order.id}`)} className="order-row">
                  <td>
                    <div className="customer-name">{order.customer_name}</div>
                    <div className="customer-email">{order.customer_email}</div>
                  </td>
                  <td>{order.items?.length || 0} item{(order.items?.length || 0) !== 1 ? "s" : ""}</td>
                  <td className="amount">R$ {Number(order.total_amount).toFixed(2)}</td>
                  <td><span className={`status-badge status-${order.status}`}>{STATUS_LABELS[order.status]}</span></td>
                  <td><span className={`priority-badge priority-${order.priority}`}>{PRIORITY_LABELS[order.priority]}</span></td>
                  <td>{new Date(order.created_at).toLocaleDateString("pt-BR")}</td>
                  <td><span className="view-link">Ver →</span></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
