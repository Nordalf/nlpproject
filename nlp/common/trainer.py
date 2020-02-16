from simpletransformers.ner import NERModel
import pandas as pd

if __name__ == '__main__':

    # Creating train_df  and eval_df for demonstration
    train_data = []
    with open('../data/dk_ner_train.tsv', 'r', encoding='utf-8') as ner_corpus:
        for line in ner_corpus:
            line = line.rstrip('\n')
            line = line.split('\t')
            if len(line) == 3:
                train_data.append(line)

    # FJERNER ALLE LINJER, SOM INDEHOLDER SKRALD DATA
    # ^(?!\d+\t[\w\.\,]+\t.+\n)\d+.*\n

    train_df = pd.DataFrame(train_data, columns=['sentence_id', 'words', 'labels'])

    # test = train_df.groupby('sentence_id').count()[['words']]
    # print(test.query("words > 128"))

    eval_data = []
    with open('../data/dk_ner_eval.tsv', 'r', encoding='utf-8') as ner_corpus:
        for line in ner_corpus:
            line = line.rstrip('\n')
            line = line.split('\t')
            if len(line) == 3:
                eval_data.append(line)

    eval_df = pd.DataFrame(eval_data, columns=['sentence_id', 'words', 'labels'])

    # test = eval_df.groupby('sentence_id').count()[['words']]

    # print(test.query("words > 128"))

    # Create a NERModel
    model = NERModel('albert', 'albert-base-v2', use_cuda=False, args={'overwrite_output_dir': True, 'reprocess_input_data': True})


    # # Train the model
    model.train_model(train_df)

    # Evaluate the model
    result, model_outputs, predictions = model.eval_model(eval_df)

    # Predictions on arbitary text strings
    predictions, raw_outputs = model.predict(["Peter er lige begyndt til badminton."])

    print(predictions)