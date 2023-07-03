import json

from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

if __name__ == '__main__':
    with open('wanted_group.txt', 'r') as f:
        sentences = json.load(f)

    max_clusters = 50

    embeddings = model.encode(sentences)

    sse = []
    for k in range(2, max_clusters + 1):
        kmeans = KMeans(n_clusters=k, n_init='auto').fit(embeddings)
        sse.append(kmeans.inertia_)

    # 繪製分群數量和SSE之間的折線圖
    plt.plot(range(2, max_clusters + 1), sse)
    plt.xlabel('分群數量')
    plt.ylabel('SSE')
    plt.show()