import requests
import json
from django.core.files.uploadedfile import UploadedFile

class IPFSService:
    """Service pour uploader des fichiers vers IPFS via Pinata"""
    
    def __init__(self, api_key=None, api_secret=None):
        # Configuration Pinata (service IPFS gratuit)
        self.api_key = api_key or "YOUR_PINATA_API_KEY"
        self.api_secret = api_secret or "YOUR_PINATA_API_SECRET"
        self.pinata_url = "https://api.pinata.cloud/pinning/pinFileToIPFS"
        self.gateway_url = "https://gateway.pinata.cloud/ipfs/"
    
    def upload_file(self, file: UploadedFile, metadata: dict = None) -> dict:
        """
        Upload un fichier vers IPFS
        
        Args:
            file: Fichier uploadé (PDF du diplôme)
            metadata: Métadonnées additionnelles (nom, prénom, date)
        
        Returns:
            dict: {'success': bool, 'ipfs_hash': str, 'url': str}
        """
        try:
            headers = {
                'pinata_api_key': self.api_key,
                'pinata_secret_api_key': self.api_secret
            }
            
            # Préparer les métadonnées
            pinata_metadata = {
                'name': metadata.get('filename', 'diploma.pdf'),
                'keyvalues': {
                    'nom': metadata.get('nom', ''),
                    'prenom': metadata.get('prenom', ''),
                    'date': metadata.get('date', ''),
                    'type': 'diploma'
                }
            }
            
            files = {
                'file': (file.name, file.read(), file.content_type),
                'pinataMetadata': (None, json.dumps(pinata_metadata), 'application/json')
            }
            
            response = requests.post(
                self.pinata_url,
                headers=headers,
                files=files
            )
            
            if response.status_code == 200:
                result = response.json()
                ipfs_hash = result['IpfsHash']
                
                return {
                    'success': True,
                    'ipfs_hash': ipfs_hash,
                    'url': f"{self.gateway_url}{ipfs_hash}",
                    'pinata_response': result
                }
            else:
                return {
                    'success': False,
                    'error': f"Erreur Pinata: {response.status_code}",
                    'message': response.text
                }
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def upload_json_metadata(self, metadata: dict) -> dict:
        """
        Upload des métadonnées JSON vers IPFS
        Utilisé pour créer le metadata.json du NFT
        """
        try:
            headers = {
                'pinata_api_key': self.api_key,
                'pinata_secret_api_key': self.api_secret,
                'Content-Type': 'application/json'
            }
            
            url = "https://api.pinata.cloud/pinning/pinJSONToIPFS"
            
            response = requests.post(
                url,
                headers=headers,
                json={
                    'pinataContent': metadata,
                    'pinataMetadata': {
                        'name': 'diploma_metadata.json'
                    }
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    'success': True,
                    'ipfs_hash': result['IpfsHash'],
                    'url': f"{self.gateway_url}{result['IpfsHash']}"
                }
            else:
                return {
                    'success': False,
                    'error': response.text
                }
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def create_nft_metadata(self, student_data: dict, diploma_ipfs_hash: str) -> dict:
        """
        Créer les métadonnées NFT au format ERC721
        
        Args:
            student_data: Données de l'étudiant
            diploma_ipfs_hash: Hash IPFS du PDF du diplôme
        
        Returns:
            dict: Métadonnées NFT formatées
        """
        metadata = {
            "name": f"Diplôme - {student_data['prenom']} {student_data['nom']}",
            "description": f"Diplôme officiel de {student_data['prenom']} {student_data['nom']} - Moyenne: {student_data['moyenne']}/20",
            "image": f"ipfs://{diploma_ipfs_hash}",
            "attributes": [
                {
                    "trait_type": "Nom",
                    "value": student_data['nom']
                },
                {
                    "trait_type": "Prénom",
                    "value": student_data['prenom']
                },
                {
                    "trait_type": "Date de Naissance",
                    "value": student_data['date_naissance']
                },
                {
                    "trait_type": "Moyenne Générale",
                    "value": student_data['moyenne']
                },
                {
                    "trait_type": "Date d'Émission",
                    "value": student_data.get('date_emission', '')
                }
            ],
            "external_url": f"ipfs://{diploma_ipfs_hash}"
        }
        
        return metadata