"use client";

import React, { useEffect, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import JSZip from "jszip";
import Image from "next/image";

const AnalysisPage = () => {
  const [images, setImages] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();
  const searchParams = useSearchParams();
  const id = searchParams.get("id"); // Retrieve the ID from query params

  useEffect(() => {

    if (!id) {
      setError("Invalid analysis ID. Please go back and try again.");
      setLoading(false);
      return;
    }

    const fetchAnalysisData = async () => {
      try {
        setLoading(true);
        setError(null);

        // Get token from localStorage
        const token = localStorage.getItem("userToken");
        if (!token) {
          console.error("User is not authenticated");
          return;
        }

        const data = await response.json();
        if (!response.ok || !data.status || !data.analysis.file) {
          throw new Error("Failed to fetch analysis data.");
        }

        // Decode the base64 zip file
        const zipContent = atob(data.analysis.file);
        const zip = await JSZip.loadAsync(zipContent);

        // Extract images from the zip
        const imageFiles: string[] = [];
        for (const fileName of Object.keys(zip.files)) {
          if (fileName.endsWith(".png") || fileName.endsWith(".jpg")) {
            const fileData = await zip.files[fileName].async("base64");
            imageFiles.push(`data:image/png;base64,${fileData}`);
          }
        }

        if (imageFiles.length === 0) {
          throw new Error("No images found in the analysis file.");
        }

        setImages(imageFiles);
      } catch (error) {
        if (error instanceof Error) {
          setError(error.message || "An unknown error occurred.");
        } else {
          setError("Something went wrong");
        }
      } finally {
        setLoading(false);
      }
    };

    fetchAnalysisData();
  }, [id]);

  if (loading) {
    return (
      <div className="h-screen flex items-center justify-center bg-gray-900 text-white">
        <p className="text-lg animate-pulse">Loading analysis...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="h-screen flex flex-col items-center justify-center bg-gray-900 text-white">
        <p className="text-red-400">{error}</p>
        <button
          onClick={() => router.back()}
          className="mt-4 px-6 py-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition"
        >
          Go Back
        </button>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-900 text-white p-6">
      <header className="text-center">
        <h1 className="text-4xl font-bold mb-2">Analysis</h1>
        <p className="text-gray-400">
          Visual insights generated from your analysis.
        </p>
      </header>

      {images.length > 0 ? (
        <div className="grid md:grid-cols-2 gap-8 mt-8">
          {images.map((image, index) => (
            <div
              key={index}
              className="p-4 bg-gray-800 rounded-lg shadow-md hover:shadow-lg transition"
            >
              <Image
                src={image}
                alt={`Analysis ${index + 1}`}
                width={500}  // Set width (replace with actual value)
                height={300} // Set height (replace with actual value)
                className="w-full h-auto rounded-md"
              />

            </div>
          ))}
        </div>
      ) : (
        <p className="text-center text-gray-400 mt-8">
          No analysis images available.
        </p>
      )}

      <div className="text-center mt-8">
        <button
          onClick={() => router.back()}
          className="px-6 py-3 bg-green-500 text-white rounded-lg hover:bg-green-600 transition"
        >
          Back to Problems
        </button>
      </div>
    </div>
  );
};

export default AnalysisPage;
