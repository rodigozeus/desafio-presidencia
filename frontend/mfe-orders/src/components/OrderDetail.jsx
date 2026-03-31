import React, { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { fetchOrder, updateOrderStatus } from "../api";
import "./OrderDetail.css";

const STATUS_LABELS = {
  pending: "Pendente", processing: "Processando",
  shipped: "Enviado", delivered: "Entregue", cancelled: "Cancelado",
};
const PRIORITY_LABELS = { low: "Baixa", medium: "Média", high: "Alta" };
const STATUS_FLOW = ["pending", "processing", "shipped", "delivered"];
const ALL_STATUSES = ["pending", "processing", "shipped", "delivered", "cancelled"];

export default function OrderDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [order, setOrder] = useState(null);
  const [loading, setLoading] = useState(true);
  const [updating, setUpdating] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    fetchOrder(id)
      .then(setOrder)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, [id]);

  const handleStatusUpdate = async (newStatus) => {
    setUpdating(true);
    try {
      const updated = await updateOrderStatus(id, newStatus);
      setOrder(updated);
    } catch (e) {
      setError(e.message);
    } finally {
      setUpdating(false);
    }
  };

  if (loading) return <div className="detail-page"><div className="loading-box">Carregando...</div></div>;
  if (error) return <div className="detail-page"><div className="error-box">{error}</div></div>;
  if (!order) return null;

  return (
    <div className="detail-page">
      <div className="detail-header">
        <button className="btn-back" onClick={() => navigate("/orders")}>← Pedidos</button>
        <div>
          <h1>Pedido #{order.order_number}</h1>
          <p className="detail-date">Criado em {new Date(order.created_at).toLocaleString("pt-BR")}</p>
        </div>
        <div className="header-badges">
          <span className={`status-badge status-${order.status}`}>{STATUS_LABELS[order.status]}</span>
          <span className={`priority-badge priority-${order.priority}`}>{PRIORITY_LABELS[order.priority]} prioridade</span>
        </div>
      </div>

      {order.ai_summary && (
        <div className="ai-card">
          <span className="ai-icon">🤖</span>
          <div>
            <strong>Resumo IA:</strong> {order.ai_summary}
          </div>
        </div>
      )}

      <div className="detail-grid">
        <div className="detail-card">
          <h2>Cliente</h2>
          <p className="detail-field"><span>Nome</span><strong>{order.customer_name}</strong></p>
          <p className="detail-field"><span>Email</span><strong>{order.customer_email}</strong></p>
          {order.notes && <p className="detail-field"><span>Observações</span><strong>{order.notes}</strong></p>}
          {order.created_by && <p className="detail-field"><span>Criado por</span><strong>{order.created_by}</strong></p>}
        </div>

        <div className="detail-card">
          <h2>Itens do Pedido</h2>
          <table className="items-table">
            <thead>
              <tr><th>Produto</th><th>Qtd</th><th>Unit.</th><th>Total</th></tr>
            </thead>
            <tbody>
              {order.items?.map((item, idx) => (
                <tr key={idx}>
                  <td>{item.product_name}</td>
                  <td>{item.quantity}</td>
                  <td>R$ {Number(item.unit_price).toFixed(2)}</td>
                  <td>R$ {(item.quantity * item.unit_price).toFixed(2)}</td>
                </tr>
              ))}
            </tbody>
          </table>
          <div className="order-total">
            <span>Total</span>
            <strong>R$ {Number(order.total_amount).toFixed(2)}</strong>
          </div>
        </div>
      </div>

      <div className="detail-card status-card">
        <h2>Atualizar Status</h2>
        <div className="status-buttons">
          {ALL_STATUSES.map((s) => (
            <button
              key={s}
              className={`status-btn ${order.status === s ? "current" : ""} status-opt-${s}`}
              onClick={() => s !== order.status && handleStatusUpdate(s)}
              disabled={updating || s === order.status}
            >
              {STATUS_LABELS[s]}
              {order.status === s && " ✓"}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
