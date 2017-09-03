from gensim.models import word2vec

sentences = word2vec.Text8Corpus('./fourChar_data/yozi_wakati_s.txt')
model = word2vec.Word2Vec(sentences,size=20, min_count=1)
model.save('four_char_w2v.model')
