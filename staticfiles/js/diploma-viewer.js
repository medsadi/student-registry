async function viewDiploma(studentId) {
    try {
        // 1. Call Django API to get metadata JSON + IPFS PDF CID

        const response = await fetch(`/diploma_metadata/${studentId}/`);

        const data = await response.json();

        if (!data.success) {
            alert("Erreur: impossible de récupérer le diplôme !");
            return;
        }

        // 2. Metadata contains diploma_uri = ipfs://CID
        let uri = data.metadata.diploma_uri;

        if (!uri.startsWith("ipfs://")) {
            alert("Format IPFS invalide !");
            return;
        }

        // 3. Extract CID
        const cid = uri.replace("ipfs://", "");

        // 4. Build direct gateway URL (PDF or image)
        const directURL = `https://ipfs.io/ipfs/${cid}`;

        // 5. Open directly the file (PDF or image)
        window.open(directURL, "_blank");

    } catch (error) {
        console.error("ERROR while viewing diploma:", error);
        alert("Erreur interne — impossible d'ouvrir le diplôme.");
    }
}
