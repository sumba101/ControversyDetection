from flask import Flask, request, jsonify
from collections import defaultdict as dd
import numpy as np
import time
import requests
import json
import pytorch_lightning as pl
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification, AdamW, BertConfig, AutoModel

def get_pers_scores(comments):
    api_key = 'AIzaSyBLnXd0ElYhQ9WzUaN-9sI4fPavky3md3o'
    url = ('https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze' +    
        '?key=' + api_key)
    lg = ['en']
    attr = ['TOXICITY', 'SEVERE_TOXICITY', 'IDENTITY_ATTACK', 'INSULT', 'PROFANITY', 'THREAT', 'SEXUALLY_EXPLICIT', 'OBSCENE']
    attr_dict = {}
    attr_results = {}
    for i in attr:
        attr_dict[i] = dd()
        attr_results[i+'_WHOLE'] = dd()
    sum = np.array([0,0,0,0,0,0,0,0]).astype(np.float)
    for i in comments:
        data_dict = {
                'comment': {'text': i[1]},
                'languages': lg,
                'requestedAttributes': attr_dict
            }
        time.sleep(1.2)
        response = requests.post(url=url, data=json.dumps(data_dict))
        response_dict = json.loads(response.content)
        score = []
        for i in attr:
            score.append(response_dict["attributeScores"][i]["summaryScore"]["value"])
        sum += np.array(score)
    return sum/len(comments)
    
class LMModelClassifier(pl.LightningModule):
    def __init__(self, params):
        super().__init__()
        self.save_hyperparameters()
        self.l1 = AutoModel.from_pretrained(params['model'])
        self.pre_classifier_1 = torch.nn.Linear(768, 768)
        self.final_layer_dim = 768
        if params['pers']:
            self.pre_classifier_2 = torch.nn.Linear(8, 8)
            self.final_layer_dim += 8
        self.pre_classifier_x = torch.nn.Linear(self.final_layer_dim, self.final_layer_dim)
        self.dropout = torch.nn.Dropout(params['dropout'])
        self.total_loss = 0
        self.batch_count = 0
        self.epoch = 0
        self.classifier = torch.nn.Linear(self.final_layer_dim, 2)
        self.preds = []
        self.targets = []
        self.test_preds = []

    def forward(self, input_ids, attention_mask, token_type_ids, pers):
        output_1 = self.l1(input_ids=input_ids, attention_mask=attention_mask)
        hidden_state_1 = output_1[0]
        pooler_1 = hidden_state_1[:, 0]
        pooler_1 = self.pre_classifier_1(pooler_1)
        pooler_1 = torch.nn.Tanh()(pooler_1)
        pooler_1 = self.dropout(pooler_1)
#         pre_final1 = self.classifier(pooler_1)
        if params['pers']:
            pooler_2 = self.pre_classifier_2(pers)
            pooler_2 = torch.nn.Tanh()(pooler_2)
            pooler_2 = self.dropout(pooler_2)
            pooler_1 = torch.cat((pooler_1, pooler_2), 1)
            pooler_1 = self.pre_classifier_x(pooler_1)
            pooler_1 = torch.nn.Tanh()(pooler_1)
            pooler_1 = self.dropout(pooler_1)
        output = self.classifier(pooler_1)
        return output
    
    def configure_optimizers(self):
        optimizer = torch.optim.Adam(params =  self.parameters(), lr=params['lr'])
        return optimizer

    def training_step(self, batch, batch_nb):
        ids = batch['ids']
        mask = batch['mask']
        token_type_ids = batch['token_type_ids']
        pers = batch['pers_scores']
        targets = batch['targets']
        outputs = self.forward(ids, mask, token_type_ids, pers)
        loss = torch.nn.CrossEntropyLoss()(outputs, targets)
        self.total_loss += loss
        self.batch_count += 1
        logger_logs = {'training_loss': loss}
        logger_logs = {'losses': logger_logs} # optional (MUST ALL BE TENSORS)
        output = {
            'loss': loss, # required
            'progress_bar': {'training_loss': loss}, # optional (MUST ALL BE TENSORS)
            'log': logger_logs
        }
        # return a dict
        return output
    
    def on_epoch_end(self):
        self.epoch += 1
        print(f'Epoch: {self.epoch}, Loss:  {self.total_loss/self.batch_count}')
        self.total_loss=0
        self.batch_count=0
    
    def validation_step(self, batch, batch_idx):
        ids = batch['ids']
        mask = batch['mask']
        token_type_ids = batch['token_type_ids']
        pers = batch['pers_scores']
        targets = batch['targets']
        outputs = self.forward(ids, mask, token_type_ids, pers)
        loss = torch.nn.CrossEntropyLoss()(outputs, targets)
        labels_hat = torch.argmax(outputs, dim=1)
        self.preds.extend(torch.sigmoid(outputs).cpu().detach().numpy().tolist())
        self.targets.extend(targets.cpu().detach().numpy().tolist())
        val_acc = torch.sum(targets == labels_hat).item() / (len(targets) * 1.0)
        output = {
            'val_loss': loss,
            'val_acc': torch.tensor(val_acc), # everything must be a tensor
        }
        return output
    
    def validation_epoch_end(self, validation_step_outputs):
        self.preds = list(np.argmax(np.array(self.preds), axis=1).flatten())
        print(classification_report(self.targets, self.preds, digits=4))
        self.preds = []
        self.targets = []
    
    def test_step(self, batch, batch_idx):
        ids = batch['ids']
        mask = batch['mask']
        token_type_ids = batch['token_type_ids']
        pers = batch['pers_scores']
        outputs = self.forward(ids, mask, token_type_ids, pers)
        labels_hat = torch.argmax(outputs, dim=1)
        self.test_preds.extend(labels_hat.cpu().detach().numpy().tolist())


def predict(model, tokenizer, params, tweet):
    inputs = tokenizer.encode_plus(
            tweet['root'],
            None,
            truncation=True,
            add_special_tokens=True,
            max_length=params['max_len'],
            pad_to_max_length=True,
            return_attention_mask = True,
            return_token_type_ids=True,
        )
    ids = torch.tensor(inputs['input_ids'], dtype=torch.long)
    mask = torch.tensor(inputs['attention_mask'], dtype=torch.long)
    token_type_ids = torch.tensor(inputs["token_type_ids"], dtype=torch.long)
    pers = torch.tensor(get_pers_scores(tweet['comments']), dtype=torch.float)
#     return ids, mask, token_type_ids, pers
    res = model.forward(torch.reshape(ids, (1,-1)), torch.reshape(mask, (1,-1)), torch.reshape(token_type_ids, (1,-1)), torch.reshape(pers, (1, -1)))
    return torch.argmax(res, dim=1).cpu().detach().numpy().tolist()[0]



app = Flask(__name__)
params = {
    'model' : 'roberta-base',
    'label' : 'is_cont',
    'valid_size' : 0,
    'rnd' : 42,
    'max_len' : 64,
    'train_batch' : 32,
    'valid_batch' : 32,
    'epochs' : 4,
    'lr' : 1e-05,
    'dropout' : 0.1,
    'pers' : True
}
model = LMModelClassifier.load_from_checkpoint('/scratch/tr/'+params['model']+'-epoch=2.ckpt')
tokenizer = AutoTokenizer.from_pretrained(params['model'])

@app.route('/predict_status', methods=['POST'])
def predict_status():
    if request.method == 'POST':
        tweet = json.loads(request.data)
        print(tweet)
        pred = predict(model, tokenizer, params, tweet)
        # print(json.loads(tweet)
        # return 0
        return jsonify({'contro': pred})
    else:
        return "Only post"
