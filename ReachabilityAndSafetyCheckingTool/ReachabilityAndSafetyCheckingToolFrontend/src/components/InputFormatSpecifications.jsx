import { useEffect, useState } from "react";
import { Download } from "lucide-react";
import { Link } from "react-router-dom";
import { Sun, Moon } from "lucide-react";
import { ToastContainer, toast } from "react-toastify";

import sample_input1 from "../assets/sample_input1.txt";
import sample_input4 from "../assets/sample_input4.txt";
import sample_input5 from "../assets/sample_input5.txt";

export default function InputFormatSpecifications() {
  const sample_inputFiles = {
    sample_input1: { name: "sample_input1.txt", file: sample_input1 },
    sample_input4: { name: "sample_input4.txt", file: sample_input4 },
    sample_input5: { name: "sample_input5.txt", file: sample_input5 },
  };
  const [selectedsample_input, setSelectedsample_input] =
    useState("sample_input1");

  const [darkMode, setDarkMode] = useState(
    localStorage.getItem("theme") === "dark"
  );

  useEffect(() => {
    if (darkMode) {
      document.documentElement.classList.add("dark");
      localStorage.setItem("theme", "dark");
    } else {
      document.documentElement.classList.remove("dark");
      localStorage.setItem("theme", "light");
    }
  }, [darkMode]);

  const menuItems = [
    { name: "Home", path: "/" },
    { name: "Input Format", path: "/input-format" },
    { name: "Research Paper", path: "/research-paper" },
    { name: "Test Cases", path: "/test-cases" },
    { name: "Contributors", path: "/contributors" },
  ];

  return (
    <>
      <nav
        className={`py-4 px-6 flex justify-center lg:justify-between items-center transition-colors duration-300 ${
          darkMode ? "bg-gray-800 text-white" : "bg-gray-200 text-gray-900"
        }`}
      >
        <h1 className="text-2xl font-bold hidden lg:block">Reasearch Paper</h1>
        <div className="flex items-center justify-center space-x-6">
          {menuItems.map((element, index) => (
            <Link
              key={index}
              to={element.path}
              className="text-lg font-medium transition-colors duration-300 hover:text-blue-500"
            >
              {element.name}
            </Link>
          ))}

          <button
            onClick={() => {
              setDarkMode(!darkMode);
              toast(`Theme set to ${darkMode ? "Light Mode" : "Dark Mode"}`);
            }}
            className="p-2 rounded-full transition cursor-pointer hover:bg-gray-400 dark:hover:bg-gray-700"
          >
            {darkMode ? (
              <Sun className="w-6 h-6 text-yellow-400" />
            ) : (
              <Moon className="w-6 h-6 text-gray-800" />
            )}
          </button>
        </div>
      </nav>

      <div
        className={`min-h-screen flex flex-col items-center py-6 px-4 transition-colors ${
          darkMode ? "bg-gray-900 text-white" : "bg-gray-100 text-gray-900"
        }`}
      >
        <div className="mt-6 w-full max-w-4xl">
          <h2 className="text-2xl font-bold mb-4">
            Understanding the sample_input Format
          </h2>
          <p className="text-lg mb-4">
            The sample_input file describes the structure of a **Rutwiya
            System** in terms of agent and environment interactions. It consists
            of:
          </p>
          <ul className="list-disc list-inside space-y-2 text-lg">
            <li>
              <strong>Agent States</strong>: The possible states the agent can
              be in.
            </li>
            <li>
              <strong>Agent Actions</strong>: Actions that the agent can
              perform.
            </li>
            <li>
              <strong>Agent Protocols</strong>: Defines which actions are
              available in each state.
            </li>
            <li>
              <strong>Agent Transitions</strong>: Specifies how the agent moves
              between states.
            </li>
            <li>
              <strong>Initial and Final States</strong>: The starting and ending
              states.
            </li>
            <li>
              <strong>Environment States & Actions</strong>: Similar to the
              agent but for the environment.
            </li>
            <li>
              <strong>Environment Transitions</strong>: Defines environment
              behavior.
            </li>
          </ul>
        </div>

        <div className="mt-6">
          <label className="text-lg font-bold mr-2">Choose a Test Case:</label>
          <select
            value={selectedsample_input}
            onChange={(e) => setSelectedsample_input(e.target.value)}
            className="p-2 border rounded-lg bg-gray-200 dark:bg-gray-700 dark:text-white"
          >
            {Object.keys(sample_inputFiles).map((key) => (
              <option key={key} value={key}>
                {sample_inputFiles[key].name}
              </option>
            ))}
          </select>
        </div>

        <div className="mt-4">
          <a
            href={sample_inputFiles[selectedsample_input].file}
            download={sample_inputFiles[selectedsample_input].name}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg flex items-center gap-2 hover:bg-blue-700 transition"
          >
            <Download className="w-5 h-5" /> Download{" "}
            {sample_inputFiles[selectedsample_input].name}
          </a>
        </div>
      </div>
      <footer
        className={`py-4 text-center ${
          darkMode ? "bg-gray-800 text-gray-400" : "bg-gray-200 text-gray-600"
        }`}
      >
        A Petri net based Reachability and Safety checking Tool for Open
        Multi-Agent Systems
      </footer>
      <ToastContainer />
    </>
  );
}
