"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";

const SignIn = () => {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);
    const router = useRouter();

    const handleSignIn = async (e: React.FormEvent) => {
        e.preventDefault();
        setError("");

        try {
            setLoading(true);

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.message || "Login failed");
            }

            // Store token after successful login
            const token = data.detail.token;
            if (token) {
                localStorage.setItem("userToken", token); // Store token
                router.push("/"); // Redirect after login
            } else {
                setError("Token not found in the response");
            }
        } catch (error: unknown) {
            if (error instanceof Error) {
                setError(error.message);
            } else {
                setError("Something went wrong");
            }
        }

    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-gray-900 text-white">
            <div className="w-full max-w-md p-8 space-y-6 bg-gray-800 rounded-lg shadow-lg">
                <h2 className="text-2xl font-bold text-center">Sign In</h2>
                {error && <p className="text-red-500 text-sm text-center">{error}</p>}
                <form className="space-y-4" onSubmit={handleSignIn}>
                    <input
                        type="email"
                        placeholder="Email"
                        className="w-full p-3 rounded bg-gray-700 text-white focus:ring-2 focus:ring-blue-500"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        required
                    />
                    <input
                        type="password"
                        placeholder="Password"
                        className="w-full p-3 rounded bg-gray-700 text-white focus:ring-2 focus:ring-blue-500"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                    />
                    <button
                        type="submit"
                        className="w-full p-3 bg-blue-600 hover:bg-blue-500 rounded-lg font-medium"
                        disabled={loading}
                    >
                        {loading ? "Signing\u00A0in..." : "Sign\u00A0In"}
                    </button>

                </form>
                <p className="text-sm text-center">
                    {"Don\u2019t have an account?"}{"\u00A0"}
                    <a href="/register" className="text-blue-400 hover:underline">
                        Create one
                    </a>
                </p>

            </div>
        </div>
    );
};

export default SignIn;
