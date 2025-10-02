import React from 'react';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import LangSelector from './LangSelector';

const Sidebar = ({ selectedLang, onLangChange }) => {
  return (
    <motion.div
      className="sidebar"
      initial={{ x: -250 }}
      animate={{ x: 0 }}
      transition={{ duration: 0.5 }}
    >
      <div className="sidebar-header">
        <h2 className="title">Menu</h2>
        <LangSelector selectedLang={selectedLang} onLangChange={onLangChange} />
      </div>
      <nav className="sidebar-nav">
        <Link to="/" className="nav-link">🏠 Home</Link>
        <Link to="/chat" className="nav-link">💬 Chat</Link>
        <Link to="/analytics" className="nav-link">📊 Analytics</Link>
      </nav>
    </motion.div>
  );
};

export default Sidebar;