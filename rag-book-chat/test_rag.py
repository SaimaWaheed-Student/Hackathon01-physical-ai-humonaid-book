from app.rag import retrieve_similar_chunks

chunks = retrieve_similar_chunks('What is Physical AI?', 'my-book', top_k=3, threshold=0.1)
print(f'Found {len(chunks)} chunks:')
for c in chunks:
    print(f"  - Score: {c['similarity_score']:.3f}")
    print(f"    Text: {c['chunk_text'][:150]}...")
    print()
