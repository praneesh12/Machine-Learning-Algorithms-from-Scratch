#================================================================================================================
#----------------------------------------------------------------------------------------------------------------
#									NAIVE BAYES
#----------------------------------------------------------------------------------------------------------------
#================================================================================================================

#Using Naive Bayes to classify emails as spam and non-spam

import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import nltk
import re

#for plotting
plt.style.use('ggplot')

class CustomNB:
	
	def __init__(self):
		pass
	
	def create_freq_table(self, texts, labels=None):
		#create the dataframe
		ft = pd.DataFrame([])
		#iterate through them emails
		for index, trm in enumerate(texts):
			vocabulary = trm #all the words of the email
			#amount of times each word occurs in the dictionary
			freq_dict = pd.Series({ v : trm.count(v) for v in vocabulary})

			if labels!=None:
				freq_dict['CLASS'] = labels[index]
				ft = ft.append(freq_dict, ignore_index=True)
		ft = ft.fillna(0)
		return 	ft

	def train(self, freq):
		fq = freq.iloc[:,1:]
		labels = fq.iloc[:, 0].values
		vocabulary = list(fq.columns.values)
		s, ns = pd.DataFrame([]), pd.DataFrame([])
		for index, rw in fq.iterrows():
			if labels[index] == 1:
				s = s.append(rw)
			else:
				ns = ns.append(rw)
		
		swc = sum([word for word in s.sum()])
		nswc = sum([word for word in ns.sum()])
		
		#Create the dicts for storing the model
		non_spam_model, spam_model = {}, {}
		
		alpha = 0.5
		for word in vocabulary:
			spam_occurances = s[word].sum()
			non_spam_occurances = ns[word].sum()
			#Now, the crux of the algo, the bayesian probablity
			bayesian_probablity_for_spam = ( spam_occurances + alpha ) / ( swc )
			bayesian_probablity_for_non_spam = ( non_spam_occurances + alpha ) / ( nswc )
			#Update the model
			non_spam_model[word], spam_model[word] = bayesian_probablity_for_spam , bayesian_probablity_for_non_spam
		print(non_spam_model)

	def predict(text, prob_o_spam, prob_o_not_spam):
		pass

def main():
	
	# 0 means spam, 1 means not spam
	emails = {"0": ["Dear friend, win 1000$ cash right now!!.", " Webcams Day & Night - All LIVE - Webcams Contest",
			"Congratulations, you've won a free car!"], 
			"1": ["Hey, Can you redo the presentation and send it on by Friday?", "Thank you for the documents, I will revert as soon as possible",
			"Open the Pod bay doors, HAL." , " I'm sorry, Dave. I'm afraid I can't do that."]}
	t= []
	labl = []

	for k in emails:
		for mail in emails[k]:
			tokens = [word.lower() for sent in nltk.sent_tokenize(mail) for word in nltk.word_tokenize(sent)]
			filtered_tokens = []
			# filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
			for token in tokens:
				if re.search('[a-zA-Z]', token):
					filtered_tokens.append(token)
			t.append(' '.join(filtered_tokens))
			labl.append(k)
	for i in range(len(t)):
		t[i] = t[i].split()
	
	nb = CustomNB()
	freq_table = nb.create_freq_table(t, labl)
	nb.train(freq_table)
	

if __name__ == "__main__":
	main()