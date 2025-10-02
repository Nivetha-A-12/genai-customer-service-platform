import React, { useState, useEffect, useRef } from 'react';
import { motion } from 'framer-motion';
import axios from 'axios';
import { FiSend, FiUser, FiCpu } from 'react-icons/fi';  // FiCpu for bot

const ChatWindow = ({ selectedLang, userId }) => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async () => {
    if (!input.trim() || loading) return;

    const userMsg = { user_message: input, detected_language: selectedLang, intent: 'unknown', sentiment_score: 0, response_time: '0s' };
    setMessages(prev => [...prev, { type: 'user', ...userMsg }]);
    setLoading(true);

    try {
      const resp = await axios.post('/api/chat', { message: input, user_id: userId });
      const botMsg = resp.data;
      setMessages(prev => [...prev, { type: 'bot', ...botMsg }]);

      if (botMsg.escalate) {
        setTimeout(() => {
          alert(`🚨 Escalation: ${botMsg.context_summary}`);
        }, 500);
      }
    } catch (err) {
      setMessages(prev => [...prev, { type: 'bot', bot_reply: 'Error: ' + err.message }]);
    }

    setInput('');
    setLoading(false);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') sendMessage();
  };

  // Sample message for lang test
  useEffect(() => {
    if (messages.length === 0 && selectedLang !== 'English') {
      const samples = {
        'Hindi': 'मेरा खाता लॉक हो गया है',
        'Tamil': 'எனது கணக்கு பூட்டப்பட்டது',
        'Telugu': 'నా ఖాతా లాక్ అయింది',
        'Marathi': 'माझे खाते लॉक झाले आहे',
        'Bengali': 'আমার অ্যাকাউন্ট লক হয়ে গেছে',
        'Gujarati': 'મારું ખાતું લોક થયું છે'
      };
      setInput(samples[selectedLang] || `Sample in ${selectedLang}`);
    }
  }, [selectedLang, messages.length]);

  return (
    <motion.div
      className="chat-window"
      initial={{ scale: 0.95, opacity: 0 }}
      animate={{ scale: 1, opacity: 1 }}
      transition={{ duration: 0.5 }}
    >
      <h2><FiCpu /> Chat History</h2>
      {messages.map((msg, idx) => (
        <motion.div
          key={idx}
          className={`message ${msg.type}-message ${msg.escalate ? 'escalation' : ''}`}
          initial={{ opacity: 0, x: msg.type === 'user' ? 50 : -50 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.3, delay: idx * 0.1 }}
        >
          <span className="icon">{msg.type === 'user' ? <FiUser /> : <FiCpu />}</span>
          <strong>{msg.type === 'user' ? 'You' : 'Bot'}:</strong> {msg.bot_reply || msg.user_message}
          {msg.intent && <span className="meta"> (Intent: {msg.intent} | Sentiment: {msg.sentiment_score.toFixed(1)})</span>}
          {msg.response_time && <span className="meta"> ({msg.response_time})</span>}
        </motion.div>
      ))}
      {loading && <motion.div className="message bot-message" initial={{ opacity: 0 }} animate={{ opacity: 1 }}><FiCpu /> Typing...</motion.div>}
      <div ref={messagesEndRef} />
      <div className="input-group">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder={`Type in ${selectedLang}...`}
          disabled={loading}
        />
        <motion.button onClick={sendMessage} whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} disabled={loading}>
          <FiSend /> Send
        </motion.button>
      </div>
      <style jsx>{`
        .icon { margin-right: 5px; }
        .meta { font-size: 0.8em; opacity: 0.7; display: block; }
      `}</style>
    </motion.div>
  );
};

export default ChatWindow;