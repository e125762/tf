from gensim.models import word2vec

sentences = word2vec.Text8Corpus('./fourChar_data/four_char_kanzi_w.txt')
model = word2vec.Word2Vec(sentences,size=100, min_count=1)
model.save('four_char_kanzi_w2v.model')
