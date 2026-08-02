import os
import json
import zipfile
import urllib.request
import shutil
import requests


# ==========================================
# Lenny Growth Assistant
# Transcript + RAG Ingestion
# ==========================================


# ==========================================
# PROJECT PATHS
# ==========================================

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


DATA_DIR = os.path.join(
    PROJECT_ROOT,
    "data"
)


TRANSCRIPT_DIR = os.path.join(
    DATA_DIR,
    "transcripts"
)


VECTOR_STORE_FILE = os.path.join(
    DATA_DIR,
    "vector_store.json"
)


ZIP_FILE = os.path.join(
    DATA_DIR,
    "lenny-transcripts.zip"
)


TEMP_DIR = os.path.join(
    DATA_DIR,
    "lenny-temp"
)


# ==========================================
# GITHUB
# ==========================================

GITHUB_ZIP_URL = (
    "https://github.com/"
    "ChatPRD/lennys-podcast-transcripts/"
    "archive/refs/heads/main.zip"
)


# ==========================================
# OLLAMA
# ==========================================

OLLAMA_URL = "http://127.0.0.1:11434"

EMBEDDING_MODEL = "nomic-embed-text"


# ==========================================
# CREATE FOLDERS
# ==========================================

def create_folders():

    os.makedirs(
        DATA_DIR,
        exist_ok=True
    )

    os.makedirs(
        TRANSCRIPT_DIR,
        exist_ok=True
    )


# ==========================================
# DOWNLOAD TRANSCRIPTS
# ==========================================

def download_repository():

    print(
        "Downloading Lenny's Podcast transcripts..."
    )

    try:

        urllib.request.urlretrieve(

            GITHUB_ZIP_URL,

            ZIP_FILE

        )

        print(
            "Repository downloaded successfully."
        )

    except Exception as e:

        print(
            "❌ Download failed:"
        )

        print(e)

        raise


# ==========================================
# EXTRACT ZIP
# ==========================================

def extract_repository():

    print(
        "Extracting transcript files..."
    )


    if os.path.exists(
        TEMP_DIR
    ):

        shutil.rmtree(
            TEMP_DIR
        )


    os.makedirs(
        TEMP_DIR,
        exist_ok=True
    )


    with zipfile.ZipFile(

        ZIP_FILE,

        "r"

    ) as zip_ref:

        zip_ref.extractall(
            TEMP_DIR
        )


    print(
        "Extraction completed."
    )


# ==========================================
# COPY TRANSCRIPTS
# ==========================================

def copy_transcripts():

    transcript_files = []


    for root, dirs, files in os.walk(

        TEMP_DIR

    ):

        for filename in files:

            if filename.lower().endswith(

                (
                    ".txt",
                    ".md",
                    ".markdown"
                )

            ):

                filepath = os.path.join(

                    root,

                    filename

                )


                transcript_files.append(

                    filepath

                )


    print(

        f"Found {len(transcript_files)} "
        "transcript files."

    )


    copied = 0


    for filepath in transcript_files:

        filename = os.path.basename(

            filepath

        )


        destination = os.path.join(

            TRANSCRIPT_DIR,

            filename

        )


        try:

            shutil.copy2(

                filepath,

                destination

            )


            copied += 1


        except Exception as e:

            print(

                f"Could not copy "
                f"{filename}: {e}"

            )


    print(

        f"✅ Copied {copied} "
        "transcripts successfully."

    )


# ==========================================
# READ TRANSCRIPTS
# ==========================================

def load_transcripts():

    documents = []


    print()

    print(
        "Reading transcript files..."
    )


    for filename in os.listdir(

        TRANSCRIPT_DIR

    ):

        if not filename.lower().endswith(

            (
                ".txt",
                ".md",
                ".markdown"
            )

        ):

            continue


        filepath = os.path.join(

            TRANSCRIPT_DIR,

            filename

        )


        try:

            with open(

                filepath,

                "r",

                encoding="utf-8",

                errors="ignore"

            ) as file:

                text = file.read()


            if text.strip():

                documents.append(

                    {
                        "filename": filename,
                        "text": text
                    }

                )


        except Exception as e:

            print(

                f"Could not read "
                f"{filename}: {e}"

            )


    print(

        f"Loaded {len(documents)} "
        "transcript documents."

    )


    return documents


# ==========================================
# SPLIT TEXT INTO CHUNKS
# ==========================================

def create_chunks(

    documents,

    chunk_size=1200,

    overlap=200

):

    chunks = []


    print()

    print(
        "Creating transcript chunks..."
    )


    for document in documents:

        text = document["text"]

        filename = document["filename"]


        start = 0


        while start < len(text):

            end = start + chunk_size


            chunk_text = text[

                start:end

            ].strip()


            if chunk_text:

                chunks.append(

                    {

                        "id": len(chunks),

                        "text": chunk_text,

                        "source": filename

                    }

                )


            start = (

                end - overlap

            )


    print(

        f"Created {len(chunks)} "
        "text chunks."

    )


    return chunks


# ==========================================
# CREATE OLLAMA EMBEDDING
# ==========================================

def create_embedding(text):

    url = (

        f"{OLLAMA_URL}/api/embeddings"

    )


    payload = {

        "model":
            EMBEDDING_MODEL,

        "prompt":
            text

    }


    response = requests.post(

        url,

        json=payload,

        timeout=120

    )


    response.raise_for_status()


    data = response.json()


    return data["embedding"]


# ==========================================
# CREATE VECTOR STORE
# ==========================================

def build_vector_store(chunks):

    print()

    print(
        "Creating embeddings using Ollama..."
    )

    print(

        f"Model: {EMBEDDING_MODEL}"

    )


    vector_store = []


    total = len(chunks)


    for index, chunk in enumerate(

        chunks

    ):

        try:

            embedding = create_embedding(

                chunk["text"]

            )


            vector_store.append(

                {

                    "id":
                        chunk["id"],

                    "text":
                        chunk["text"],

                    "source":
                        chunk["source"],

                    "embedding":
                        embedding

                }

            )


            if (

                index + 1

            ) % 10 == 0:

                print(

                    f"Embedded "
                    f"{index + 1}/{total}"

                )


        except Exception as e:

            print()

            print(

                f"❌ Embedding failed "
                f"for chunk {index}"

            )

            print(e)


    print()

    print(

        f"Saving {len(vector_store)} "
        "embeddings..."

    )


    with open(

        VECTOR_STORE_FILE,

        "w",

        encoding="utf-8"

    ) as file:

        json.dump(

            vector_store,

            file

        )


    print()

    print(
        "✅ Vector store created."
    )


    print(

        "Saved at:"

    )


    print(

        VECTOR_STORE_FILE

    )


# ==========================================
# CLEANUP
# ==========================================

def cleanup():

    if os.path.exists(

        ZIP_FILE

    ):

        os.remove(

            ZIP_FILE

        )


    if os.path.exists(

        TEMP_DIR

    ):

        shutil.rmtree(

            TEMP_DIR

        )


    print()

    print(
        "Temporary files cleaned."
    )


# ==========================================
# MAIN
# ==========================================

def main():

    print(
        "======================================"
    )

    print(
        " Lenny Growth Assistant"
    )

    print(
        " Transcript + RAG Ingestion"
    )

    print(
        "======================================"
    )


    # Step 1

    create_folders()


    # Step 2

    download_repository()


    # Step 3

    extract_repository()


    # Step 4

    copy_transcripts()


    # Step 5

    documents = load_transcripts()


    if not documents:

        print()

        print(
            "❌ No transcripts found."
        )

        return


    # Step 6

    chunks = create_chunks(

        documents

    )


    # Step 7

    build_vector_store(

        chunks

    )


    # Step 8

    cleanup()


    print()

    print(
        "======================================"
    )

    print(
        "✅ RAG INGESTION COMPLETED!"
    )

    print(
        "======================================"
    )


    print()

    print(

        f"Transcripts: "
        f"{len(documents)}"

    )


    print(

        f"Chunks: "
        f"{len(chunks)}"

    )


    print()

    print(

        "Vector store:"

    )


    print(

        VECTOR_STORE_FILE

    )


# ==========================================
# RUN
# ==========================================

if __name__ == "__main__":

    main()