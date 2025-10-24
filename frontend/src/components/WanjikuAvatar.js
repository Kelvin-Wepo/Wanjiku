import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';

const AvatarContainer = styled(motion.div)`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 20px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  margin-bottom: 2rem;
`;

const Avatar = styled(motion.div)`
  width: 120px;
  height: 120px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 4rem;
  margin-bottom: 1rem;
  position: relative;
  overflow: hidden;
`;

const AvatarImage = styled.div`
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 4rem;
`;

const SpeechBubble = styled(motion.div)`
  background: white;
  border-radius: 20px;
  padding: 1rem 1.5rem;
  box-shadow: 0 5px 15px rgba(0,0,0,0.1);
  position: relative;
  max-width: 300px;
  margin-bottom: 1rem;
  
  &::after {
    content: '';
    position: absolute;
    bottom: -10px;
    left: 50%;
    transform: translateX(-50%);
    width: 0;
    height: 0;
    border-left: 10px solid transparent;
    border-right: 10px solid transparent;
    border-top: 10px solid white;
  }
`;

const SpeechText = styled.p`
  color: ${props => props.theme.colors.text};
  font-size: 1rem;
  line-height: 1.5;
  margin: 0;
  text-align: center;
`;

const AvatarName = styled.h3`
  color: ${props => props.theme.colors.primary};
  font-size: 1.5rem;
  font-weight: 600;
  margin: 0.5rem 0;
  text-align: center;
`;

const AvatarTitle = styled.p`
  color: ${props => props.theme.colors.gray};
  font-size: 1rem;
  margin: 0;
  text-align: center;
`;

const StatusIndicator = styled.div`
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-top: 1rem;
  padding: 0.5rem 1rem;
  background: ${props => props.isListening ? props.theme.colors.warning : props.theme.colors.success};
  color: white;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 500;
`;

const StatusDot = styled.div`
  width: 8px;
  height: 8px;
  background: white;
  border-radius: 50%;
  animation: ${props => props.isListening ? 'pulse 1s infinite' : 'none'};
  
  @keyframes pulse {
    0% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.5; transform: scale(1.2); }
    100% { opacity: 1; transform: scale(1); }
  }
`;

const WanjikuAvatar = ({ 
  isListening = false, 
  isSpeaking = false, 
  currentMessage = "Karibu! Mimi ni Wanjiku, msaidizi wako wa serikali. Ninawezaje kukusaidia leo?",
  onAvatarClick 
}) => {
  const [animationKey, setAnimationKey] = useState(0);

  useEffect(() => {
    if (isSpeaking) {
      setAnimationKey(prev => prev + 1);
    }
  }, [isSpeaking]);

  const avatarVariants = {
    idle: {
      scale: 1,
      rotate: 0,
    },
    listening: {
      scale: [1, 1.1, 1],
      rotate: [0, 5, -5, 0],
      transition: {
        duration: 2,
        repeat: Infinity,
        ease: "easeInOut"
      }
    },
    speaking: {
      scale: [1, 1.05, 1],
      rotate: [0, 2, -2, 0],
      transition: {
        duration: 0.5,
        repeat: Infinity,
        ease: "easeInOut"
      }
    }
  };

  return (
    <AvatarContainer
      initial={{ opacity: 0, y: 50 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.8 }}
    >
      <Avatar
        variants={avatarVariants}
        animate={isListening ? 'listening' : isSpeaking ? 'speaking' : 'idle'}
        key={animationKey}
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
        onClick={onAvatarClick}
        style={{ cursor: 'pointer' }}
      >
        <AvatarImage>
          {isListening ? '🎤' : isSpeaking ? '🗣️' : '👩🏾‍💼'}
        </AvatarImage>
      </Avatar>

      {currentMessage && (
        <SpeechBubble
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.3 }}
        >
          <SpeechText>{currentMessage}</SpeechText>
        </SpeechBubble>
      )}

      <AvatarName>Wanjiku</AvatarName>
      <AvatarTitle>Msaidizi wa Serikali wa Kenya</AvatarTitle>
      
      <StatusIndicator isListening={isListening}>
        <StatusDot isListening={isListening} />
        {isListening ? 'Anasikiliza...' : isSpeaking ? 'Anazungumza...' : 'Tayari'}
      </StatusIndicator>
    </AvatarContainer>
  );
};

export default WanjikuAvatar;

