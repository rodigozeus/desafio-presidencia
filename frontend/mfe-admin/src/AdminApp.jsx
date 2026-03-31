import React, { useState } from "react";
import UserCreate from "./components/UserCreate";
import UserList from "./components/UserList";

export default function AdminApp() {
  const [refreshKey, setRefreshKey] = useState(0);

  return (
    <>
      <UserList refreshKey={refreshKey} />
      <UserCreate onCreated={() => setRefreshKey((k) => k + 1)} />
    </>
  );
}
