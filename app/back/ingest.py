from pathlib import Path
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import chromadb

def ingest_pdfs(pdf_folder="./data", collection_name="documents"):
    """
    Charge tous les PDFs d'un dossier et les stocke dans ChromaDB
    """
    # Initialiser le modèle d'embedding
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # Initialiser ChromaDB
    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_or_create_collection(name=collection_name)
    
    # Lire tous les PDFs
    pdf_path = Path(pdf_folder)
    pdf_files = list(pdf_path.glob("*.pdf"))
    
    print(f"Trouvé {len(pdf_files)} PDFs")
    
    documents = []
    metadatas = []
    ids = []
    
    for idx, pdf_file in enumerate(pdf_files):
        reader = PdfReader(pdf_file)
        
        # Extraire le texte de chaque page
        for page_num, page in enumerate(reader.pages):
            text = page.extract_text()
            
            if text.strip():  # Ignorer les pages vides
                documents.append(text)
                metadatas.append({
                    "source": pdf_file.name,
                    "page": page_num + 1
                })
                ids.append(f"{pdf_file.stem}_page_{page_num + 1}")
    
    # Générer les embeddings et stocker
    print(f"Génération des embeddings pour {len(documents)} pages...")
    embeddings = model.encode(documents)
    
    collection.add(
        embeddings=embeddings.tolist(),
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )
    
    print(f"✅ Ingestion terminée : {len(documents)} pages indexées")

if __name__ == "__main__":
    ingest_pdfs()