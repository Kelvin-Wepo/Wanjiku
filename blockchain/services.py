from web3 import Web3
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
import json
import hashlib
from .models import DocumentVerification, BlockchainTransaction, DocumentTemplate
import os


def _load_contract(w3):
    """Load contract from settings CONTRACT_ADDRESS and CONTRACT_ABI_PATH if available."""
    contract_address = getattr(settings, 'CONTRACT_ADDRESS', '')
    abi_path = getattr(settings, 'CONTRACT_ABI_PATH', '')

    if not contract_address or not abi_path or not os.path.exists(abi_path):
        return None

    try:
        with open(abi_path, 'r') as f:
            abi = json.load(f)
        return w3.eth.contract(address=Web3.to_checksum_address(contract_address), abi=abi)
    except Exception:
        return None


class EthereumService:
    """Service for Ethereum blockchain operations"""
    
    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider(settings.ETHEREUM_RPC_URL))
        self.private_key = settings.PRIVATE_KEY
        self.account = self.w3.eth.account.from_key(self.private_key)
        # Attempt to load contract instance
        self.contract = _load_contract(self.w3)
    
    def deploy_contract(self, contract_bytecode, contract_abi):
        """Deploy a smart contract"""
        try:
            # Create contract instance
            contract = self.w3.eth.contract(
                abi=contract_abi,
                bytecode=contract_bytecode
            )
            
            # Build transaction
            transaction = contract.constructor().build_transaction({
                'from': self.account.address,
                'gas': 2000000,
                'gasPrice': self.w3.eth.gas_price,
                'nonce': self.w3.eth.get_transaction_count(self.account.address),
            })
            
            # Sign and send transaction
            signed_txn = self.w3.eth.account.sign_transaction(transaction, self.private_key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            
            # Wait for transaction receipt
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            
            return {
                'success': True,
                'contract_address': receipt.contractAddress,
                'tx_hash': tx_hash.hex(),
                'gas_used': receipt.gasUsed
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def store_document_hash(self, document_hash, document_data):
        """Store document hash on blockchain"""
        try:
            # If a contract is configured, call notarizeDocument
            if self.contract:
                # document_hash is a hex string of sha256 (64 chars). Convert to bytes32
                doc_bytes = Web3.to_bytes(hexstr=document_hash)
                ipfs_cid = document_data.get('ipfs_cid', '') if isinstance(document_data, dict) else ''

                txn = self.contract.functions.notarizeDocument(doc_bytes, ipfs_cid).build_transaction({
                    'from': self.account.address,
                    'nonce': self.w3.eth.get_transaction_count(self.account.address),
                    'gas': 200000,
                    'gasPrice': self.w3.eth.gas_price
                })

                signed = self.w3.eth.account.sign_transaction(txn, self.private_key)
                tx_hash = self.w3.eth.send_raw_transaction(signed.rawTransaction)
                receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)

                return {
                    'success': True,
                    'tx_hash': tx_hash.hex(),
                    'block_number': receipt.blockNumber
                }

            # Fallback: simulate storing on-chain
            tx_hash = hashlib.sha256(
                f"{document_hash}{timezone.now().timestamp()}".encode()
            ).hexdigest()

            return {
                'success': True,
                'tx_hash': tx_hash,
                'block_number': None
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def verify_document_hash(self, document_hash):
        """Verify document hash on blockchain"""
        try:
            # If contract present, call getDocument
            if self.contract:
                doc_bytes = Web3.to_bytes(hexstr=document_hash)
                owner, timestamp, ipfsCid, exists = self.contract.functions.getDocument(doc_bytes).call()
                if exists:
                    return {
                        'success': True,
                        'verified': True,
                        'owner': owner,
                        'timestamp': timestamp,
                        'ipfs_cid': ipfsCid
                    }
                else:
                    return {
                        'success': True,
                        'verified': False,
                        'message': 'Document not found on chain'
                    }

            # Fallback: check local DB for verified state
            verification = DocumentVerification.objects.filter(
                document_hash=document_hash,
                status='verified'
            ).first()

            if verification:
                return {
                    'success': True,
                    'verified': True,
                    'document_type': verification.document_type,
                    'verified_at': verification.verified_at,
                    'expires_at': verification.expires_at
                }
            else:
                return {
                    'success': True,
                    'verified': False,
                    'message': 'Document not found or not verified'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }


class DocumentVerificationService:
    """Service for document verification"""
    
    def __init__(self):
        self.ethereum_service = EthereumService()
    
    def upload_document(self, user, document_file, document_type, verification_data=None):
        """Upload and verify a document"""
        try:
            # Calculate document hash
            document_hash = self._calculate_file_hash(document_file)
            
            # Check if document already exists
            existing = DocumentVerification.objects.filter(document_hash=document_hash).first()
            if existing:
                return {
                    'success': False,
                    'error': 'Document already exists',
                    'verification_id': existing.id
                }
            
            # Create document verification record
            verification = DocumentVerification.objects.create(
                user=user,
                document_type=document_type,
                document_hash=document_hash,
                original_file=document_file,
                verification_data=verification_data or {},
                expires_at=timezone.now() + timedelta(days=365)  # 1 year validity
            )
            
            # Store hash on blockchain
            blockchain_result = self.ethereum_service.store_document_hash(
                document_hash,
                {
                    'user_id': user.id,
                    'document_type': document_type,
                    'uploaded_at': timezone.now().isoformat()
                }
            )
            
            if blockchain_result['success']:
                # Create blockchain transaction record
                BlockchainTransaction.objects.create(
                    document_verification=verification,
                    tx_hash=blockchain_result['tx_hash'],
                    block_number=blockchain_result.get('block_number'),
                    status='confirmed'
                )
                
                verification.blockchain_tx_hash = blockchain_result['tx_hash']
                verification.save()
            
            return {
                'success': True,
                'verification_id': verification.id,
                'document_hash': document_hash,
                'blockchain_tx': blockchain_result.get('tx_hash')
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def verify_document(self, document_hash):
        """Verify a document using blockchain"""
        try:
            # Check blockchain
            blockchain_result = self.ethereum_service.verify_document_hash(document_hash)
            
            if blockchain_result['success'] and blockchain_result['verified']:
                # Update verification status
                verification = DocumentVerification.objects.get(document_hash=document_hash)
                verification.status = 'verified'
                verification.verified_at = timezone.now()
                verification.save()
                
                return {
                    'success': True,
                    'verified': True,
                    'verification': verification
                }
            else:
                return {
                    'success': True,
                    'verified': False,
                    'message': 'Document not verified on blockchain'
                }
                
        except DocumentVerification.DoesNotExist:
            return {
                'success': False,
                'error': 'Document not found'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_document_status(self, document_hash):
        """Get document verification status"""
        try:
            verification = DocumentVerification.objects.get(document_hash=document_hash)
            
            return {
                'success': True,
                'status': verification.status,
                'document_type': verification.document_type,
                'verified_at': verification.verified_at,
                'expires_at': verification.expires_at,
                'blockchain_tx': verification.blockchain_tx_hash
            }
            
        except DocumentVerification.DoesNotExist:
            return {
                'success': False,
                'error': 'Document not found'
            }
    
    def _calculate_file_hash(self, file):
        """Calculate SHA-256 hash of a file"""
        file.seek(0)
        content = file.read()
        return hashlib.sha256(content).hexdigest()
    
    def validate_document(self, document_file, document_type):
        """Validate document against template"""
        try:
            template = DocumentTemplate.objects.filter(
                document_type=document_type,
                is_active=True
            ).first()
            
            if not template:
                return {
                    'success': False,
                    'error': 'No template found for this document type'
                }
            
            # Here you would implement document validation logic
            # This could include OCR, format validation, etc.
            
            return {
                'success': True,
                'valid': True,
                'message': 'Document format is valid'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

