**VeriTool documentation**

VeriTool is a plugin for determining the truth value of a sentence. 
Choose to process a corpus or enter your own sentence to determine whether it's a fact or not!

---

## Preconditions

Before launching the execution of the tool, you will need the following:

1. A conda environment (AllenNLP is easier to install on a conda env);
2. Make sure you have Python 3.7 or higher;
3. Install the AllenNLP in the Conda environment;
4. Install spaCy using conda (installing it with pip has a Visual Studio dependency which gives an error if it is not installed)
5. Install the required dependencies from the requirements file: pip install -r requirements.txt
6. Finally, install the spaCy large English model: python -m spacy download en core web lg

---

## Running in the batch mode

This use case focuses on running the VeriTool on a dataset corpus.
Make sure the structure of the corpus is the same as the default dataset (see train.csv). Update the name of the corpus in the dataset_reader module;
The steps are:

1. read dataset: python -m modules.dataset_reader filename.csv; Note: the name of the corpus should be provided, and the corpus stored in the root folder;
2. split into keywords: python -m modules.keyword_selector; Note: you may add 2 command line arguments here, for lower and upper limist:
		python -m modules.keyword_selector lower_limit upper_limit
		This reads from the dataset the entries starting with the index lower_limit and ending with upper_limit;
3. gather information: python -m modules.document_gather;
4. compute and save similarities: python -m modules.doc_scanner write;
5. determine the facts and counterfacts: python -m modules.doc_scanner read;


---

## Run the free input mode

This feature is the easiest, since a single file needs to be run:

1. launch_veritool.sh

The tool will run as long as you don't type "exit". This command will stop the VeriTool's execution