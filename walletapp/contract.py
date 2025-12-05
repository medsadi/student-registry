# ==========================================
# CONTRACT ABIs - Student Registry + Diploma NFT
# ==========================================

# ABI du contrat StudentRegistry (ancien contrat)
CONTRACT_ABI = [
    {
        "inputs": [
            {"internalType": "string", "name": "_nom", "type": "string"},
            {"internalType": "string", "name": "_prenom", "type": "string"},
            {"internalType": "string", "name": "_dateNaissance", "type": "string"},
            {"internalType": "uint256", "name": "_moyenneGenerale", "type": "uint256"}
        ],
        "name": "addStudent",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "uint256", "name": "_studentId", "type": "uint256"}],
        "name": "getStudent",
        "outputs": [
            {"internalType": "string", "name": "nom", "type": "string"},
            {"internalType": "string", "name": "prenom", "type": "string"},
            {"internalType": "string", "name": "dateNaissance", "type": "string"},
            {"internalType": "uint256", "name": "moyenneGenerale", "type": "uint256"}
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "getTotalStudents",
        "outputs": [{"internalType": "uint256", "name": "total", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "getAllStudentIds",
        "outputs": [{"internalType": "uint256[]", "name": "ids", "type": "uint256[]"}],
        "stateMutability": "view",
        "type": "function"
    }
]

# ABI du contrat DiplomaRegistry (nouveau contrat NFT)
DIPLOMA_CONTRACT_ABI = [
    {
        "inputs": [
            {"internalType": "string", "name": "_nom", "type": "string"},
            {"internalType": "string", "name": "_prenom", "type": "string"},
            {"internalType": "string", "name": "_dateNaissance", "type": "string"},
            {"internalType": "uint256", "name": "_moyenneGenerale", "type": "uint256"},
            {"internalType": "address", "name": "_studentAddress", "type": "address"}
        ],
        "name": "addStudent",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "uint256", "name": "_studentId", "type": "uint256"},
            {"internalType": "string", "name": "_ipfsHash", "type": "string"}
        ],
        "name": "mintDiploma",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "uint256", "name": "_studentId", "type": "uint256"}],
        "name": "getStudent",
        "outputs": [
            {"internalType": "string", "name": "nom", "type": "string"},
            {"internalType": "string", "name": "prenom", "type": "string"},
            {"internalType": "string", "name": "dateNaissance", "type": "string"},
            {"internalType": "uint256", "name": "moyenneGenerale", "type": "uint256"},
            {"internalType": "bool", "name": "diplomaMinted", "type": "bool"},
            {"internalType": "uint256", "name": "diplomaTokenId", "type": "uint256"}
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "getAllStudentIds",
        "outputs": [{"internalType": "uint256[]", "name": "ids", "type": "uint256[]"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "getTotalStudents",
        "outputs": [{"internalType": "uint256", "name": "total", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "uint256", "name": "_studentId", "type": "uint256"}],
        "name": "hasDiploma",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "uint256", "name": "_studentId", "type": "uint256"}],
        "name": "getDiplomaURI",
        "outputs": [{"internalType": "string", "name": "", "type": "string"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "address", "name": "_address", "type": "address"}],
        "name": "getStudentsByAddress",
        "outputs": [{"internalType": "uint256[]", "name": "", "type": "uint256[]"}],
        "stateMutability": "view",
        "type": "function"
    }
]