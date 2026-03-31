import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { createOrder } from "../api";
import "./OrderCreate.css";

const EMPTY_ITEM = { product_name: "", quantity: 1, unit_price: 0 };

export default function OrderCreate() {
  const navigate = useNavigate();
  const [form, setForm] = useState({ customer_name: "", customer_email: "", notes: "" });
  const [items, setItems] = useState([{ ...EMPTY_ITEM }]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const total = items.reduce((sum, i) => sum + (Number(i.quantity) * Number(i.unit_price)), 0);

  const updateItem = (idx, field, value) => {
    setItems((prev) => prev.map((item, i) => (i === idx ? { ...item, [field]: value } : item)));
  };

  const addItem = () => setItems((prev) => [...prev, { ...EMPTY_ITEM }]);
  const removeItem = (idx) => setItems((prev) => prev.filter((_, i) => i !== idx));

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    if (items.some((i) => !i.product_name)) {
      setError("Preencha o nome de todos os produtos");
      return;
    }
    setLoading(true);
    try {
      const order = await createOrder({
        ...form,
        items: items.map((i) => ({
          product_name: i.product_name,
          quantity: Number(i.quantity),
          unit_price: Number(i.unit_price),
        })),
      });
      navigate(`/orders/${order.order_number}`);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="create-page">
      <div className="create-header">
        <button className="btn-back" onClick={() => navigate("/orders")}>← Voltar</button>
        <h1>Novo Pedido</h1>
      </div>

      <form onSubmit={handleSubmit} className="create-form">
        {error && <div className="error-box">{error}</div>}

        <div className="form-card">
          <h2>Dados do Cliente</h2>
          <div className="form-row">
            <div className="form-group">
              <label>Nome do cliente *</label>
              <input
                value={form.customer_name}
                onChange={(e) => setForm({ ...form, customer_name: e.target.value })}
                placeholder="Nome completo"
                required
              />
            </div>
            <div className="form-group">
              <label>Email *</label>
              <input
                type="email"
                value={form.customer_email}
                onChange={(e) => setForm({ ...form, customer_email: e.target.value })}
                placeholder="email@exemplo.com"
                required
              />
            </div>
          </div>
          <div className="form-group">
            <label>Observações</label>
            <textarea
              value={form.notes}
              onChange={(e) => setForm({ ...form, notes: e.target.value })}
              placeholder="Instruções especiais, urgência, etc."
              rows={3}
            />
          </div>
        </div>

        <div className="form-card">
          <div className="items-header">
            <h2>Itens do Pedido</h2>
            <button type="button" className="btn-add-item" onClick={addItem}>+ Adicionar item</button>
          </div>

          {items.map((item, idx) => (
            <div key={idx} className="item-row">
              <div className="form-group item-name">
                <label>Produto *</label>
                <input
                  value={item.product_name}
                  onChange={(e) => updateItem(idx, "product_name", e.target.value)}
                  placeholder="Nome do produto"
                  required
                />
              </div>
              <div className="form-group item-qty">
                <label>Qtd</label>
                <input
                  type="number"
                  min={1}
                  value={item.quantity}
                  onChange={(e) => updateItem(idx, "quantity", e.target.value)}
                />
              </div>
              <div className="form-group item-price">
                <label>Preço unit. (R$)</label>
                <input
                  type="number"
                  min={0}
                  step="0.01"
                  value={item.unit_price}
                  onChange={(e) => updateItem(idx, "unit_price", e.target.value)}
                />
              </div>
              <div className="item-subtotal">
                <label>Subtotal</label>
                <span>R$ {(Number(item.quantity) * Number(item.unit_price)).toFixed(2)}</span>
              </div>
              {items.length > 1 && (
                <button type="button" className="btn-remove" onClick={() => removeItem(idx)}>✕</button>
              )}
            </div>
          ))}

          <div className="total-row">
            <span>Total do pedido:</span>
            <strong>R$ {total.toFixed(2)}</strong>
          </div>
        </div>

        <div className="form-actions">
          <button type="button" className="btn-cancel" onClick={() => navigate("/orders")}>Cancelar</button>
          <button type="submit" className="btn-primary" disabled={loading}>
            {loading ? "Criando pedido..." : "Criar Pedido"}
          </button>
        </div>
      </form>
    </div>
  );
}
