import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import { motion, AnimatePresence } from 'framer-motion';
import axios from 'axios';
import toast from 'react-hot-toast';

const ServicesContainer = styled.div`
  max-width: 1000px;
  margin: 0 auto;
`;

const ServicesHeader = styled.div`
  text-align: center;
  margin-bottom: 2rem;
  color: white;
`;

const ServicesTitle = styled.h2`
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 1rem;
  text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
`;

const ServicesSubtitle = styled.p`
  font-size: 1.1rem;
  opacity: 0.9;
`;

const SearchContainer = styled.div`
  background: rgba(255, 255, 255, 0.95);
  border-radius: 15px;
  padding: 1.5rem;
  margin-bottom: 2rem;
  box-shadow: 0 5px 15px rgba(0,0,0,0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
`;

const SearchInput = styled.input`
  width: 100%;
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

const CategoryFilter = styled.div`
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-top: 1rem;
`;

const CategoryButton = styled(motion.button)`
  padding: 0.5rem 1rem;
  border: 2px solid ${props => props.active 
    ? props.theme.colors.primary 
    : props.theme.colors.lightGray};
  border-radius: 20px;
  background: ${props => props.active 
    ? props.theme.colors.primary 
    : 'transparent'};
  color: ${props => props.active 
    ? 'white' 
    : props.theme.colors.text};
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.3s ease;
  
  &:hover {
    border-color: ${props => props.theme.colors.primary};
    background: ${props => props.theme.colors.primary};
    color: white;
  }
`;

const ServicesGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
`;

const ServiceCard = styled(motion.div)`
  background: rgba(255, 255, 255, 0.95);
  border-radius: 15px;
  padding: 1.5rem;
  box-shadow: 0 5px 15px rgba(0,0,0,0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  transition: all 0.3s ease;
  
  &:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 25px rgba(0,0,0,0.15);
  }
`;

const ServiceIcon = styled.div`
  font-size: 2.5rem;
  margin-bottom: 1rem;
  text-align: center;
`;

const ServiceTitle = styled.h3`
  color: ${props => props.theme.colors.primary};
  font-size: 1.3rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  text-align: center;
`;

const ServiceDescription = styled.p`
  color: ${props => props.theme.colors.text};
  line-height: 1.6;
  margin-bottom: 1rem;
  text-align: center;
`;

const ServiceDetails = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  font-size: 0.9rem;
  color: ${props => props.theme.colors.gray};
`;

const ServiceCost = styled.span`
  font-weight: 600;
  color: ${props => props.theme.colors.success};
`;

const ServiceTime = styled.span`
  font-weight: 500;
`;

const ServiceButton = styled(motion.button)`
  width: 100%;
  padding: 0.8rem 1.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 25px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(0,0,0,0.2);
  }
`;

const LoadingSpinner = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  height: 200px;
  font-size: 1.5rem;
  color: white;
`;

const ErrorMessage = styled.div`
  background: rgba(220, 53, 69, 0.1);
  border: 1px solid rgba(220, 53, 69, 0.3);
  color: ${props => props.theme.colors.danger};
  padding: 1rem;
  border-radius: 10px;
  text-align: center;
  margin: 2rem 0;
`;

const ServicesList = () => {
  const [services, setServices] = useState([]);
  const [filteredServices, setFilteredServices] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');

  const categories = [
    { key: 'all', label: 'Zote', icon: '📋' },
    { key: 'identity', label: 'Vitambulisho', icon: '🆔' },
    { key: 'business', label: 'Biashara', icon: '💼' },
    { key: 'education', label: 'Elimu', icon: '🎓' },
    { key: 'health', label: 'Afya', icon: '🏥' },
    { key: 'transport', label: 'Usafiri', icon: '🚗' },
    { key: 'agriculture', label: 'Kilimo', icon: '🌾' },
    { key: 'social', label: 'Jamii', icon: '👥' }
  ];

  useEffect(() => {
    fetchServices();
  }, []);

  useEffect(() => {
    filterServices();
  }, [services, searchQuery, selectedCategory]);

  const fetchServices = async () => {
    try {
      setLoading(true);
      const response = await axios.get('/api/services/services/');
      setServices(response.data);
    } catch (error) {
      console.error('Error fetching services:', error);
      setError('Kuna tatizo la kupata huduma. Tafadhali jaribu tena.');
    } finally {
      setLoading(false);
    }
  };

  const filterServices = () => {
    let filtered = services;

    // Filter by category
    if (selectedCategory !== 'all') {
      filtered = filtered.filter(service => service.category === selectedCategory);
    }

    // Filter by search query
    if (searchQuery) {
      filtered = filtered.filter(service =>
        service.name_swahili.toLowerCase().includes(searchQuery.toLowerCase()) ||
        service.description_swahili.toLowerCase().includes(searchQuery.toLowerCase())
      );
    }

    setFilteredServices(filtered);
  };

  const handleServiceClick = (service) => {
    toast.success(`Umechagua: ${service.name_swahili}`);
    // Here you would typically navigate to a service details page or start a service request
  };

  if (loading) {
    return (
      <ServicesContainer>
        <LoadingSpinner>
          <motion.div
            animate={{ rotate: 360 }}
            transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
          >
            ⚡
          </motion.div>
          <span style={{ marginLeft: '1rem' }}>Inapakia huduma...</span>
        </LoadingSpinner>
      </ServicesContainer>
    );
  }

  if (error) {
    return (
      <ServicesContainer>
        <ErrorMessage>{error}</ErrorMessage>
      </ServicesContainer>
    );
  }

  return (
    <ServicesContainer>
      <ServicesHeader>
        <ServicesTitle>Huduma za Serikali</ServicesTitle>
        <ServicesSubtitle>
          Chagua huduma unayohitaji na uanze mchakato wa maombi
        </ServicesSubtitle>
      </ServicesHeader>

      <SearchContainer>
        <SearchInput
          type="text"
          placeholder="Tafuta huduma..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />
        <CategoryFilter>
          {categories.map((category) => (
            <CategoryButton
              key={category.key}
              active={selectedCategory === category.key}
              onClick={() => setSelectedCategory(category.key)}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              {category.icon} {category.label}
            </CategoryButton>
          ))}
        </CategoryFilter>
      </SearchContainer>

      <ServicesGrid>
        <AnimatePresence>
          {filteredServices.map((service) => (
            <ServiceCard
              key={service.id}
              initial={{ opacity: 0, y: 50 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -50 }}
              transition={{ duration: 0.5 }}
              whileHover={{ scale: 1.02 }}
            >
              <ServiceIcon>
                {service.category === 'identity' && '🆔'}
                {service.category === 'business' && '💼'}
                {service.category === 'education' && '🎓'}
                {service.category === 'health' && '🏥'}
                {service.category === 'transport' && '🚗'}
                {service.category === 'agriculture' && '🌾'}
                {service.category === 'social' && '👥'}
                {!['identity', 'business', 'education', 'health', 'transport', 'agriculture', 'social'].includes(service.category) && '📋'}
              </ServiceIcon>
              
              <ServiceTitle>{service.name_swahili}</ServiceTitle>
              <ServiceDescription>{service.description_swahili}</ServiceDescription>
              
              <ServiceDetails>
                <ServiceCost>
                  {service.cost ? `KSh ${service.cost}` : 'Bure'}
                </ServiceCost>
                <ServiceTime>{service.processing_time_swahili}</ServiceTime>
              </ServiceDetails>
              
              <ServiceButton
                onClick={() => handleServiceClick(service)}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
              >
                Anza Maombi
              </ServiceButton>
            </ServiceCard>
          ))}
        </AnimatePresence>
      </ServicesGrid>

      {filteredServices.length === 0 && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          style={{
            textAlign: 'center',
            color: 'white',
            padding: '2rem',
            fontSize: '1.2rem'
          }}
        >
          Hakuna huduma zilizopatikana kwa kipengele chako cha utafutaji.
        </motion.div>
      )}
    </ServicesContainer>
  );
};

export default ServicesList;

