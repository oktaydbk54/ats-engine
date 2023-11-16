from transformers import BertTokenizer, BertModel
import torch
from sklearn.metrics.pairwise import cosine_similarity

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

def bert_encode(text, tokenizer):
    encoded_dict = tokenizer.encode_plus(
        text,
        add_special_tokens = True,  
        max_length = 512,           
        pad_to_max_length = True,   
        return_attention_mask = True,   
        return_tensors = 'pt',     
    )
    
    return encoded_dict['input_ids'], encoded_dict['attention_mask']

def get_bert_embeddings(text, tokenizer, model):
    input_ids, attention_mask = bert_encode(text, tokenizer)
    with torch.no_grad():
        outputs = model(input_ids, attention_mask=attention_mask)
    # [CLS] tokeninin embeddingini döndür
    # cls_embedding = outputs[0][:, 0, :]
    # return cls_embedding
    return outputs[0].mean(dim=1).squeeze()  # Ortalama pooling


def calculate_cosine_similarity(embedding1, embedding2):
    return torch.nn.functional.cosine_similarity(embedding1, embedding2)

def match_results(resume_text, job_descriptions):
    resume_embedding = get_bert_embeddings(resume_text, tokenizer, model)

    job_descriptions['Match Scores'] = 0  

    for index, row in job_descriptions.iterrows():
        job_desc = row['description']
        job_embedding = get_bert_embeddings(job_desc, tokenizer, model)
        score = cosine_similarity(resume_embedding.unsqueeze(0), job_embedding.unsqueeze(0))
        job_descriptions.at[index, 'Match Scores'] = score.item()

    return job_descriptions