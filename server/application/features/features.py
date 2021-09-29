#######################
## Problem Types
######################
from typing import List, Tuple
import pandas as pd
import numpy as np


class FeatureSet:
    def n_binary_features(self):
        return len(self.binary_feature_names())

    def n_scalar_features(self):
        return len(self.scalar_feature_names())

    def binary_feature_names(self) -> List[str]:
        """(optional) returns a list of names for BINARY features. which can be used for heuristic label"""
        pass

    def scalar_feature_names(self) -> List[str]:
        """Returns a list of names for the features computed by this feature set"""
        raise NotImplementedError("has to be overwritten")

    def scalar2binary(self, scalar_features):
        """

        :param scalar_features: numpy array where each line corresponds to the feature vector for one text element
            computed by this feature set
        :return: binary numpy array of same length but possibly different width. Of Votes whether a feature is activated
        """
        pass

    @property
    def id_column_names(self):
        """Return string of the names of columns used as ID for this type of problem"""
        pass

    def document_2_featureMatrix(self, document_tree, filename=None) -> Tuple[pd.DataFrame, np.array]:
        """
        parse a document into a pandas dataframe with feature rows
        Each row is one unit (e.g. textline, page, textbox, depending on the subclass)

        :param document_tree:
        :param filename:
        :return: (ids, featureMatrix)
            ids: pandas dataframe with columns as in id_column_names. len(ids) number_of_elements (e.g. textline, textbos, page) in the document.
            featureMatrix: numpy array [number_of_elements, num_features]
        """
        raise NotImplementedError("has to be overwritten")

class LineLevelFeatures(FeatureSet):
    # Document -> one feature vector per line in the document
    # see line_features.py for already implemented features
    @property
    def id_column_names(self):
        return ["page_id", "bbox"]
    
class BlockLevelFeatures(FeatureSet):
    # Document -> one feature vector per block (textbox) in the document
    @property
    def id_column_names(self):
        return ["page_id", "bbox"]    

class PageLevelFeatures(FeatureSet):
    # Document -> one feature vector per page in the document
    @property
    def id_column_names(self):
        return ["page_id"]
