import React, { useState, useEffect, useRef } from 'react';
import styled from 'styled-components';
import { motion, AnimatePresence } from 'framer-motion';
import WanjikuAvatar from './WanjikuAvatar';
import axios from 'axios';
import toast from 'react-hot-toast';

const ChatContainer = styled.div`
  display: flex;
  flex-direction: column;
  height: 100%;
  max-width: 800px;
  margin: 0 auto;
  gap: 2rem;
`;

const ChatMessages = styled.div`
  flex: 1;
  overflow-y: auto;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 15px;
  box-shadow: 0 5px 15px rgba(0,0,0,0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  max-height: 400px;
`;

const Message = styled(motion.div)`
  display: flex;
  margin-bottom: 1rem;
  justify-content: ${props => props.isUser ? 'flex-end' : 'flex-start'};
`;

const MessageBubble = styled.div`
  max-width: 70%;
  padding: 1rem 1.5rem;
  border-radius: 20px;
  background: ${props => props.isUser 
    ? 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' 
    : 'rgba(255, 255, 255, 0.9)'};
  color: ${props => props.isUser ? 'white' : props.theme.colors.text};
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  word-wrap: break-word;
  line-height: 1.5;
`;

const MessageTime = styled.div`
  font-size: 0.8rem;
  opacity: 0.7;
  margin-top: 0.5rem;
`;

const ChatInput = styled.div`
  display: flex;
  gap: 1rem;
  align-items: center;
  background: rgba(255, 255, 255, 0.95);
  padding: 1rem;
  border-radius: 15px;
  box-shadow: 0 5px 15px rgba(0,0,0,0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
`;

const InputField = styled.input`
  flex: 1;
  padding: 1rem;
  border: 2px solid ${props => props.theme.colors.lightGray};
  border-radius: 25px;
  font-size: 1rem;
  outline: none;
  transition: border-color 0.3s ease;
  
  &:focus {
    border-color: ${props => props.theme.colors.primary};
  }
  
  &::placeholder {
    color: ${props => props.theme.colors.gray};
  }
`;

const SendButton = styled(motion.button)`
  padding: 1rem 1.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 25px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s ease;
  
  &:hover {
    transform: translateY(-2px);
  }
  
  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
    transform: none;
  }
`;

const TypingIndicator = styled(motion.div)`
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem;
  color: ${props => props.theme.colors.gray};
  font-style: italic;
`;

const TypingDots = styled.div`
  display: flex;
  gap: 0.3rem;
  
  span {
    width: 8px;
    height: 8px;
    background: ${props => props.theme.colors.primary};
    border-radius: 50%;
    animation: typing 1.4s infinite ease-in-out;
    
    &:nth-child(1) { animation-delay: -0.32s; }
    &:nth-child(2) { animation-delay: -0.16s; }
    &:nth-child(3) { animation-delay: 0s; }
  }
  
  @keyframes typing {
    0%, 80%, 100% { transform: scale(0); }
    40% { transform: scale(1); }
  }
`;

const ChatInterface = () => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      text: "Karibu! Mimi ni Wanjiku, msaidizi wako wa serikali. Ninawezaje kukusaidia leo?",
      isUser: false,
      timestamp: new Date()
    }
  ]);
  const [inputText, setInputText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    // Create a new chat session
    const newSessionId = `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    setSessionId(newSessionId);
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const sendMessage = async () => {
    if (!inputText.trim() || isLoading) return;

    const userMessage = {
      id: Date.now(),
      text: inputText,
      isUser: true,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputText('');
    setIsLoading(true);

    try {
      const response = await axios.post('/api/chat/sessions/send_message/', {
        message: inputText,
        session_id: sessionId,
        language: 'sw'
      });

      const botMessage = {
        id: Date.now() + 1,
        text: response.data.response,
        isUser: false,
        timestamp: new Date()
      };

      setTimeout(() => {
        setMessages(prev => [...prev, botMessage]);
        setIsLoading(false);
      }, 1000);

    } catch (error) {
      console.error('Error sending message:', error);
      toast.error('Kuna tatizo la kutumia ujumbe. Tafadhali jaribu tena.');
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const formatTime = (date) => {
    return date.toLocaleTimeString('sw-KE', { 
      hour: '2-digit', 
      minute: '2-digit' 
    });
  };

  return (
    <ChatContainer>
      <WanjikuAvatar 
        isSpeaking={isLoading}
        currentMessage={isLoading ? "Anafikiria..." : messages[messages.length - 1]?.text}
      />
      
      <ChatMessages>
        <AnimatePresence>
          {messages.map((message) => (
            <Message
              key={message.id}
              isUser={message.isUser}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.3 }}
            >
              <MessageBubble isUser={message.isUser}>
                {message.text}
                <MessageTime>
                  {formatTime(message.timestamp)}
                </MessageTime>
              </MessageBubble>
            </Message>
          ))}
        </AnimatePresence>
        
        {isLoading && (
          <TypingIndicator
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
          >
            Wanjiku anafikiria
            <TypingDots>
              <span></span>
              <span></span>
              <span></span>
            </TypingDots>
          </TypingIndicator>
        )}
        
        <div ref={messagesEndRef} />
      </ChatMessages>

      <ChatInput>
        <InputField
          type="text"
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Andika ujumbe wako hapa..."
          disabled={isLoading}
        />
        <SendButton
          onClick={sendMessage}
          disabled={!inputText.trim() || isLoading}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          {isLoading ? '⏳' : '📤'}
        </SendButton>
      </ChatInput>
    </ChatContainer>
  );
};

export default ChatInterface;
