import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import { motion, AnimatePresence } from 'framer-motion';
import axios from 'axios';
import toast from 'react-hot-toast';

const DocumentContainer = styled.div`
  max-width: 1000px;
  margin: 0 auto;
`;

const DocumentHeader = styled.div`
  text-align: center;
  margin-bottom: 2rem;
  color: white;
`;

const DocumentTitle = styled.h2`
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 1rem;
  text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
`;

const DocumentSubtitle = styled.p`
  font-size: 1.1rem;
  opacity: 0.9;
`;

const UploadSection = styled.div`
  background: rgba(255, 255, 255, 0.95);
  border-radius: 15px;
  padding: 2rem;
  margin-bottom: 2rem;
  box-shadow: 0 5px 15px rgba(0,0,0,0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
`;

const UploadArea = styled(motion.div)`
  border: 2px dashed ${props => props.isDragOver 
    ? props.theme.colors.primary 
    : props.theme.colors.lightGray};
  border-radius: 15px;
  padding: 3rem;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  background: ${props => props.isDragOver 
    ? 'rgba(46, 139, 87, 0.1)' 
    : 'transparent'};
  
  &:hover {
    border-color: ${props => props.theme.colors.primary};
    background: rgba(46, 139, 87, 0.05);
  }
`;

const UploadIcon = styled.div`
  font-size: 3rem;
  margin-bottom: 1rem;
  color: ${props => props.theme.colors.primary};
`;

const UploadText = styled.p`
  color: ${props => props.theme.colors.text};
  font-size: 1.1rem;
  margin-bottom: 0.5rem;
`;

const UploadSubtext = styled.p`
  color: ${props => props.theme.colors.gray};
  font-size: 0.9rem;
`;

const HiddenInput = styled.input`
  display: none;
`;

const DocumentTypeSelect = styled.select`
  width: 100%;
  padding: 1rem;
  border: 2px solid ${props => props.theme.colors.lightGray};
  border-radius: 10px;
  font-size: 1rem;
  margin-bottom: 1rem;
  outline: none;
  transition: border-color 0.3s ease;
  
  &:focus {
    border-color: ${props => props.theme.colors.primary};
  }
`;

const UploadButton = styled(motion.button)`
  width: 100%;
  padding: 1rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 1rem;
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

const DocumentsList = styled.div`
  background: rgba(255, 255, 255, 0.95);
  border-radius: 15px;
  padding: 1.5rem;
  box-shadow: 0 5px 15px rgba(0,0,0,0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
`;

const DocumentItem = styled(motion.div)`
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem;
  border: 1px solid ${props => props.theme.colors.lightGray};
  border-radius: 10px;
  margin-bottom: 1rem;
  background: white;
  transition: all 0.3s ease;
  
  &:hover {
    box-shadow: 0 3px 10px rgba(0,0,0,0.1);
    transform: translateY(-2px);
  }
`;

const DocumentInfo = styled.div`
  display: flex;
  align-items: center;
  gap: 1rem;
`;

const DocumentIcon = styled.div`
  font-size: 2rem;
  color: ${props => props.theme.colors.primary};
`;

const DocumentDetails = styled.div`
  flex: 1;
`;

const DocumentName = styled.h4`
  color: ${props => props.theme.colors.text};
  font-size: 1.1rem;
  font-weight: 600;
  margin-bottom: 0.3rem;
`;

const DocumentMeta = styled.div`
  color: ${props => props.theme.colors.gray};
  font-size: 0.9rem;
  display: flex;
  gap: 1rem;
`;

const DocumentStatus = styled.span`
  padding: 0.3rem 0.8rem;
  border-radius: 15px;
  font-size: 0.8rem;
  font-weight: 600;
  background: ${props => {
    switch (props.status) {
      case 'verified': return props.theme.colors.success;
      case 'pending': return props.theme.colors.warning;
      case 'rejected': return props.theme.colors.danger;
      default: return props.theme.colors.gray;
    }
  }};
  color: white;
`;

const DocumentActions = styled.div`
  display: flex;
  gap: 0.5rem;
`;

const ActionButton = styled(motion.button)`
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 5px;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.3s ease;
  
  &.download {
    background: ${props => props.theme.colors.info};
    color: white;
  }
  
  &.verify {
    background: ${props => props.theme.colors.success};
    color: white;
  }
  
  &.delete {
    background: ${props => props.theme.colors.danger};
    color: white;
  }
  
  &:hover {
    transform: translateY(-1px);
    box-shadow: 0 3px 8px rgba(0,0,0,0.2);
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

const EmptyState = styled.div`
  text-align: center;
  padding: 3rem;
  color: ${props => props.theme.colors.gray};
`;

const DocumentManager = () => {
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [dragOver, setDragOver] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);
  const [documentType, setDocumentType] = useState('');

  const documentTypes = [
    { value: 'birth_certificate', label: 'Cheti cha Kuzaliwa' },
    { value: 'id_card', label: 'Kitambulisho cha Taifa' },
    { value: 'passport', label: 'Pasipoti' },
    { value: 'driving_license', label: 'Leseni ya Kuendesha' },
    { value: 'business_license', label: 'Leseni ya Biashara' },
    { value: 'education_certificate', label: 'Cheti cha Elimu' },
    { value: 'marriage_certificate', label: 'Cheti cha Ndoa' },
    { value: 'death_certificate', label: 'Cheti cha Kifo' }
  ];

  useEffect(() => {
    fetchDocuments();
  }, []);

  const fetchDocuments = async () => {
    try {
      setLoading(true);
      const response = await axios.get('/api/documents/documents/');
      setDocuments(response.data);
    } catch (error) {
      console.error('Error fetching documents:', error);
      toast.error('Kuna tatizo la kupata hati. Tafadhali jaribu tena.');
    } finally {
      setLoading(false);
    }
  };

  const handleFileSelect = (event) => {
    const file = event.target.files[0];
    if (file) {
      setSelectedFile(file);
    }
  };

  const handleDragOver = (event) => {
    event.preventDefault();
    setDragOver(true);
  };

  const handleDragLeave = (event) => {
    event.preventDefault();
    setDragOver(false);
  };

  const handleDrop = (event) => {
    event.preventDefault();
    setDragOver(false);
    const file = event.dataTransfer.files[0];
    if (file) {
      setSelectedFile(file);
    }
  };

  const handleUpload = async () => {
    if (!selectedFile || !documentType) {
      toast.error('Tafadhali chagua faili na aina ya hati.');
      return;
    }

    try {
      setUploading(true);
      const formData = new FormData();
      formData.append('document', selectedFile);
      formData.append('document_type', documentType);
      formData.append('title', selectedFile.name);
      formData.append('title_swahili', selectedFile.name);

      await axios.post('/api/documents/documents/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      toast.success('Hati imepakiwa kwa mafanikio!');
      setSelectedFile(null);
      setDocumentType('');
      fetchDocuments();
    } catch (error) {
      console.error('Error uploading document:', error);
      toast.error('Kuna tatizo la kupakia hati. Tafadhali jaribu tena.');
    } finally {
      setUploading(false);
    }
  };

  const handleDownload = async (document) => {
    try {
      const response = await axios.get(`/api/documents/documents/${document.id}/download/`, {
        responseType: 'blob'
      });
      
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `${document.title}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error('Error downloading document:', error);
      toast.error('Kuna tatizo la kupakua hati.');
    }
  };

  const handleVerify = async (document) => {
    try {
      await axios.post('/api/blockchain/verifications/verify_document/', {
        document_hash: document.file_hash
      });
      toast.success('Hati imethibitishwa kwa mafanikio!');
      fetchDocuments();
    } catch (error) {
      console.error('Error verifying document:', error);
      toast.error('Kuna tatizo la kuthibitisha hati.');
    }
  };

  const handleDelete = async (document) => {
    if (window.confirm('Je, una uhakika unataka kufuta hati hii?')) {
      try {
        await axios.delete(`/api/documents/documents/${document.id}/`);
        toast.success('Hati imefutwa kwa mafanikio!');
        fetchDocuments();
      } catch (error) {
        console.error('Error deleting document:', error);
        toast.error('Kuna tatizo la kufuta hati.');
      }
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'verified': return 'Imethibitishwa';
      case 'pending': return 'Inasubiri';
      case 'rejected': return 'Imekataliwa';
      default: return 'Haijulikani';
    }
  };

  const getDocumentIcon = (type) => {
    switch (type) {
      case 'birth_certificate': return '👶';
      case 'id_card': return '🆔';
      case 'passport': return '📘';
      case 'driving_license': return '🚗';
      case 'business_license': return '💼';
      case 'education_certificate': return '🎓';
      case 'marriage_certificate': return '💒';
      case 'death_certificate': return '⚰️';
      default: return '📄';
    }
  };

  if (loading) {
    return (
      <DocumentContainer>
        <LoadingSpinner>
          <motion.div
            animate={{ rotate: 360 }}
            transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
          >
            ⚡
          </motion.div>
          <span style={{ marginLeft: '1rem' }}>Inapakia hati...</span>
        </LoadingSpinner>
      </DocumentContainer>
    );
  }

  return (
    <DocumentContainer>
      <DocumentHeader>
        <DocumentTitle>Usimamizi wa Hati</DocumentTitle>
        <DocumentSubtitle>
          Pakia, thibitisha na usimamize hati zako za kidijitali
        </DocumentSubtitle>
      </DocumentHeader>

      <UploadSection>
        <UploadArea
          isDragOver={dragOver}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          onClick={() => document.getElementById('fileInput').click()}
          whileHover={{ scale: 1.02 }}
        >
          <UploadIcon>📁</UploadIcon>
          <UploadText>
            {selectedFile ? selectedFile.name : 'Bonyeza au vuta faili hapa'}
          </UploadText>
          <UploadSubtext>
            Aina za faili zinazokubalika: PDF, JPG, PNG (Kiwango cha juu: 10MB)
          </UploadSubtext>
        </UploadArea>

        <HiddenInput
          id="fileInput"
          type="file"
          accept=".pdf,.jpg,.jpeg,.png"
          onChange={handleFileSelect}
        />

        <DocumentTypeSelect
          value={documentType}
          onChange={(e) => setDocumentType(e.target.value)}
        >
          <option value="">Chagua aina ya hati</option>
          {documentTypes.map((type) => (
            <option key={type.value} value={type.value}>
              {type.label}
            </option>
          ))}
        </DocumentTypeSelect>

        <UploadButton
          onClick={handleUpload}
          disabled={!selectedFile || !documentType || uploading}
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
        >
          {uploading ? 'Inapakia...' : 'Pakia Hati'}
        </UploadButton>
      </UploadSection>

      <DocumentsList>
        <h3 style={{ 
          color: '#2C3E50', 
          marginBottom: '1rem', 
          textAlign: 'center' 
        }}>
          Hati Zako ({documents.length})
        </h3>

        {documents.length === 0 ? (
          <EmptyState>
            <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>📄</div>
            <p>Hakuna hati bado. Pakia hati yako ya kwanza!</p>
          </EmptyState>
        ) : (
          <AnimatePresence>
            {documents.map((document) => (
              <DocumentItem
                key={document.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                transition={{ duration: 0.3 }}
              >
                <DocumentInfo>
                  <DocumentIcon>
                    {getDocumentIcon(document.document_type)}
                  </DocumentIcon>
                  <DocumentDetails>
                    <DocumentName>{document.title_swahili}</DocumentName>
                    <DocumentMeta>
                      <span>{document.document_type.replace('_', ' ').toUpperCase()}</span>
                      <span>{new Date(document.created_at).toLocaleDateString('sw-KE')}</span>
                      <DocumentStatus status={document.is_verified ? 'verified' : 'pending'}>
                        {getStatusColor(document.is_verified ? 'verified' : 'pending')}
                      </DocumentStatus>
                    </DocumentMeta>
                  </DocumentDetails>
                </DocumentInfo>

                <DocumentActions>
                  <ActionButton
                    className="download"
                    onClick={() => handleDownload(document)}
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                  >
                    📥 Pakua
                  </ActionButton>
                  {!document.is_verified && (
                    <ActionButton
                      className="verify"
                      onClick={() => handleVerify(document)}
                      whileHover={{ scale: 1.05 }}
                      whileTap={{ scale: 0.95 }}
                    >
                      ✅ Thibitisha
                    </ActionButton>
                  )}
                  <ActionButton
                    className="delete"
                    onClick={() => handleDelete(document)}
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                  >
                    🗑️ Futa
                  </ActionButton>
                </DocumentActions>
              </DocumentItem>
            ))}
          </AnimatePresence>
        )}
      </DocumentsList>
    </DocumentContainer>
  );
};

export default DocumentManager;

