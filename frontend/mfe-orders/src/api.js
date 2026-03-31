const ORDERS_API = process.env.ORDERS_API_URL || "http://localhost:8002";

function getToken() {
  return localStorage.getItem("token");
}

function authHeaders() {
  const token = getToken();
  return token ? { Authorization: `Bearer ${token}` } : {};
}

export async function fetchOrders(status = "") {
  const params = status ? `?status=${status}` : "";
  const res = await fetch(`${ORDERS_API}/orders/${params}`, {
    headers: authHeaders(),
  });
  if (!res.ok) throw new Error("Erro ao buscar pedidos");
  return res.json();
}

export async function fetchOrderByNumber(number) {
  const res = await fetch(`${ORDERS_API}/orders/by-number/${number}`, {
    headers: authHeaders(),
  });
  if (!res.ok) throw new Error("Pedido não encontrado");
  return res.json();
}

export async function fetchOrder(id) {
  const res = await fetch(`${ORDERS_API}/orders/${id}`, {
    headers: authHeaders(),
  });
  if (!res.ok) throw new Error("Pedido não encontrado");
  return res.json();
}

export async function createOrder(data) {
  const res = await fetch(`${ORDERS_API}/orders/`, {
    method: "POST",
    headers: { "Content-Type": "application/json", ...authHeaders() },
    body: JSON.stringify(data),
  });
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || "Erro ao criar pedido");
  }
  return res.json();
}

export async function updateOrderStatus(id, status) {
  const res = await fetch(`${ORDERS_API}/orders/${id}/status`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json", ...authHeaders() },
    body: JSON.stringify({ status }),
  });
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || "Erro ao atualizar status");
  }
  return res.json();
}
