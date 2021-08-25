## Functions associated to each form

- Create a project
  - When clicking on `Create Project`:
    - Create DB for the project, and the main table `Project information`
      - This functionality is not implemented so far. Currently we make use of the class `SupervisionLoop`
    - Create endpoint where we will start storing the associated files, in principle, only the pdfs, as we will need them to obtain the images
      - Currently, when creating a new annotation experiment, a new folder is created. But now, we should create one endpoint per case study.
    - Start the preprocessing of files:
      - Conversion of pdf to xml
        - Function `pdf2xml` in `utils_proc.py`. It requires `pdfminer.six installed`, and the path to the function `pdf2txt.py`.
      - Simplification of xml, to reduce the <text> level
        - Function `get_text_onefile` in `preproc_docs.py` allows merging all <text> into a single textline, using `[font face=X size= X]` to store the sizes of fonts
      - Extraction of the features from the xml files
        - In file `s01_run_extraction_feats.py` you have the script used to launch the conversion.
        - The available parsers are in `feature_parsing.py`. By default, we will use the 3 already defined for the text lines (`Title Parser`), the text blocks (`Features for textboxes `), and the pages (`Overview Page_classifier`). BUT, we will remove the field `line_features.RegexHits`. This can be later added through the options in `Create a case study`, triggering then the extraction of Regex hits, and adding a new column to the table `Samples information`
      - Creation of table `Samples information`, linked to the table for the project
        - Computed the features, the tables is created, and the information is added, with the fields indicated later
      - We run the creation of the vocabulary: the vocabulary file is stored at the endpoint, or all the words could be another entry at the DB table
        - Function `create_save_vocab` in `utils_feat.py` triggers the creation of the vocabulary, that is dump into a pickle file

**NOTE:** despite is not contemplated currently, it would be cool to, once we have the project created, we could still add more files. This option can be included in the `Project - Settings` form, and once we add new files, we initiate all the steps detailed in `Start the preprocessing of files`. And the new samples are just appended to the existing table, and the vocabulary is generated again. We can obviously remove also documents, and then the associanted files are removed from the endpoint, and the rows from the table `Samples information`

**NOTE 2:** if for the moment you are integrating the Case studies with the Project creation, hence the table `Case study` needs also to be created, already with the information of the labels, and the rest of fields empty

**NOTE 3:** we may allow also to import XML files. BUT, indicating that these need to have the following hierarchy: <pages> -> <page> -> <textblock> -> <textline>. And all of those, information on the bounding boxes.

- Project - Overview

  - When selecting to create a case study, we move to the form `Create a case study` (currently it reads Create a Project on figma)
    - No interaction with the backend
  - Updating field `Notes` on `Project information` table
    - We just update the field `Notes` on `Project information` table

- Create a case study

  - When clicking on the `Create` button, we proceed to:
    - Create `Case study` table, filling in all the required fields. For the columns related with the classifier type, ocurrence matrix, etc., we just consider default values. This can be modified afterwards in the settings of the Case Study. If we select `Default` vocabulary, we used the one created with the project. With `Custom`, the file is copied to the endpoint
      - The table is created and the fields are added

- Case study - Overview

  - Updating field `Notes` on `Case study` table
    - We just update the field `Notes` on `Case study` table

- Case study - Training

  - Updating features to use on `Case study` table
    - Update features used on `Case study` table
  - Updating set to label on the `Case study` table (the field `Training type` we need to discuss again)
    - Update `Case study` table
  - Update `Retraining interval` on `Case study` table
    - Update `Case study` table
  - Select classifier
    - Update classifier type on `Case study` table

- Case study - Output
  - Generate predictions for all the documents
    - In file `s06_generate_predictions.py` you have an example on how to generate the predictions for all files. From line 90 to 142, where the dataframe is saved. Also, we could also include the last part, from line 148 to 254, where the final predictions generated, which will then be used by the user, are merged with the human labels, as we have them already.
  - Generate accuracy results, either with CV or on a different test set.
    - For the accuracy using CV, you need to use `check_acc_cv` function in `utils_extractdiscussions.py` file. Remove lines from 1719 to 1791, as this relates with something exclusive to the other data. Also, many inputs could be removed.
    - To get the accuracy using a separate validation set, you need to use `check_acc` function in `utils_extractdiscussions.py` file. Remove everything from line 1311 to 1384, as this relates with something exclusive to the other data. Also, many inputs could be removed.
  - Generate a plot, using all the models trained, from the oldest to the most recent ones, that shows how the accuracies changed as we label data. This helps to assess when the accuracies saturate, and it may not make more sense to continue labelling
    - In this case, we can just make use of all the presaved models. Ideally, it would be great to know with how many samples each of those models was trained, and then show a plot were we can see the evolution of the precision or the recall for all classes, depending on the number of samples.

**NOTE:** obviously, all these functions that I send make use of methods of the `SupervisionLoop` class.
**NOTE 2:** no need to implement all this for the prototype!
**NOTE 3:** we need to add another mode for perform model selection. For this, we would still need to define all hyperparameters in the model. So far, some default values are defined on `CONSTANTS.py`, but later we need to allow specifying them, and also provide ranges to perform grid search for model selection (or any Bayesian method for model selection). Still, this is a future functionality!

- Case study - Settings

  - Change description or author of case study on table
    - Update `Case study` table

- Project - Settings

  - Change description or author of project on table
    - Update `Project information` table
    - Delete project. Removing the entry on `Project information` table, and all associated case studies and samples on the other tables

- Annotate
  - Generate images for pages
    - Function `pdf2png` in `utils_proc.py`. See Note later for some more comments on this.
  - Click on element on page: label updated on table
    - Update `Samples information` table
  - Select a class and click on `Toogle all`: change all labels on DB table
    - Update `Samples information` table
  - Update the field `Notes` on the table, for the specific page being labelled
    - Update `Samples information` table, the first entry for the specific page we are labelling, and modidy the field `Notes`
  - Use the filter to search for some pages according to some criteria: I cannot really say here a proper use case, but I guess we can just search by: the content in the actual page; the content only in the note, in case we use specific keywords on the notes; by the labels in the pages; and using the flags.
    - This is not part of any existing code
  - Automatically inititate retraining of classifier and update of predictions
    - You can use similar procedures as those described for `Generate predictions for all the documents`
  - Slider to specify the labels we want to show, depending on their probability (as we have before on the Dashbord)

**NOTE:** we have the issue of the extraction of the images from the pdf. There are two possibilities:

1. When we click on a page, since we have the pdf, we extract the image of the page, and the png is stored at the endpoint. This will cause a brief delay when clicking on an image
2. When we move to the annotation section, we just start obtaining the images for the first, for example, 100 pages, obviously starting from the top one, the one that will be shown first. All pngs are stored at the endpoint

**NOTE 2:** some extra consideration for the classifier, both for training and prediction:

- Since we are going to save now the models, at least those need to have a time stamp, and information on the number of samples used for training, as we need this for plotting some information.
- During prediction, in the old code, we were many times selecting subsets of the pages, i.e., only those we were going to label, in order to reduce the computation time as we have 100K+ pages. Now, since we are going to work with a specific table on a DB, it may not be that problematic, as we can reuse the predictions from the last round, and on the background update these predictions.

## DBs, tables and columns

In principle, we could create one separate table per project. But also, have only 2 tables on the database, and 1 extra table `Samples information` for each case study. We differentiate projects and case studies through their uid, and the links on the linking tables. This is how I will structure the following tables

- Table `Project information`

Fields:
uid, project_name, description, author, doc_level, end_point, notes

- Table `Case study`

Fields:
uid, uid_parent_proj, case_study_name, description, author, notes, names_labels, uid_table_regex_feat, vocab_flag, file_vocab, n_words_use_features, classifier_type, freq_matrix_type, n_estimators_classif, training type (default `Train`), retrain_interval, name_table_samples_inf

**NOTE:** at some point we need to allow a proper model selection, using all other parameters, such as lambdas for regularizers, learning rate for gradient boosting, etc. For the moment, we just take those values from `CONSTANTS.py`, but at some point, we need to implement this also, and that will then add more columns, for each of the hyperparameters.

- Table `Samples information`

The columns that will be used as unique ids for the elements in the pages are: name_doc, page_id, bbox

Fields:
uid*parent_case, name_doc, page_id, bbox, [one column per feature extracted, as this depends on the level of the document], [one column per regex defined as feature], [one column per class, appended with `pred*`], [one column per class, appended with `human\_`], time_labeling, split (none by default, and as we label them, we give the label `train`, or `test`if the`Training type`is changed in`Case study - Training`) split (training or test), flags (defined in `Annotation` form), notes

- Other tables

  - `Cases in project`: just a table linking the uid of the project with its associated case studies (uid of `Project information` and uid of `Case Study`). Fields: uid_proj, uid_case
  - `regex strings for case study`: for a given `uid_table_regex_feat`, all the regex strings used to extract those additional features. Fields: uid_table_regex_feat, string_regex
