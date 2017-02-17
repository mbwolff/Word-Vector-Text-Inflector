# Word Vector Text Modulator
A contribution to 2016 NaNoGenMo

This repository contains the code and data necessary to generate _Madame Bovary modulée_, a novel based on the text by Flaubert but modified with word vectors derived from over 1300 nineteenth-century French texts.

Run the following command to produce the novel:

```
./transformText.py > MadameBovaryModulée.txt
```
A quick explanation of what's under the hood
Using [gensim](https://radimrehurek.com/gensim/models/word2vec.html) to build a word2Vec model based on over 1300 French texts from the nineteenth century, I am writing code that takes a pair of words (e.g. "homme" and "femme") and a text (_Le Père Goriot_, by Balzac) as parameters and generates an "modulated" text. Each word in the original text is replaced by a word that is "most similar" to it according to the word pair. For instance, if "roi" is a word in the original text, it would be replaced thusly:

```
>>> model.most_similar(positive=['femme', 'roi'], negative=['homme'], topn=1)
[(u'reine', 0.8085041046142578)]
```
Handling verb conjugations and adjective agreements in French is tricky but I aim to produce a mostly readable text. The code will hopefully be able to "modulate" any text in French against any pair of words.
