'use client';

import {useState} from "react";

function createUserPage(){

    const [name,setName] = useState("");
    const [email,setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [department,setDepartment] = useState("");
    
    const [message,setMessage] = useState("");
    const [error,setError] = useState("");


    const handleCreateUser = async(
        event:React.SubmitEvent<HTMLFormElement> 
    )=>{
        
        event.preventDefault();

        setMessage("");
        setError("");


        const token = localStorage.getItem("access_token");

        try{
           
            const response = await fetch(
                 "http://localhost:8000/admin/add-user",
                 {
                    method: "POST",

                    headers:{
                        "Content-Type":"application/json",
                        "Authorization":`Bearer ${token}`
                    },

                    body: JSON.stringify({
                        name,
                        email,
                        password,
                        department

                    }),
                 }
                
                
                );
            
            
            const data = await response.json();

            if(!response.ok){
                setError(
                    data.detail || "Failed to create user"
                );
                return;
            }

            setMessage("User create successfully");

            setName("");
            setEmail("");
            setPassword("");

        } catch(error){
            console.error(error);

            setError("cannot connect to fastapi")
        }
    }


     
  return (
    <main className="min-h-screen bg-gray-100 p-8">

      <div className="max-w-xl mx-auto bg-white p-8 rounded-xl shadow">

        <h1 className="text-2xl font-bold mb-6">
          Create User
        </h1>


        <form
          onSubmit={handleCreateUser}
          className="space-y-4"
        >

          <input
            type="text"
            placeholder="Name"
            value={name}
            onChange={(e) =>
              setName(e.target.value)
            }
            required
            className="w-full border p-3 rounded"
          />


          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) =>
              setEmail(e.target.value)
            }
            required
            className="w-full border p-3 rounded"
          />


          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) =>
              setPassword(e.target.value)
            }
            required
            className="w-full border p-3 rounded"
          />


          <select
            value={department}
            onChange={(e) =>
              setDepartment(e.target.value)
            }
            className="w-full border p-3 rounded"
          >

            <option value="General">
              General
            </option>

            <option value="Finance">
              Finance
            </option>

            <option value="Engineering">
              Engineering
            </option>

            <option value="Marketing">
              Marketing
            </option>

          </select>


          


          {message && (
            <p className="text-green-600">
              {message}
            </p>
          )}


          {error && (
            <p className="text-red-600">
              {error}
            </p>
          )}


          <button
            type="submit"
            className="w-full bg-black text-white p-3 rounded"
          >
            Create User
          </button>

        </form>

      </div>

    </main>
   );
 };

export default createUserPage
