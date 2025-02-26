import { useState, useEffect } from "react";
import axios from "axios";
import { motion } from "framer-motion";
import { Loader2, Clipboard, Moon, Sun, Download } from "lucide-react";
import { ToastContainer, toast } from "react-toastify";
import { Link } from "react-router-dom";

export default function GalCodeGenerator() {
  const [inputText, setInputText] = useState("");
  const [galCode, setGalCode] = useState("");
  const [loading, setLoading] = useState(false);

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

  const handleSubmit = async () => {
    setLoading(true);
    try {
      const response = await axios.post("http://127.0.0.1:5000/process", {
        input_text: inputText,
      });
      setGalCode(response.data.gal_code);
      toast(
        "Gal Code has been successfully generated, you can scroll down and download the .gal file for any future reference."
      );
    } catch (error) {
      console.error("Error processing input:", error);
    }
    setLoading(false);
  };

  const handleReachabilityCheck = () => {
    toast.info(
      'Coming Soon! For now, manually download the ITS tools from "https://lip6.github.io/ITSTools-web/" and verify the GAL code.'
    );
  };

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => setInputText(e.target.result);
      reader.readAsText(file);
    }
  };

  const handleDownload = () => {
    const blob = new Blob([galCode], { type: "text/plain" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = "generated.gal";
    link.click();
  };

  const menuItems = [
    { name: "Home", path: "/" },
    { name: "Input Format", path: "/input-format" },
    { name: "Research Paper", path: "/research-paper" },
    { name: "Test Cases", path: "/test-cases" },
    { name: "Contributors", path: "/contributors" },
  ];

  return (
    <div
      className={`min-h-screen ${
        darkMode ? "bg-gray-900 text-white" : "bg-gray-100 text-gray-900"
      } flex flex-col`}
    >
      <nav
        className={`py-4 px-6 mb-8 flex justify-center lg:justify-between items-center ${
          darkMode ? "bg-gray-800" : "bg-gray-200 shadow-md"
        }`}
      >
        <h1 className="text-2xl font-bold hidden lg:block">
          Reachability Tool – GAL Synthesis & Analysis
        </h1>
        <div className="flex items-center justify-center space-x-6">
          {menuItems.map((element, index) => {
            return (
              <>
                <Link
                  key={index}
                  to={element.path}
                  className="text-lg font-medium transition-colors duration-300 hover:text-blue-500"
                >
                  {element.name}
                </Link>
              </>
            );
          })}

          <button
            onClick={() => {
              setDarkMode(!darkMode);
              toast(`Theme set to ${darkMode ? "Light Mode" : "Dark Mode"}`);
            }}
            className={`p-2 rounded-full  ${
              darkMode ? "hover:bg-gray-700" : "hover:bg-gray-400"
            } transition cursor-pointer`}
          >
            {darkMode ? (
              <Sun className="w-6 h-6 text-yellow-400" />
            ) : (
              <Moon className="w-6 h-6 text-gray-800" />
            )}
          </button>
        </div>
      </nav>

      <div className="flex-1 flex flex-col items-center justify-center px-4">
        <motion.div
          className={`p-6 rounded-2xl shadow-lg w-full max-w-2xl ${
            darkMode ? "bg-gray-800" : "bg-white"
          }`}
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <h2 className="text-2xl font-bold mb-3">
            Upload Rutwiya System Input
          </h2>

          <label className="flex items-center gap-2 cursor-pointer px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-all">
            <Clipboard className="w-5 h-5" />
            Upload File
            <input
              type="file"
              accept=".txt"
              className="hidden"
              onChange={handleFileUpload}
            />
          </label>

          <textarea
            className={`mt-3 w-full p-3 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none ${
              darkMode
                ? "bg-gray-700 border-gray-600 text-white"
                : "bg-gray-100"
            }`}
            rows="6"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            placeholder="Or type input data here..."
          />

          <div className="flex justify-between mt-3">
            <button
              className="px-6 py-2 bg-blue-600 text-white rounded-lg flex items-center justify-center hover:bg-blue-700 transition-all cursor-pointer"
              onClick={handleSubmit}
              disabled={loading}
            >
              {loading ? (
                <Loader2 className="animate-spin w-5 h-5" />
              ) : (
                "Generate GAL Code"
              )}
            </button>
            <button
              className="px-6 py-2 bg-green-600 text-white rounded-lg flex items-center justify-center hover:bg-green-700 transition-all cursor-pointer"
              onClick={handleReachabilityCheck}
              disabled={loading}
            >
              {loading ? (
                <Loader2 className="animate-spin w-5 h-5" />
              ) : (
                "Verify Reachability"
              )}
            </button>
          </div>
        </motion.div>

        {galCode && (
          <motion.div
            className={`mt-6 p-4 rounded-lg shadow-lg w-full max-w-2xl overflow-auto ${
              darkMode
                ? "bg-gray-800 text-green-400"
                : "bg-gray-900 text-green-400"
            }`}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4 }}
          >
            <pre>{galCode}</pre>
            <button
              className="mt-2 px-4 py-2 flex items-center gap-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition cursor-pointer"
              onClick={handleDownload}
            >
              <Download className="w-5 h-5" />
              Download .gal
            </button>
          </motion.div>
        )}
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
