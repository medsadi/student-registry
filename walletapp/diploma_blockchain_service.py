from web3 import Web3
from django.conf import settings
from .contract import DIPLOMA_CONTRACT_ABI
from .ipfs_service import IPFSService
from datetime import datetime

class DiplomaBlockchainService:
    """Service pour gérer les diplômes NFT sur la blockchain"""
    
    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider(settings.ALCHEMY_URL))
        self.contract = self.w3.eth.contract(
            address=settings.DIPLOMA_CONTRACT_ADDRESS,
            abi=DIPLOMA_CONTRACT_ABI
        )
        self.ipfs_service = IPFSService(
            api_key=settings.PINATA_API_KEY,
            api_secret=settings.PINATA_API_SECRET
        )
    
    def is_connected(self):
        """Vérifier la connexion blockchain"""
        return self.w3.is_connected()
    
    def add_student_with_address(self, nom, prenom, date_naissance, moyenne, student_address):
        """
        Ajouter un étudiant avec son adresse wallet
        
        Args:
            student_address: Adresse MetaMask de l'étudiant
        """
        try:
            # 🔧 CORRECTION: Convertir en checksum address
            student_address = Web3.to_checksum_address(student_address)
            
            moyenne_int = int(float(moyenne) * 100)
            
            nonce = self.w3.eth.get_transaction_count(settings.WALLET_ADDRESS)
            
            transaction = self.contract.functions.addStudent(
                nom,
                prenom,
                date_naissance,
                moyenne_int,
                student_address
            ).build_transaction({
                'from': settings.WALLET_ADDRESS,
                'gas': 500000,
                'gasPrice': self.w3.eth.gas_price,
                'nonce': nonce,
                'chainId': settings.CHAIN_ID
            })
            
            signed_txn = self.w3.eth.account.sign_transaction(
                transaction,
                settings.PRIVATE_KEY
            )
            
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.raw_transaction)
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            
            return {
                'success': True,
                'tx_hash': tx_hash.hex(),
                'block_number': receipt['blockNumber'],
                'message': f'Étudiant {prenom} {nom} ajouté avec succès!'
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def mint_and_send_diploma(self, student_id, diploma_file, student_data):
        """
        Créer un NFT diplôme et l'envoyer à l'étudiant
        
        Process:
        1. Upload PDF vers IPFS
        2. Créer métadonnées NFT
        3. Upload métadonnées vers IPFS
        4. Mint NFT sur la blockchain
        5. NFT est automatiquement envoyé au wallet de l'étudiant
        """
        try:
            # 1. Upload PDF du diplôme vers IPFS
            print("📤 Upload du diplôme vers IPFS...")
            
            file_metadata = {
                'filename': f"diplome_{student_data['nom']}_{student_data['prenom']}.pdf",
                'nom': student_data['nom'],
                'prenom': student_data['prenom'],
                'date': student_data['date_naissance']
            }
            
            ipfs_result = self.ipfs_service.upload_file(diploma_file, file_metadata)
            
            if not ipfs_result['success']:
                return {
                    'success': False,
                    'error': 'Erreur upload IPFS: ' + ipfs_result.get('error', 'Unknown')
                }
            
            diploma_ipfs_hash = ipfs_result['ipfs_hash']
            print(f"✅ Diplôme uploadé: {diploma_ipfs_hash}")
            
            # 2. Créer métadonnées NFT
            print("📝 Création des métadonnées NFT...")
            
            nft_metadata = self.ipfs_service.create_nft_metadata(
                student_data={
                    'nom': student_data['nom'],
                    'prenom': student_data['prenom'],
                    'date_naissance': student_data['date_naissance'],
                    'moyenne': student_data['moyenne'],
                    'date_emission': datetime.now().strftime('%d/%m/%Y')
                },
                diploma_ipfs_hash=diploma_ipfs_hash
            )
            
            # 3. Upload métadonnées vers IPFS
            metadata_result = self.ipfs_service.upload_json_metadata(nft_metadata)
            
            if not metadata_result['success']:
                return {
                    'success': False,
                    'error': 'Erreur upload métadonnées: ' + metadata_result.get('error', 'Unknown')
                }
            
            metadata_ipfs_hash = metadata_result['ipfs_hash']
            print(f"✅ Métadonnées uploadées: {metadata_ipfs_hash}")
            
            # 4. Mint NFT sur la blockchain
            print("⛓️ Mint du NFT sur la blockchain...")
            
            nonce = self.w3.eth.get_transaction_count(settings.WALLET_ADDRESS)
            
            transaction = self.contract.functions.mintDiploma(
                student_id,
                metadata_ipfs_hash
            ).build_transaction({
                'from': settings.WALLET_ADDRESS,
                'gas': 500000,
                'gasPrice': self.w3.eth.gas_price,
                'nonce': nonce,
                'chainId': settings.CHAIN_ID
            })
            
            signed_txn = self.w3.eth.account.sign_transaction(
                transaction,
                settings.PRIVATE_KEY
            )
            
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.raw_transaction)
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            
            print(f"✅ NFT minté! Transaction: {tx_hash.hex()}")
            
            return {
                'success': True,
                'tx_hash': tx_hash.hex(),
                'block_number': receipt['blockNumber'],
                'diploma_ipfs_hash': diploma_ipfs_hash,
                'metadata_ipfs_hash': metadata_ipfs_hash,
                'diploma_url': ipfs_result['url'],
                'opensea_url': self.get_opensea_url(receipt),
                'message': f'Diplôme NFT créé et envoyé avec succès!'
            }
        
        except Exception as e:
            print(f"❌ Erreur: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_all_students(self):
        """Récupérer tous les étudiants"""
        try:
            student_ids = self.contract.functions.getAllStudentIds().call()
            students = []
            
            for student_id in student_ids:
                student_data = self.contract.functions.getStudent(student_id).call()
                students.append({
                    'id': student_id,
                    'nom': student_data[0],
                    'prenom': student_data[1],
                    'dateNaissance': student_data[2],
                    'moyenne': student_data[3] / 100,
                    'diplomaMinted': student_data[4],
                    'diplomaTokenId': student_data[5]
                })
            
            return students
        except Exception as e:
            print(f"Erreur récupération: {e}")
            return []
    
    def get_diploma_info(self, student_id):
        """Obtenir les informations du diplôme d'un étudiant"""
        try:
            has_diploma = self.contract.functions.hasDiploma(student_id).call()
            
            if not has_diploma:
                return {
                    'has_diploma': False
                }
            
            diploma_uri = self.contract.functions.getDiplomaURI(student_id).call()
            
            return {
                'has_diploma': True,
                'diploma_uri': diploma_uri,
                'ipfs_url': diploma_uri.replace('ipfs://', 'https://gateway.pinata.cloud/ipfs/')
            }
        
        except Exception as e:
            return {
                'has_diploma': False,
                'error': str(e)
            }
    
    def get_opensea_url(self, receipt):
        """Générer l'URL OpenSea pour le NFT"""
        contract_address = settings.DIPLOMA_CONTRACT_ADDRESS
        return f"https://testnets.opensea.io/assets/amoy/{contract_address}"