import networkx
# 一个图结构的相关操作包，没用过无所谓，有兴趣可以搜索学习
import numpy as np
import pandas as pd

from sklearn.metrics.pairwise import cosine_similarity
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords

from Utils.Translator import Translator


def English_Summary(text):
    # nltk.download('punkt')
    # nltk.download('stopwords')
    # 下载断句和停用词数据，下载一次就行，后续运行可直接注释掉

    # file_name = 'Data/News.txt'
    # file = open(file_name, "r", encoding='utf-8')
    # text = file.read()
    sentences = sent_tokenize(text)

    word_embeddings = {}
    GLOVE_DIR = './Data/glove.6B.100d.txt'
    with open(GLOVE_DIR, encoding='utf-8') as f:
        for line in f:
            values = line.split()
            word = values[0]
            coefs = np.asarray(values[1:], dtype='float32')
            word_embeddings[word] = coefs
    # 获取词向量
    # 该词向量文件形式为：词 空格 词向量，然后换行，自行理解上述操作代码

    clean_sentences = pd.Series(sentences).str.replace('[^a-zA-Z]', ' ', regex=True)
    clean_sentences = [s.lower() for s in clean_sentences]
    # 文本清洗，去除标点、数字、特殊符号、统一小写
    stop_words = stopwords.words('english')


    def remove_stopwords(str):
        sen = ' '.join([i for i in str if i not in stop_words])
        return sen


    clean_sentences = [remove_stopwords(r.split()) for r in clean_sentences]
    # 去停用词
    sentences_vectors = []
    for i in clean_sentences:
        if len(i) != 0:
            v = sum(
                [word_embeddings.get(w, np.zeros((100,))) for w in i.split()]
            ) / (len(i.split()) + 1e-2)
        else:
            v = np.zeros((100,))
        sentences_vectors.append(v)
    # 获取每个句子的所有组成词的向量（从GloVe词向量文件中获取，每个向量大小为100），
    # 然后取这些向量的平均值，得出这个句子的合并向量为这个句子的特征向量

    similarity_matrix = np.zeros((len(clean_sentences), len(clean_sentences)))
    # 初始化相似度矩阵（全零矩阵）
    for i in range(len(clean_sentences)):
        for j in range(len(clean_sentences)):
            if i != j:
                similarity_matrix[i][j] = cosine_similarity(
                    sentences_vectors[i].reshape(1, -1), sentences_vectors[j].reshape(1, -1)
                )
    # 计算相似度矩阵，基于余弦相似度
    nx_graph = networkx.from_numpy_array(similarity_matrix)
    scores = networkx.pagerank(nx_graph)

    # 将相似度矩阵转为图结构
    ranked_sentences = sorted(
        ((scores[i], s) for i, s in enumerate(sentences)), reverse=True
    )

    en_res = ""
    zh_res = ""
    translator = Translator()

    # 排序，打印得分最高的前3个句子，即为摘要
    for i in range(min((5, len(ranked_sentences)))):
        en_res += str(ranked_sentences[i][1]) + "\n"
        zh_res += str(translator.translate(ranked_sentences[i][1])) + "\n"

    return [en_res, zh_res]