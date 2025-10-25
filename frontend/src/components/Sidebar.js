import React from 'react';
import styled from 'styled-components';
import WanjikuAvatar from './WanjikuAvatar';

const SidebarContainer = styled.aside`
  width: 320px;
  padding: 1.5rem;
  display: none;
  flex-direction: column;
  gap: 1.5rem;
  position: sticky;
  top: 1rem;

  @media (min-width: 769px) {
    display: flex;
  }
`;

const QuickActions = styled.div`
  background: rgba(255,255,255,0.95);
  border-radius: 15px;
  padding: 1rem;
  box-shadow: 0 5px 15px rgba(0,0,0,0.06);
  border: 1px solid rgba(0,0,0,0.04);
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
`;

const ActionButton = styled.button`
  padding: 0.7rem 1rem;
  border-radius: 10px;
  border: none;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  font-weight: 600;
  cursor: pointer;
  width: 100%;
  text-align: left;
`;

const Sidebar = ({ setCurrentView }) => {
  return (
    <SidebarContainer>
      <WanjikuAvatar />

      <QuickActions>
        <ActionButton onClick={() => setCurrentView('chat')}>💬 Anza Mazungumzo</ActionButton>
        <ActionButton onClick={() => setCurrentView('voice')}>🎤 Sauti</ActionButton>
        <ActionButton onClick={() => setCurrentView('services')}>📋 Huduma</ActionButton>
        <ActionButton onClick={() => setCurrentView('documents')}>📄 Hati</ActionButton>
      </QuickActions>
    </SidebarContainer>
  );
};

export default Sidebar;
