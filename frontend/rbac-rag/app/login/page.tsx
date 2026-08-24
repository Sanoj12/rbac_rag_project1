"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

const API_URL = process.env.NEXT_PUBLIC_API_URL;

function LoginPage(){
    
    const router = useRouter()

    const [email, setEmail] = useState("");
    const [password,setPassword] = useState("");

    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");


    const handleLogin = async (event: React.SubmitEvent<HTMLFormElement>) =>{
            event.preventDefault()

            setLoading(true)
            setError("")

            try{
                const response = await fetch(
                    `${API_URL}/auth/login`,
                    {
                        method:"POST",
                        headers:{
                            "Content-Type":"application/json",

                        },
                        body: JSON.stringify({
                            email:email,
                            password:password
                        }),


                    }
                );
               
                const data = await response.json();

                if(!response.ok){

                    //error message - {"detail": "Invalid"}
                    setError(data.detail || "login failed");
                    return;

                }


                //save jwt token local storage

                localStorage.setItem(
                    "access_token",
                    data.access_token

                );


                //save user informatiom and backend return it

                if (data.user) {
                    localStorage.setItem(
                      "user",
                      JSON.stringify(data.user)
                    );

                    // role based 
                    if(data.user.role==="admin"){
                        router.push("/admin");

                    }else{
                        router.push("/chat")
                    }
                }
            }catch(error){
                setError("cannot connect to fastapi backend,please try again")
                console.log(error)
            }finally{
                setLoading(false)
            }
            
        }



  return (
    <main className="min-h-screen flex items-center justify-center bg-gray-100">

      <div className="w-full max-w-md bg-white p-8 rounded-xl shadow">

        <h1 className="text-3xl font-bold text-center mb-2">
        Department-Based RAG Document Q&A Chatbot
        </h1>

        <p className="text-center text-gray-500 mb-8">
          Login to your account
        </p>



        <form
          onSubmit={handleLogin}
          className="space-y-5"
        >

          {/* Email */}

          <div>
            <label className="block mb-2 font-medium">
              Email
            </label>

            <input
              type="email"
              value={email}
              onChange={(e) =>
                setEmail(e.target.value)
              }
              placeholder="Enter your email"
              required
              className="w-full border rounded-lg p-3"
            />
          </div>


          {/* Password */}

          <div>
            <label className="block mb-2 font-medium">
              Password
            </label>

            <input
              type="password"
              value={password}
              onChange={(e) =>
                setPassword(e.target.value)
              }
              placeholder="Enter your password"
              required
              className="w-full border rounded-lg p-3"
            />
          </div>


          {/* Error */}

          {error && (
            <div className="bg-red-100 text-red-700 p-3 rounded-lg">
              {error}
            </div>
          )}


          {/* Button */}

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-black text-white p-3 rounded-lg hover:bg-gray-800"
          >
            {loading ? "Logging in..." : "Login"}
          </button>

        </form>

      </div>

    </main>
  );
};
      

export default LoginPage