from gensim.models import word2vec

sentences = word2vec.Text8Corpus('./yozi_wakati.txt')
model = word2vec.Word2Vec(sentences,size=20)
model.save('four_char_w2v.model')
