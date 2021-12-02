#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 17:23:15 2019

@author: luissalamanca
"""

"""
All the different functions for generating features
"""

import os, sys

import numpy as np

import pickle
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

from pathlib import Path
import time
import pandas as pd

# TODO: BETTER TO BE IMPORTED FROM CONSTANTS OR .env
SEP_UID_NAME = '_S_'

def get_vocab(text_ext_col, min_ocurr = 10, flag_lower = 1, flag_stopw = 1, n_words = 100,
              lang_stopw = ['german','french','italian'], list_extra_words = []):
    """
    Function to compute a vocabulary, giving some minimum occurrence of the words, plus some 
    stopwords to remove. 
    :params
    - text_ext: a column from the feature matrix with the text of that textblock, textline, etc.
    - min_ocurr: minimum ocurrence
    - flag_lower: to lowercase the text
    - flag_stopw: to remove stopwords in the languages specified later
    - n_words: words to keep for the final vocabulary
    - lang_stopw: languages for removing stopwords
    """
    all_text = get_alltext(text_ext_col)
    if flag_lower:
        all_text = all_text.lower()
    print('Start tokenization')
    st = time.time()  
    text_tokens = word_tokenize(all_text)
    print(time.time() - st)
    if flag_stopw:
        if len(lang_stopw):
            stopw = stopwords.words(lang_stopw)
        else:
            stopw = []

        #text_tokens = [word for word in text_tokens if word not in np.concatenate([stopw, list_ext])]
    all_words_remove = np.concatenate([stopw, list_extra_words])
    
    print('Start counting ocurrence')
    st = time.time()   
    vocab, ocurrence = np.unique(text_tokens, return_counts=True)
    print(time.time() - st)
      
    ind_rem = list()
    for word_r in all_words_remove:
        ind_aux = np.argwhere(np.asarray(vocab) == word_r)    
        if len(ind_aux):
            ind_rem.append(ind_aux)
    print('Removed stopwords')
    ind_keep = np.setdiff1d(np.arange(len(vocab)),ind_rem) 
    vocab = vocab[ind_keep]
    ocurrence = ocurrence[ind_keep]
    
    ind_ch = np.ravel(np.argsort(ocurrence[ocurrence > min_ocurr])[::-1][:n_words])
    vocab_final = vocab[ocurrence > min_ocurr][ind_ch]
    return vocab_final, ocurrence[ocurrence > min_ocurr][ind_ch]

def create_save_vocab(feature_mat, min_ocurr = 20, n_words = 400,
                    flag_lower = 1, flag_stopw = 1):
    """
    Given some input column with text, obtains a vocabulary using the
    parameters defined by the user for the specific case study
    """
    print("-- Creating vocabulary")
    
    type_text = np.intersect1d(["blocktext", "linetext", "pagetext"], feature_mat.columns)[0]

    text_col = np.array(feature_mat[type_text])

    vocab_final, ocurrence = get_vocab(text_col, min_ocurr = min_ocurr, flag_lower = flag_lower, 
                                            flag_stopw = flag_stopw, n_words = n_words)        
    print('Vocabulary computed')
    return vocab_final

def get_alltext(text_ext_col):
    """
    Just group together all the text from the blocktext column
    """
    all_text_str = ''
    for text_ind in np.arange(len(text_ext_col)):
        if text_ext_col[text_ind] is not None:
            all_text_str += text_ext_col[text_ind]
    return all_text_str

def get_coordinates_of_boxes(boxes):
    """
    :param boxes: list of xml elements that have a bbox attribute
    :return: a 4-tuple [topL, topR, bottomL, bottomR] each containing a numpy array with the coordinates
    """
    #TODO top and buttom might acutally be switched since origin is at bottom left page corner
    topL = list()
    topR = list()
    bottomL = list()
    bottomR = list()

    def add_tuple_to_lists(tL, tR, bL, bR):
        topL.append(float(tL))
        topR.append(float(tR))
        bottomL.append(float(bL))
        bottomR.append(float(bR))

    for box in boxes:
        bbox = box.attrib["bbox"]
        coords = bbox.split(",")
        add_tuple_to_lists(*coords)

    return [np.array(c) for c in [topL, topR, bottomL, bottomR]]

def info_from_uri(uri):
    name = Path(uri).stem
    uid = name.split(SEP_UID_NAME)[0]
    filename = name.split(SEP_UID_NAME)[1]
    suffix = Path(uri).suffix
    return uid, filename, suffix

####################
## I believe all this belongs more to the learning model
####################

def probs_for_HMM(datadf, class_n):
    datadf = datadf.groupby(['year','file_id','page_id'], sort=False)[class_n]

    vec_start = list()
    trans_mat = None
    for i,g in enumerate(datadf):
        auxmat = np.asarray(g[1][class_n]).reshape(-1,len(class_n))
        class_val = np.argwhere(auxmat)[:,1]
        vec_start.append(class_val[0])
        trans_mat = trans_matrix_counts(class_val, class_n, trans_mat)

    probs_trans = trans_probs(trans_mat)

    # To avoid some classes going to 0 on the start prob, we first extend this
    vec_start.extend(range(len(class_n)))
    probs_start = np.unique(vec_start, return_counts=True)[1]
    probs_start = probs_start/np.sum(probs_start)
    
    return probs_trans, probs_start

def trans_matrix_counts(sec_vals, vec_classes, trans_mat = None):
    
    if trans_mat is None:
        trans_mat = np.zeros((len(vec_classes), len(vec_classes)))
        
    for i,j in zip(sec_vals[:-1],sec_vals[1:]):
        trans_mat[i,j] += 1
        
    return trans_mat

def trans_probs(trans_mat):
    
    trans_probs = trans_mat/(1e-10 + np.sum(trans_mat, axis = 1).reshape(-1,1))
    return trans_probs

def build_fg_comp_postp(mat_probs, probs_trans):
    from sumproduct import Variable, Factor, FactorGraph
    import time

    st = time.time()
    g = FactorGraph(silent=True) # init the graph without message printouts

    for p in range(mat_probs.shape[0]):
        exec('z{} = Variable("z{}", {})'.format(p, p, mat_probs.shape[1]))
        exec('x{} = Variable("x{}", {})'.format(p, p, 1)) 
        exec('fz{}x{} = Factor("fz{}x{}", mat_probs[p].reshape(-1,1))'.format(p,p,p,p))
        exec('g.add(fz{}x{})'.format(p,p))
        exec('g.append("fz{}x{}",z{})'.format(p,p,p))
        exec('g.append("fz{}x{}",x{})'.format(p,p,p))
        # Adding transition matrices
        
    for p in range(mat_probs.shape[0]):    
        if p < (mat_probs.shape[0] - 1):
            exec('tz{}z{} = Factor("tz{}z{}", probs_trans)'.format(p + 1,p,p + 1,p))
            exec('g.add(tz{}z{})'.format(p + 1,p))
            exec('g.append("tz{}z{}",z{})'.format(p+1,p,p+1))
            exec('g.append("tz{}z{}",z{})'.format(p+1,p,p))        
    #print('graph time: %f' % (time.time() - st))

    g.compute_marginals()
    #print('graph time: %f' % (time.time() - st))

    mat_probs_new = []
    for p in range(mat_probs.shape[0]):
        v_n = 'z{}'.format(p)
        mat_probs_new.append(g.nodes[v_n].marginal())

    mat_probs_new = np.asarray(mat_probs_new)
    #print('total time: %f' % (time.time() - st))
    return mat_probs_new

def train_crf(datadf, class_n, flag_c, L1c = 0.1, L2c = 0.1):

    import sklearn_crfsuite

    datadf = datadf.groupby(['year','file_id','page_id'])[class_n]

    X_train = list()
    y_train = list()
    for i,g in enumerate(datadf):
        auxmat = np.asarray(g[1][class_n]).reshape(-1,len(class_n))
        class_val = np.argwhere(auxmat)[:,1]
        auxmat_b = np.zeros(auxmat.shape)
        auxmat_b[auxmat] = 1
        if flag_c == 2:
            X_train.append(sent2features(class_val))
        elif flag_c == 3:
            X_train.append(sent2features_l(auxmat_b))
        elif flag_c == 4:
            X_train.append(sent2features_2l(auxmat_b))
        y_train.append(sent2labels(class_val))
    
    print('  - Regularization CRF, L1 =',L1c,'L2 =',L2c)

    crf = sklearn_crfsuite.CRF(
        algorithm='lbfgs',
        c1=L1c, #L1
        c2=L2c, #L2
        max_iterations=100,
        all_possible_transitions=True
    )
    crf.fit(X_train, y_train)
    
    return crf

def word2features(class_vec, i):

    features = {
        'bias': 1.0,
        'class': int(class_vec[i]),
    }
    if i > 0:
        features.update({
            'class-1': int(class_vec[i-1]),
        })
    else:
        features['BOS'] = True

    if i < len(class_vec)-1:
        features.update({
            'class+1': int(class_vec[i+1]),
        })
    else:
        features['EOS'] = True

    return features

def word2features_l(prob_mat, i):

    def add_row(f_d, rows_mat, extra_str):
        for i in range(len(rows_mat)):
            name_c = 'class{}.{}'.format(i,extra_str)
            f_d[name_c] = float(rows_mat[i])
        return f_d
            
    features = {
        'bias': 1.0,
    }
    features = add_row(features, prob_mat[i], '0')    
    
    if i > 0:
        features = add_row(features, prob_mat[i-1], '-1')
    else:
        features['BOS'] = True

    if i < len(prob_mat)-1:
        features = add_row(features, prob_mat[i+1], '+1')
    else:
        features['EOS'] = True

    return features

def word2features_2l(prob_mat, i):

    def add_row(f_d, rows_mat, extra_str):
        for i in range(len(rows_mat)):
            name_c = 'class{}.{}'.format(i,extra_str)
            f_d[name_c] = float(rows_mat[i])
        return f_d
            
    features = {
        'bias': 1.0,
    }
    features = add_row(features, prob_mat[i], '0')    
    
    if i > 1:
        features = add_row(features, prob_mat[i-2], '-2')
        features = add_row(features, prob_mat[i-1], '-1')
    if i > 0:
        features = add_row(features, prob_mat[i-1], '-1')        
    else:
        features['BOS'] = True

    if i < len(prob_mat)-2:
        features = add_row(features, prob_mat[i+2], '+2')
        features = add_row(features, prob_mat[i+1], '+1')
    if i < len(prob_mat)-1:
        features = add_row(features, prob_mat[i+1], '+1')        
    else:
        features['EOS'] = True

    return features

def sent2features_2l(prob_mat):
    return [word2features_2l(prob_mat, i) for i in range(len(prob_mat))]

def sent2features_l(prob_mat):
    return [word2features_l(prob_mat, i) for i in range(len(prob_mat))]

def sent2features(class_vec):
    return [word2features(class_vec, i) for i in range(len(class_vec))]

def sent2labels(class_vec):
    return [str(label) for label in class_vec]

