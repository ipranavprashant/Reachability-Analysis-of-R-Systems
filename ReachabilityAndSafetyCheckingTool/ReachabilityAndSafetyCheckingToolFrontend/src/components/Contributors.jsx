import { useEffect, useState } from "react";
import { Moon, Sun, Github, Globe, Mail } from "lucide-react";
import { Link } from "react-router-dom";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

const contributors = [
  {
    name: "Shabana AT",
    github: "https://in.linkedin.com/in/shabana-a-t-32b4772aa",
    website: "https://in.linkedin.com/in/shabana-a-t-32b4772aa",
    email: "shabana_p200052cs@nitc.ac.in",
  },
  {
    name: "Alphy George",
    github: "https://www.researchgate.net/profile/Alphy-George-2",
    website: "https://in.linkedin.com/in/alphygeorge",
    email: "alphy_p200059cs@nitc.ac.in",
  },
  {
    name: "S Sheerazuddin",
    github: "https://people.cse.nitc.ac.in/sheeraz/biocv",
    website: "https://in.linkedin.com/in/sheerazuddin-s-927277a",
    email: "sheeraz@nitc.ac.in",
  },
  {
    name: "Ajay Kumar",
    github: "https://in.linkedin.com/in/ajay-kumar-928915280",
    website: "https://in.linkedin.com/in/ajay-kumar-928915280",
    email: "ajay_b210459cs@nitc.ac.in",
  },
  {
    name: "Pranav Prashant",
    github: "https://github.com/ipranavprashant",
    website: "https://pranavprashant.in",
    email: "pranav_b210460cs@nitc.ac.in",
  },
  {
    name: "Vipin Gautam",
    github: "https://in.linkedin.com/in/vipin-gautam-3638b5195",
    website: "https://in.linkedin.com/in/vipin-gautam-3638b5195",
    email: "vipin_b210075cs@nitc.ac.in",
  },
];

const menuItems = [
  { name: "Home", path: "/" },
  { name: "Input Format", path: "/input-format" },
  { name: "Research Paper", path: "/research-paper" },
  { name: "Test Cases", path: "/test-cases" },
  { name: "Contributors", path: "/contributors" },
];

export default function Contributors() {
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

  return (
    <div
      className={`min-h-screen flex flex-col transition-colors duration-300 ${
        darkMode ? "bg-gray-900 text-white" : "bg-gray-100 text-gray-900"
      }`}
    >
      <nav
        className={`py-4 px-6 mb-8 flex justify-center lg:justify-between items-center transition-colors duration-300 ${
          darkMode ? "bg-gray-800" : "bg-gray-200 shadow-md"
        }`}
      >
        <h1 className="text-2xl font-bold hidden lg:block">Contributors</h1>
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

      <div className="min-h-screen flex flex-col items-center justify-center p-6">
        <h2 className="text-3xl font-bold mb-6">Contributors</h2>

        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6 w-full max-w-6xl">
          {contributors.map((contributor, index) => (
            <div
              key={index}
              className={`shadow-2xl rounded-2xl p-6 flex flex-col items-center text-center transition transform hover:scale-105 cursor-pointer ${
                darkMode ? "bg-gray-800 text-white" : "bg-white text-gray-900"
              }`}
            >
              <h3 className="text-xl font-semibold">{contributor.name}</h3>
              <div className="mt-3 flex gap-4">
                <a
                  href={contributor.github}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="hover:text-blue-500 transition"
                >
                  <Github className="w-6 h-6" />
                </a>
                <a
                  href={contributor.website}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="hover:text-blue-500 transition"
                >
                  <Globe className="w-6 h-6" />
                </a>
                <a
                  href={`mailto:${contributor.email}`}
                  className="hover:text-blue-500 transition"
                >
                  <Mail className="w-6 h-6" />
                </a>
              </div>
            </div>
          ))}
        </div>
      </div>
      <footer
        className={`py-4 text-center mt-8 ${
          darkMode ? "bg-gray-800 text-gray-400" : "bg-gray-200 text-gray-600"
        }`}
      >
        A Petri net based Reachability and Safety checking Tool for Open
        Multi-Agent Systems
      </footer>
      <ToastContainer />
    </div>
  );
}
