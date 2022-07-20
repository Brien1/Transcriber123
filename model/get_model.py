import os
os.system("cp /Users/brienhall/Documents/FinalProject/model.pkl /Users/brienhall/Documents/Transcriber123/model/model.pkl")
size = os.path.getsize("/Users/brienhall/Documents/Transcriber123/model/model.pkl")
size = size/1000000
print(" model file size = ", size)
_100mb = 100
if (size > _100mb ):
    #do things
    print("j")
    import pickle
    f= pickle.load(open("/Users/brienhall/Documents/Transcriber123/model/model.pkl","rb"))
    f = pickle.dumps(f)
    print(pickle.loads(f))
    print(len(f)/2 + len(f)/2 , "   \t ", len(f))
    print(f[int(len(f)/2)])
    f1 = f[0:int(len(f)/2)]
    f2 = f[int(len(f)/2):]
    # print(pickle.loads(f1+f2))
    print(len(f1), " ", len(f2))
    pickle.dump(f1, open("/Users/brienhall/Documents/Transcriber123/model/model1.pkl","wb"))
    pickle.dump(f2, open("/Users/brienhall/Documents/Transcriber123/model/model2.pkl","wb"))
    
    obj = pickle.load(open("/Users/brienhall/Documents/Transcriber123/model/model1.pkl","rb"))+ pickle.load(open("/Users/brienhall/Documents/Transcriber123/model/model2.pkl","rb"))
    print("len of loaded object:: ",len(obj))
    obj = pickle.loads(obj)
    from sklearn.neural_network import MLPClassifier
    print(obj)
    os.remove("/Users/brienhall/Documents/Transcriber123/model/model.pkl")