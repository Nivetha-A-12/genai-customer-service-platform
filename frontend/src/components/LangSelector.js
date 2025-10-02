import React from 'react';

const LangSelector = ({ selectedLang, onLangChange }) => {
  const languages = ['English', 'Hindi', 'Tamil', 'Telugu', 'Marathi', 'Bengali', 'Gujarati'];

  return (
    <select value={selectedLang} onChange={(e) => onLangChange(e.target.value)} className="lang-select">
      {languages.map(lang => <option key={lang} value={lang}>{lang}</option>)}
    </select>
  );
};

export default LangSelector;