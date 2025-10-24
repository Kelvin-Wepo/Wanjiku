import React from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';

const HeaderContainer = styled.header`
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  padding: 1rem 2rem;
  box-shadow: 0 2px 20px rgba(0,0,0,0.1);
`;

const HeaderContent = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
`;

const Logo = styled(motion.div)`
  display: flex;
  align-items: center;
  gap: 1rem;
`;

const LogoIcon = styled.div`
  font-size: 2rem;
  color: ${props => props.theme.colors.primary};
`;

const LogoText = styled.div`
  h1 {
    font-size: 1.8rem;
    font-weight: 700;
    color: ${props => props.theme.colors.primary};
    margin: 0;
  }
  
  p {
    font-size: 0.9rem;
    color: ${props => props.theme.colors.gray};
    margin: 0;
  }
`;

const StatusIndicator = styled.div`
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: ${props => props.theme.colors.success};
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
  animation: pulse 2s infinite;
  
  @keyframes pulse {
    0% { opacity: 1; }
    50% { opacity: 0.5; }
    100% { opacity: 1; }
  }
`;

const Header = () => {
  return (
    <HeaderContainer>
      <HeaderContent>
        <Logo
          initial={{ opacity: 0, x: -50 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.8 }}
        >
          <LogoIcon>🤖</LogoIcon>
          <LogoText>
            <h1>Wanjiku 2.0</h1>
            <p>Msaidizi wa Serikali wa Kenya</p>
          </LogoText>
        </Logo>
        
        <StatusIndicator
          initial={{ opacity: 0, x: 50 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.8, delay: 0.3 }}
        >
          <StatusDot />
          Imeunganishwa
        </StatusIndicator>
      </HeaderContent>
    </HeaderContainer>
  );
};

export default Header;

