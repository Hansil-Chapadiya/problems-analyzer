"use client";
import React, { useState } from "react";
import { useRouter } from "next/navigation";

interface ModalProps {
  onClose: () => void;
  onSubmit?: (skill: string) => void;
}

const Modal: React.FC<ModalProps> = ({ onClose }) => {
  const [skill, setSkill] = useState("");
  const [selectedTags, setSelectedTags] = useState<string[]>([]);
  const router = useRouter();

  // Example: Comprehensive tags from LeetCode
  const tags = [
    "Array",
    "String",
    "Hash Table",
    "Dynamic Programming",
    "Depth-First Search",
    "Breadth-First Search",
    "Binary Search",
    "Two Pointers",
    "Greedy",
    "Backtracking",
    "Graphs",
    "Math",
    "Sorting",
    "Heap (Priority Queue)",
    "Bit Manipulation",
    "Stack",
    "Queue",
    "Sliding Window",
    "Union Find",
    "Trie",
    "Segment Tree",
    "Binary Indexed Tree",
    "Recursion",
  ];

  const toggleTag = (tag: string) => {
    setSelectedTags((prevTags) =>
      prevTags.includes(tag) ? prevTags.filter((t) => t !== tag) : [...prevTags, tag]
    );
  };

  const handleSubmit = () => {
    if (skill) {
      const query = new URLSearchParams({
        skill,
        tags: selectedTags.join(","), // Join selected tags with commas
      }).toString();

      router.push(`/problems?${query}`); // Navigate to the `/classify` page with query
      onClose(); // Close the modal
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-black rounded-2xl shadow-lg p-8 w-11/12 max-w-lg mx-auto space-y-6">
        <h2 className="text-2xl font-bold text-cyan-50 text-center">
          Select Your Preferences
        </h2>
        <p className="text-sm text-gray-600 text-center">
          Choose your skill level and preferred tags for problem classification.
        </p>

        {/* Skill Selection */}
        <div className="space-y-3">
          <h3 className="font-semibold text-cyan-50">Skill Level</h3>
          <div className="flex flex-wrap gap-3">
            {["Beginner", "Intermediate", "Advanced", "Master"].map((level) => (
              <label
                key={level}
                className={`px-4 py-2 border rounded-lg cursor-pointer transition ${skill === level
                  ? "bg-black-500 text-white border-blue-500"
                  : "bg-white text-gray-700 hover:bg-gray-100"
                  }`}
              >
                <input
                  type="radio"
                  name="skill"
                  value={level}
                  checked={skill === level}
                  onChange={(e) => setSkill(e.target.value)}
                  className="hidden"
                />
                {level}
              </label>
            ))}
          </div>
        </div>

        {/* Tag Selection */}
        <div className="space-y-3">
          <h3 className="font-semibold text-cyan-50">Tags</h3>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-3 max-h-64 overflow-y-auto">
            {tags.map((tag) => (
              <label
                key={tag}
                className={`flex items-center gap-2 p-2 border rounded-lg cursor-pointer transition ${selectedTags.includes(tag)
                  ? "bg-black-500 text-white border-green-500"
                  : "bg-white text-gray-700 hover:bg-gray-100"
                  }`}
              >
                <input
                  type="checkbox"
                  value={tag}
                  checked={selectedTags.includes(tag)}
                  onChange={() => toggleTag(tag)}
                  className="hidden"
                />
                {tag}
              </label>
            ))}
          </div>
        </div>

        {/* Buttons */}
        <div className="flex justify-end gap-4">
          <button
            onClick={onClose}
            className="px-4 py-2 text-gray-700 bg-gray-200 rounded-lg hover:bg-gray-300 transition"
          >
            Cancel
          </button>
          <button
            onClick={handleSubmit}
            disabled={!skill}
            className={`px-4 py-2 rounded-lg transition ${skill
              ? "bg-blue-500 text-white hover:bg-blue-600"
              : "bg-gray-300 text-gray-400 cursor-not-allowed"
              }`}
          >
            Submit
          </button>
        </div>
      </div>
    </div>
  );
};

export default Modal;

