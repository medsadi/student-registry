from web3 import Web3
from django.conf import settings
from .contract import CONTRACT_ABI

class BlockchainService:
    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider(settings.ALCHEMY_URL))
        self.contract = self.w3.eth.contract(
            address=settings.CONTRACT_ADDRESS,
            abi=CONTRACT_ABI
        )
    
    def is_connected(self):
        """Vérifier la connexion à la blockchain"""
        return self.w3.is_connected()
    
    def get_all_students(self):
        """Récupérer tous les étudiants depuis la blockchain"""
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
                    'moyenne': student_data[3] / 100
                })
            
            return students
        except Exception as e:
            print(f"Erreur lors de la récupération: {e}")
            return []
    
    def get_total_students(self):
        """Obtenir le nombre total d'étudiants"""
        try:
            return self.contract.functions.getTotalStudents().call()
        except:
            return 0
    
    def add_student(self, nom, prenom, date_naissance, moyenne):
        """Ajouter un étudiant sur la blockchain"""
        try:
            moyenne_int = int(float(moyenne) * 100)
            
            nonce = self.w3.eth.get_transaction_count(settings.WALLET_ADDRESS)
            
            transaction = self.contract.functions.addStudent(
                nom, prenom, date_naissance, moyenne_int
            ).build_transaction({
                'from': settings.WALLET_ADDRESS,
                'gas': 300000,
                'gasPrice': self.w3.eth.gas_price,
                'nonce': nonce,
                'chainId': settings.CHAIN_ID
            })
            
            signed_txn = self.w3.eth.account.sign_transaction(
                transaction, 
                settings.PRIVATE_KEY
            )
            
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.raw_transaction)
            
            return {
                'success': True,
                'tx_hash': tx_hash.hex(),
                'message': f'Étudiant {prenom} {nom} ajouté avec succès!'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': f'Erreur: {str(e)}'
            }