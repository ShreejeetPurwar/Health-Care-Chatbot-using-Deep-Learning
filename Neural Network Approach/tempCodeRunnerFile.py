def getdata():
    df = pd.read_csv('Diseases - Sheet1 (1).csv')
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