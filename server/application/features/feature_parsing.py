
import numpy as np

import xml.etree.ElementTree as ET
import urllib.request

import pandas as pd
import sys
import os
from typing import List

from . import page_features
from . import block_features
from . import line_features
from . import features

from . import utils_feat

#%%

class Document2FeaturesParser:
    def __init__(self, featureSets: List[features.FeatureSet],
                 filter_function=None,
                 binary_feature_weights=None, threshold_true=None, threshold_false=None,
                 heuristic_classnames=None
                 ):
        """
        For each text element classification problem there is going to be one designated instance of this class.
        Each instance merges the features of all featureSets passed in the constructor.

        :param featureSets: a list of featureSet subclass instances that will be applied to the document
        :param filter_function: a filter function to ignore certain text elements. e.g. feature_parsing.filter_empty_lines
            to ignore lines that don't contain any text
        :param binary_feature_weights: for each featureSet a list of scalar weights for all binary features returned by
            the featureSet. The binary veatures (aka votes) of are weighted with these weights and summed to compute a score
        :param threshold_true: if the score is above this threshold the text element gets the heurisic label true
        :param threshold_false: if the score is below this threshold the text element gets the heuristic label false
        :param heuristic_classnames: the names for the False and True classes. (e.g. ['not_title', 'title']
        """
        self.featureSets = featureSets
        self.id_column_names = self.get_id_colum_names()

        self.filter_function = filter_function

        # An heuristic guess is done using the features computed, but also some binary_feature_weights, 
        # threshold_true and threshold_true manually defined. If these are not, then, there is not any heuristic
        # previous classification
        # ON September 27th, 2021, I am leaving this here, BUT, so far we won't allow this option, as it will
        # add too many new option to the menus, plus the definition of the weights is not straightforward
        _heuristic_label_status = self._all_or_none([binary_feature_weights, threshold_true, threshold_true, heuristic_classnames])
        if _heuristic_label_status == 'all':
            self._check_size_of_binary_feature_weights(self.featureSets, binary_feature_weights)
            self.heuristic_label_computable = True
            self.threshold_true = threshold_true
            self.threshold_false = threshold_false
            assert(len(heuristic_classnames)==2)
            self.heuristic_classnames = ["heuristic_{}".format(c) for c in heuristic_classnames]
            self.binary_feature_weights = np.concatenate(binary_feature_weights, axis=0)
        elif _heuristic_label_status == 'some':
            raise ValueError("All or none of the constructor parameters [binary_feature_weights, threshold_true, threshold_false, heuristic_classnames] have to be specified")
        else:
            self.heuristic_label_computable = False

    def get_id_colum_names(self):
        """
        :return: a list of strings with the columns that uniquely identify a text element
        """
        within_doc_ids = self.featureSets[0].id_column_names
        for f in self.featureSets[1:]:
            _t = f.id_column_names
            if _t != within_doc_ids:
                raise ValueError("Not all featureSets return the same names from their property id_column_names")

        file_level_id_cols = ['uid']
        return file_level_id_cols + within_doc_ids


    def parse_document(self, uri):
        """
        Compute the feature table for the document

        :param document: Document instance
        :return: a pandas dataframe with one row per text element and its features as columns
        """
        if (uri.find('http://') > -1) or (uri.find('https://') > -1):
            opener = urllib.request.build_opener()
            XML_tree = ET.parse(opener.open(uri))
        else:
            XML_tree = ET.parse(uri)
        atomised_tree = XML_tree.getroot()  

        _, filename, _ = utils_feat.info_from_uri(uri)

        ids_collector = list()
        features_df_collector = list()
        for featureSet in self.featureSets:
            ids, feats = featureSet.document_2_featureMatrix(atomised_tree, filename)

            # THIS IS REQUIRED FROM Sept 28th, 2021, since we have some
            # extra hierarchy in the XML, with textgroup, and inside of them
            # we find the textboxes duplicated. The valid textboxes are the first ones
            ids_un = ids.drop_duplicates()
            ind_use = ids_un.index
            ids_un = ids_un.reset_index(drop = True)
            feats = np.asarray(feats)[ind_use]

            ids_collector.append(ids_un)

            feature_names = featureSet.scalar_feature_names()

            feats_dataframe = pd.DataFrame(data=feats, columns=feature_names)
            features_df_collector.append(feats_dataframe)

        self._check_ids_same(ids_collector)
        ids = ids_collector[0] # they are all the same just take the first
        
        id_vec = np.arange(len(ids))
        uid_vec = ['_'.join([filename, str(ids['page_id'].iloc[o]), str(o)]) for o in id_vec]
        ids.loc[:, "uid"] = uid_vec

        final = pd.concat([ids]+ features_df_collector, axis=1)
        assert(len(final)==len(features_df_collector[0]))

        final_filtered = self.filter_atoms(final)

        return final_filtered

    def filter_atoms(self, df):
        """Used to filer out for example empty textlines"""
        if self.filter_function is not None:
            try:
                mask = self.filter_function(df)
                filtered = df[mask]
                reindexed = filtered.reset_index(inplace=False, drop=True)
                return reindexed
            except Exception as e:
                msg = """ERROR: The user supplied a filter_function = {} to the constructor. It threw an error. 
                Maybe it relies on a feature (eg 'linetext') but no featureSet to compute this feature was given
                 (features.RawLineText in case of missing linetext). The exception raised by the filter function: \n {}: {}""".\
                    format(self.filter_function, type(e), e)
                raise ValueError(msg)
        else:
            return df

    def _check_size_of_binary_feature_weights(self, list_of_feature_sets, list_of_corresponding_weights):
        if len(list_of_feature_sets) != len(list_of_corresponding_weights):
            raise ValueError("An array of feature weights has to be given for each feature set")
        else:
            for featureSet, weights in zip(list_of_feature_sets, list_of_corresponding_weights):
                same_length = len(featureSet.binary_feature_names()) == len(weights)
                if not same_length:
                    raise ValueError("The featureSet {} returns the binary features {} but there is a wrong number of weights given for them: {}".format(
                        featureSet, featureSet.binary_feature_names(), weights
                    ))

    def _check_ids_same(self, ids_list):
        first_ids = ids_list[0]
        for featureSet_id, ids in enumerate(ids_list[1:]):
            if len(first_ids) != len(ids):
                raise ValueError("All Feature Sets have to return a dataframe with the same number of entries.")

            same_as_first = np.all(first_ids.values == ids)
            if not same_as_first:
                raise RuntimeError("""
                All FeatureSets have to return the same ids in the same order. 
                I.e. each row in the returned feature matrix returned from each featureSet has to correspond to the same element (textline, textbox, page etc.) in the document.
                {} returned different ids then {} for example. 
                """.format(self.featureSets[0], self.featureSets[featureSet_id]))

    def scalar2binary_heuristicLabel(self, scalarFeatureDf):
        """
        Computes the heuristic label for each textLine given the scalar features

        :param scalarFeatureDf: a pandas dataframe as returned by self.parse_document
        :return: a pandas dataframe with the same id columns and heuristic label
        """

        if not self.heuristic_label_computable:
            raise ValueError("This parser cant compute heuristic label because, feature_weights and thresholds were not set in the constructor")

        ids = scalarFeatureDf.loc[:, self.id_column_names]

        votes_collector = list()
        for currentFeatureSet in self.featureSets:
            binary_votes_names = currentFeatureSet.binary_feature_names()
            if len(binary_votes_names) >0:
                scalar_feature_names = currentFeatureSet.scalar_feature_names()
                current_scalar_features = scalarFeatureDf.loc[:, scalar_feature_names].values

                votes = currentFeatureSet.scalar2binary(current_scalar_features)

                df = pd.DataFrame(data=votes, columns = binary_votes_names)
                votes_collector.append(df)

        all_votes_df = pd.concat(votes_collector, axis=1)
        assert(len(all_votes_df)==len(votes_collector[0])) # no nan funny buisness

        weighted = all_votes_df.values * self.binary_feature_weights
        score = np.sum(weighted, axis=1)

        final = pd.concat([ids, all_votes_df], axis=1)
        assert(len(final) == len(all_votes_df))

        final.loc[:, "score"] = score
        is_title = 0.5*np.ones(len(score))
        is_title[score >= self.threshold_true] = 1.0
        is_title[score <= self.threshold_false] = 0.0

        final.loc[:, self.heuristic_classnames[0]] = 1- is_title
        final.loc[:, self.heuristic_classnames[1]] = is_title

        return final

    def _all_or_none(self, list_of_vars):
        # small helper to check if all vars or none of the vars are None
        is_defined = np.array([v is not None for v in list_of_vars])
        if np.all(is_defined):
            return 'all'
        elif np.any(is_defined):
            return 'some'
        else:
            return 'none'

def make_highlight_instructions_from_heuristic_label(heuristic_label, col_name):
    """return highlight instructions for doc.save_highlighted_to_file"""
    all_instructons = list()
    for page_id in np.unique(heuristic_label.page_id):
        vote_matrix = heuristic_label[heuristic_label.page_id == page_id]

        positive_bboxes = vote_matrix.bbox[vote_matrix.loc[:, col_name]==1.0]

        negative_bboxes = vote_matrix.bbox[vote_matrix.loc[:, col_name]==0.0]

        instructions_page = [(coords, "g") for coords in positive_bboxes] + [(coords, "r") for coords in negative_bboxes]

        all_instructons.append(instructions_page)
    return all_instructons


def extract_features_for_file(parser: Document2FeaturesParser, uri, 
                               compute_heuristic_label=False):

    print('Computing for:',uri)
    # Passing the uid and uri of the file, where it is
    features_all_files = parser.parse_document(uri)

    if compute_heuristic_label:
        heuristic_label_all_files = parser.scalar2binary_heuristicLabel(features_all_files)
        features_all_files = pd.concat([features_all_files, heuristic_label_all_files], axis = 1)

    return features_all_files

def filter_empty_lines(df):
    if not 'linetext' in df.columns:
        raise ValueError("""In order to use the filter function filter function 'filter_empty_lines' with
        the Document2FeaturesParser you must include features.RawLineText().byLine() as a feature. I.e. the column 'linetext' does not exist.
         """)

    return df.linetext.str.len() > 0

def get_available_parsers():

    """
    ######## I just leave this definition here as the example of a more complex feature parser
    ## Title Parser
    titleFeatures, titleFeatureWeights = zip(*[
        (line_features.IndentationFeatureSet(distance_threshold=20).byColumn(), [10]),
        (line_features.YSeparationFeatureSet().byColumn(), []),
        (line_features.CharacterTypeFeatures(n_chars_to_consider=18, list_of_min_number_in_category=[1, 1, 2]).byLine(), [10, 2, 5]), # at least 1 numbers, 1 bracket, 2 letters
        (line_features.FormatFeatures(n_chars_to_consider=20, min_number_per_font_type=[1, 5, 1, 0]).byLine(), [2, 9, 2, 0]), # one BoldItalic, 5 Bold, any Italic any Normal
        (line_features.RegexHits(['^ ?(X|x)? ?[0-9]{1,3} ?[a-zA-Z]? ?\(?[ 0-9]{0,4}\)? ?\.',
                             '^ ?(X|x)? ?[0-9]{1,3}[ a-zA-Z]? ?\(?[ 0-9]{0,4}\)? ?[\.\,]? ?[a-zA-Z]?']).byLine(), [5, 5]),
        (line_features.RawLineText().byLine(), []),
        (line_features.YearFeature().byPage(), [])
    ])
    titleParser = Document2FeaturesParser(titleFeatures, binary_feature_weights=titleFeatureWeights,
                                          filter_function = filter_empty_lines, # empty lines are ignored
                                          threshold_true=38, threshold_false=8, heuristic_classnames = CONSTANTS.title.class_names)
    """

    # Features for textboxes 
    aggregation_dict = dict(mean=np.mean, sum=np.sum, min=np.min, max=np.max)
    block_parser = Document2FeaturesParser(
        featureSets=[
            block_features.BlockText(),
            block_features.PageNormFeature(),
            block_features.BboxFeatures(),
            block_features.LengthBlock(),
            block_features.AggregateByBlock(line_features.CharacterTypeFeatures(n_chars_to_consider=999),
                                          aggregation_dict),
            block_features.AggregateByBlock(line_features.FormatFeatures(n_chars_to_consider=999),
                                          aggregation_dict)                                          
        ])      

    # Overview Page_classifier
    aggregation_dict = dict(mean=np.mean, sum=np.sum, min=np.min, max=np.max)
    textline_parser = Document2FeaturesParser(
        featureSets=[
            line_features.IndentationFeatureSet(distance_threshold=20).byBlock(),
            line_features.YSeparationFeatureSet().byBlock(),
            line_features.CharacterTypeFeatures(n_chars_to_consider=20).byLine(),
            line_features.FormatFeatures(n_chars_to_consider=20).byLine(),
            line_features.RawLineText().byLine()
        ])

    # Overview Page_classifier
    aggregation_dict = dict(mean=np.mean, sum=np.sum, min=np.min, max=np.max)
    page_parser = Document2FeaturesParser(
        featureSets=[
            page_features.PageText(),
            page_features.AggregateByPage(line_features.CharacterTypeFeatures(n_chars_to_consider=999),
                                          aggregation_dict),
            page_features.AggregateByPage(line_features.FormatFeatures(n_chars_to_consider=999),
                                          aggregation_dict),
            page_features.AggregateByPage(line_features.IndentationFeatureSet(distance_threshold=20),
                                          aggregation_dict)
        ])
            
    available_parser = dict(textline_type = textline_parser, page_type = page_parser, textblock_type = block_parser)

    return available_parser

"""
if __name__ == "__main__":
    available_parser = get_available_parsers()
    parser_names = list(available_parser.keys())

    import argparse
    argparser = argparse.ArgumentParser(description='Extract instances and features across years.')
    argparser.add_argument('--start', type=int, default = 1891, help="first year to process")
    argparser.add_argument('--end', type=int, default = 1995, help="last year to process")
    argparser.add_argument('--parser_name', required=True, choices=parser_names, help="Which parser to use, available: {}".format(parser_names))
    argparser.add_argument('--output_path', required=False, default="", type=str, help="Where to save the generated feature and possibly heursitic label files, if empty (recommended) it tries to find the path from a config in CONSTANTS.py corresponding to the given parser_name")
    argparser.add_argument('--visualise_foldername', type=str, default="", help="If a name is given, in each year folder of the data directory a subfolder with this name will be created that contains pdfs with the heuristic label of the documents marked")
    argparser.add_argument('--data_path', type=str, default="Path to the folder containing the original documents. ")
    argparser.add_argument("--heuristic_label", action='store_true', help="Flag. If present heursitic label will also be computed.")
    argparser.add_argument("--flag_type", type=int, default = 3, help="Flag. To indicate the type of document: 1 Amtliches Bulletin, 2 Additional protocols, and 3 Summary files")
    argparser.add_argument("--flag_forcecomp", type=str, default = 0, help="In case we want to compute again the corrected xml")
    argparser.add_argument("--flag_save_figs", type=int, default = 0, help="To save the preview of the corrected files. Careful, takes a lot of memory!")


    args = argparser.parse_args()
    print(args.flag_type)

    if args.output_path == "":
        if hasattr(CONSTANTS, args.parser_name):
            args.output_path = getattr(CONSTANTS, args.parser_name).problem_folder
        else:
            raise ValueError("No output path given and no configuration found for {} in CONSTANTS.py".format(args.parser_name))

    if args.data_path == "":
        if hasattr(CONSTANTS, args.parser_name):
            args.data_path = getattr(CONSTANTS, args.parser_name).path_to_input_files
        else:
            raise ValueError("No output path given and no configuration found for {} in CONSTANTS.py".format(args.parser_name))

    doc_parser = available_parser[args.parser_name]

    extract_features_for_years(doc_parser, args.start, args.end, output_path=args.output_path,
                               visualise_foldername=args.visualise_foldername,
                               compute_heuristic_label=args.heuristic_label, data_path = args.data_path,
                               flag_type=args.flag_type,
                               flag_forcecomp=args.flag_forcecomp, flag_save_figs=args.flag_save_figs)
"""