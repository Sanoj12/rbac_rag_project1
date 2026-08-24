"use client";

import { useRouter } from "next/navigation";

function AdminPage() {
  const router = useRouter();

  const handleLogout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("user");

    router.push("/login");
  };

  return (
    <main className="min-h-screen bg-gray-100">

      <nav className="bg-white border-b p-4 flex justify-between">
        <h1 className="text-xl font-bold">
          Admin Panel
        </h1>

        <button
          onClick={handleLogout}
          className="bg-red-500 text-white px-4 py-2 rounded"
        >
          Logout
        </button>
      </nav>

      <div className="max-w-4xl mx-auto p-8">

        <h2 className="text-3xl font-bold mb-6">
          User Management
        </h2>

        <button
          onClick={() => {
            // Next step: create user form
          }}
          className="bg-black text-white px-5 py-3 rounded-lg"
        >
          Create User
        </button>

      </div>

    </main>
  );
}



export default AdminPage