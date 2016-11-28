#!/usr/bin/env python

import os, re, gensim, treetaggerwrapper
from pattern.fr import singularize, pluralize, conjugate, tenses, lemma, \
	predicative, parsetree, split, parse, pprint, \
	INFINITIVE, INDICATIVE, CONDITIONAL, SUBJUNCTIVE, \
	PERFECTIVE, IMPERFECTIVE, PROGRESSIVE, PRESENT, PAST, FUTURE, SG, PL
from pprint import pprint


# pos_pattern = { 'JJ', 'JJR', 'JJS', 'NN', 'NNS', 'RB', 'RBR', 'RBS', 'VB', 'NNP', 'NNPS' }
pos_tt = { 'ABR', 'ADJ', 'ADV', 'NOM', 'VER:cond', 'VER:futu', 'VER:impe',
	'VER:impf', 'VER:infi', 'VER:pper', 'VER:ppre', 'VER:pres', 'VER:simp',
	'VER:subi', 'VER:subp' }
specials = { u'sommer|\xeatre': u'\xeatre' }

def correct_grammar(string, mot, pos, lemma):
	# maybe we can just use the original string
#	print('Mot: ' + mot.encode('utf-8') + \
#		', pos: ' + pos.encode('utf-8') + \
#		', lem: ' + lemma.encode('utf-8') + \
#		', str: ' + string.encode('utf-8'))
#	if specials[string]: string = specials[string]
	if pos == 'PUN': string = mot
	elif string.lower() == mot.lower() or \
		pos not in pos_tt or \
		mot.lower() in { 'l', 'ne', 'le', 'la', 'les', 'd', 'n'}:
		string = mot
	else: # we need to inflect
#		print('Str: ' + string.encode('utf-8') + \
#			', Mot: ' + mot.encode('utf-8') + \
#			', pos: ' + pos.encode('utf-8') + \
#			', lemma: ' + lemma.encode('utf-8'))
		if (pos == 'NOM' or pos == 'PRO') and mot != lemma:
#				print(pos.encode('utf-8') + \
#					'  string: ' + string.encode('utf-8') + \
#					'  mot: ' + mot.encode('utf-8') + \
#					'  lemma: ' + lemma.encode('utf-8'))
#				pprint([ string, mot, pos, lemma ])
			if singularize(mot) == lemma:
				string = pluralize(string)
			else: string = singularize(string)
		else: # verbs
#			pprint([ string, mot, pos, lemma ])
			if pos == 'VER:pper':
				string = conjugate(string, tense=PAST,
					mood=INDICATIVE, aspect=PROGRESSIVE )
			elif pos == 'VER:ppre':
				string = conjugate(string, tense=PRESENT,
					mood=INDICATIVE, aspect=PROGRESSIVE )
			elif pos == 'VER:impe':
				if mot.endswith('ez'):
					string = conjugate(string, tense=PRESENT,
						mood=IMPERATIVE, aspect=IMPERFECTIVE, person=2,
						number=PL)
				elif mot.endswith('ons'):
					string = conjugate(string, tense=PRESENT,
						mood=IMPERATIVE, aspect=IMPERFECTIVE, person=1,
						number=PL)
				else:
					string = conjugate(string, tense=PRESENT,
						mood=IMPERATIVE, aspect=IMPERFECTIVE, person=2,
						number=SG)
			elif pos == 'VER:impf':
				if mot.endswith('ez'):
					string = conjugate(string, tense=PAST,
						mood=INDICATIVE, aspect=IMPERFECTIVE, person=2,
						number=PL)
				elif mot.endswith('ons'):
					string = conjugate(string, tense=PAST,
						mood=INDICATIVE, aspect=IMPERFECTIVE, person=1,
						number=PL)
				elif mot.endswith('aient'):
					string = conjugate(string, tense=PAST,
						mood=INDICATIVE, aspect=IMPERFECTIVE, person=3,
						number=PL)
				elif mot.endswith('ait'):
					string = conjugate(string, tense=PAST,
						mood=INDICATIVE, aspect=IMPERFECTIVE, person=3,
						number=SG)
				else:
					string = conjugate(string, tense=PAST,
						mood=INDICATIVE, aspect=IMPERFECTIVE, person=2,
						number=SG)
			elif pos == 'VER:cond':
				if mot.endswith('ez'):
					string = conjugate(string, tense=PRESENT,
						mood=CONDITIONAL, aspect=IMPERFECTIVE, person=2,
						number=PL)
				elif mot.endswith('ons'):
					string = conjugate(string, tense=PRESENT,
						mood=CONDITIONAL, aspect=IMPERFECTIVE, person=1,
						number=PL)
				elif mot.endswith('aient'):
					string = conjugate(string, tense=PRESENT,
						mood=CONDITIONAL, aspect=IMPERFECTIVE, person=3,
						number=PL)
				elif mot.endswith('ait'):
					string = conjugate(string, tense=PRESENT,
						mood=CONDITIONAL, aspect=IMPERFECTIVE, person=3,
						number=SG)
				else:
					string = conjugate(string, tense=PRESENT,
						mood=CONDITIONAL, aspect=IMPERFECTIVE, person=2,
						number=SG)
			elif pos == 'VER:futu':
				if mot.endswith('ez'):
					string = conjugate(string, tense=FUTURE,
						mood=INDICATIVE, aspect=IMPERFECTIVE, person=2,
						number=PL)
				elif mot.endswith('ons'):
					string = conjugate(string, tense=FUTURE,
						mood=INDICATIVE, aspect=IMPERFECTIVE, person=1,
						number=PL)
				elif mot.endswith('ont'):
					string = conjugate(string, tense=FUTURE,
						mood=INDICATIVE, aspect=IMPERFECTIVE, person=3,
						number=PL)
				elif mot.endswith('a'):
					string = conjugate(string, tense=FUTURE,
						mood=INDICATIVE, aspect=IMPERFECTIVE, person=3,
						number=SG)
				else:
					string = conjugate(string, tense=FUTURE,
						mood=INDICATIVE, aspect=IMPERFECTIVE, person=2,
						number=SG)
			elif pos == 'VER:simp':
				if mot.endswith('tes'):
					string = conjugate(string, tense=PAST,
							mood=INDICATIVE, aspect=PERFECTIVE, person=2,
							number=PL)
				elif mot.endswith('mes'):
					string = conjugate(string, tense=PAST,
							mood=INDICATIVE, aspect=PERFECTIVE, person=1,
							number=PL)
				elif mot.endswith('ent'):
					string = conjugate(string, tense=PAST,
						mood=INDICATIVE, aspect=PERFECTIVE, person=3,
						number=PL)
				elif mot.endswith('t'):
					string = conjugate(string, tense=PAST,
						mood=INDICATIVE, aspect=PERFECTIVE, person=3,
						number=SG)
				else:
					string = conjugate(string, tense=PAST,
						mood=INDICATIVE, aspect=PERFECTIVE, person=2,
						number=SG)
			elif pos == 'VER:subi':
				if mot.endswith('ez'):
					string = conjugate(string, tense=PRESENT,
						mood=SUBJUNCTIVE, aspect=IMPERFECTIVE, person=2,
						number=PL)
				elif mot.endswith('ons'):
					string = conjugate(string, tense=PRESENT,
						mood=SUBJUNCTIVE, aspect=IMPERFECTIVE, person=1,
						number=PL)
				elif mot.endswith('ent'):
					string = conjugate(string, tense=PRESENT,
						mood=SUBJUNCTIVE, aspect=IMPERFECTIVE, person=3,
						number=PL)
				elif mot.endswith('t'):
					string = conjugate(string, tense=PRESENT,
						mood=SUBJUNCTIVE, aspect=IMPERFECTIVE, person=3,
						number=SG)
				elif mot.endswith('es'):
					string = conjugate(string, tense=PRESENT,
						mood=SUBJUNCTIVE, aspect=IMPERFECTIVE, person=2,
						number=SG)
				else:
					string = conjugate(string, tense=PRESENT,
						mood=SUBJUNCTIVE, aspect=IMPERFECTIVE, person=1,
						number=SG)
			elif pos == 'VER:subp':
				if mot.endswith('ez'):
					string = conjugate(string, tense=PAST,
						mood=SUBJUNCTIVE, aspect=IMPERFECTIVE, person=2,
						number=PL)
				elif mot.endswith('ons'):
					string = conjugate(string, tense=PAST,
						mood=SUBJUNCTIVE, aspect=IMPERFECTIVE, person=1,
						number=PL)
				elif mot.endswith('ent'):
					string = conjugate(string, tense=PAST,
						mood=SUBJUNCTIVE, aspect=IMPERFECTIVE, person=3,
						number=PL)
				elif mot.endswith('t'):
					string = conjugate(string, tense=PAST,
						mood=SUBJUNCTIVE, aspect=IMPERFECTIVE, person=3,
						number=SG)
				elif mot.endswith('es'):
					string = conjugate(string, tense=PAST,
						mood=SUBJUNCTIVE, aspect=IMPERFECTIVE, person=2,
						number=SG)
				else:
					string = conjugate(string, tense=PAST,
						mood=SUBJUNCTIVE, aspect=IMPERFECTIVE, person=1,
						number=SG)
			elif pos == 'VER:pres':
				if mot.endswith('ez'):
					string = conjugate(string, tense=PRESENT,
						mood=INDICATIVE, aspect=IMPERFECTIVE, person=2,
						number=PL)
				elif mot.endswith('ons'):
					string = conjugate(string, tense=PRESENT,
						mood=INDICATIVE, aspect=IMPERFECTIVE, person=1,
						number=PL)
				elif mot.endswith('ent'):
					string = conjugate(string, tense=PRESENT,
						mood=INDICATIVE, aspect=IMPERFECTIVE, person=3,
						number=PL)
				elif mot.endswith('t'):
					string = conjugate(string, tense=PRESENT,
						mood=INDICATIVE, aspect=IMPERFECTIVE, person=3,
						number=SG)
				elif mot.endswith('es'):
					string = conjugate(string, tense=PRESENT,
						mood=INDICATIVE, aspect=IMPERFECTIVE, person=2,
						number=SG)
				else:
					string = conjugate(string, tense=PRESENT,
						mood=INDICATIVE, aspect=IMPERFECTIVE, person=1,
						number=SG)

#	if (word.type in {'VB'}):
#	if mot[0].isupper(): string = string.capitalize()
	if mot.isupper(): string = string.upper()
	elif mot[0].isupper(): string = string[0].upper() + string[1:]
	return string

def fix_agreements(words):
	i = 0
	while i < len(words) - 1:
		if words[i][1] == 'DET:ART' and words[i][0].lower() in {'le', 'la'} \
				and re.match('^[aeiouhy]', words[i + 1][0].lower()):
				words[i][0] = "l'"
		elif words[i][0].lower() == 'ce' and \
			re.match('^[aeiouhy]', words[i + 1][0].lower()):
			words[i][0] = 'cet'
		i += 1
	return words

def fix_word(tt):
	if len(tt) == 3:
		if tt[0] == "j'": tt = [ "j'", 'PRO:PER', 'je' ]
		elif tt[0] == 'j': tt = [ 'j', 'PRO:PER', 'je' ]
	return tt
