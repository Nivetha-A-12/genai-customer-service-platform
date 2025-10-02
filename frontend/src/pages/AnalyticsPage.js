import React from 'react';
import AnalyticsTab from '../components/AnalyticsTab';

const AnalyticsPage = () => {
  const userId = 1;

  return (
    <div>
      <h1>Analytics Dashboard</h1>
      <AnalyticsTab userId={userId} />
    </div>
  );
};

export default AnalyticsPage;