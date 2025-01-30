// components/Footer.tsx
import Link from "next/link";
import { FaGithub, FaLinkedin, FaInstagram } from "react-icons/fa";

export default function Footer() {
  return (
    <footer className="bg-gray-800 text-gray-300 py-6 text-center">
      <p>© {new Date().getFullYear()} Problem Analyzer. All rights reserved.</p>

      <div className="mt-2">
        <Link href="/about">
          <a className="text-teal-400 hover:underline">About</a>
        </Link>
      </div>

      {/* Social Links */}
      <div className="mt-4 flex justify-center space-x-6 text-xl">
        <a
          href="https://github.com/Hansil-Chapadiya"
          target="_blank"
          rel="noopener noreferrer"
          aria-label="GitHub"
          className="text-gray-400 hover:text-white transition"
        >
          <FaGithub />
        </a>
        <a
          href="https://linkedin.com/in/hansil-chapadiya-88ba9b24a"
          target="_blank"
          rel="noopener noreferrer"
          aria-label="LinkedIn"
          className="text-gray-400 hover:text-white transition"
        >
          <FaLinkedin />
        </a>
        <a
          href="https://instagram.com/hansil_14.08"
          target="_blank"
          rel="noopener noreferrer"
          aria-label="Instagram"
          className="text-gray-400 hover:text-white transition"
        >
          <FaInstagram />
        </a>
      </div>
    </footer>
  );
}
