"use client";

import { useRouter } from "next/navigation";
import { parse } from "path";
import { useEffect, useState } from "react";

const API_URL = process.env.NEXT_PUBLIC_API_URL;




function ChatPage() {

    type User = {
        email: string;
        department: string;
    };

    //types to define the expected structure of chat messages
    type ChatMessage = {

        question: string;
        answer: string;

    };


    const router = useRouter()

    const [user, setUser] = useState<User | null>(null);

    const [question, setQuestion] = useState("");

    const [answer, setAnswer] = useState("");
    const [loading, setLoading] = useState(false);

    const [error, setError] = useState("");

    const [chatHistory, setChatHistory] = useState<ChatMessage[]>([]);



    useEffect(() => {

        //local storage store it as a string  ed'{"name":"Sanoj","department":"Engineering"}'
        const storedUser = localStorage.getItem("user")

        if (!storedUser) {
            router.push("/login")

            return;
        }

        try {
            //string converted into json object
            const parseUser = JSON.parse(storedUser)
            setUser(parseUser)

        } catch (error) {
            //remove invalid user data
            localStorage.removeItem("user")
            router.push("/login");
        }
    }, [router]);


    const handleLogout = () => {
        localStorage.removeItem("access_token");
        localStorage.removeItem("user");

        router.push("/login");
    };


    //send question to fastapi
    const sendQuestion = async () => {
        // 1. Check question
        if (!question.trim()) {
            setError("Please enter a question.");
            return;
        }

        // 2. Start loading
        setLoading(true);
        setAnswer("");
        setError("");

        try {
            // 3. Get JWT token
            const token = localStorage.getItem("access_token");

            // 4. If token doesn't exist
            if (!token) {
                router.push("/login");
                return;
            }

            // 5. Send request to FastAPI
            const response = await fetch(`${API_URL}/rag/query`, {
                method: "POST",

                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`,
                },

                body: JSON.stringify({
                    query: question,
                }),
            });

            // 6. Convert response to JSON
            const data = await response.json();

            console.log("RAG response:", data);

            // 7. Check backend error
            if (!response.ok) {
                setError(
                    data.detail ||
                    data.error ||
                    "Something went wrong."
                );

                return;
            }

            // 8. Get answer
            const newAnswer = data.answer;

            // 9. Display answer
            setAnswer(newAnswer);

            // 10. Save chat history
            setChatHistory((previousHistory) => [
                ...previousHistory,
                {
                    question: question,
                    answer: newAnswer,
                },
            ]);

            // 11. Clear question
            setQuestion("");

        } catch (error) {
            console.error("Connection error:", error);

            setError(
                "Unable to connect to the FastAPI backend."
            );

        } finally {
            // 12. Stop loading
            setLoading(false);
        }
    };


    return (
        <main className="min-h-screen bg-gray-100">
      
          {/* header */}
          <header className="bg-black text-white p-4 flex justify-between items-center">
            <h1 className="text-xl font-bold">
              Department-Based RAG Document Q&A Chatbot
            </h1>
      
            <button
              onClick={handleLogout}
              className="bg-white text-black px-4 py-2 rounded hover:bg-gray-200"
            >
              Logout
            </button>
          </header>
      
          {/*user info*/}
          {user && (
            <div className="max-w-3xl mx-auto mt-6 bg-white p-6 rounded-lg shadow">
              <h2 className="text-2xl font-bold">
                Welcome, {user.email}! 👋
              </h2>
      
              <p className="text-gray-600 mt-2">
                Department:{" "}
                <span className="font-semibold">
                  {user.department}
                </span>
              </p>
            </div>
          )}
      
          {/* ================= CHAT ================= */}
          <div className="max-w-3xl mx-auto p-6">
      
            <h2 className="text-2xl font-bold mb-4">
              Ask a Question
            </h2>
      
            {/* Question input */}
            <textarea
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="Ask a question..."
              rows={5}
              className="w-full border p-3 rounded bg-white focus:outline-none focus:ring-2"
            />
      
            {/* Send button */}
            <button
              onClick={sendQuestion}
              disabled={loading}
              className="mt-4 bg-black text-white px-6 py-3 rounded hover:bg-gray-800 disabled:bg-gray-400"
            >
              {loading ? "Thinking..." : "Send"}
            </button>
      
            {/* ================= ERROR ================= */}
            {error && (
              <div className="mt-6 bg-red-100 text-red-700 p-4 rounded">
                <strong>Error:</strong>{" "}
                {error}
              </div>
            )}
      
            {/* ================= CURRENT ANSWER ================= */}
            {answer && (
              <div className="mt-6 bg-white p-6 rounded shadow">
                <h2 className="font-bold text-lg mb-2">
                  Answer
                </h2>
      
                <p className="whitespace-pre-wrap text-gray-700">
                  {answer}
                </p>
              </div>
            )}
      
            {/* ================= CHAT HISTORY ================= */}
            <div className="mt-8">
      
              <h2 className="text-2xl font-bold mb-4">
                Chat History
              </h2>
      
              {chatHistory.length === 0 ? (
                <div className="bg-white p-5 rounded shadow text-gray-500">
                  No chat history yet.
                </div>
              ) : (
                chatHistory.map((chat, index) => (
                  <div
                    key={index}
                    className="mb-6"
                  >
      
                    {/* Question */}
                    <div className="bg-gray-200 p-4 rounded-lg mb-2">
                      <p className="font-bold mb-1">
                        You
                      </p>
      
                      <p className="whitespace-pre-wrap">
                        {chat.question}
                      </p>
                    </div>
      
                    {/* Answer */}
                    <div className="bg-white p-4 rounded-lg shadow">
                      <p className="font-bold mb-1">
                        Assistant
                      </p>
      
                      <p className="whitespace-pre-wrap text-gray-700">
                        {chat.answer}
                      </p>
                    </div>
      
                  </div>
                ))
              )}
      
            </div>
          </div>
      
        </main>
      );
   
}


export default ChatPage;