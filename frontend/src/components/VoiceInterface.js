import React, { useState, useEffect, useRef } from 'react';
import styled from 'styled-components';
import { motion, AnimatePresence } from 'framer-motion';
import WanjikuAvatar from './WanjikuAvatar';
import axios from 'axios';
import toast from 'react-hot-toast';

const VoiceContainer = styled.div`
  display: flex;
  flex-direction: column;
  height: 100%;
  max-width: 800px;
  margin: 0 auto;
  gap: 2rem;
`;

const VoiceControls = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2rem;
  background: rgba(255, 255, 255, 0.95);
  padding: 2rem;
  border-radius: 20px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
`;

const VoiceButton = styled(motion.button)`
  width: 120px;
  height: 120px;
  border-radius: 50%;
  border: none;
  background: ${props => props.isListening 
    ? 'linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%)' 
    : 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'};
  color: white;
  font-size: 3rem;
  cursor: pointer;
  box-shadow: 0 10px 30px rgba(0,0,0,0.2);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  
  &:hover {
    transform: translateY(-5px);
    box-shadow: 0 15px 40px rgba(0,0,0,0.3);
  }
  
  &:active {
    transform: translateY(-2px);
  }
  
  &::before {
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    width: 0;
    height: 0;
    background: rgba(255, 255, 255, 0.3);
    border-radius: 50%;
    transform: translate(-50%, -50%);
    transition: all 0.3s ease;
  }
  
  &:hover::before {
    width: 100%;
    height: 100%;
  }
`;

const VoiceStatus = styled.div`
  text-align: center;
  color: ${props => props.theme.colors.text};
`;

const StatusText = styled.h3`
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
  color: ${props => props.isListening ? props.theme.colors.danger : props.theme.colors.primary};
`;

const StatusSubtext = styled.p`
  color: ${props => props.theme.colors.gray};
  font-size: 1rem;
`;

const TranscriptContainer = styled.div`
  background: rgba(255, 255, 255, 0.95);
  border-radius: 15px;
  padding: 1.5rem;
  box-shadow: 0 5px 15px rgba(0,0,0,0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  min-height: 200px;
  max-height: 300px;
  overflow-y: auto;
`;

const TranscriptTitle = styled.h4`
  color: ${props => props.theme.colors.primary};
  font-size: 1.2rem;
  margin-bottom: 1rem;
  text-align: center;
`;

const TranscriptText = styled.div`
  color: ${props => props.theme.colors.text};
  line-height: 1.6;
  font-size: 1rem;
  text-align: center;
  min-height: 100px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-style: italic;
  opacity: 0.7;
`;

const ResponseContainer = styled.div`
  background: rgba(255, 255, 255, 0.95);
  border-radius: 15px;
  padding: 1.5rem;
  box-shadow: 0 5px 15px rgba(0,0,0,0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  min-height: 200px;
  max-height: 300px;
  overflow-y: auto;
`;

const ResponseTitle = styled.h4`
  color: ${props => props.theme.colors.primary};
  font-size: 1.2rem;
  margin-bottom: 1rem;
  text-align: center;
`;

const ResponseText = styled.div`
  color: ${props => props.theme.colors.text};
  line-height: 1.6;
  font-size: 1rem;
  text-align: center;
  min-height: 100px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-style: italic;
  opacity: 0.7;
`;

const ControlButtons = styled.div`
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
`;

const ControlButton = styled(motion.button)`
  padding: 0.8rem 1.5rem;
  border: none;
  border-radius: 25px;
  background: ${props => props.variant === 'primary' 
    ? 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' 
    : 'rgba(255, 255, 255, 0.9)'};
  color: ${props => props.variant === 'primary' ? 'white' : props.theme.colors.text};
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(0,0,0,0.2);
  }
  
  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
    transform: none;
  }
`;

const VoiceInterface = () => {
  const [isListening, setIsListening] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [transcript, setTranscript] = useState('');
  const [response, setResponse] = useState('');
  const [sessionId, setSessionId] = useState(null);
  const [mediaRecorder, setMediaRecorder] = useState(null);
  const [audioChunks, setAudioChunks] = useState([]);

  useEffect(() => {
    // Create a new voice session
    const newSessionId = `voice_session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    setSessionId(newSessionId);
  }, []);

  const startListening = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const recorder = new MediaRecorder(stream);
      const chunks = [];

      recorder.ondataavailable = (event) => {
        chunks.push(event.data);
      };

      recorder.onstop = async () => {
        const audioBlob = new Blob(chunks, { type: 'audio/wav' });
        await processAudio(audioBlob);
        setAudioChunks([]);
      };

      setMediaRecorder(recorder);
      recorder.start();
      setIsListening(true);
      setTranscript('Anasikiliza...');
      
    } catch (error) {
      console.error('Error accessing microphone:', error);
      toast.error('Haiwezi kufikia mikrofoni. Tafadhali ruhusu matumizi ya mikrofoni.');
    }
  };

  const stopListening = () => {
    if (mediaRecorder && isListening) {
      mediaRecorder.stop();
      setIsListening(false);
      setTranscript('Anachakata...');
    }
  };

  const processAudio = async (audioBlob) => {
    setIsProcessing(true);
    setTranscript('Anachakata sauti...');

    try {
      const formData = new FormData();
      formData.append('audio', audioBlob, 'recording.wav');
      formData.append('session_id', sessionId);

      const response = await axios.post('/api/voice/sessions/process_voice/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      if (response.data.transcript) {
        setTranscript(response.data.transcript);
        
        // Generate voice response
        const responseData = await axios.post('/api/voice/sessions/generate_response/', {
          text: response.data.transcript,
          session_id: sessionId
        });

        if (responseData.data.text_response) {
          setResponse(responseData.data.text_response);
          // Play the response audio if available
          if (responseData.data.audio_url) {
            playAudio(responseData.data.audio_url);
          }
        }
      }

    } catch (error) {
      console.error('Error processing audio:', error);
      toast.error('Kuna tatizo la kuchakata sauti. Tafadhali jaribu tena.');
      setTranscript('Kuna tatizo la kuchakata sauti.');
    } finally {
      setIsProcessing(false);
    }
  };

  const playAudio = (audioUrl) => {
    const audio = new Audio(audioUrl);
    audio.play().catch(error => {
      console.error('Error playing audio:', error);
    });
  };

  const clearTranscript = () => {
    setTranscript('');
    setResponse('');
  };

  const speakText = (text) => {
    if ('speechSynthesis' in window) {
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.lang = 'sw-KE';
      utterance.rate = 0.8;
      speechSynthesis.speak(utterance);
    }
  };

  return (
    <VoiceContainer>
      <WanjikuAvatar 
        isListening={isListening}
        isSpeaking={isProcessing}
        currentMessage={response || "Bonyeza kitufe cha kuzungumza na mimi"}
      />
      
      <VoiceControls>
        <VoiceButton
          onClick={isListening ? stopListening : startListening}
          disabled={isProcessing}
          isListening={isListening}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          {isListening ? '⏹️' : '🎤'}
        </VoiceButton>

        <VoiceStatus>
          <StatusText isListening={isListening}>
            {isListening ? 'Anasikiliza...' : isProcessing ? 'Anachakata...' : 'Bonyeza kuzungumza'}
          </StatusText>
          <StatusSubtext>
            {isListening 
              ? 'Sema sasa, kisha bonyeza tena kuacha' 
              : isProcessing 
                ? 'Anachakata sauti yako...' 
                : 'Bonyeza na uchukue kuzungumza na Wanjiku'
            }
          </StatusSubtext>
        </VoiceStatus>

        <ControlButtons>
          <ControlButton
            onClick={clearTranscript}
            variant="secondary"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            🗑️ Safisha
          </ControlButton>
          <ControlButton
            onClick={() => speakText(response)}
            variant="primary"
            disabled={!response}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            🔊 Soma
          </ControlButton>
        </ControlButtons>
      </VoiceControls>

      <TranscriptContainer>
        <TranscriptTitle>Maelezo Yako</TranscriptTitle>
        <TranscriptText>
          {transcript || 'Hakuna maelezo bado. Bonyeza kitufe cha kuzungumza.'}
        </TranscriptText>
      </TranscriptContainer>

      <ResponseContainer>
        <ResponseTitle>Jibu la Wanjiku</ResponseTitle>
        <ResponseText>
          {response || 'Hakuna jibu bado. Bonyeza kitufe cha kuzungumza.'}
        </ResponseText>
      </ResponseContainer>
    </VoiceContainer>
  );
};

export default VoiceInterface;

