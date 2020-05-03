from ner import NER

model = NER()
result = model.predict("Dette dokument indeholder en sætning om Karsten Madsen, som er bosat i København med sin kone Hanne Madsen, arbejder i Ørsted og er altid glad for GDPR.")

print(result)