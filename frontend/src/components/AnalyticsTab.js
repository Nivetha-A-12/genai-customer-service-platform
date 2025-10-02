import React, { useState } from 'react';
import { motion } from 'framer-motion';
import axios from 'axios';
import { FiBarChart2 } from 'react-icons/fi';

const AnalyticsTab = ({ userId }) => {
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(false);

  const fetchAnalytics = async () => {
    setLoading(true);
    try {
      const resp = await axios.get(`/api/analytics/${userId}`);
      setAnalytics(resp.data);
    } catch (err) {
      alert('Error fetching analytics: ' + err.message);
    }
    setLoading(false);
  };

  return (
    <motion.div
      className="analytics-tab"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <h2><FiBarChart2 /> Performance Analytics</h2>
      <motion.button onClick={fetchAnalytics} disabled={loading} whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
        {loading ? 'Loading...' : `Fetch for User ${userId}`}
      </motion.button>
      {analytics && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.3 }}
          className="metrics"
        >
          <p><strong>Avg Sentiment:</strong> {analytics.avg_sentiment}</p>
          <p><strong>Escalation Rate:</strong> {analytics.escalation_rate}</p>
          <p><strong>Total Conversations:</strong> {analytics.total_conversations}</p>
          <p><strong>Avg Response Time:</strong> {analytics.avg_response_time}</p>
        </motion.div>
      )}
    </motion.div>
  );
};

export default AnalyticsTab;