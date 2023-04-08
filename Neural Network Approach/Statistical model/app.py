from flask import Flask, render_template,request,jsonify
import numpy as np
import pandas as pd 
import operator

app = Flask(__name__, template_folder="template", static_folder="static")

df = pd.read_csv('Diseases - Sheet1 (1).csv')

data = []
common_symptoms = []
active_symptoms = []
THRESHOLD = 0.8



def getdata():
    symp = []
    for i in range(df.shape[0]):
        a = df['General_Symptom'].values[i].split(',')
        for i in a:
            tmp = i.strip()
            symp.append(tmp)
    t1,symptom = [],[]
    for i in symp:
        if i not in t1:
            t1.append(i)
    for i in t1:
        if i not in symptom:
            temp = {}
            temp['name'] = i
            symptom.append(temp)
    return symptom

def get_common_symptoms():    
    freq = {}
    result = []
    for i in df['General_Symptom']:
        s = i.split(', ')
        for j in s:
            if j not in freq:
                freq[j] = 1
            else:
                freq[j] += 1
    sort = dict(sorted(freq.items(),key=operator.itemgetter(1),reverse=True))
    temp = list(dict(list(sort.items())[:10]).keys())
    for i in temp:
        t = {}
        t['name'] = i
        result.append(t)
    return result

def disease_symptom_data():
    disease_data = {}
    for i in range(df.shape[0]):
        disease_data[df['Disease_Name'].values[i]] = df['General_Symptom'].values[i].split(", ")
    return disease_data

def compute_probability(active_symptoms, disease_data):
    probabilities = {}
    termination_flag = False
    for key, value in disease_data.items():
        probabilities[key] = 0
        for i in active_symptoms:
            if i in value:
                probabilities[key] += 1
        probabilities[key] = probabilities[key] / len(value)
        if(probabilities[key] > THRESHOLD):
            termination_flag = True
    return dict(sorted(probabilities.items(), key = operator.itemgetter(1), reverse=True)), termination_flag

def recommender_system(probabilities, active_symptoms, disease_data, fail = 0):
    display_symptoms = []
    do_not_display = []
    termination = False
    if fail > 0:
        for _ in range(fail):
            for key in list(probabilities.keys()):
                count = 0
                if(len(display_symptoms) >= 10):
                    break
                for i in disease_data[key]:
                    if count == 3:
                        continue
                    if i not in active_symptoms and i not in do_not_display:
                        do_not_display.append(i)
                        count += 1
    for key in list(probabilities.keys()):
        count = 0
        if(termination):
            break
        for i in disease_data[key]:
            if(len(display_symptoms) == 10):
                termination = True
                break
            if count == 3:
                continue
            if i not in active_symptoms and i not in display_symptoms and i not in do_not_display:
                display_symptoms.append(i)
                count += 1
    return display_symptoms


common_symptoms = get_common_symptoms()
data = getdata()

@app.route('/top')
def top():
    return jsonify(common_symptoms)

@app.route('/append')
def append():
    label = request.args.get('a', '')

    if label in active_symptoms:
        active_symptoms.remove(label)
    else:
        active_symptoms.append(label)

    print(active_symptoms)
    
    res = []
    for i in active_symptoms:
        t = {}
        t['name'] = i
        res.append(t)
    return jsonify(res)


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


disease_data = disease_symptom_data()

# Get active_symptoms symptoms data
display_symptoms = []
diagnosed = []
fail = 0


@app.route("/response")
def get_bot_response():
    userText = request.args.get('msg')
    print(userText)
    return "ih"

@app.route('/main')
def main_loop():
    disease_data = disease_symptom_data()
    display_symptoms = []
    diagnosed = []
    fail = 0
    res = []

    pred_class = ""
    response = ""
    
    probabilities, termination_flag = compute_probability(active_symptoms, disease_data)

    print(probabilities)

    if(termination_flag):
        for key, value in probabilities.items():
            if value >= THRESHOLD:
                diagnosed.append(key)
        res = [{'name' : "terminate"}]
        for i in diagnosed:
            t = {}
            t['name'] = i
            res.append(t)
        return jsonify(res)

    if(pred_class == "NotDetected"):
        fail += 1
    else:
        fail = 0

    display_symptoms = recommender_system(probabilities, active_symptoms, disease_data, fail)

    for i in display_symptoms:
        t = {}
        t['name'] = i
        res.append(t)


 
    return jsonify(res)

    # Display these symptoms and get active symptoms data






if __name__ == '__main__':
    app.run(debug=True, port=8001)


