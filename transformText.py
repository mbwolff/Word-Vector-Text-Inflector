#!/usr/bin/env python

# from __future__ import print_function
import os, re, gensim, treetaggerwrapper, pickle, aspell, sys
from pattern.fr import singularize, pluralize, conjugate, tenses, lemma, \
	predicative, parsetree, split, parse, pprint, \
	INFINITIVE, INDICATIVE, CONDITIONAL, SUBJUNCTIVE, \
	PERFECTIVE, IMPERFECTIVE, PROGRESSIVE, PRESENT, PAST, FUTURE, SG, PL
from fixWords import correct_grammar, fix_agreements, fix_word
from pprint import pprint

# sourcefile = 'FlaubertMadameBovary.txt'
# sourcefile = 'BaudelaireEnivrez.txt'
# focus1 = 'homme'
# focus2 = 'femme'
# focus1 = 'boire'
# focus2 = 'dormir'
focus1 = sys.argv[1]
focus2 = sys.argv[2]
sourcefile = sys.argv[3]

w2vfile = 'ARTFLmodel'
pklf = 'pos_dict.pkl'

pickleFile = open(pklf, 'rb')
pd = pickle.load(pickleFile)
# pprint(pd)

# pos_pattern = { 'JJ', 'JJR', 'JJS', 'NN', 'NNS', 'RB', 'RBR', 'RBS', 'VB', 'NNP', 'NNPS' }
pos_tt = { 'ABR', 'ADJ', 'ADV', 'NOM', 'VER:cond', 'VER:futu', 'VER:impe',
	'VER:impf', 'VER:infi', 'VER:pper', 'VER:ppre', 'VER:pres', 'VER:simp',
	'VER:subi', 'VER:subp' }

sourcetext = open(sourcefile, 'r').read().decode('utf-8')
model = gensim.models.Word2Vec.load(w2vfile)

tagger = treetaggerwrapper.TreeTagger(TAGLANG='fr')
s = aspell.Speller('lang', 'fr')

text = parsetree(sourcetext, relations = True, lemmata = True)

for sentence in text:
	newsentence = list()
#	print sentence.string.encode('utf-8')
#	print('-------')
	parsed = tagger.tag_text(sentence.string)
	for word in parsed:
		[ mot, pos, lemma ] = fix_word(word.split('\t'))
		if pos in pos_tt and model.vocab.get(lemma):
			string = mot
			swap = model.most_similar(positive=[focus2, lemma],
				negative=[focus1], topn=10)
			while len(swap) > 0: # go through the top 10 matches and find the
			# first one that (1) has a pos (2) that is valid and (3) is a real
			# word according to aspell
				match = swap.pop(0)
				if pd.get(match[0]) and pos in pd[match[0]] \
					and s.check(match[0].encode('utf-8')):
					string = match[0]
					break
			newsentence.append([correct_grammar(string, mot, pos, lemma), pos])
		else: newsentence.append([mot, pos])
	fixedsentence = fix_agreements(newsentence)
	processed = ' '.join([x[0] for x in fixedsentence])
	processed = processed.replace(" ' ", "'")
	processed = processed.replace(" - ", "-")
	processed = processed.replace(" , ", ", ")
	processed = processed.replace(" .", ".")
	processed = re.sub(r" -(\w)", r"-\1", processed)
#	processed = re.sub('\' ', '\'', processed)
#	processed = re.sub(' n ', ' ne ', processed)
#	processed = re.sub('([Qq])ue ([aeiouh\xe9\xe8\xe0])', r"\1u'\2", processed)
#	processed = re.sub("'([^aeiouh\xe9\xe8\xe0])", r'e \1', processed)
#	print('-------')
	print(processed.encode('utf-8'))
#	print('=======')
