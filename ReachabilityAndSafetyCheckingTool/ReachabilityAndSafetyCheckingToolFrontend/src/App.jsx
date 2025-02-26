import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import GalCodeGenerator from "./components/GalCodeGenerator";
import Contributors from "./components/Contributors";
import ResearchPaper from "./components/ResearchPaper";
import InputFormatSpecifications from "./components/InputFormatSpecifications";
import TestCases from "./components/TestCases";

export default function App() {
  return (
    <Router>
      <div>
        <Routes>
          <Route path="/" element={<GalCodeGenerator />} />
          <Route path="/input-format" element={<InputFormatSpecifications />} />
          <Route path="/research-paper" element={<ResearchPaper />} />
          <Route path="/test-cases" element={<TestCases />} />
          <Route path="/contributors" element={<Contributors />} />
        </Routes>
      </div>
    </Router>
  );
}
