import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import './App.css'; // Import custom styles

function App() {
  const [queryText, setQueryText] = useState('');
  const [messages, setMessages] = useState([]);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleTextQuery = async () => {
    if (!queryText.trim()) return;

    setMessages(prev => [...prev, { type: 'user', content: queryText }]);

    try {
      const response = await axios.post('http://127.0.0.1:5000/search_by_text', { 
        query_text: queryText 
      });

      // Build image URLs to display in the frontend
      const imageUrls = response.data.map(image => `http://127.0.0.1:5000/images/${image}`);
      
      setMessages(prev => [...prev, { type: 'bot', content: imageUrls, isImageList: true }]);
    } catch (error) {
      console.error("Error:", error);
      setMessages(prev => [...prev, { type: 'bot', content: 'Error processing request', isError: true }]);
    }
    setQueryText('');
  };

  const handleImageQuery = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (e) => {
      setMessages(prev => [...prev, { type: 'user', content: e.target.result, isImage: true }]);
    };
    reader.readAsDataURL(file);

    const formData = new FormData();
    formData.append('image', file);

    try {
      const response = await axios.post('http://127.0.0.1:5000/search_by_image', formData, { 
        headers: { 'Content-Type': 'multipart/form-data' } 
      });

      // Build image URLs to display in the frontend
      const imageUrls = response.data.map(image => `http://127.0.0.1:5000/images/${image}`);

      setMessages(prev => [...prev, { type: 'bot', content: imageUrls, isImageList: true }]);
    } catch (error) {
      console.error("Error:", error);
      setMessages(prev => [...prev, { type: 'bot', content: 'Error processing request', isError: true }]);
    }
  };

  return (
    <div className="chat-container">
      {/* Chat Header */}
      <div className="chat-header">Imagination Bot</div>
      <p className='chat-header'>Query with text & Images </p>

      {/* Chat Messages */}
      <div className="chat-messages">
        {messages.map((message, index) => (
          <div key={index} className={`chat-message ${message.type === 'user' ? 'user-message' : 'bot-message'}`}>
            {message.isImage ? (
              <img src={message.content} alt="Uploaded" className="image-preview" />
            ) : message.isImageList ? (
              message.content.map((imageUrl, idx) => (
                <img key={idx} src={imageUrl} alt="Similar result" className="image-preview" />
              ))
            ) : (
              <p>{message.content}</p>
            )}
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      {/* Chat Input */}
      <div className="chat-input-container">
        <input
          type="text"
          value={queryText}
          onChange={(e) => setQueryText(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && handleTextQuery()}
          placeholder="Type a message..."
          className="chat-input"
        />
        <label className="upload-button">
          📎
          <input type="file" onChange={handleImageQuery} className="file-input" />
        </label>
        <button onClick={handleTextQuery} className="send-button">📤</button>
      </div>
    </div>
  );
}

export default App;
