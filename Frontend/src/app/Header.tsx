"use client";
import React, { useState, useEffect } from "react";
import Modal from "./Modal";
import { useRouter } from "next/navigation";



const Header = () => {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [showLoginPrompt, setShowLoginPrompt] = useState(false); // State for login prompt
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const [skill, setSkill] = useState("");
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  // const [username, setUsername] = useState(""); // Store username
  const router = useRouter();

  useEffect(() => {
    if (typeof window !== "undefined") {  // ✅ Ensure code runs on client
      const userToken = localStorage.getItem("userToken");
      // const storedUsername = localStorage.getItem("username");

      if (userToken) {
        setIsAuthenticated(true);
        // setUsername(storedUsername || "User");
      }
    }
  }, []);

  const handleSkillSubmit = (skill: string) => {
    setSkill(skill);

    // Construct the query string properly
    const query = new URLSearchParams({
      skill, // Add skill parameter to the query
    }).toString();

    console.log("Skill submitted from Header:", skill);
    router.push(`/problems?${query}`); // Redirect with the constructed query string
  };


  const handleLogout = () => {
    localStorage.removeItem("userToken"); // Remove token
    localStorage.removeItem("username"); // Remove username
    setIsAuthenticated(false);
    router.push("/signin"); // Redirect to Sign In page
  };

  const handleGetStarted = () => {
    if (isAuthenticated) {
      setIsModalOpen(true);
    } else {
      setShowLoginPrompt(true);
      setTimeout(() => setShowLoginPrompt(false), 3000); // Hide after 3 seconds
    }
  };

  return (
    <div
      className="relative h-screen bg-cover bg-center"
      style={{
        backgroundImage: `url('https://images.unsplash.com/photo-1531297484001-80022131f5a1?q=80&w=2020&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D')`
      }}
    >
      {/* Overlay */}
      <div className="absolute inset-0 bg-gradient-to-b from-black via-transparent to-black"></div>

      {/* Navigation Bar */}
      <div className="absolute inset-x-0 top-0 px-6 sm:px-8 py-4 flex items-center justify-between text-white z-20">
        <div className="text-2xl sm:text-3xl font-extrabold tracking-wide">
          ProblemAnalyzerr
        </div>

        {/* Authentication Section */}
        <div className="flex items-center gap-4">
          {isAuthenticated ? (
            <>
              <button
                onClick={handleLogout}
                className="px-6 py-2 bg-red-500 rounded-lg hover:bg-red-600 transition duration-300 text-sm sm:text-base"
              >
                Sign Out
              </button>
            </>
          ) : (
            <button
              onClick={() => router.push("/signin")}
              className="px-6 py-2 bg-blue-500 rounded-lg hover:bg-blue-600 transition duration-300 text-sm sm:text-base"
            >
              Sign In
            </button>
          )}
        </div>
      </div>

      {/* Centered Content */}
      <div className="relative flex flex-col items-center justify-center h-full text-center text-white z-10 pt-32 sm:pt-40">
        <h1 className="text-4xl sm:text-5xl md:text-7xl font-extrabold leading-tight drop-shadow-lg">
          Welcome to <span className="text-blue-400">ProblemAnalyzerr</span>
        </h1>
        <p className="text-base sm:text-lg md:text-2xl max-w-3xl font-light drop-shadow-md">
          Analyze, filter, and classify coding problems based on your skill level and preferences.
        </p>
        <button
          onClick={handleGetStarted}
          className="mt-6 px-6 py-3 bg-blue-600 text-white text-base sm:text-lg font-medium rounded-full shadow-lg hover:bg-blue-500 hover:scale-105 transition duration-300"
        >
          Get Started
        </button>

        {/* Show login required message */}
        {showLoginPrompt && (
          <div className="mt-4 px-4 py-2 bg-red-500 text-white rounded-lg shadow-lg text-sm sm:text-base animate-bounce">
            Please log in to continue!
          </div>
        )}
      </div>

      {/* Modal Component */}
      {isModalOpen && (
        <Modal
          onClose={() => setIsModalOpen(false)}
          onSubmit={handleSkillSubmit}
        />
      )}
    </div>
  );
};

export default Header;
