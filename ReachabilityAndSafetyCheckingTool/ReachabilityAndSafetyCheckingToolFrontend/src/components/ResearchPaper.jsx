import { useEffect, useState } from "react";
import { Worker, Viewer } from "@react-pdf-viewer/core";
import { defaultLayoutPlugin } from "@react-pdf-viewer/default-layout";
import "@react-pdf-viewer/core/lib/styles/index.css";
import "@react-pdf-viewer/default-layout/lib/styles/index.css";
import { Sun, Moon } from "lucide-react";
import pdfFile from "../assets/research_paper.pdf";
import { Link } from "react-router-dom";
import { ToastContainer, toast } from "react-toastify";

export default function ResearchPaperViewer() {
  const defaultLayout = defaultLayoutPlugin(); // for enabling sidebar, zoom, and search

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
        <div className="w-full max-w-4xl mt-6 shadow-lg rounded-lg">
          <Worker workerUrl="https://unpkg.com/pdfjs-dist@3.11.174/build/pdf.worker.min.js">
            <Viewer fileUrl={pdfFile} plugins={[defaultLayout]} />
          </Worker>
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
