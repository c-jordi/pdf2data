
import pandas as pd
import numpy as np

from . import features
from . import line_features

class AggregateByBlock(features.BlockLevelFeatures):
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

    def scalar_feature_names(self):
        return self.feature_names

    def aggregate(self, feats):
        aggegration_in_each_type = [self.dictionary_of_aggregators[agg_name](feats, axis=0) for agg_name in self.aggregator_names]
        # this should now be an iterator of vectors
        feature_vector_block =  np.concatenate(aggegration_in_each_type) #
        assert(len(feature_vector_block.shape)==1)
        return feature_vector_block

    def document_2_featureMatrix(self, document_tree, filename=None):
        # loop through pages. compute all the features make the matrix
        page_ids = list()
        feature_collector_all = list()
        bbox = list()

        for page in document_tree.findall(".//page"):
            for block in page.findall(".//textbox"):
                all_textlines = block.findall(".//textline")

                # This condition is again introduced in Sept21, as now the XML
                # may include these extra elements, without textline inside, that 
                # were causing this error
                if len(all_textlines):
                    feats = self.featureSet.scalar_features_line_collection(all_textlines, filename=filename)

                    if len(feats):
                        aggregated_features = self.aggregate(feats)
        
                        if 'bbox' in block.keys():
                            page_ids.append(int(page.attrib["id"]))
                            bbox.append(block.attrib["bbox"])
                            feature_collector_all.append(aggregated_features[None, :]) # make sure it's a row vector

        index_df = pd.DataFrame(data=dict(page_id = page_ids, bbox = bbox))
        final_feature_matrix = np.concatenate(feature_collector_all, axis=0)

        return index_df, final_feature_matrix

class BlockText(features.BlockLevelFeatures):
    def scalar_feature_names(self):
        return ["blocktext"]

    def document_2_featureMatrix(self, document_tree, filename=None):
        # loop through pages. compute all the features make the matrix
        page_ids = list()
        feature_collector_all = list()
        bbox = list()

        for page in document_tree.findall(".//page"):
            for block in page.findall(".//textbox"):
                all_textblocks = block.findall(".//text_block")
                block_string = np.array(" ".join([textblock.text for textblock in all_textblocks]))
                # we have to wrap it in a single element numpy array.
                #print(block_string)
                
                if 'bbox' in block.keys():
                    bbox.append(block.attrib["bbox"])
                    page_ids.append(int(page.attrib["id"]))
                    feature_collector_all.append(block_string[None, None])
                # make sure it's a row vector, since it is a 'string scalar' before we have to blow it up to a 2d array

        index_df = pd.DataFrame(data=dict(page_id = page_ids, bbox = bbox))
        final_feature_matrix = np.concatenate(feature_collector_all, axis=0)

        return index_df, final_feature_matrix
    
class PageNormFeature(features.BlockLevelFeatures):

    def scalar_feature_names(self):
        return ["page_norm"]

    def document_2_featureMatrix(self, document_tree, filename=None):
        # loop through pages. compute all the features make the matrix
        page_ids = list()
        feature_collector_all = list()
        bbox = list()
        n_pages = len(document_tree.findall(".//page"))
        if n_pages == 1:
            n_pages = 2
        
        for page in document_tree.findall(".//page"):
            for block in page.findall(".//textbox"):
                page_norm = (float(page.attrib["id"]) - 1)/(n_pages-1)
                # we have to wrap it in a single element numpy array.
                #print(block_string)
                
                if 'bbox' in block.keys():
                    page_ids.append(int(page.attrib["id"]))
                    bbox.append(block.attrib["bbox"])
                    feature_collector_all.append(page_norm)
                # make sure it's a row vector, since it is a 'string scalar' before we have to blow it up to a 2d array

        index_df = pd.DataFrame(data=dict(page_id = page_ids, bbox = bbox))
        #final_feature_matrix = np.concatenate(feature_collector_all, axis=0)

        return index_df, feature_collector_all

class BboxFeatures(features.BlockLevelFeatures):

    def binary_feature_names(self):
        return ["bbox_features"]

    def scalar_feature_names(self):
        return ["x_coord", "y_coord", "height", "width"]

    def document_2_featureMatrix(self, document_tree, filename=None):
        # loop through pages. compute all the features make the matrix
        page_ids = list()
        feature_collector_all = np.array([]).reshape((0,4))
        bbox = list()
        
        for page in document_tree.findall(".//page"):
            for block in page.findall(".//textbox"):
                # we have to wrap it in a single element numpy array.
                #print(block_string)
                if 'bbox' in block.keys():                
                    bbox_val = block.attrib["bbox"].split(',')
                    xc = float(bbox_val[0])
                    yc = float(bbox_val[1])
                    height = float(bbox_val[3]) - float(bbox_val[1])
                    width = float(bbox_val[2]) - float(bbox_val[0])                    
                    page_ids.append(int(page.attrib["id"]))
                    bbox.append(block.attrib["bbox"])
                    feature_collector_all = np.concatenate([feature_collector_all,np.array([xc, yc, height, width]).reshape((1,4))])
                # make sure it's a row vector, since it is a 'string scalar' before we have to blow it up to a 2d array

        index_df = pd.DataFrame(data=dict(page_id = page_ids, bbox = bbox))
        #final_feature_matrix = np.concatenate(feature_collector_all, axis=0)

        return index_df, feature_collector_all
    
class LengthBlock(features.BlockLevelFeatures):
    def scalar_feature_names(self):
        return ["n_char"]

    def document_2_featureMatrix(self, document_tree, filename=None):
        # loop through pages. compute all the features make the matrix
        page_ids = list()
        feature_collector_all = list()
        bbox = list()

        for page in document_tree.findall(".//page"):
            for block in page.findall(".//textbox"):
                all_textblocks = block.findall(".//text_block")
                len_str = len(" ".join([textblock.text for textblock in all_textblocks]))
                # we have to wrap it in a single element numpy array.
                #print(block_string)
                if 'bbox' in block.keys():                
                    page_ids.append(int(page.attrib["id"]))
                    bbox.append(block.attrib["bbox"])
                    feature_collector_all.append(len_str)
                # make sure it's a row vector, since it is a 'string scalar' before we have to blow it up to a 2d array

        index_df = pd.DataFrame(data=dict(page_id = page_ids, bbox = bbox))
        #final_feature_matrix = np.concatenate(feature_collector_all, axis=0)

        return index_df, feature_collector_all    

