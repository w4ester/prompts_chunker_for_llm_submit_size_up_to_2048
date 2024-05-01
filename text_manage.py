import os
import sqlite3

def process_directory(directory_path):
    for filename in os.listdir(directory_path):
        if filename.endswith('.txt'):
            file_path = os.path.join(directory_path, filename)
            read_and_chunk_file(file_path)
            print(f"Processed {filename}")

def chunk_text(text, size=512):
    return [text[i:i+size] for i in range(0, len(text), size)]

def store_chunks(chunks, db_path='text_chunks.db'):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS TextChunks (id INTEGER PRIMARY KEY AUTOINCREMENT, chunk TEXT)')
    for chunk in chunks:
        c.execute('INSERT INTO TextChunks (chunk) VALUES (?)', (chunk,))
    conn.commit()
    conn.close()

def read_and_chunk_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    chunks = chunk_text(text)
    store_chunks(chunks)

def retrieve_chunks(db_path='text_chunks.db'):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('SELECT id, chunk FROM TextChunks')
    chunks = c.fetchall()
    conn.close()
    return chunks

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        directory_path = sys.argv[1]
    else:
        # Set default path directly here
        directory_path = '/Users/willf/vscode/junebug_projects/prompts_chunker_for_llm_submit_size_up_to_2048'
    process_directory(directory_path)
