// static/js/metamask.js

document.addEventListener("DOMContentLoaded", async () => {
    const metamaskStatus = document.getElementById("metamaskStatus");
    const walletInfo = document.getElementById("walletInfo");
    const walletAddressEl = document.getElementById("walletAddress");

    // Vérifie si MetaMask est installé
    if (typeof window.ethereum === "undefined") {
        document.getElementById("metamaskModal").style.display = "block";
        metamaskStatus.innerHTML = '<i class="fas fa-times-circle"></i> MetaMask not found';
        return;
    }

    try {
        // Demande la connexion
        const accounts = await ethereum.request({ method: 'eth_requestAccounts' });
        const account = accounts[0];
        walletAddressEl.textContent = account;
        metamaskStatus.style.display = "none";
        walletInfo.style.display = "block";

        // Optionnel: écoute des changements de compte ou réseau
        ethereum.on('accountsChanged', (accounts) => {
            if (accounts.length === 0) {
                walletInfo.style.display = "none";
                metamaskStatus.style.display = "block";
                metamaskStatus.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Connect MetaMask';
            } else {
                walletAddressEl.textContent = accounts[0];
            }
        });

        ethereum.on('chainChanged', (_chainId) => {
            window.location.reload();
        });

    } catch (error) {
        metamaskStatus.innerHTML = '<i class="fas fa-exclamation-triangle"></i> Connection rejected';
        console.error("MetaMask connection error:", error);
    }
});

// Fonction pour ouvrir directement le PDF/image du diplôme
async function viewDiploma(studentId) {
    const diplomaModal = document.getElementById("diplomaModal");
    const diplomaContent = document.getElementById("diplomaContent");
    diplomaContent.innerHTML = '<div class="loading-spinner"></div><p>Loading diploma...</p>';
    diplomaModal.style.display = "block";

    try {
        const response = await fetch(`/blockchain/diploma_metadata/${studentId}/`);
        const data = await response.json();

        if (!data.success) {
            diplomaContent.innerHTML = `<p>Error: ${data.error || 'Diploma not found'}</p>`;
            return;
        }

        // Récupère le PDF/image direct depuis IPFS
        const metadataUrl = data.metadata_url;
        const metadataResp = await fetch(metadataUrl);
        const metadata = await metadataResp.json();

        // Vérifie que l'image/PDF existe
        if (!metadata || !metadata.image) {
            diplomaContent.innerHTML = `<p>No diploma file found in metadata</p>`;
            return;
        }

        const fileUrl = metadata.image.replace("ipfs://", "https://ipfs.io/ipfs/");

        // Détecte PDF ou image pour afficher correctement
        if (fileUrl.endsWith(".pdf")) {
            diplomaContent.innerHTML = `<iframe src="${fileUrl}" width="100%" height="600px" frameborder="0"></iframe>`;
        } else {
            diplomaContent.innerHTML = `<img src="${fileUrl}" alt="Diploma Image" style="width:100%; max-height:600px; object-fit:contain;">`;
        }

    } catch (err) {
        console.error(err);
        diplomaContent.innerHTML = `<p>Error loading diploma</p>`;
    }
}

// Fermer modal
function closeDiplomaModal() {
    document.getElementById("diplomaModal").style.display = "none";
}

// Permet de pré-remplir le formulaire Mint
function selectStudent(studentId) {
    document.getElementById("student_id").value = studentId;
}
