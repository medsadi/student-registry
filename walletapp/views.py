from django.shortcuts import render, redirect
from django.contrib import messages
from .blockchain_service import BlockchainService
from .diploma_blockchain_service import DiplomaBlockchainService

# ==========================================
# VIEW 1: PAGE D'ACCUEIL (ancien système)
# ==========================================
def home(request):
    """Page d'accueil avec formulaire simple (sans NFT)"""
    blockchain = BlockchainService()
    
    # Vérifier la connexion
    if not blockchain.is_connected():
        messages.error(request, "Impossible de se connecter à la blockchain")
    
    # Traitement du formulaire
    if request.method == 'POST':
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        date_naissance = request.POST.get('dateNaissance')
        moyenne = request.POST.get('moyenne')
        
        # Ajouter l'étudiant
        result = blockchain.add_student(nom, prenom, date_naissance, moyenne)
        
        if result['success']:
            messages.success(request, result['message'])
            messages.info(request, f"Transaction: {result['tx_hash']}")
        else:
            messages.error(request, result['message'])
    
    # Récupérer les données
    students = blockchain.get_all_students()
    total_students = blockchain.get_total_students()
    
    # Calculer les statistiques
    moyenne_generale = 0
    if students:
        moyenne_generale = sum(s['moyenne'] for s in students) / len(students)
    
    context = {
        'students': students,
        'total_students': total_students,
        'moyenne_generale': round(moyenne_generale, 2),
        'is_connected': blockchain.is_connected(),
        'CONTRACT_ADDRESS': blockchain.contract.address
    }
    
    return render(request, 'home.html', context)


# ==========================================
# VIEW 2: PAGE ADMIN DIPLOMES
# ==========================================
def admin_diploma(request):
    """Page d'administration pour gérer les diplômes NFT"""
    diploma_service = DiplomaBlockchainService()
    
    # Vérifier la connexion
    if not diploma_service.is_connected():
        messages.error(request, "Impossible de se connecter à la blockchain")
    
    # Récupérer tous les étudiants
    students = diploma_service.get_all_students()
    total_students = len(students)
    
    # Compter les diplômes mintés
    diplomas_minted = sum(1 for s in students if s['diplomaMinted'])
    
    context = {
        'students': students,
        'total_students': total_students,
        'diplomas_minted': diplomas_minted,
        'is_connected': diploma_service.is_connected()
    }
    
    return render(request, 'admin_diploma.html', context)


# ==========================================
# VIEW 3: AJOUTER UN ÉTUDIANT (avec adresse wallet)
# ==========================================
def add_student_admin(request):
    """Ajouter un étudiant avec son adresse MetaMask"""
    if request.method == 'POST':
        diploma_service = DiplomaBlockchainService()
        
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        date_naissance = request.POST.get('dateNaissance')
        moyenne = request.POST.get('moyenne')
        student_address = request.POST.get('studentAddress')
        
        # Validation de l'adresse Ethereum
        if not student_address or not student_address.startswith('0x') or len(student_address) != 42:
            messages.error(request, "Adresse MetaMask invalide")
            return redirect('blockchain:admin_diploma')
        
        # Ajouter l'étudiant
        result = diploma_service.add_student_with_address(
            nom, prenom, date_naissance, moyenne, student_address
        )
        
        if result['success']:
            messages.success(request, result['message'])
            messages.info(request, f"Transaction: {result['tx_hash']}")
            messages.info(request, f"Block: {result['block_number']}")
        else:
            messages.error(request, f"Erreur: {result['error']}")
    
    return redirect('blockchain:admin_diploma')


# ==========================================
# VIEW 4: MINT ET ENVOYER DIPLOME NFT
# ==========================================
def mint_diploma(request):
    """Créer un NFT diplôme et l'envoyer à l'étudiant"""
    if request.method == 'POST':
        diploma_service = DiplomaBlockchainService()
        
        student_id = request.POST.get('student_id')
        diploma_file = request.FILES.get('diploma_file')
        
        # Validation
        if not student_id:
            messages.error(request, "Veuillez sélectionner un étudiant")
            return redirect('blockchain:admin_diploma')
        
        if not diploma_file:
            messages.error(request, "Veuillez uploader un fichier PDF")
            return redirect('blockchain:admin_diploma')
        
        if not diploma_file.name.endswith('.pdf'):
            messages.error(request, "Le fichier doit être un PDF")
            return redirect('blockchain:admin_diploma')
        
        # Récupérer les données de l'étudiant
        try:
            student_data_raw = diploma_service.contract.functions.getStudent(int(student_id)).call()
            student_data = {
                'nom': student_data_raw[0],
                'prenom': student_data_raw[1],
                'date_naissance': student_data_raw[2],
                'moyenne': student_data_raw[3] / 100
            }
        except Exception as e:
            messages.error(request, f"Erreur lors de la récupération de l'étudiant: {str(e)}")
            return redirect('blockchain:admin_diploma')
        
        # Créer et envoyer le NFT
        messages.info(request, "⏳ Création du NFT en cours... Veuillez patienter (30-60 secondes)")
        
        result = diploma_service.mint_and_send_diploma(
            int(student_id),
            diploma_file,
            student_data
        )
        
        if result['success']:
            messages.success(request, result['message'])
            messages.success(request, f"📄 Diplôme IPFS: {result['diploma_ipfs_hash']}")
            messages.info(request, f"⛓️ Transaction: {result['tx_hash']}")
            messages.info(request, f"📦 Block: {result['block_number']}")
            messages.info(request, f"🔗 Voir sur IPFS: {result['diploma_url']}")
            
            if 'opensea_url' in result:
                messages.info(request, f"🎨 OpenSea: {result['opensea_url']}")
        else:
            messages.error(request, f"❌ Erreur: {result['error']}")
    
    return redirect('blockchain:admin_diploma')


# ==========================================
# VIEW 5: VOIR UN DIPLOME
# ==========================================
def view_diploma(request, student_id):
    """Afficher les détails d'un diplôme NFT"""
    diploma_service = DiplomaBlockchainService()
    
    try:
        # Récupérer les infos du diplôme
        diploma_info = diploma_service.get_diploma_info(student_id)
        
        if not diploma_info['has_diploma']:
            messages.error(request, "Cet étudiant n'a pas encore de diplôme")
            return redirect('blockchain:admin_diploma')
        
        # Récupérer les données de l'étudiant
        student_data = diploma_service.contract.functions.getStudent(student_id).call()
        
        context = {
            'student_id': student_id,
            'nom': student_data[0],
            'prenom': student_data[1],
            'date_naissance': student_data[2],
            'moyenne': student_data[3] / 100,
            'diploma_uri': diploma_info['diploma_uri'],
            'ipfs_url': diploma_info['ipfs_url']
        }
        
        return render(request, 'view_diploma.html', context)
    
    except Exception as e:
        messages.error(request, f"Erreur: {str(e)}")
        return redirect('blockchain:admin_diploma')


# ==========================================
# VIEW 6: PORTFOLIO ÉTUDIANT
# ==========================================
def student_portfolio(request):
    """Page où l'étudiant peut voir ses diplômes NFT"""
    # Cette vue nécessitera l'authentification de l'étudiant
    # Pour l'instant, c'est une page simple
    
    context = {
        'message': 'Connectez votre wallet MetaMask pour voir vos diplômes'
    }
    
    return render(request, 'student_portfolio.html', context)