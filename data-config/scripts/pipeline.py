import os
from scripts.steps.download import download_all
from scripts.steps.extract import extract_all
from scripts.steps.clean import clean_all
from scripts.steps.chunk import chunk_all
from scripts.steps.embed_load import embed_all

def main():
    print("=== PIPELINE START ===")
    download_all()
    extract_all()
    clean_all()
    chunk_all()
    embed_all()
    print("=== PIPELINE DONE ===")

if __name__ == "__main__":
    main()
