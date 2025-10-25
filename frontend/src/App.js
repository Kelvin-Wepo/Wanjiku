import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import styled, { ThemeProvider } from 'styled-components';
import { Toaster } from 'react-hot-toast';
import { motion } from 'framer-motion';
import GlobalStyle from './styles/GlobalStyle';

// Components
import Header from './components/Header';
import WanjikuAvatar from './components/WanjikuAvatar';
import ChatInterface from './components/ChatInterface';
import VoiceInterface from './components/VoiceInterface';
import ServicesList from './components/ServicesList';
import DocumentManager from './components/DocumentManager';
import Navigation from './components/Navigation';
import Sidebar from './components/Sidebar';
import theme from './theme';

const AppContainer = styled.div`
  min-height: 100vh;
  background: ${props => `linear-gradient(135deg, 
    ${props.theme.colors.primary}20 0%, 
    ${props.theme.colors.secondary}20 50%,
    ${props.theme.colors.accent}20 100%
  )`};
  display: flex;
  flex-direction: column;
  position: relative;
  
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 60vh;
    background: ${props => props.theme.colors.gradient.primary};
    clip-path: polygon(0 0, 100% 0, 100% 60%, 0% 100%);
    z-index: 0;
  }
`;

const Inner = styled.div`
  flex: 1;
  display: flex;
  gap: 2rem;
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem;
  width: 100%;
  position: relative;
  z-index: 1;
`;

const MainContent = styled.main`
  flex: 1;
  display: flex;
  flex-direction: column;
`;

const WelcomeSection = styled(motion.div)`
  text-align: center;
  margin-bottom: 2rem;
  color: white;
`;

const WelcomeTitle = styled.h1`
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 1rem;
  text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
  
  @media (max-width: ${props => props.theme.breakpoints.mobile}) {
    font-size: 2rem;
  }
`;

const WelcomeSubtitle = styled.p`
  font-size: 1.2rem;
  opacity: 0.9;
  margin-bottom: 2rem;
`;

const FeatureGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-top: 2rem;
`;

const FeatureCard = styled(motion.div)`
  background: rgba(255, 255, 255, 0.95);
  border-radius: 15px;
  padding: 2rem;
  box-shadow: 0 10px 30px rgba(0,0,0,0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
`;

const FeatureTitle = styled.h3`
  color: ${props => props.theme.colors.primary};
  font-size: 1.5rem;
  margin-bottom: 1rem;
  font-weight: 600;
`;

const FeatureDescription = styled.p`
  color: ${props => props.theme.colors.text};
  line-height: 1.6;
  margin-bottom: 1rem;
`;

const FeatureList = styled.ul`
  list-style: none;
  padding: 0;
`;

const FeatureItem = styled.li`
  color: ${props => props.theme.colors.gray};
  margin-bottom: 0.5rem;
  padding-left: 1.5rem;
  position: relative;
  
  &::before {
    content: '✓';
    position: absolute;
    left: 0;
    color: ${props => props.theme.colors.success};
    font-weight: bold;
  }
`;

function App() {
  const [currentView, setCurrentView] = useState('home');
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Simulate loading
    const timer = setTimeout(() => {
      setIsLoading(false);
    }, 2000);

    return () => clearTimeout(timer);
  }, []);

  if (isLoading) {
    return (
      <ThemeProvider theme={theme}>
        <AppContainer>
          <div style={{ 
            display: 'flex', 
            justifyContent: 'center', 
            alignItems: 'center', 
            height: '100vh',
            color: 'white',
            fontSize: '1.5rem'
          }}>
            <motion.div
              animate={{ rotate: 360 }}
              transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
            >
              ⚡
            </motion.div>
            <span style={{ marginLeft: '1rem' }}>Wanjiku 2.0 inapakia...</span>
          </div>
        </AppContainer>
      </ThemeProvider>
    );
  }

  const renderContent = () => {
    switch (currentView) {
      case 'chat':
        return <ChatInterface />;
      case 'voice':
        return <VoiceInterface />;
      case 'services':
        return <ServicesList />;
      case 'documents':
        return <DocumentManager />;
      default:
        return (
          <>
            <WelcomeSection
              initial={{ opacity: 0, y: 50 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8 }}
            >
              <WelcomeTitle>Karibu Wanjiku 2.0</WelcomeTitle>
              <WelcomeSubtitle>
                Msaidizi wako wa Serikali wa Kenya - Huduma za Kidijitali kwa Wote
              </WelcomeSubtitle>
            </WelcomeSection>

            <FeatureGrid>
              <FeatureCard
                initial={{ opacity: 0, y: 50 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8, delay: 0.2 }}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                <FeatureTitle>💬 Mazungumzo ya Swahili</FeatureTitle>
                <FeatureDescription>
                  Wanjiku anaweza kuzungumza na wewe kwa Kiswahili na kukusaidia na maswali yako.
                </FeatureDescription>
                <FeatureList>
                  <FeatureItem>Mazungumzo ya asili ya Kiswahili</FeatureItem>
                  <FeatureItem>Kujibu maswali ya huduma za serikali</FeatureItem>
                  <FeatureItem>Kusaidia na mchakato wa maombi</FeatureItem>
                </FeatureList>
              </FeatureCard>

              <FeatureCard
                initial={{ opacity: 0, y: 50 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8, delay: 0.4 }}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                <FeatureTitle>🎤 Sauti na Maandishi</FeatureTitle>
                <FeatureDescription>
                  Tumia sauti yako au andika ujumbe kwa Wanjiku.
                </FeatureDescription>
                <FeatureList>
                  <FeatureItem>Kutambua sauti ya Kiswahili</FeatureItem>
                  <FeatureItem>Kujibu kwa sauti</FeatureItem>
                  <FeatureItem>Kubadilisha maandishi kuwa sauti</FeatureItem>
                </FeatureList>
              </FeatureCard>

              <FeatureCard
                initial={{ opacity: 0, y: 50 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8, delay: 0.6 }}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                <FeatureTitle>📄 Huduma za Serikali</FeatureTitle>
                <FeatureDescription>
                  Pata msaada na huduma mbalimbali za serikali.
                </FeatureDescription>
                <FeatureList>
                  <FeatureItem>Cheti cha kuzaliwa</FeatureItem>
                  <FeatureItem>Leseni ya biashara</FeatureItem>
                  <FeatureItem>Kitambulisho cha taifa</FeatureItem>
                  <FeatureItem>Pasipoti</FeatureItem>
                </FeatureList>
              </FeatureCard>

              <FeatureCard
                initial={{ opacity: 0, y: 50 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8, delay: 0.8 }}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                <FeatureTitle>🔒 Usalama wa Blockchain</FeatureTitle>
                <FeatureDescription>
                  Hati zako zinaaminishwa kwa teknolojia ya blockchain.
                </FeatureDescription>
                <FeatureList>
                  <FeatureItem>Kuthibitisha hati za kidijitali</FeatureItem>
                  <FeatureItem>Usalama wa juu</FeatureItem>
                  <FeatureItem>Kuepuka uongo</FeatureItem>
                </FeatureList>
              </FeatureCard>
            </FeatureGrid>
          </>
        );
    }
  };

  return (
    <ThemeProvider theme={theme}>
      <GlobalStyle />
      <Router>
        <AppContainer>
          <Header />
          <Inner>
            <Sidebar setCurrentView={setCurrentView} />
            <MainContent>
              {renderContent()}
            </MainContent>
          </Inner>
          <Navigation currentView={currentView} setCurrentView={setCurrentView} />
          <Toaster 
            position="top-right"
            toastOptions={{
              duration: 4000,
              style: {
                background: theme.colors.surface,
                color: theme.colors.text,
                borderRadius: '8px',
                boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
                border: `1px solid ${theme.colors.lightGray}`,
              },
            }}
          />
        </AppContainer>
      </Router>
    </ThemeProvider>
  );
}

export default App;

