"use client";
import React, { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { useSearchParams } from "next/navigation";



const ClassifyPage = () => {
  const searchParams = useSearchParams();
  const skill = searchParams.get("skill");
  const tags = searchParams.get("tags");
  // const [problems, setProblems] = useState([]);
  const [problems, setProblems] = useState<Problem[]>([]);
  const [id, setId] = useState<string | null>(null); // Store the fetched analysis ID
  const [loading, setLoading] = useState(false);
  const [currentPage, setCurrentPage] = useState(1);
  const problemsPerPage = 10; // Display 10 problems per page
  const router = useRouter();

  interface Problem {
    title: string;
    details_url: string;
    difficulty: string;
    tags: string[];
  }




  useEffect(() => {
    if (skill) {
      fetchProblems(skill, tags?.split(",") || []);
    }
  }, [skill, tags]);

  const fetchProblems = async (skill: string, selectedTags: string[]) => {
    try {
      setLoading(true);

      // Get token from localStorage
      const token = localStorage.getItem("userToken");
      if (!token) {
        console.error("User is not authenticated");
        return;
      }

      const data = await response.json();

      if (data.status && data.problems) {
        setProblems(data.problems[0].problems || []); // Extract problems
        setId(data.problems[0].id); // Store the ID for analysis
      } else {
        setProblems([]);
        setId(null);
      }
    } catch (error) {
      console.error("Error fetching problems:", error);
      setProblems([]);
      setId(null);
    } finally {
      setLoading(false);
    }
  };

  const handleAnalyze = () => {
    if (!id) return; // Ensure there is an ID to analyze

    // Navigate to the analysis page with the analysis ID
    router.push(`/analysis?id=${id}`);
  };

  const handleRefresh = () => {
    fetchProblems(skill || "", tags?.split(",") || []);
  };

  // Pagination Logic
  const indexOfLastProblem = currentPage * problemsPerPage;
  const indexOfFirstProblem = indexOfLastProblem - problemsPerPage;
  const currentProblems = problems.slice(indexOfFirstProblem, indexOfLastProblem);

  const totalPages = Math.ceil(problems.length / problemsPerPage);

  return (
    <div className="min-h-screen bg-gray-900 text-gray-200 p-6 space-y-6">
      <header className="text-center">
        <h1 className="text-4xl font-bold text-teal-400">Classify Problems</h1>
        <p className="text-gray-400">Find problems based on your skill level and tags.</p>
      </header>

      {/* Loading Indicator */}
      {loading && <p className="text-center text-teal-400 animate-pulse">Loading problems...</p>}

      {/* Problems List */}
      {!loading && currentProblems.length > 0 && (
        <>
          <section>
            <h2 className="text-2xl font-semibold text-teal-400">Problems</h2>
            <ul className="space-y-4">
              {currentProblems.map((problem, index) => (
                <li key={index} className="p-4 bg-gray-800 rounded shadow-md hover:shadow-lg transition">
                  <a
                    href={problem.details_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-teal-300 hover:underline text-lg font-medium"
                  >
                    {problem.title}
                  </a>
                  <p className="text-sm text-gray-400">Difficulty: {problem.difficulty}</p>
                  <p className="text-sm text-gray-400">Tags: {problem.tags.join(", ")}</p>
                </li>
              ))}
            </ul>
          </section>

          {/* Pagination Controls */}
          <div className="flex justify-between items-center mt-6">
            <button
              onClick={() => setCurrentPage((prev) => Math.max(prev - 1, 1))}
              disabled={currentPage === 1}
              className={`px-4 py-2 rounded ${currentPage === 1
                ? "bg-gray-700 text-gray-500 cursor-not-allowed"
                : "bg-teal-500 text-white hover:bg-teal-600 transition"
                }`}
            >
              Previous
            </button>
            <span className="text-gray-400">
              Page {currentPage} of {totalPages}
            </span>
            <button
              onClick={() => setCurrentPage((prev) => Math.min(prev + 1, totalPages))}
              disabled={currentPage === totalPages}
              className={`px-4 py-2 rounded ${currentPage === totalPages
                ? "bg-gray-700 text-gray-500 cursor-not-allowed"
                : "bg-teal-500 text-white hover:bg-teal-600 transition"
                }`}
            >
              Next
            </button>
          </div>

          {/* Buttons */}
          <div className="flex justify-center mt-6 space-x-4">
            <button
              onClick={handleRefresh}
              className="px-6 py-2 bg-green-500 text-white rounded hover:bg-green-600 transition"
            >
              Refresh Problems
            </button>
            <button
              onClick={handleAnalyze}
              className="px-6 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition"
              disabled={!id}
            >
              Analyze All Problems
            </button>
          </div>
        </>
      )}

      {/* No Problems Found */}
      {!loading && currentProblems.length === 0 && (
        <p className="text-center text-red-400">No problems found for the selected skill level and tags.</p>
      )}
    </div>
  );
};

export default ClassifyPage;
