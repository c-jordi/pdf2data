import os
import subprocess
import re
from pdf2image import convert_from_path, convert_from_bytes
import copy


def process_pdf(path):
    print("running")
    print(os.path.isfile(path))
    output = "/".join(path.split("/")[:-1])+'/test.xml'
    cmd = f"pdf2txt -o {output} -t 'xml' {path}" 
    subprocess.call(cmd)

def get_text_onefile(XML_root, flag_all = 1):
    """
    Args:
        input file
    Cleans up xml

    
    """

    XML_root = ET.parse(input_file_handler).getroot()

    def clean_text(text):
        # replace newline
        text = text.replace('\n', ' ')

        # account for hyphenation (not completely correct...)
        # TODO: needs to be improved
        text = text.replace('- ', '')

        return text


    XML_new = copy.deepcopy(XML_root)

    # GROUPING

    for ind_p, page in enumerate(XML_root):
        #print(page.tag, page.attrib)
        # for every textbox on that page

        for ind_t, textbox in enumerate(page):
            if (textbox.tag == 'textbox'):
              
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
                        complete_text = clean_text(complete_text)
                        XML_new[ind_p][ind_t][ind_tl].text = complete_text


    return XML_new


def extract_features():
    """Extracts the features
    -> Put them in the database
    Drop the begin year and the end year
    """