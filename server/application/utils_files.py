
import os, sys
from uuid import uuid4
import numpy as np
from pathlib import Path
import xml.etree.ElementTree as ET

import copy
import re

from urllib import request, parse
from pdfminer.layout import LAParams
from pdfminer.high_level import extract_text_to_fp

from pdf2image import convert_from_path

import matplotlib.pyplot as plt

from .constants import TMP_FOLDER, TMP_SUFFIX, SEP_UID_NAME, IMG_FOLDER, POPPLER_PATH

def extract_xml(uri):
    """
    Obtain the xml from the pdf
    """
    uid, name, suffix = info_from_uri(uri)

    file_name = name + '.xml'
    # We cannot use tempfile because the file is being closed and
    # deleted automatically, and we need it for further processing
    #fout = tempfile.TemporaryFile(dir = TMP_FOLDER)
    uri_out = create_tmp(file_name)
    fout = open(uri_out, 'wb')
    fin = open_urlopen_seek(uri)
    extract_text_to_fp(fin, fout, laparams=LAParams(),
                        output_type='xml', codec="utf-8")
    return uri_out

def clean_xml(uri):
    """
    Works on an xml file, and perform some cleaning
    and simplification
    """
    tree = ET.parse(uri)
    root = tree.getroot()
    root_new = remove_attrib_textl(root, keys_rem = ['colourspace', 'ncolour'])
    return root_new


def remove_attrib_textl(tree, keys_rem = ['colourspace', 'ncolour']):
    """
    Remove the indicated attributes from the <text> level of the xml
    """
    for ip, page in enumerate(tree):
        for ib, block in enumerate(page):
            for it, textline in enumerate(block):
                for itext, text in enumerate(textline):
                    keys_t = text.keys()
                    val_keys = np.setdiff1d(keys_t, keys_rem)
                    if len(val_keys):
                        aux_dict = text.attrib
                        tree[ip][ib][it][itext].attrib = dict()
                        for key in val_keys:
                            tree[ip][ib][it][itext].attrib[key] = aux_dict[key]
    return tree

def info_from_uri(uri):
    name = Path(uri).stem
    uid = name.split(SEP_UID_NAME)[0]
    filename = name.split(SEP_UID_NAME)[1]
    suffix = Path(uri).suffix
    return uid, filename, suffix

def create_tmp(filename):
    """
    Just creates a tmp file in /tmp folder inside the storage folder
    """
    uid = uuid4().hex
    fname = uid + SEP_UID_NAME + Path(filename).stem + Path(filename).suffix 
    uri = TMP_FOLDER + fname
    return uri

def open_urlopen_seek(uri):
    """
    To obtain the xml from the pdf, we need a seekable file object, and the
    http response does not have that method. We need to create and intermediate
    file, open that, and remove it
    """    
    resp = request.urlretrieve(uri, TMP_FOLDER + uuid4().hex + TMP_SUFFIX)
    resp_seek = open(resp[0],'rb')
    os.remove(resp[0])
    return resp_seek

def get_text_onefile(XML_root, flag_clean = True):
    """
    Groups all characters inside the <text> level as proper sentences in the
    <textline> level, preserving information on the fontsize
    """
    # helper function to clean text
    # !!! so far only removing new lines and primitive dehyphenation
    def clean_text(text):
        # replace newline
        text = text.replace('\n', ' ')

        # account for hyphenation (not completely correct...)
        # TODO: needs to be improved
        text = text.replace('- ', '')

        return text

    # initialize textbox count and empty dictionary

    XML_new = copy.deepcopy(XML_root)

    # for every page

    for ind_p, page in enumerate(XML_root):
        #print(page.tag, page.attrib)
        # for every textbox on that page

        for ind_t, textbox in enumerate(page):
            if (textbox.tag == 'textbox'):
                # initialize string

                #print(textbox.tag, textbox.attrib)
                # for every textline in that textbox
                for ind_tl, textline in enumerate(textbox):
                    prev_fontsize = 0
                    prev_fonttype = 'Def'
                    complete_text = ''
                    flag_in = 0
                    if textline.tag == 'textline':
                    #print(textline.tag, textline.attrib)
                    # for every text (actually just a letter)

                        for ind_ch, text in enumerate(textline):
                            #print(ind_ch, text.text, len(textline), len(XML_new[ind_p][ind_t][ind_tl]))
                            # extend string
                            if 'font' in text.attrib.keys():
                                if (text.attrib['font'] != prev_fonttype) or (text.attrib['size'] != str(prev_fontsize)):
                                    if flag_in:
                                        complete_text += '[/font]'
                                    else:
                                        flag_in = 1
                                    complete_text += '[font face="' + text.attrib['font'] + '" size="' + text.attrib['size'] + '"]'
                                    prev_fontsize = text.attrib['size']
                                    prev_fonttype = text.attrib['font']
                            complete_text = complete_text + text.text
                            child_new = XML_new[ind_p][ind_t][ind_tl][0] # Because we are removing elements
                            XML_new[ind_p][ind_t][ind_tl].remove(child_new)
                        # clean text
                        complete_text += '[/font]'
                        # Remove \n and - from hypenation
                        if flag_clean:
                            complete_text = clean_text(complete_text)

                        XML_new[ind_p][ind_t][ind_tl].text = complete_text

    return XML_new

def structure_text_string(text):
    """
    Takes a string with font annotations and returns a list of dict objects. (one for each block of text)
    :param text: a string with "[font face=...] blabla [/font]" annotations
    :return: a list of dicionaries, one for each block of text in certain font. each has the fields 'font', 'size', 'text', 'l_text'
    """
    if text is None:
        return []

    regex_string = '\[font face="([a-zA-Z\-]*)" size="(\d+\.\d*)"]([^[]*)\[\/font\]'
    pattern = re.compile(regex_string)

    matches = re.findall(pattern, text)
    # This simply because in the past the face and size were wrongly labelled
    if not len(matches):
        regex_string = '\[font face="(\d+\.\d*)" size="([a-zA-Z\-]*)"]([^[]*)\[\/font\]'
        pattern = re.compile(regex_string)
        matches = re.findall(pattern, text)
        
        collector = list()
        for m in matches:
            f = dict(font=m[1], size=float(m[0]), text=m[2], l_text=len(m[2]))
            collector.append(f)
    
        return collector
    else:
        collector = list()
        for m in matches:
            f = dict(font=m[0], size=float(m[1]), text=m[2], l_text=len(m[2]))
            collector.append(f)
    
        return collector

def convert_textlines_in_xml_tree(orig):
    """
    Adds one more hierarchy level of children in each 'textline' tag in the document xml tree obtained from the 04_corrected_xml.
    Specifically each 'textline' then contains children with tag 'text_block'.
    Each 'text_block' represents a part of the textline with the same formatting. It has attributes ['font', 'size'] and
    contains the actual text formatted in this way.

    :param orig: the xml tree obtained from 04_corrected xml
    :return: a modified copy of it where each 'textline' tag has children with tag 'text_block'
    """
    new = copy.deepcopy(orig)

    for tL in new.findall(".//textline"):
        annotated_text = tL.text
        tL.text = ""
        for text_block in structure_text_string(annotated_text):
            params = dict(font=text_block["font"], size=str(text_block["size"]))
            text_block_element = ET.Element("text_block", params)
            text_block_element.text = text_block["text"]
            tL.append(text_block_element)

    return new

def pdf2imgobj(pdf_uri, resolution = 150, first_page=None, last_page=None):
    """
    Function that receives the pdf_uri and obtain the images, for some pages, 
    storing them directly in the folder for tmp images
    """
    uid, filename, suffix = info_from_uri(pdf_uri)

    img_obj_array_tmp = convert_from_path(pdf_uri, dpi = resolution, first_page = first_page, last_page = last_page,
                        poppler_path=POPPLER_PATH)

    for image, page_numb in zip(img_obj_array_tmp,range(first_page, last_page + 1)):
        fname = os.path.join(IMG_FOLDER, filename + '_' + str(page_numb) + '.png')
        plt.imsave(fname, np.asarray(image))


