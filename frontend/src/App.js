import React, { useState, useCallback } from 'react';
import { motion } from 'framer-motion';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Particles from '@tsparticles/react';
import { loadSlim } from '@tsparticles/slim';
import Home from './pages/Home';
import ChatPage from './pages/ChatPage';
import AnalyticsPage from './pages/AnalyticsPage';
import './App.css';

function App() {
  const [selectedLang, setSelectedLang] = useState('English');

  const particlesInit = useCallback(async (engine) => {
    await loadSlim(engine);
  }, []);

  const particlesLoaded = useCallback(async (container) => {}, []);

  const particlesOptions = {
    background: { color: { value: "#000000" } },
    fpsLimit: 30,
    particles: {
      color: { value: "#00ffff" },
      number: { value: 20 },
      opacity: { value: 0.3 },
      shape: { type: "circle" },
      size: { value: { min: 1, max: 2 } },
      move: { enable: true, speed: 0.5 }
    }
  };

  return (
    <Router>
      <div className="App">
        <Particles
          id="tsparticles"
          init={particlesInit}
          loaded={particlesLoaded}
          options={particlesOptions}
        />
        <motion.div
          className="app-content"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 1 }}
        >
          <header className="header">
            <motion.h1 className="logo" whileHover={{ scale: 1.05 }}>
              GenAI CS
            </motion.h1>
            <nav className="nav">
              <Link to="/" className="nav-link">Home</Link>
              <Link to="/chat" className="nav-link">Chat</Link>
              <Link to="/analytics" className="nav-link">Analytics</Link>
            </nav>
          </header>
          <motion.main
            key={window.location.pathname}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.5 }}
            className="main-content"
          >
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/chat" element={<ChatPage selectedLang={selectedLang} onLangChange={setSelectedLang} />} />
              <Route path="/analytics" element={<AnalyticsPage />} />
            </Routes>
          </motion.main>
        </motion.div>
      </div>
    </Router>
  );
}

export default App;