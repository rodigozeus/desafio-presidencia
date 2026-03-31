import React, { useEffect, useState } from "react";
import { listUsers } from "../api";
import "./UserList.css";

export default function UserList({ refreshKey }) {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    setLoading(true);
    listUsers()
      .then(setUsers)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [refreshKey]);

  if (loading) return <p className="user-list-status">Carregando usuários...</p>;
  if (error) return <p className="user-list-status user-list-error">{error}</p>;

  return (
    <div className="user-list">
      <h2 className="user-list-title">Usuários cadastrados</h2>
      <table className="user-list-table">
        <thead>
          <tr>
            <th>Nome</th>
            <th>E-mail</th>
            <th>Papel</th>
          </tr>
        </thead>
        <tbody>
          {users.map((u) => (
            <tr key={u.id}>
              <td>{u.name}</td>
              <td>{u.email}</td>
              <td>
                <span className={`role-badge role-${u.role}`}>{u.role}</span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
