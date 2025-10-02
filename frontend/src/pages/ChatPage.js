import React from 'react';
import ChatWindow from '../components/ChatWindow';
import LangSelector from '../components/LangSelector';  // Added this import

const ChatPage = ({ selectedLang, onLangChange }) => {
  const userId = 1;

  return (
    <div className="chat-page">
      <h1 className="chat-title">Live Chat</h1>
      <LangSelector selectedLang={selectedLang} onLangChange={onLangChange} />
      <ChatWindow selectedLang={selectedLang} userId={userId} />
    </div>
  );
};

export default ChatPage;