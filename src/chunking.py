text = open('documents\catcaterpillar.txt', encoding = 'UTF8').readlines()
text = ''.join(text)
print(text)
import re

def chunk_text_by_sentence(text: str, n: int):
    sentences = re.split(r'(?<=[.?!])\s+', text)
    
    chunks = []
    current_chunk = ""
    
    for sentence in sentences:
        if len(current_chunk) + len(sentence) + 1 > n and current_chunk:
            current_chunk += sentence + " "
            chunks.append(current_chunk.strip())
            current_chunk = sentence + " "

        else:
            current_chunk += sentence + " "
            
    if current_chunk:
        chunks.append(current_chunk.strip())
        
    return chunks

N = 400
chunks = chunk_text_by_sentence(text, N)

for i, chunk in enumerate(chunks):
    print(f"Чанк {i+1} (Длина {len(chunk)}): '{chunk}'")