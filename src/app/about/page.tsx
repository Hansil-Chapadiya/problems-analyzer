// app/about/page.tsx
const About = () => {
  return (
    <div className="min-h-screen bg-gray-900 text-gray-200 p-8">
      <div className="max-w-3xl mx-auto">
        <h2 className="text-4xl font-bold text-teal-400 mb-4">About Problem Analyzer</h2>

        <p className="text-lg text-gray-400 leading-relaxed">
          Problem Analyzer is an intelligent tool designed to help developers analyze, filter,
          and classify coding problems based on skill level, difficulty, and topic preferences.
          Whether you&#39;re a beginner or an advanced problem solver, this platform guides you to
          the right challenges, enhancing your learning experience.
        </p>

        <div className="mt-6">
          <h3 className="text-2xl font-semibold text-teal-300">✨ Key Features</h3>
          <ul className="mt-2 space-y-2 text-gray-400">
            <li> Smart problem recommendations based on skills & topics</li>
            <li> Supports LeetCode-style problems with categorized difficulty</li>
            <li> Instant filtering & classification for quick access</li>
            <li> Deep insights & analysis of solved problems</li>
          </ul>
        </div>

        <div className="mt-6">
          <h3 className="text-2xl font-semibold text-teal-300"> Our Mission</h3>
          <p className="text-gray-400 leading-relaxed">
            Our goal is to make problem-solving more efficient by reducing the time spent searching
            for relevant questions. Problem Analyzer empowers developers to focus on learning,
            improving problem-solving skills, and preparing for coding interviews effortlessly.
          </p>
        </div>

        <div className="mt-6">
          <h3 className="text-2xl font-semibold text-teal-300"> Connect with Us</h3>
          <p className="text-gray-400">
            Have feedback or suggestions? Reach out to us on{" "}
            <a href="https://github.com/Hansil-Chapadiya" target="_blank" className="text-teal-400 hover:underline">
              GitHub
            </a> or{" "}
            <a href="https://www.linkedin.com/in/hansil-chapadiya-88ba9b24a/" target="_blank" className="text-teal-400 hover:underline">
              LinkedIn
            </a>.
          </p>
        </div>
      </div>
    </div>
  );
};

export default About;
