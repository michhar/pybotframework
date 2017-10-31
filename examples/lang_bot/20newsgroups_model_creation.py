from sklearn.datasets import fetch_20newsgroups
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.externals import joblib
import numpy as np

# Get all data
twenty_train = fetch_20newsgroups(subset='train',
     shuffle=True, random_state=42)


# Data categories and shape
print(twenty_train.target_names)
print(len(twenty_train.data))

# A sample and some data exploration
print("\n".join(twenty_train.data[0].split("\n")[:3]))
print(twenty_train.target_names[twenty_train.target[0]])

for t in twenty_train.target[:10]:
    print(twenty_train.target[t])
    print(twenty_train.target_names[t])

# A test set
twenty_test = fetch_20newsgroups(subset='test',
                                 categories=categories, 
                                 shuffle=True, 
                                 random_state=42)
docs_test = twenty_test.data

# count_vect = CountVectorizer()
# tfidf_transformer = TfidfTransformer(use_idf=False)
text_clf = Pipeline([('vect', count_vect),
                     ('tfidf', tfidf_transformer),
                     ('clf', SGDClassifier(loss='hinge', penalty='l2',
                                           alpha=1e-3, random_state=42)),
])

text_clf.fit(twenty_train.data, twenty_train.target)  

predicted = text_clf.predict(docs_test)
np.mean(predicted == twenty_test.target) 

# # Try out our classifier on new documents
# docs_new = ['God is love', 'OpenGL on the GPU is fast']
# X_new_counts = count_vect.transform(docs_new)
# X_new_tfidf = tfidf_transformer.transform(X_new_counts)

docs_new = ['Laughter and tears are both responses to frustration and exhaustion. \
I myself prefer to laugh, since there is less cleaning up to do afterward.',
            
           'There is no reason why good cannot triumph as often as evil. The triumph \
           of anything is a matter of organization. If there are such things as angels, \
           I hope that they are organized along the lines of the Mafia.']

predicted = text_clf.predict(docs_new)

for doc, category in zip(docs_new, predicted):
    print('%r => %s' % (doc, twenty_train.target_names[category]))
    
# Save the classifier
joblib.dump(text_clf, 'text_clf.pkl') 

# Load the classifier
text_clf = joblib.load('text_clf.pkl')

predicted = text_clf.predict(['My favorite toy as a child was a floppy disk.'])
print(twenty_train.target_names[predicted[0]])
