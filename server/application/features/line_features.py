import re

import numpy as np
import pandas as pd
from sklearn.cluster import AgglomerativeClustering

from . import features
from . import utils_feat

class LineCollection2ListOfFeatureVecs:
    # multiple textlines -> multiple feature vectors (using other textlines as context)
    """each subclass is used to compute a set of features for a collection of textlines. (for example all textlines on a page)"""

    def __init__(self):
        raise RuntimeError("This is an abstract class and should not be initialised.")

    def n_binary_features(self):
        return len(self.binary_feature_names())

    def n_scalar_features(self):
        return len(self.scalar_feature_names())

    def binary_feature_names(self):
        return []

    def scalar_feature_names(self):
        raise NotImplementedError("scalar_feature_names has to be overwritten")

    def scalar2binary(self, scalar_features):
        return np.zeros((len(scalar_features), 0))

    def scalar_features_line_collection(self, line_collection, filename=None):
        """returns a float numpy array with a float number for each feature
            line_collection: a array of text_line xml elements
        """
        pass

    def byPage(self):
        """apply the line set feature for each page in the document"""
        return ByPage(self)

    def byBlock(self):
        """apply the line set feature for each block in the document"""
        return ByBlock(self)        

class SingleLineFeatureSet(LineCollection2ListOfFeatureVecs):
    # single text line -> single feature vector
    # naturally this also implements multiple textlines -> multiple feature vectors

    def __init__(self):
        raise RuntimeError("This is an abstract class and should not be initialised.")

    def n_binary_features(self):
        return len(self.binary_feature_names())

    def n_scalar_features(self):
        return len(self.scalar_feature_names())

    def scalar_features_line(self, textline, filename=None):
        raise NotImplementedError("Should be overwritten")

    def scalar_features_line_collection(self, line_collection, filename=None):
        all_feats = [self.scalar_features_line(tl, filename)[None, :] for tl in line_collection]
        if len(all_feats):
            return np.concatenate(all_feats, axis=0)
        else:
            return all_feats
        
    def binary_feature_names(self):
        return []

    def scalar_feature_names(self):
        raise NotImplementedError("scalar_feature_names has to be overwritten")

    def scalar2binary(self, scalar_features):
        return np.zeros((len(scalar_features), 0))
    # convenience function to easily get wrappers

    def byLine(self):
        """apply the single line feature line by line"""
        return ByLine(self)


class RawLineText(SingleLineFeatureSet):
    """ just returns the text of the line without formatting options, this is special as the datatype of the feature is string"""
    def __init__(self):
        pass

    def scalar_feature_names(self):
        return ["linetext"]

    def scalar_features_line(self, textline, filename=None):
        text_blocks = textline.findall("./text_block")
        text = "".join([tB.text for tB in text_blocks])
        return np.array([text], dtype=str)


class CharacterTypeFeatures(SingleLineFeatureSet):
    """ count number of character types in bins in the line """

    def __init__(self, bucket_boundaries=None, n_chars_to_consider=None, list_of_min_number_in_category=None):
        """
        Count number of letters, digits, brackets in buckets of the line


        :param bucket_boundaries: (optional) list of integer number specifying boundaries. The returned feature vector
            will have 3 entries per bucket with the counts of numbers, brackets, letters in that bucket
        :param n_chars_to_consider: (optional) only the first n characters are considered
        :param list_of_min_number_in_category: (optional) The minimum number of each character type above which the binary
            feature for the character type is true.
        """
        # :param bucket_boundaries: e.g. [0, 4, 9] then there will be two outputs for each character type indicating it's number in the interval [0,4[ and [4, 9[ characters
        if (bucket_boundaries is None) == (n_chars_to_consider is None):
            raise ValueError("exactly one of bucket_boundaries or n_chars_to_consider has to be specified")

        if bucket_boundaries is None:
            self.bucket_boundaries = [0, n_chars_to_consider]
        else:
            self.bucket_boundaries = bucket_boundaries

        self.min_numbers_per_category = list_of_min_number_in_category

        self.character_types = [list('0123456789I'),
                                list('[](){}|.,'),
                                list('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz')]


    def scalar_feature_names(self):
        return self.binary_feature_names()

    def binary_feature_names(self):
        character_type_names = ["numbers", "brackets", "letters"]
        out = list()
        for bucked_id in range(len(self.bucket_boundaries)-1):
            texts = [char_type + "_bucket"+str(bucked_id) for char_type in character_type_names]
            out += texts
        return out

    def scalar2binary(self, scalar_features):
        if len(self.bucket_boundaries) != 2:
            raise ValueError("For simplicity binary features on Character Type counts do not work with buckets. Please specifiy n_chars_to_consider as single integer")

        if self.min_numbers_per_category is None:
            raise ValueError("To use CharacterTypeFeatures for heuristic label please pass 3 entries as list_of_min_number_in_category in the constructor")
        return scalar_features >= self.min_numbers_per_category

    def scalar_features_line(self, textline, filename=None):
        text = "".join([tB.text for tB in textline.findall("./text_block")])

        out = np.zeros((len(self.bucket_boundaries)-1, len(self.character_types)))
        if text == "":
            return out.flatten()

        for bucket_id in range(len(self.bucket_boundaries) - 1):
            bucket_text = text[self.bucket_boundaries[bucket_id]: self.bucket_boundaries[bucket_id + 1]]
            for current_type_id, current_char_types in enumerate(self.character_types):
                char_in_type = np.isin(np.array(list(bucket_text)), current_char_types)

                n_char_in_type = np.count_nonzero(char_in_type)

                out[bucket_id, current_type_id] = n_char_in_type

        return out.flatten()



class FormatFeatures(SingleLineFeatureSet):
    """ number of character per font type in first n charaters. See _get_font_type_vec for the types of font"""

    def __init__(self, n_chars_to_consider, min_number_per_font_type=None):
        """
        Number of character per font type in first n characters. These are 4 features  corresponding to the number of
        BoldItalic, Bold, Italic and Normal characters respectively

        :param n_chars_to_consider: number of characters to consider
        :param min_number_per_font_type: (optional) for heuristic parsing the minimum number of each type above which
            the binary feature is true
        """

        self.n_chars_to_consider = n_chars_to_consider
        self.min_number_per_font_type = np.array(min_number_per_font_type)


    def _get_font_type_vec(self, font_type_string):
        if font_type_string.find("BoldItalic") != -1:
            return np.array([1,0,0,0])
        elif font_type_string.find("Bold") != -1:
            return np.array([0,1,0,0])
        elif font_type_string.find("Italic") != -1:
            return np.array([0,0,1,0])
        else:
            return np.array([0,0,0,1])

    def scalar_feature_names(self):
        return self.binary_feature_names()

    def binary_feature_names(self):
        return ["BoldItalic", "Bold", "Italic", "Normal"]

    def scalar_features_line(self, textline, filename=None):
        result = np.zeros(self.n_scalar_features())
        n_chars_so_far = 0
        for tB in textline.findall("./text_block"):
            text = tB.text
            font_string = tB.attrib["font"]
            font_type_indicator = self._get_font_type_vec(font_string)
            n_chars = len(tB.text)
            if n_chars_so_far+n_chars > self.n_chars_to_consider:
                n_chars_to_count = (self.n_chars_to_consider-n_chars_so_far)

            else:
                n_chars_to_count = n_chars

            result += n_chars_to_count*font_type_indicator
            n_chars_so_far += n_chars_to_count
            if n_chars_so_far >= self.n_chars_to_consider:
                assert(np.sum(result) == self.n_chars_to_consider)
                break

        return result

    def scalar2binary(self, scalar_features):
        out = scalar_features >= self.min_number_per_font_type
        return out


class RegexHits(SingleLineFeatureSet):
    """ checks for each regex if it hit"""
    def __init__(self, list_of_regex):
        """
        Checks for a list or regular expressions if each is present in the line

        :param list_of_regex: a list of strings with regular expressions
        """
        self.regex_texts = list_of_regex
        self.list_of_regex = [re.compile(pattern) for pattern in list_of_regex]

    def binary_feature_names(self):
        return ["Regex({})".format(r) for r in self.regex_texts]

    def scalar_feature_names(self):
        return self.binary_feature_names()

    def scalar_features_line(self, textline, filename=None):
        result = np.zeros(self.n_scalar_features())

        text_of_line = "".join([block.text for block in textline.findall("./text_block")])
        if len(text_of_line) == 0:
            return result

        for p_id, pattern in enumerate(self.list_of_regex):
            hit = re.search(pattern, text_of_line)
            result[p_id] = (hit is not None)

        return result

    def scalar2binary(self, scalar_features_page):
        return scalar_features_page

class YSeparationFeatureSet(LineCollection2ListOfFeatureVecs):
    def __init__(self):
        self.max_dist_filler_value = 1000

    def scalar_feature_names(self):
        return ['dist_prev_line', 'dist_next_line']

    def scalar_features_line_collection(self, line_collection, filename=None):
        """
        :param line_collection:
        :return: numpy array out:
            out[:, 0] distance to closest nonempty line before
            out[:, 1] distance to closes nonempty line after line
        """
        # get min above and bellow
        (x0, y0, x1, y1) = utils_feat.get_coordinates_of_boxes(line_collection) #[l.attrib['bbox'] for l in line_collection])


        is_not_empty = np.array([len(l)>=1 for l in line_collection])

        nonempty_y1 = y1[is_not_empty]
        nonempty_y0 = y0[is_not_empty]

        dist_to_above = np.zeros(len(line_collection))
        dist_to_next = np.zeros(len(line_collection))
        for i in range(len(line_collection)):
            current_y1 = y1[i]
            current_y0 = y0[i]

            is_above = nonempty_y0 > current_y1
            is_bellow = nonempty_y1 < current_y0

            if np.any(is_above):
                dist_to_above[i] = np.min(nonempty_y0[is_above]) - current_y1
            else:
                dist_to_above[i] = self.max_dist_filler_value

            if np.any(is_bellow):
                dist_to_next[i] = current_y0 - np.max(nonempty_y1[is_bellow])
            else:
                dist_to_next[i] = self.max_dist_filler_value

        out = np.concatenate([dist_to_above[:, None], dist_to_next[:, None]], axis=1)
        assert(np.all(out > 0))
        return out



class IndentationFeatureSet(LineCollection2ListOfFeatureVecs):
    def __init__(self, clustering_algo=None, distance_threshold=15):
        """
        Compute indentation levels for each line in a group of lines

        :param clustering_algo: (optional) an sklearn clustering algorithm.
        :param distance_threshold: (optional) distance_threshold parameter for the default AgglomorativeClustering.
            Should ideally be slightly bellow the difference in x-coordinates of two different indentation levels
        """
        self.titles = None

        if clustering_algo is None:
            self.clustering_algo = AgglomerativeClustering(distance_threshold=distance_threshold, n_clusters=None)
        else:
            self.clustering_algo = clustering_algo

    def binary_feature_names(self):
        return ["first_indent_level"]

    def scalar_feature_names(self):
        return ["indentation_level", "percent_rank_x", "x_coord"]

    def scalar_features_line_collection(self, line_collection, filename=None):
        """
        :param line_collection:
        :return: numpy array out:
            out[:, 0] identation level of each line (i.e. how many times tab key pressed)
            out[:, 1] the percentage of how far to the right each line is relative to the other ones
            out[:, 2] the absolut x-coordinate of each line
        """

        topL, _, _, _ = utils_feat.get_coordinates_of_boxes(line_collection)

        n_lines = len(topL)

        out = np.zeros((n_lines, self.n_scalar_features()))


        out[:, 0] = self.indentation_levels_from_pos(topL)

        ####
        percent_rank_of_lines = np.argsort(topL) / len(topL)
        out[:, 1] = percent_rank_of_lines

        ####
        out[:, 2] = topL

        return out

    def indentation_levels_from_pos(self, list_of_pos):
        """
        Returns the indentation level for a list of lines given by their coordinate position
        :param list_of_pos: a numpy array with the x position of each line
        :return: a int numpy array of same length indicating the indentation level of each line, 0 is leftmost
        """
        if len(list_of_pos) == 1:
            return 0 # a single line has indentation level 0

        arg_sorted_topL = np.argsort(list_of_pos) # i.e. for each line the rank it has among all other lines in terms of coordinates.

        cluster_ids_of_lines = self.clustering_algo.fit_predict(np.expand_dims(list_of_pos, axis=-1))

        cluster_ids_of_sorted_lines = cluster_ids_of_lines[arg_sorted_topL]
        t = np.unique(cluster_ids_of_sorted_lines, return_index=True)[1]
        rank_of_clusters = np.argsort(t) # the cluster ids ordered in increasing coordinate of the center

        cluster_id_2_indentation_level = np.argsort(rank_of_clusters) # _[k] is the indentation level of cluster k

        semantic_cluster_ids_of_lines = cluster_id_2_indentation_level[cluster_ids_of_lines] # now a line has clusterid 0 if it is leftmost

        return semantic_cluster_ids_of_lines

    def scalar2binary(self, scalar_features):
        is_first_indentation = scalar_features[:, 0] == 0
        return np.expand_dims(is_first_indentation, axis=1)

class ByLine(features.LineLevelFeatures):

    def __init__(self, single_line_feature_set: SingleLineFeatureSet):
        """
        apply a SingleLineFeatureSet line by line for all lines in the document

        :param single_line_feature_set: An instance of an arbitrary subclass of SingleLineFeatureSet
        """
        self.featureSet = single_line_feature_set

    def binary_feature_names(self):
        return self.featureSet.binary_feature_names()

    def scalar_feature_names(self):
        return self.featureSet.scalar_feature_names()

    def scalar2binary(self, scalar_features):
        return self.featureSet.scalar2binary(scalar_features)

    def document_2_featureMatrix(self, document_tree, filename=None):
        # loop through pages. compute all the features make the matrix
        page_ids = list()
        bbox = list()
        feature_collector = list()

        for page in document_tree.findall(".//page"):
            for line in page.findall(".//textline"):
                feats = self.featureSet.scalar_features_line(line, filename=filename)

                feature_collector.append(feats[None, :])
                bbox.append(line.attrib["bbox"])
                page_ids.append(int(page.attrib["id"]))

        index_df = pd.DataFrame(data=dict(page_id=page_ids, bbox=bbox))
        final_feature_matrix = np.concatenate(feature_collector, axis=0)

        return index_df, final_feature_matrix

class ByBlock(features.LineLevelFeatures):
    # apply a LineCollectionFeatureSet for each textbox in a document

    def __init__(self, line_collection_feature_set: LineCollection2ListOfFeatureVecs):
        self.featureSet = line_collection_feature_set

    def binary_feature_names(self):
        return self.featureSet.binary_feature_names()

    def scalar_feature_names(self):
        return self.featureSet.scalar_feature_names()

    def scalar2binary(self, scalar_features):
        return self.featureSet.scalar2binary(scalar_features)

    def document_2_featureMatrix(self, document_tree, filename=None):
        # loop through pages. compute all the features make the matrix
        page_ids = list()
        bbox_ids_all = list()
        feature_collector = list()

        for page in document_tree.findall(".//page"):
            for block in page.findall(".//textbox"):
                
                all_textlines = block.findall(".//textline")
                all_bboxes = [str(l.attrib["bbox"]) for l in all_textlines]
                
                feats = self.featureSet.scalar_features_line_collection(all_textlines, filename=filename)

                feature_collector.append(feats)
                bbox_ids_all.extend(all_bboxes)
                page_ids.extend(len(all_textlines)*[int(page.attrib["id"])])                         

        index_df = pd.DataFrame(data=dict(page_id=page_ids, bbox=bbox_ids_all))
        final_feature_matrix = np.concatenate(feature_collector, axis=0)

        return index_df, final_feature_matrix

"""
# Not applicable anymore as we don't have attributes for column type
class ByColumn(LineLevelFeatures):
    # apply a LineCollectionFeatureSet for each textcolumn in a document

    def __init__(self, line_collection_feature_set: LineCollection2ListOfFeatureVecs):
        self.featureSet = line_collection_feature_set

    def binary_feature_names(self):
        return self.featureSet.binary_feature_names()

    def scalar_feature_names(self):
        return self.featureSet.scalar_feature_names()

    def scalar2binary(self, scalar_features):
        return self.featureSet.scalar2binary(scalar_features)


    def document_2_featureMatrix(self, document_tree, filename=None):
        # loop through pages. compute all the features make the matrix
        page_ids = list()
        bbox_ids_all = list()
        feature_collector_all = list()


        for page in document_tree.findall(".//page"):
            all_textlines = page.findall(".//textline")
            for l in all_textlines:
                if "type" not in l.attrib:
                    pass
            types_of_lines = np.array([l.attrib["type"] for l in all_textlines])
            original_position_of_lines = np.arange(len(all_textlines))

            feature_collector_page = list()
            ids_in_original_order = list()

            _bboxes_in_processed_order = list()
            for type in np.unique(types_of_lines):

                lines_with_types = [l for l in all_textlines if l.attrib["type"] == type] #all_textlines[types_of_lines == type]
                _bboxes_in_processed_order.extend([l.attrib["bbox"] for l in all_textlines if l.attrib["type"] == type])

                original_positions_of_selected_lines = original_position_of_lines[types_of_lines == type]
                ids_in_original_order.extend(original_positions_of_selected_lines)

                features_of_type = self.featureSet.scalar_features_line_collection(lines_with_types, filename=filename) # matrix n_lines, n_feats

                feature_collector_page.append(features_of_type)

            ids_to_order = np.argsort(ids_in_original_order)

            all_features_page = np.concatenate(feature_collector_page, axis=0)
            features_page_original_order = all_features_page[ids_to_order, :]

            _reordered_bboxes = np.array(_bboxes_in_processed_order)[ids_to_order]
            _target = np.array([l.attrib["bbox"] for l in all_textlines])

            assert(np.all(_reordered_bboxes == _target))
            bbox_ids_all.extend(_reordered_bboxes)
            feature_collector_all.append(features_page_original_order)
            page_ids.extend([int(page.attrib["id"])]*features_page_original_order.shape[0])

        index_df = pd.DataFrame(data=dict(page_id = page_ids, bbox=bbox_ids_all))
        final_feature_matrix = np.concatenate(feature_collector_all, axis=0)

        return index_df, final_feature_matrix
"""

class ByPage(features.LineLevelFeatures):
    # apply a LineCollectionFeatureSet for each textcolumn in a document

    def __init__(self, line_collection_feature_set: LineCollection2ListOfFeatureVecs):
        self.featureSet = line_collection_feature_set

    def binary_feature_names(self):
        return self.featureSet.binary_feature_names()

    def scalar_feature_names(self):
        return self.featureSet.scalar_feature_names()

    def scalar2binary(self, scalar_features):
        return self.featureSet.scalar2binary(scalar_features)


    def document_2_featureMatrix(self, document_tree, filename=None):
        # loop through pages. compute all the features make the matrix
        page_ids = list()
        bbox_ids_all = list()
        feature_collector_all = list()


        for page in document_tree.findall(".//page"):
            all_textlines = page.findall(".//textline")

            all_bboxes = [str(l.attrib["bbox"]) for l in all_textlines]

            feats = self.featureSet.scalar_features_line_collection(all_textlines, filename=filename)

            feature_collector_all.append(feats)
            bbox_ids_all.extend(all_bboxes)
            page_ids.extend(len(all_textlines)*[int(page.attrib["id"])])

        index_df = pd.DataFrame(data=dict(page_id = page_ids, bbox=bbox_ids_all))
        final_feature_matrix = np.concatenate(feature_collector_all, axis=0)

        return index_df, final_feature_matrix