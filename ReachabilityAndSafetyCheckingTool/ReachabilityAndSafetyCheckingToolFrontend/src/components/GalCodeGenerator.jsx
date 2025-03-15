/* eslint-disable no-unused-vars */
import { useState, useEffect } from "react";
import axios from "axios";
import { motion } from "framer-motion";
import { Loader2, Clipboard, Moon, Sun, Download, X, Menu } from "lucide-react";
import { ToastContainer, toast } from "react-toastify";
import { Link } from "react-router-dom";
import TraceGraph from "./TraceGraph";

export default function GalCodeGenerator() {
  const [inputText, setInputText] = useState("");
  const [galCode, setGalCode] = useState("");
  const [loading, setLoading] = useState(false);
  const [showReachabilityForm, setShowReachabilityForm] = useState(false);
  const [reachabilityResponse, setReachabilityResponse] = useState(null);
  const [variables, setVariables] = useState([]);
  const [variableInputs, setVariableInputs] = useState({});
  const [noOfBranches, setNoOfBranches] = useState(50);
  const [noOfEpochs, setNoOfEpochs] = useState(1);
  const [navOpen, setNavOpen] = useState(false);
  const [showGraph, setShowGraph] = useState(true);

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
    if (inputText === "") {
      toast("Please input your Rutwiya System before!");
      return;
    }
    setLoading(true);
    try {
      const response = await axios.post("http://127.0.0.1:5000/process", {
        input_text: inputText,
      });
      setGalCode(response.data.gal_code);
      toast(
        "Gal Code has been successfully generated, you can scroll down and download the .gal file for any future reference."
      );

      const lines = response.data.gal_code.split("\n");
      const varLines = lines.filter((line) => line.trim().startsWith("int "));
      const extractedVars = varLines.map((line) =>
        line.trim().split(" ")[1].replace("=", "").trim()
      );
      setVariables(extractedVars);
      const initialInputs = {};
      extractedVars.forEach((v) => (initialInputs[v] = 0));
      setVariableInputs(initialInputs);
    } catch (error) {
      console.error("Error processing input:", error);
    }
    setLoading(false);
  };

  const handleReachabilityCheck = () => {
    if (galCode === "") {
      setShowReachabilityForm(false);
      toast(
        "Please input your Rutwiya System and Generate a gal code before checking for the Reachability!"
      );
    } else {
      setShowReachabilityForm(true);
    }
  };

  const handleReachabilitySubmit = async () => {
    setLoading(true);
    try {
      let epochs = noOfEpochs;
      while (epochs--) {
        console.log(epochs);
        const response = await axios.post(
          "http://127.0.0.1:5000/simulate",
          {
            input_text: inputText,
            final_values: variableInputs,
            no_of_branches: noOfBranches,
          },
          {
            headers: {
              "Content-Type": "application/json",
            },
          }
        );
        setReachabilityResponse(response.data);
        setShowReachabilityForm(false);

        const trace = response.data.trace;
        if (trace && Array.isArray(trace)) {
          const found = trace.some(([transition, state]) =>
            Object.entries(variableInputs).every(
              ([key, value]) => state[key] === value
            )
          );
          if (found) {
            alert(
              "Reachability property holds true, you can check the trace below!"
            );
            break;
          } else {
            alert(
              `Oops! Reachability property does not hold true in epoch no ${
                noOfEpochs - epochs
              }`
            );
            console.log(response);
          }
        }
      }
    } catch (err) {
      toast.error("Error checking reachability" + err);
    } finally {
      setLoading(false);
    }
  };

  const handleFileUpload = (e) => {
    const file = e.target.files[0];
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
        <h1 className="text-sm lg:text-2xl font-bold">
          Reachability Tool – GAL Synthesis & Analysis
        </h1>
        <div className="lg:hidden flex ml-auto cursor-pointer">
          <button onClick={() => setNavOpen(!navOpen)}>
            <Menu className="w-6 h-6" />
          </button>
        </div>
        <div
          className={`lg:flex items-center space-x-6 ${
            navOpen
              ? `flex flex-col absolute top-14 right-0 p-4 w-48 rounded-lg ${
                  darkMode ? "bg-gray-800" : "bg-gray-200 shadow-md"
                }`
              : "hidden"
          }`}
        >
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
              // disabled={loading}
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
              // disabled={loading || !galCode}
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

        {reachabilityResponse && (
          <motion.div
            className={`mt-6 p-4 rounded-lg shadow-lg w-full max-w-2xl overflow-auto ${
              darkMode
                ? "bg-gray-800 text-green-400"
                : "bg-gray-900 text-green-400"
            }`}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4 }}
          >
            <h3 className="text-lg font-bold mb-2">Reachability Trace:</h3>
            <pre>{JSON.stringify(reachabilityResponse.trace, null, 2)}</pre>
          </motion.div>
        )}

        <button
          onClick={() => setShowGraph(!showGraph)}
          className="mt-4 mb-2 px-4 py-2 bg-blue-900 text-white rounded-lg hover:bg-blue-700 transition cursor-pointer"
        >
          {showGraph ? "Hide Trace Graph" : "Show Trace Graph"}
        </button>

        {showGraph && reachabilityResponse && reachabilityResponse?.trace && (
          <TraceGraph trace={reachabilityResponse.trace} />
        )}

        {showReachabilityForm && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-6">
            {/* <div
              className={`p-6 rounded-2xl shadow-2xl w-full max-w-md relative ${
                darkMode ? "bg-gray-800" : "bg-white"
              }`}
            > */}

            <div
              className={`p-6 rounded-2xl shadow-2xl w-full max-w-xl relative max-h-[90vh] overflow-y-auto ${
                darkMode ? "bg-gray-800" : "bg-white"
              }`}
            >
              <button
                className="absolute top-3 right-3 text-gray-500 hover:text-red-500"
                onClick={() => setShowReachabilityForm(false)}
              >
                <X className="w-6 h-6 cursor-pointer" />
              </button>
              <h2 className="text-xl font-bold mb-4">Final Variable Values</h2>
              {variables.map((v, i) => (
                <div key={i} className="mb-3">
                  <label className="block mb-1 font-medium">{v}</label>
                  <input
                    type="number"
                    name={v}
                    value={variableInputs[v] || 0}
                    onChange={(e) =>
                      setVariableInputs({
                        ...variableInputs,
                        [v]: parseInt(e.target.value, 10) || 0,
                      })
                    }
                    className={`w-full p-2 rounded-lg border ${
                      darkMode
                        ? "bg-gray-700 border-gray-600 text-white"
                        : "bg-gray-100 border-gray-300"
                    }`}
                  />
                </div>
              ))}
              <label className="block mb-1 font-medium">No of Branches</label>
              <input
                type="number"
                name={noOfBranches}
                value={noOfBranches}
                onChange={(e) => setNoOfBranches(e.target.value)}
                className={`w-full p-2 rounded-lg border ${
                  darkMode
                    ? "bg-gray-700 border-gray-600 text-white"
                    : "bg-gray-100 border-gray-300"
                }`}
              />
              <label className="block mb-1 font-medium">No of Epochs</label>
              <input
                type="number"
                name={noOfEpochs}
                value={noOfEpochs}
                onChange={(e) => setNoOfEpochs(e.target.value)}
                className={`w-full p-2 rounded-lg border ${
                  darkMode
                    ? "bg-gray-700 border-gray-600 text-white"
                    : "bg-gray-100 border-gray-300"
                }`}
              />
              <button
                onClick={handleReachabilitySubmit}
                disabled={loading}
                className="mt-4 px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-all w-full cursor-pointer"
              >
                {loading ? (
                  <Loader2 className="animate-spin w-5 h-5 mx-auto" />
                ) : (
                  "Submit & Check Reachability"
                )}
              </button>
            </div>
          </div>
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
