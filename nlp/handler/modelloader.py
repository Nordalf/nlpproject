import os
# from simpletransformers.ner import NERModel
from .ner import NER

class ModelLoader:
    def __new__(self, model='bert-base-multilingual-cased', use_cuda=False):
        return NER(model_name_or_path=model, labels=os.path.join(os.path.dirname(os.path.abspath(__file__)),'labels.txt'), fine_tuned_model=os.path.join(os.path.dirname(os.path.abspath(__file__)),'outputs_new/'))