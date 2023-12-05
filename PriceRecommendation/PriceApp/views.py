from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt
from django.http import JsonResponse
from sklearn import metrics
import joblib
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import hstack
from sklearn.metrics import mean_squared_error
import nltk
from nltk.corpus import stopwords
from sklearn.preprocessing import LabelEncoder
from tqdm import tqdm
import pandas as pd
import os
import scipy

def authenticated(request):
    # Your custom authentication logic here
    # Return True if the user is authenticated; otherwise, return False
    if 'id' in request.session and request.session['id']:
        return True
    else:
        return False


def index(request):
    return render(request, 'forms.html')


def register(request):
    errors = User.objects.basic_validator(request.POST)
    users = User.objects.all()
    for user in users:
        if user.email == request.POST['email']:
            errors["email"] = "This email already exists"
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        User.objects.create(firstname=firstname, lastname=lastname, email=email, password=pw_hash)
        user = User.objects.last()
        request.session['firstname'] = user.firstname
        request.session['id'] = user.id
        return redirect('/dashboard')


def dashboard(request):
    if authenticated(request):
        user = User.objects.get(id=request.session['id'])
        context = {
            'user': user
        }
        return render(request, 'dashboard.html', context)
    return redirect('/')


def login(request):
    user = User.objects.filter(email=request.POST['email']).first()
    if user:
        if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
            request.session['firstname'] = user.firstname
            request.session['lastname'] = user.lastname
            request.session['id'] = user.id
            messages.success = "login successful"
            return redirect('/dashboard')
        messages.error(request, "invalid credential")
        return redirect('/')
    messages.error(request, "invalid credential")
    return redirect('/')


def logout(request):
    request.session.clear()
    return redirect('/')


def price_form(request):
    if authenticated(request):
        return render(request, 'index.html')
    return redirect('/')



def process(input_data):
    data = pd.DataFrame([input_data])
    #data = pd.DataFrame.from_dict(input_data)
    def decontracted(phrase):
        # specific
        phrase = re.sub(r"won\'t", "will not", phrase)
        phrase = re.sub(r"can\'t", "can not", phrase)

        # general
        phrase = re.sub(r"n\'t", " not", phrase)
        phrase = re.sub(r"\'re", " are", phrase)
        phrase = re.sub(r"\'s", " is", phrase)
        phrase = re.sub(r"\'d", " would", phrase)
        phrase = re.sub(r"\'ll", " will", phrase)
        phrase = re.sub(r"\'t", " not", phrase)
        phrase = re.sub(r"\'ve", " have", phrase)
        phrase = re.sub(r"\'m", " am", phrase)
        return phrase

    st_words = stopwords.words('english')

    def name_process(text):
        '''THIS FUNCTION IS USED TO PREPROCESS THE NAME FEATURE'''
        text = decontracted(text)
        text = re.sub("[^A-Za-z0-9 ]","",text) # REMOVE EVERYTHING EXCEPT THE PROVIDED CHARACTERS
        text = text.lower() # CONVERT TO LOWER CASE
        text =  " ".join([i for i in text.split() if i not in st_words])
        if len(text)==0:
            text = "missing"
        return text # RETURN THE OUTPUT TEXT
    
    # APPLYING THE "preprocessing" FUNCTION ON THE FEAUTRE "name"
    data["name_processed"] = data.name.apply(name_process)
    data[data.name_processed.isnull()].name_processed ="missing" 
    
    
    #CREATING PREPROCESSING FUNCTION FOR BRAND NAME
    def brand_process(text):
        text = re.sub("[^A-Za-z0-9 ]","",text) # REMOVE EVERYTHING EXCEPT THE PROVIDED CHARACTERS
        text = text.lower()                    # CONVERT TO LOWER CASE
        return text
    
    brand_score = dict(data[data.brand_name.notnull()]["brand_name"].apply(brand_process).value_counts())

    processed_brand_name = [] #storing the barand name after preprocessing
    for index,i in tqdm(data.iterrows()) : # for each row in the dataset

        if  pd.isnull(i.brand_name): #if the brand name isnull we follow this

            words = i.name_processed.split() # we will split the name for that datapoint
            score  = [] # this variable stores the score for each word that we calculated above
            for j in words: # for each word 
                if j in brand_score.keys(): #if the words in name is present in the keys of brand score dict
                    score.append(brand_score[j]) # take the score from the dict and append in the score variable
                else: #if the word is not a brand name append -1
                    score.append(-1)
            # once we get the scores for all the words in the name the word with maximum score woulb be the brand name
            if max(score) > 0: #if the maximum score is greater than 0 then it contains a brand name so we append the brand name
                processed_brand_name.append(words[score.index(max(score))])
            else: # if maximum value is less than 0 then it means no brand name was found so "missing" is appended
                processed_brand_name.append("missing")

        else: # if the brand_name is not null we follow this
            processed_brand_name.append(brand_process(i.brand_name))
            
    #CREATING NEW COLUMN WITH PROCESSED BRAND NAMES
    data["brand_name_processed"] = processed_brand_name
    
    def category_name_preprocessing(text):
        #THIS FUNCTION PREPROCESSES THE TEXT IN "category_name" FEATURE
        text = re.sub("[^A-Za-z0-9/ ]","",text)# REMOVING ALL THE TEXT EXCEPT THE GIVEN CHARACTERS
        text = re.sub("s "," ",text) # REMOVING  "s" AT THE END OF THE WORD
        text = re.sub("s/","/",text) # REMOVING  "s" AT THE END OF THE WORD
        text = re.sub("  "," ",text) # REMOVING ONE SPACE WHERE TWO SPACES ARE PRESENT
        text = text.lower() # CONVERTING THE TEXT TO LOWER CASE
        return text # RETURNING THE PROCESSED TEXT

    # HERE WE ARE REPLACING THE NULL VALUES IN "category_name" WITH WORD "missing"
    data.category_name[data.category_name.isnull()] = "missing"
    # HERE WE ARE PREPROCESSING THE TEXT IN "category_name"
    data["category_name_preprocessed"] = data.category_name.apply(category_name_preprocessing)
    
    # FORMING A COLUMN "Tier_1"
    data["Tier_1"] = data.category_name_preprocessed.apply(lambda x:   x.split("/")[0] if len(x.split("/"))>=1 else "missing")
    
    # FORMING A COLUMN "Tier_2"
    data["Tier_2"] = data.category_name_preprocessed.apply(lambda x:   x.split("/")[1] if len(x.split("/"))>1 else "missing")
    
    # FORMING A COLUMN "Tier_3"
    data["Tier_3"] = data.category_name_preprocessed.apply(lambda x:   x.split("/")[2] if len(x.split("/"))>1 else "missing")
    
    #PREPROCESSING FUNCTION FOR ITEM DESCRIPTION
    def processing_item_description(text):
        '''THIS FUNCTION PREPROCESSES THE TEXT IN "item_description"'''
        text = re.sub("\[rm\] ","",str(text))
        text = decontracted(text)
        text = re.sub("[^A-Za-z0-9 ]","",str(text))
        text = str(text).lower()
        text =  " ".join([i for i in text.split() if i not in st_words])
        if len(text)==0:
            text = "missing"
        return text
    #REPLACING THE NULL VALUVE WITH WORD "missing"
    data.item_description[data.item_description.isnull()]="missing"

    #HERE WE ARE PREPROCESSING THE TEXT IN FEATURE "item_description" '''
    data["processed_item_description"] = data.item_description.apply(processing_item_description)
    
    return data

def encod(data):
    #ITEM CONDITION ID
    item_path = os.path.join(os.path.dirname(__file__), 'models', 'item_enc.pkl')
    item_enc = joblib.load(item_path)
    train_vec_item_con = item_enc[data.item_condition_id]
    #SHIPPING
    shipping_path = os.path.join(os.path.dirname(__file__), 'models', 'shipping_enc.pkl')
    shipping_enc = joblib.load(shipping_path)
    train_vec_shipping = shipping_enc[data.shipping]
    #BRAND NAME
    brand_path = os.path.join(os.path.dirname(__file__), 'models', 'brand_enc.pkl')
    brand_enc = joblib.load(brand_path)
    train_vec_brand =brand_enc.transform(data.brand_name_processed.values.reshape(-1,1))
    #train_vec_brand =brand_enc.transform(data.brand_name_processed)

    #TIER1 
    tier1_path = os.path.join(os.path.dirname(__file__), 'models', 'tier_enc.pkl')
    tier1_enc = joblib.load(tier1_path)
    train_vec_t1 = tier1_enc.transform(data.Tier_1.values.reshape(-1,1))
    #train_vec_t1 = tier1_enc.transform(data.Tier_1)
    #TIER2
    tier2_path = os.path.join(os.path.dirname(__file__), 'models', 'tier2_enc.pkl')
    tier2_enc = joblib.load(tier2_path)
    train_vec_t2 =tier2_enc.transform(data.Tier_2.values.reshape(-1,1))
    #train_vec_t2 =tier2_enc.transform(data.Tier_2)
    #TIER3
    tier3_path = os.path.join(os.path.dirname(__file__), 'models', 'tier3_enc.pkl')
    tier3_enc = joblib.load(tier3_path)
    train_vec_t3 =tier3_enc.transform(data.Tier_3.values.reshape(-1,1))
    #train_vec_t3 =tier3_enc.transform(data.Tier_3)
    
    #NAME TFIDF VECTORIZER
    name_tfidf_path = os.path.join(os.path.dirname(__file__), 'models', 'name_tfidf_enc.pkl')
    name_tfidf_enc = joblib.load(name_tfidf_path)
    train_vec_name = name_tfidf_enc.transform(data.name_processed)
    
    #ITEM DESCRIPTION TFIDF 
    desc_tfidf_path = os.path.join(os.path.dirname(__file__), 'models', 'desc_tfidf_enc.pkl')
    desc_tfidf_enc = joblib.load(desc_tfidf_path)
    train_vec_desc = desc_tfidf_enc.transform(data.processed_item_description)
    
    #IS MISSIN FEATURE 
    data["is_missing"]  =  (data.brand_name_processed=="missing") | (data.name_processed =="missing")| (data.processed_item_description=="missing")
    data["is_missing"]  = data["is_missing"].astype(int)
    
    X = hstack((train_vec_item_con,train_vec_shipping,train_vec_name,train_vec_brand,
                        train_vec_t1,train_vec_t2,train_vec_t3,
                        data.is_missing.values.reshape(-1,1),train_vec_desc))
    return X





def predict(request):
    if authenticated(request):
        if request.method == 'POST':
            # Load the trained linear regression model
            model_path = os.path.join(os.path.dirname(__file__), 'models', 'model.pkl')
            model = joblib.load(model_path)

            # Extract form data from the request
            name = request.POST['name']
            item_condition_id = int(request.POST['item_condition_id'])
            category_name = request.POST['category_name']
            brand_name = request.POST['brand_name']
            shipping = int(request.POST['shipping'])
            item_description = request.POST['item_description']

            # Prepare input data as a dictionary
            input_data = {
                'name': name,
                'item_condition_id': item_condition_id,
                'category_name': category_name,
                'brand_name': brand_name,
                'shipping': shipping,
                'item_description': item_description
            }

            # Process and encode the data
            processed_data = process(input_data)
            encoded_data = encod(processed_data)

            # Perform prediction
            predicted_price = model.predict(encoded_data)

            # Prepare the response
            context = {
                'predicted_price': float(predicted_price)
            }

            return render(request, 'index.html', context)
    return render(request, 'dashboard.html')
