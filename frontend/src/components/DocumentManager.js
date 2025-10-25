import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import { motion, AnimatePresence } from 'framer-motion';
import axios from 'axios';
import toast from 'react-hot-toast';
import { ethers } from 'ethers';
import DocumentVerification from '../abi/DocumentVerification.json';

// Styled Components
const WalletSection = styled.div`
  display: flex;
  justify-content: flex-end;
  margin-bottom: 1rem;
`;

const WalletAddress = styled.span`
  background: rgba(255, 255, 255, 0.1);
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.9rem;
  color: white;
  margin-left: 1rem;
`;

const WalletButton = styled(motion.button)`
  padding: 0.8rem 1.5rem;
  background: ${props => props.connected ? props.theme.colors.success : props.theme.colors.gradient.primary};
  color: ${props => props.theme.colors.white};
  border: none;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  
  &:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  }
  
  &:disabled {
    opacity: 0.7;
    cursor: not-allowed;
    transform: none;
  }
`;

const DocumentContainer = styled.div`
  max-width: 1000px;
  margin: 0 auto;
  padding: 2rem;
`;

const DocumentHeader = styled.div`
  text-align: center;
  margin-bottom: 3rem;
  color: ${props => props.theme.colors.text};
  
  h1 {
    background: ${props => props.theme.colors.gradient.primary};
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 700;
    margin-bottom: 1rem;
  }
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
  background: ${props => props.theme.colors.surface};
  border-radius: 16px;
  padding: 2.5rem;
  margin-bottom: 2.5rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  border: 1px solid ${props => props.theme.colors.lightGray};
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  }
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
  background: ${props => props.theme.colors.surface};
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  border: 1px solid ${props => props.theme.colors.lightGray};
`;

const DocumentItem = styled(motion.div)`
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.25rem;
  border: 1px solid ${props => props.theme.colors.lightGray};
  border-radius: 12px;
  margin-bottom: 1rem;
  background: ${props => props.theme.colors.surface};
  transition: all 0.3s ease;
  
  &:hover {
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    transform: translateY(-2px);
    border-color: ${props => props.theme.colors.primary};
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
  padding: 0.625rem 1.25rem;
  border: none;
  border-radius: 8px;
  font-size: 0.9rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  
  &.download {
    background: ${props => props.theme.colors.gradient.primary};
    color: ${props => props.theme.colors.white};
  }
  
  &.verify {
    background: ${props => props.theme.colors.gradient.accent};
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

  const handleNotarize = async (document) => {
    if (!signer) {
      toast.error('Tafadhali unganisha pochi yako kwanza');
      return;
    }

    try {
      setUploading(true);
      const contractAddress = process.env.REACT_APP_CONTRACT_ADDRESS;
      const contract = new ethers.Contract(contractAddress, DocumentVerification.abi, signer);
      
      toast.loading('Inathibitisha hati kwenye blockchain...');
      const tx = await contract.notarizeDocument(document.id, document.file_hash);
      await tx.wait();
      
      // Update backend with transaction hash
      const response = await axios.post('/api/blockchain/verifications/notarize_document/', {
        document_id: document.id,
        tx_hash: tx.hash
      });

      if (response.data.success) {
        toast.success('Hati imethibitishwa kwenye blockchain!');
        fetchDocuments();
      } else {
        toast.error('Haikuwezekana kuthibitisha kwenye blockchain');
      }
    } catch (error) {
      console.error('Error notarizing document:', error);
      if (error.code === 4001) {
        toast.error('Umetengua ombi la MetaMask');
      } else {
        toast.error('Kuna tatizo la kuthibitisha kwenye blockchain');
      }
    } finally {
      setUploading(false);
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


  const [walletConnected, setWalletConnected] = useState(false);
  const [walletAddress, setWalletAddress] = useState('');
  const [signer, setSigner] = useState(null);

  const connectWallet = async () => {
    if (!window.ethereum) {
      toast.error('Tafadhali weka MetaMask ili kutumia blockchain');
      return;
    }

    try {
      await window.ethereum.request({ method: 'eth_requestAccounts' });
      const provider = new ethers.providers.Web3Provider(window.ethereum);
      const currentSigner = provider.getSigner();
      const address = await currentSigner.getAddress();
      
      setSigner(currentSigner);
      setWalletAddress(address);
      setWalletConnected(true);
      toast.success('Pochi imeunganishwa kwa mafanikio!');
    } catch (error) {
      console.error('Error connecting wallet:', error);
      toast.error('Imeshindwa kuunganisha pochi');
    }
  };

  useEffect(() => {
    const checkWalletConnection = async () => {
      if (window.ethereum) {
        try {
          const provider = new ethers.providers.Web3Provider(window.ethereum);
          const accounts = await provider.listAccounts();
          if (accounts.length > 0) {
            const currentSigner = provider.getSigner();
            const address = await currentSigner.getAddress();
            setSigner(currentSigner);
            setWalletAddress(address);
            setWalletConnected(true);
          }
        } catch (error) {
          console.error('Error checking wallet connection:', error);
        }
      }
    };

    checkWalletConnection();

    if (window.ethereum) {
      window.ethereum.on('accountsChanged', (accounts) => {
        if (accounts.length === 0) {
          setWalletConnected(false);
          setWalletAddress('');
          setSigner(null);
        } else {
          checkWalletConnection();
        }
      });
    }

    return () => {
      if (window.ethereum) {
        window.ethereum.removeAllListeners('accountsChanged');
      }
    };
  }, []);

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
        <WalletSection>
          <WalletButton
            onClick={connectWallet}
            connected={walletConnected}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
          >
            {walletConnected ? (
              <>
                <span>Imeunganishwa</span>
                <WalletAddress>{`${walletAddress.slice(0, 6)}...${walletAddress.slice(-4)}`}</WalletAddress>
              </>
            ) : (
              'Unganisha Pochi'
            )}
          </WalletButton>
        </WalletSection>
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
                  {!document.blockchain_tx_hash && (
                    <ActionButton
                      className="verify"
                      onClick={() => handleNotarize(document)}
                      whileHover={{ scale: 1.05 }}
                      whileTap={{ scale: 0.95 }}
                    >
                      🔒 Thibitisha Kwenye Blockchain
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

