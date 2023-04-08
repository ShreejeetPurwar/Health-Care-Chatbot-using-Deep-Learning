from flask import Flask, render_template,request,jsonify
import numpy as np
import pandas as pd 
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from sklearn.model_selection import train_test_split

app = Flask(__name__, template_folder="template", static_folder="static")

df = pd.read_csv('dataset.csv')

data = []
active_symptoms = []


def get_data():
    symp = []
    for j in range(df.shape[0]):
        for i in df.iloc[j,1:]:
            if pd.isna(i):
                continue
            if i not in symp:
                symp.append(i)
    t1 = []
    for i in symp:
        if i not in t1:
            t1.append(i.replace('_',' ').strip())

    res = []
    for i in t1:
        t = {}
        t['name'] = i
        res.append(t)
        
    return res



class Diagnose(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(Diagnose, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.relu1 = nn.Dropout(0.5)
        self.fc2 = nn.Linear(hidden_size, 128)
        self.relu2 = nn.Dropout(0.5)
        self.fc3 = nn.Linear(128, output_size)
        self.softmax = nn.Softmax(dim=1)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = self.relu1(x)
        x = torch.relu(self.fc2(x))
        x = self.relu2(x)
        x = self.fc3(x)
        x = self.softmax(x)
        return x
    

input_size = 131
hidden_size = 128
output_size = 41
model = Diagnose(input_size, hidden_size, output_size)
model.load_state_dict(torch.load('chatbotmodelnew.pth'))


def get_active_symptoms():
    symptoms = []
    for j in range(df.shape[0]):
        for i in df.iloc[j,1:]:
            if pd.isna(i):
                continue
            if i not in symptoms:
                symptoms.append(i)
    formatted_symptoms = []
    for i in symptoms:
        formatted_symptoms.append(i.replace("_", " ").strip())
    dictionary_symptoms = {}
    for n, i in enumerate(formatted_symptoms):
        dictionary_symptoms[i] = n
    vector = [0] * len(formatted_symptoms)
    for i in active_symptoms:
        vector[dictionary_symptoms[i]] = 1
    return vector, dictionary_symptoms


def diagnosis(vector, dictionary_symptoms):
    res = []
    diseases = []
    for i in df['Disease']:
        if i not in diseases:
            diseases.append(i)
    dictionary = {}
    for n, i in enumerate(diseases):
        dictionary[n] = i
    model.eval()
    with torch.no_grad():
        ypred = model(torch.Tensor(torch.Tensor([vector])))
        for i in ypred.tolist():
            for j in i:
                if j > 0.2:
                    print(dictionary[i.index(j)])
                    t = {}
                    t['name'] = dictionary[i.index(j)]
                    res.append(t)
        return res


data = get_data()

@app.route('/append')
def append():
    label = request.args.get('a', '')

    if label in active_symptoms:
        active_symptoms.remove(label)
    else:
        active_symptoms.append(label)

    print(active_symptoms)

    if(len(active_symptoms)>3):
        vector, dictionary = get_active_symptoms()
        res = diagnosis(vector,dictionary)
        return res
    
    # res = []
    # for i in active_symptoms:
    #     t = {}
    #     t['name'] = i
    #     res.append(t)
        
    # return jsonify(res)


@app.route('/search')
def search():
    query = request.args.get('q', '')
    results = []
    for item in data:
        if query.lower() in active_symptoms:
            continue
        if query.lower() in item['name'].lower():
            results.append(item)
    return jsonify(results)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat')
def index():
    return render_template('chat.html')


display_symptoms = []
diagnosed = []
fail = 0


@app.route("/response")
def get_bot_response():
    userText = request.args.get('msg')
    print(userText)
    return "System"

if __name__ == '__main__':
    app.run(debug=True, port=8001)
