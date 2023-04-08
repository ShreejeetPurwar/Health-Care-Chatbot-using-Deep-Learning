import nltk
import numpy as np
from nltk.stem.porter import PorterStemmer
import torch
import torch.nn as nn
import torch.optim as optim
import json
from sklearn.model_selection import train_test_split
import nltk.data

# nltk.download('punkt')

tokenizer = nltk.data.load('nltk:tokenizers/punkt/english.pickle')

disease_name = r'/Users/tejasmadhukar/Downloads/ISM/archive (18)/tuberculosis'

nltk.download('punkt')

stemmer = PorterStemmer()

with open(f'{disease_name}.json', 'r') as f:
    data = json.load(f)

words = []
tags = []
docs = []
for intent in data['intents']:
    for pattern in intent['patterns']:
        w = nltk.word_tokenize(pattern)
        words.extend(w)
        docs.append((w, intent['tag']))
        if intent['tag'] not in tags:
            tags.append(intent['tag'])

def bow(tokenized, words):
    sentence_words = [stemmer.stem(word.lower()) for word in tokenized]
    bag = np.zeros(len(words), dtype = np.float32)
    for i, n in enumerate(words):
        if n in sentence_words:
            bag[i] = 1
    return bag

words = [stemmer.stem(w.lower()) for w in words if w not in ['?', '.', ',', '!']]
words = sorted(list(set(words)))

X = []
y = []
for doc in docs:
    bow_vec = bow(doc[0], words)
    X.append(bow_vec)
    label = tags.index(doc[1])
    y.append(label)

class ChatBotModel(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(ChatBotModel, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.dropout1 = nn.Dropout(0.5)
        self.fc2 = nn.Linear(hidden_size, 128)
        self.dropout2 = nn.Dropout(0.5)
        self.fc3 = nn.Linear(128, output_size)
        self.softmax = nn.Softmax(dim=1)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = self.dropout1(x)
        x = torch.relu(self.fc2(x))
        x = self.dropout2(x)
        x = self.fc3(x)
        x = self.softmax(x)
        return x
    
input_size = len(X[0])
hidden_size = 128
output_size = len(y)
model = ChatBotModel(input_size, hidden_size, output_size)

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr = 0.001)

xtrain, xtest, ytrain, ytest = train_test_split(X, y, train_size = 0.8)

train_x = torch.Tensor(np.array(xtrain))
train_y = torch.Tensor([np.argmax(y) for y in ytrain])

num_epochs = 20

for epoch in range(num_epochs):
    batch_x = train_x
    batch_y = train_y
    optimizer.zero_grad()
    outputs = model(batch_x)

    loss = criterion(outputs, batch_y.long())
    loss.backward()
    optimizer.step()

    if epoch % 10 == 0:
        print(f'Epoch {epoch}, Loss: {loss.item()}')

torch.save(model.state_dict(), f'{disease_name}.pth')

data = {
"input_size": input_size,
"hidden_size": hidden_size,
"output_size": output_size,
"all_words": words,
"tags": tags
}

FILE = f"{disease_name}_data.pth"
torch.save(data, FILE)

model.eval()
with torch.no_grad():
    ypred = model(torch.Tensor(np.array(xtest)))
    acc = 0
    for i in range(len(xtest)):
        if np.argmax(ypred[i].tolist()) == np.argmax(ytest[i]):
            acc += 1
    print(acc / len(xtest))