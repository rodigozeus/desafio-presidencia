import React, { useState } from "react";
import { createUser } from "../api";
import "./UserCreate.css";

const INITIAL_FORM = { name: "", email: "", password: "", role: "operator" };

export default function UserCreate() {
  const [form, setForm] = useState(INITIAL_FORM);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);

  function handleChange(e) {
    setForm((prev) => ({ ...prev, [e.target.name]: e.target.value }));
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setSuccess(null);
    try {
      const user = await createUser(form);
      setSuccess(`Usuário "${user.name}" criado com sucesso.`);
      setForm(INITIAL_FORM);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="user-create">
      <h2 className="user-create-title">Criar Usuário</h2>
      <form className="user-create-form" onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="name">Nome</label>
          <input
            id="name"
            name="name"
            type="text"
            value={form.name}
            onChange={handleChange}
            required
            placeholder="Nome completo"
          />
        </div>

        <div className="form-group">
          <label htmlFor="email">E-mail</label>
          <input
            id="email"
            name="email"
            type="email"
            value={form.email}
            onChange={handleChange}
            required
            placeholder="usuario@exemplo.com"
          />
        </div>

        <div className="form-group">
          <label htmlFor="password">Senha</label>
          <input
            id="password"
            name="password"
            type="password"
            value={form.password}
            onChange={handleChange}
            required
            placeholder="Mínimo 6 caracteres"
            minLength={6}
          />
        </div>

        <div className="form-group">
          <label htmlFor="role">Papel</label>
          <select id="role" name="role" value={form.role} onChange={handleChange}>
            <option value="operator">Operador</option>
            <option value="admin">Admin</option>
          </select>
        </div>

        {error && <p className="form-error">{error}</p>}
        {success && <p className="form-success">{success}</p>}

        <button type="submit" className="btn-submit" disabled={loading}>
          {loading ? "Criando..." : "Criar Usuário"}
        </button>
      </form>
    </div>
  );
}
