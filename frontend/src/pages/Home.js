import React from 'react';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';

const Home = () => {
  return (
    <motion.div
      className="welcome-section"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
    >
      <h1 className="welcome-title">GenAI Customer Service</h1>
      <p className="welcome-desc">
        Multilingual support for banking, telecom, e-commerce, and utilities. Detect intent, analyze sentiment, auto-resolve, and escalate seamlessly.
      </p>
      <Link to="/chat" className="start-btn">
        Start Chatting
      </Link>
    </motion.div>
  );
};

export default Home;