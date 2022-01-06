import sys

import re
import numpy as np
import pandas as pd
import pickle
import nltk
nltk.download(['punkt', 'wordnet', 'stopwords'])

from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords

from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.multioutput import MultiOutputClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report


import xgboost
from xgboost import XGBClassifier

from sqlalchemy import create_engine


def load_data(database_filepath):
    engine = create_engine('sqlite:///{}'.format(database_filepath))
    df = pd.read_sql_table('Messages', engine)
    X = df.message 
    Y = df.iloc[:,4:]
    category_names = Y.columns
    
    return X, Y, category_names


def tokenize(text):
    text = re.sub("[^a-zA-z0-9]"," ", text)
        
    tokens = word_tokenize(text)
    tokens = [t for t in tokens if t not in stopwords.words("english")]
    
    lemmatizer = WordNetLemmatizer()
    stemmer = PorterStemmer()
        
    clean_tokens = []
    for tok in tokens:
        lemmed_tok = lemmatizer.lemmatize(tok).lower().strip()
        stemmed_tok = stemmer.stem(lemmed_tok)
        cleaned_tok = stemmed_tok
        
        clean_tokens.append(cleaned_tok)

    return clean_tokens


def build_model():
    # text processing and model pipeline
    pipeline = Pipeline([
            ('vect', CountVectorizer(tokenizer=tokenize)),
            ('tfidf', TfidfTransformer()),
            ('clf', MultiOutputClassifier(XGBClassifier(eval_metric='logloss', 
                                                        use_label_encoder=False)))
        ])

    parameters = {'vect__ngram_range': ((1, 1), (1, 2))}
    
    # create gridsearch object and return as final model pipeline
    cv = GridSearchCV(pipeline, param_grid=parameters, cv=2, n_jobs=-1, verbose=3)
    
    return cv


def evaluate_model(model, X_test, Y_test, category_names):
    
    y_pred = pd.DataFrame(model.predict(X_test), columns=category_names)
    
    for cat in category_names:
        y_test_col = list(Y_test[cat])
        y_pred_col = list(y_pred[cat])
        print("Category: ", cat)
        print("\n", classification_report(y_test_col, y_pred_col))
     
 
def save_model(model, model_filepath):
    # Export model as a pickle file    
    pickle.dump(model, open(model_filepath, 'wb'))


def main():
    if len(sys.argv) == 3:
        database_filepath, model_filepath = sys.argv[1:]
        print('Loading data...\n    DATABASE: {}'.format(database_filepath))
        X, Y, category_names = load_data(database_filepath)
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)
        
        print('Building model...')
        model = build_model()
        
        print('Training model...')
        model.fit(X_train, Y_train)
        
        print('Evaluating model...')
        evaluate_model(model, X_test, Y_test, category_names)

        print('Saving model...\n    MODEL: {}'.format(model_filepath))
        save_model(model, model_filepath)

        print('Trained model saved!')

    else:
        print('Please provide the filepath of the disaster messages database '\
              'as the first argument and the filepath of the pickle file to '\
              'save the model to as the second argument. \n\nExample: python '\
              'train_classifier.py ../data/DisasterResponse.db classifier.pkl')


if __name__ == '__main__':
    main()