import React from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';

const NavigationContainer = styled.nav`
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-top: 1px solid rgba(255, 255, 255, 0.2);
  padding: 1rem;
  z-index: 1000;

  @media (min-width: 769px) {
    display: none; /* hide bottom nav on wider screens, use sidebar instead */
  }
`;

const NavigationContent = styled.div`
  display: flex;
  justify-content: center;
  gap: 1rem;
  max-width: 600px;
  margin: 0 auto;
`;

const NavButton = styled(motion.button)`
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.3rem;
  padding: 0.8rem 1rem;
  border: none;
  border-radius: 15px;
  background: ${props => props.active 
    ? 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' 
    : 'transparent'};
  color: ${props => props.active 
    ? 'white' 
    : props.theme.colors.text};
  font-size: 0.8rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  min-width: 80px;
  
  &:hover {
    background: ${props => props.active 
      ? 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' 
      : 'rgba(102, 126, 234, 0.1)'};
    transform: translateY(-2px);
  }
`;

const NavIcon = styled.div`
  font-size: 1.2rem;
`;

const NavLabel = styled.span`
  font-size: 0.7rem;
  text-align: center;
  line-height: 1.2;
`;

const Navigation = ({ currentView, setCurrentView }) => {
  const navItems = [
    {
      id: 'home',
      icon: '🏠',
      label: 'Nyumbani',
      active: currentView === 'home'
    },
    {
      id: 'chat',
      icon: '💬',
      label: 'Mazungumzo',
      active: currentView === 'chat'
    },
    {
      id: 'voice',
      icon: '🎤',
      label: 'Sauti',
      active: currentView === 'voice'
    },
    {
      id: 'services',
      icon: '📋',
      label: 'Huduma',
      active: currentView === 'services'
    },
    {
      id: 'documents',
      icon: '📄',
      label: 'Hati',
      active: currentView === 'documents'
    }
  ];

  return (
    <NavigationContainer>
      <NavigationContent>
        {navItems.map((item) => (
          <NavButton
            key={item.id}
            active={item.active}
            onClick={() => setCurrentView(item.id)}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3 }}
          >
            <NavIcon>{item.icon}</NavIcon>
            <NavLabel>{item.label}</NavLabel>
          </NavButton>
        ))}
      </NavigationContent>
    </NavigationContainer>
  );
};

export default Navigation;

