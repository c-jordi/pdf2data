
import pandas as pd
import numpy as np

from . import features
from . import line_features

class AggregateByPage(features.PageLevelFeatures):
    # apply a LineCollectionFeatureSet for each textcolumn in a document

    def __init__(self, line_collection_feature_set: line_features.LineCollection2ListOfFeatureVecs,
                    dictionary_of_aggregators
                 ):
        """
        :param line_collection_feature_set: an instance of LineCollection2ListOfFeatureVecs or SingleLineFeatureSet.
            The later is naturally a subclass of the former since (when called with a list of lines) it will just apply the
            single line feature transformation to each line in that list)
        :param dictionary_of_aggregators: a dictionary with string keys and callable values. the values are functions
            that take an axis argument which are used for aggregating (e.g. np.mean, np.std, np.max ...)
        """
        self.featureSet = line_collection_feature_set

        self.aggregator_names = list(dictionary_of_aggregators.keys())

        self.feature_names = ["{}_{}".format(agg_name, feat_name) for agg_name in self.aggregator_names for feat_name in self.featureSet.scalar_feature_names()]
        self.dictionary_of_aggregators = dictionary_of_aggregators


    def binary_feature_names(self): #
        raise NotImplementedError()

    def scalar2binary(self, scalar_features):
        raise NotImplementedError()

    def scalar_feature_names(self):
        return self.feature_names

    def aggregate(self, feats):
        aggegation_in_each_type = [self.dictionary_of_aggregators[agg_name](feats, axis=0) for agg_name in self.aggregator_names]
        # this should now be an iterator of vectors
        feature_vector_page =  np.concatenate(aggegation_in_each_type) #
        assert(len(feature_vector_page.shape)==1)
        return feature_vector_page

    def document_2_featureMatrix(self, document_tree, filename=None):
        # loop through pages. compute all the features make the matrix
        page_ids = list()
        feature_collector_all = list()

        for page in document_tree.findall(".//page"):
            all_textlines = page.findall(".//textline")

            feats = self.featureSet.scalar_features_line_collection(all_textlines, filename=filename)

            aggregated_features = self.aggregate(feats)

            page_ids.append(int(page.attrib["id"]))
            feature_collector_all.append(aggregated_features[None, :]) # make sure it's a row vector

        index_df = pd.DataFrame(data=dict(page_id = page_ids))
        final_feature_matrix = np.concatenate(feature_collector_all, axis=0)

        return index_df, final_feature_matrix

class PageText(features.PageLevelFeatures):
    def scalar_feature_names(self):
        return ["pagetext"]

    def document_2_featureMatrix(self, document_tree, filename=None):
        # loop through pages. compute all the features make the matrix
        page_ids = list()
        feature_collector_all = list()

        for page in document_tree.findall(".//page"):
            all_textblocks = page.findall(".//text_block")
            page_string = np.array(" ".join([textblock.text for textblock in all_textblocks]))
            # we have to wrap it in a single element numpy array.

            page_ids.append(int(page.attrib["id"]))
            feature_collector_all.append(page_string[None, None])
            # make sure it's a row vector, since it is a 'string scalar' before we have to blow it up to a 2d array


        index_df = pd.DataFrame(data=dict(page_id = page_ids))
        final_feature_matrix = np.concatenate(feature_collector_all, axis=0)

        return index_df, final_feature_matrix

