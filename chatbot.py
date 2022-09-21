import torch
import pickle

#These are Bert model and tokenizer which has been pickled
#Import the model via transformer and pretrain it on "bert-large-uncased-whole-word-masking-finetuned-squad" for both model and tokenizer
#Form the pickle of the file to fasten preprocessing and loading of the module

# from transformers import BertForQuestionAnswering 
# from transformers import BertTokenizer
# model= BertForQuestionAnswering.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
# tokenizer= BertTokenizer.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')

#The model and tokenizer can be installed via these steps.

#loading the tokenizer and model pickle as model and tokenizer
open_file = open("model.pickle", "rb")
model= pickle.load(open_file)
open_file.close()

open_file = open("tokenizer.pickle", "rb")
tokenizer= pickle.load(open_file)
open_file.close()



def question_answer(question, text):
    #tokenizes the question and the text given as a pair
    input_ids = tokenizer.encode(question, text)
    #converted to string inn the form of cls and sep
    tokens = tokenizer.convert_ids_to_tokens(input_ids)

    #segment IDs of the inputs
    #when was sep token first used in the list of the tokenized version
    sep_idx = input_ids.index(tokenizer.sep_token_id)
    #no of tokens in Question
    num_seg_a = sep_idx+1
    #no of tokens in text given
    num_seg_b = len(input_ids) - num_seg_a
    
    #list of 0s and 1s for segment embeddings
    #1 for tokens that are not masked,0 for tokens that are masked.
    #Bert masks 15% percent of the sentence randomly hence....
    segment_ids = [0]*num_seg_a + [1]*num_seg_b
    assert len(segment_ids) == len(input_ids)
    
    #model output using input_ids and segment_ids, token type ids define the first or second portion of the input 
    output = model(torch.tensor([input_ids]),
                   token_type_ids=torch.tensor([segment_ids]))
    
    #reconstructing the answer with start and end logits
    #start logits are span start scores, ends are vice versa
    answer_start_index = output.start_logits.argmax()
    answer_end_index = output.end_logits.argmax()
    
    #forming of the answers
    if answer_end_index >= answer_start_index:
        answer = tokens[answer_start_index]
        for i in range(answer_start_index+1, answer_end_index+1):
            if tokens[i][0:2] == "##": # here ## stands as a subword for example if the word is tokenization --> token and ##ization
                answer += tokens[i][2:]
            else:
                answer += " " + tokens[i]
                
    # if answer starts with cls.....
    else:
        answer = "Unable to find the answer to your question."
    return answer.capitalize()
