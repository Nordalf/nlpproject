from .custom_ner import NER
import os

model = NER(model_name_or_path='bert-base-multilingual-cased', labels=os.path.join(os.path.dirname(os.path.abspath(__file__)),'labels.txt'))
# result = model.predict("Dette dokument indeholder en sætning om Karsten Madsen, som er bosat i København med sin kone Hanne Madsen, arbejder i Ørsted og er altid glad for GDPR.")

model.train()

# print(result)