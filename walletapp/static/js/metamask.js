// ==========================================
// METAMASK AUTO-CONNECT
// ==========================================

let userAccount = null;
let web3 = null;

// 🔥 AUTO-CONNECT au chargement de la page
document.addEventListener('DOMContentLoaded', async function() {
    await autoConnectMetaMask();
});

// Fonction de connexion automatique
async function autoConnectMetaMask() {
    const statusDiv = document.getElementById('metamaskStatus');
    const modalDiv = document.getElementById('metamaskModal');
    
    if (typeof window.ethereum !== 'undefined') {
        console.log('✅ MetaMask détecté!');
        web3 = window.ethereum;
        
        // 🔥 CONNEXION AUTOMATIQUE
        try {
            statusDiv.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Auto-connecting...';
            
            // Demander la connexion automatiquement
            const accounts = await ethereum.request({ method: 'eth_requestAccounts' });
            
            if (accounts.length > 0) {
                userAccount = accounts[0];
                
                // Obtenir le réseau
                const chainId = await ethereum.request({ method: 'eth_chainId' });
                const networkName = getNetworkName(chainId);
                
                // Mettre à jour l'interface
                statusDiv.innerHTML = `
                    <i class="fas fa-circle pulse"></i> ${networkName}
                `;
                
                const walletInfo = document.getElementById('walletInfo');
                const walletAddress = document.getElementById('walletAddress');
                
                if (walletInfo && walletAddress) {
                    walletAddress.textContent = formatAddress(userAccount);
                    walletInfo.style.display = 'block';
                }
                
                console.log('✅ Auto-connecté:', userAccount);
                showMetaMaskNotification('MetaMask connected successfully!', 'success');
            }
        } catch (error) {
            console.error('❌ Erreur auto-connexion:', error);
            
            // Si l'utilisateur refuse, afficher bouton
            statusDiv.innerHTML = `
                <i class="fas fa-wallet"></i> MetaMask Detected
                <button class="btn-small btn-primary" onclick="connectWallet()">
                    Connect Wallet
                </button>
            `;
        }
        
        // Écouter les changements
        ethereum.on('accountsChanged', handleAccountsChanged);
        ethereum.on('chainChanged', handleChainChanged);
        
    } else {
        console.log('❌ MetaMask NON installé');
        
        // Afficher modal d'installation
        statusDiv.innerHTML = `
            <i class="fas fa-exclamation-triangle"></i> MetaMask Required
        `;
        
        if (modalDiv) {
            modalDiv.style.display = 'flex';
        }
    }
}

// Connexion manuelle (si auto-connexion échoue)
async function connectWallet() {
    const statusDiv = document.getElementById('metamaskStatus');
    const walletInfo = document.getElementById('walletInfo');
    const walletAddress = document.getElementById('walletAddress');
    
    try {
        statusDiv.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Connecting...';
        
        const accounts = await ethereum.request({ method: 'eth_requestAccounts' });
        userAccount = accounts[0];
        
        const chainId = await ethereum.request({ method: 'eth_chainId' });
        const networkName = getNetworkName(chainId);
        
        statusDiv.innerHTML = `
            <i class="fas fa-circle pulse"></i> ${networkName}
        `;
        
        if (walletInfo && walletAddress) {
            walletAddress.textContent = formatAddress(userAccount);
            walletInfo.style.display = 'block';
        }
        
        console.log('✅ Connecté:', userAccount);
        showMetaMaskNotification('Connected successfully!', 'success');
        
        return userAccount;
        
    } catch (error) {
        console.error('❌ Erreur connexion:', error);
        
        statusDiv.innerHTML = `
            <i class="fas fa-exclamation-triangle"></i> Connection Failed
            <button class="btn-small btn-primary" onclick="connectWallet()">
                Retry
            </button>
        `;
        
        showMetaMaskNotification('Connection failed: ' + error.message, 'error');
    }
}

// Gérer changement de compte
function handleAccountsChanged(accounts) {
    if (accounts.length === 0) {
        console.log('❌ Déconnecté de MetaMask');
        userAccount = null;
        location.reload();
    } else if (accounts[0] !== userAccount) {
        userAccount = accounts[0];
        console.log('🔄 Compte changé:', userAccount);
        location.reload();
    }
}

// Gérer changement de réseau
function handleChainChanged(chainId) {
    console.log('🔄 Réseau changé:', chainId);
    location.reload();
}

// Obtenir le nom du réseau
function getNetworkName(chainId) {
    const networks = {
        '0x1': 'Ethereum Mainnet',
        '0x89': 'Polygon Mainnet',
        '0x13882': 'Polygon Amoy Testnet',
        '0xaa36a7': 'Sepolia Testnet',
        '0x5': 'Goerli Testnet'
    };
    return networks[chainId] || `Chain ${chainId}`;
}

// Formater l'adresse
function formatAddress(address) {
    return `${address.substring(0, 6)}...${address.substring(38)}`;
}

// Afficher modal de confirmation
function showConfirmationModal() {
    const modal = document.getElementById('confirmationModal');
    if (modal) {
        modal.style.display = 'flex';
    }
}

// Cacher modal de confirmation
function hideConfirmationModal() {
    const modal = document.getElementById('confirmationModal');
    if (modal) {
        modal.style.display = 'none';
    }
}

// Notification MetaMask
function showMetaMaskNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} glass-effect metamask-notification`;
    
    const icon = type === 'success' ? 'check-circle' : 
                 type === 'error' ? 'exclamation-circle' : 'info-circle';
    
    notification.innerHTML = `
        <i class="fas fa-${icon}"></i>
        <span>${message}</span>
    `;
    
    notification.style.position = 'fixed';
    notification.style.top = '100px';
    notification.style.right = '20px';
    notification.style.zIndex = '10001';
    notification.style.minWidth = '300px';
    notification.style.animation = 'slideIn 0.3s ease';
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 4000);
}

// ==========================================
// VIEW DIPLOMA FUNCTION - FIXED VERSION
// ==========================================
function viewDiploma(studentId) {
    console.log('🔍 Viewing diploma for student:', studentId);
    
    // Get the base URL dynamically
    const baseUrl = window.location.origin;
    const diplomaUrl = `${baseUrl}/admin/diploma/${studentId}/`;
    
    console.log('📍 Redirecting to:', diplomaUrl);
    
    // Redirect to the diploma view page
    window.location.href = diplomaUrl;
}

// Intercepter soumissions de formulaires
document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            showConfirmationModal();
        });
    });
});

// Styles CSS
const style = document.createElement('style');
style.textContent = `
    .metamask-modal {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.8);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 10000;
        backdrop-filter: blur(10px);
    }
    
    .modal-content {
        max-width: 500px;
        padding: 40px;
        text-align: center;
    }
    
    .modal-header {
        margin-bottom: 24px;
    }
    
    .modal-header i {
        font-size: 4em;
        color: var(--gold);
        margin-bottom: 16px;
    }
    
    .modal-header h2 {
        font-size: 2em;
        color: var(--text-primary);
    }
    
    .modal-body {
        color: var(--text-secondary);
        line-height: 1.8;
    }
    
    .modal-body p {
        margin-bottom: 16px;
    }
    
    .modal-body .btn {
        margin-top: 24px;
    }
    
    .loading-spinner {
        width: 60px;
        height: 60px;
        border: 4px solid rgba(212, 175, 55, 0.2);
        border-top: 4px solid var(--gold);
        border-radius: 50%;
        animation: spin 1s linear infinite;
        margin: 0 auto 24px;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(500px);
            opacity: 0;
        }
    }
    
    .wallet-info {
        margin-top: 10px;
    }
    
    .wallet-address {
        font-family: monospace;
        background: rgba(212, 175, 55, 0.1);
        padding: 6px 12px;
        border-radius: 8px;
        font-size: 0.9em;
        color: var(--gold);
        border: 1px solid rgba(212, 175, 55, 0.3);
    }
    
    .btn-small {
        padding: 8px 16px;
        font-size: 0.9em;
        border: none;
        border-radius: 8px;
        cursor: pointer;
        font-weight: 600;
        transition: all 0.3s ease;
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }
    
    .btn-small.btn-primary {
        background: linear-gradient(135deg, var(--dark-blue), var(--secondary-navy));
        color: var(--gold);
        border: 1px solid var(--gold);
    }
    
    .btn-small.btn-info {
        background: rgba(6, 182, 212, 0.2);
        color: var(--info);
        border: 1px solid var(--info);
    }
    
    .btn-small:hover {
        transform: translateY(-2px);
    }
    
    .diploma-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 0.9em;
        font-weight: 600;
    }
    
    .diploma-badge.minted {
        background: rgba(16, 185, 129, 0.2);
        color: var(--success);
        border: 1px solid var(--success);
    }
    
    .diploma-badge.pending {
        background: rgba(245, 158, 11, 0.2);
        color: var(--warning);
        border: 1px solid var(--warning);
    }
    
    .form-help {
        font-size: 0.85em;
        color: var(--text-muted);
        margin-top: 4px;
    }
    
    .upload-info {
        padding: 20px;
        margin: 20px 0;
        border-left: 3px solid var(--info);
    }
    
    .upload-info i {
        color: var(--info);
        font-size: 1.5em;
        margin-bottom: 12px;
    }
    
    .upload-info strong {
        color: var(--text-primary);
        display: block;
        margin-bottom: 8px;
    }
    
    .upload-info p {
        color: var(--text-secondary);
        font-size: 0.9em;
        line-height: 1.6;
    }
    
    .metamask-status {
        display: flex;
        flex-direction: column;
        align-items: flex-end;
        gap: 10px;
    }
    
    .admin-button {
        position: fixed;
        bottom: 30px;
        right: 30px;
        z-index: 999;
        padding: 16px 24px;
        background: linear-gradient(135deg, var(--gold), var(--gold-light));
        color: var(--primary-navy);
        border: none;
        border-radius: 50px;
        font-weight: 700;
        font-size: 1.1em;
        cursor: pointer;
        box-shadow: 0 8px 24px rgba(212, 175, 55, 0.4);
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .admin-button:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 32px rgba(212, 175, 55, 0.6);
    }
`;
document.head.appendChild(style);