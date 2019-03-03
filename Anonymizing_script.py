def Anonymize(text):
    from nltk.tag import StanfordNERTagger
    from nltk.tokenize import word_tokenize
    import re
    import spacy
    import os
    import sys
    from pathlib import Path
    import csv

    csv_file = open('generated_database.csv', 'w')
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Entity', 'Type', 'Text id'])

    # Create your views here.	
    def preprocess(text):
        contractions = {
            "ain't": "is not",
            "amn't": "am not",
            "aren't": "are not",
            "can't": "cannot",
            "can't've": "cannot have",
            "'cause": "because",
            "could've": "could have",
            "couldn't": "could not",
            "couldn't've": "could not have",
            "daren't": "dared not",
            "daresn't": "dare not",
            "dasn't": "dare not",
            "didn't": "did not",
            "doesn't": "does not",
            "don't": "do not",
            "e'er": "ever",
            "everyone's": "everyone is",
            "finna": "fixing to",
            "gimme": "give me",
            "gonna": "going to",
            "gon't": "go not",
            "gotta": "got to",
            "hadn't": "had not",
            "hadn't've": "had not have",
            "hasn't": "has not",
            "haven't": "have not",
            "he'd": "he had",
            "he'd've": "he would have",
            "he'll": "he shall",
            "he'll've": "he will have",
            "he's": "he has",
            "how'd": "how did",
            "how'd'y": "how do you",
            "how'll": "how will",
            "how's": "how has",
            "I'd": "I had",
            "I'd've": "I would have",
            "I'll": "I will",
            "I'll've": "I will have",
            "I'm": "I am",
            "I'm'a": "I am about to",
            "I'm'o": "I am going to",
            "I've": "I have",
            "isn't": "is not",
            "it'd": "it had",
            "it'd've": "it would have",
            "it'll": "it will",
            "it'll've": "it will have",
            "it's": "it is",
            "let's": "let us",
            "ma'am": "madam",
            "mayn't": "may not",
            "might've": "might have",
            "mightn't": "might not",
            "mightn't've": "might not have",
            "must've": "must have",
            "mustn't": "must not",
            "mustn't've": "must not have",
            "needn't": "need not",
            "needn't've": "need not have",
            "ne'er": "never",
            "o'clock": "of the clock",
            "o'er": "over",
            "ol'": "old",
            "oughtn't": "ought not",
            "oughtn't've": "ought not have",
            "shan't": "shall not",
            "sha'n't": "shall not",
            "shan't've": "shall not have",
            "she'd": "she had",
            "she'd've": "she would have",
            "she'll": "she shall",
            "she'll've": "she shall have",
            "she's": "she has",
            "should've": "should have",
            "shouldn't": "should not",
            "shouldn't've": "should not have",
            "somebody's": "somebody has",
            "someone's": "someone has",
            "something's": "something has",
            "so're": "so are",
            "so've": "so have",
            "so's": "so is",
            "that'll": "that all",
            "that're": "that are",
            "that'd": "that had",
            "that'd've": "that would have",
            "that's": "that is",
            "there'd": "there had",
            "there'd've": "there would have",
            "there's": "there is",
            "there're": "there are",
            "they'd": "they had",
            "they'd've": "they would have",
            "they'll": "they will",
            "they'll've": "they will have",
            "they're": "they are",
            "they've": "they have",
            "this's": "this is",
            "those're": "those are",
            "'tis": "it is",
            "'twas": "it was",
            "to've": "to have",
            "wasn't": "was not",
            "we'd": "we would",
            "we'd've": "we would have",
            "we'll": "we will",
            "we'll've": "we will have",
            "we're": "we are",
            "we've": "we have",
            "weren't": "were not",
            "what'd": "what did",
            "what'll": "what will",
            "what'll've": "what will have",
            "what're": "what are",
            "what's": "what is",
            "what've": "what have",
            "when's": "when is",
            "when've": "when have",
            "where'd": "where did",
            "where's": "where is",
            "where've": "where have",
            "who'd": "who would",
            "who'd've": "who would have",
            "who'll": "who will",
            "who'll've": "who will have",
            "whom'st'd've": "whom hast had have",
            "who're": "who are",
            "who's": "who is",
            "who've": "who have",
            "why'd": "why did",
            "why're": "why are",
            "why's": "why is",
            "why've": "why have",
            "will've": "will have",
            "won't": "will not",
            "won't've": "will not have",
            "would've": "would have",
            "wouldn't": "would not",
            "wouldn't've": "would not have",
            "y'all": "you all",
            "y'all'd": "you all would",
            "y'all'd've": "you all would have",
            "y'all're": "you all are",
            "y'all've": "you all have",
            "you'd": "you would",
            "you'd've": "you would have",
            "you'll": "you will",
            "you'll've": "you will have",
            "you're": "you are",
            "you've": "you have"
        }
        #text = 'I ain\'t don\'t do this to me. I ain\'t don\'t do this to me. I ain\'t don\'t do this to me.'
        # text = text.lower()
        for contraction in contractions:
            text = re.sub(contraction, contractions[contraction], text)
        ''' Splitting text into sentences and words '''
        sentences = text.split('.')
        tokenized_sentences = [word_tokenize(sentence) for sentence in sentences]
        print (tokenized_sentences)
        return tokenized_sentences

    def entity_recognition_spacy(text):
        ''' Uses the SPACY NER model. Currently written using the en_core_web_sm model '''
        spacy_model = spacy.load('en_core_web_sm')
        document = spacy_model(text)
        old_text = text
        anonymized_text = ''
        entities_in_document = document.ents
        number_of_entities = len(entities_in_document)
        ''' Function to slice and replace substrings with entity labels '''
        for index, ent in enumerate(entities_in_document):
            csv_writer.writerow([ ent, ent.label_, 'Text id'])
            if index is 0:
                anonymized_text += old_text[:ent.start_char] + ent.label_ + \
                    old_text[ent.end_char:entities_in_document[index].start_char]
            elif index is number_of_entities-1:
                anonymized_text += ent.label_ + old_text[ent.end_char:]
            else:
                anonymized_text += ent.label_ + \
                    old_text[ent.end_char:entities_in_document[index].start_char]
        return anonymized_text

        # Spacy
        preprocessed_text = preprocess(text)
        sentences = [' '.join(word) for word in preprocessed_text]
        text = '. '.join(sentences)
    return entity_recognition_spacy(text)