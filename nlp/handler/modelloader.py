import os
from simpletransformers.ner import NERModel

class ModelLoader:
    def __new__(self, model_type, use_cuda=False):
        return NERModel('bert', os.path.join(os.path.dirname(os.path.abspath(__file__)),'outputs/'), use_cuda=use_cuda, args={})