from flask import Flask, render_template, request
import os
import random
import numpy as np
import random
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.applications.vgg16 import preprocess_input
app = Flask(__name__)
app.config['UPLOAD_FOLDER']=os.path.join('static','pics')
#rendering home page for initial GET request
@app.route("/",methods=['GET', 'POST'])
def home():
    return render_template('page.html')
#rendering prediction page for POST request 
@app.route("/imgfile", methods = ['GET','POST'])
def predict():
    if request.method=="POST":
        imagefile=request.files['file']
        image_path=os.path.join(r'static/pics/',imagefile.filename)
        imagefile.save(image_path)
        # initialising variable for visualising the image uploaded in ./imgfile site
        filename1=os.path.join(app.config['UPLOAD_FOLDER'],imagefile.filename)

        model = load_model('FER_model.h5', compile = False)
        # Preprocess Input Image and Make Prediction
        image_dir = image_path
        #load the image
        my_image = load_img(image_dir, target_size=(48, 48))
        #preprocess the image
        my_image = img_to_array(my_image)
        my_image = my_image.reshape((1, my_image.shape[0], my_image.shape[1], my_image.shape[2]))
        my_image = preprocess_input(my_image)

        #make the prediction
        prediction = model.predict(my_image)
        print(prediction)
        out = np.argmax(prediction)
        print(out)
        emote={0:'Angry',1:'Disgust',2:'Fear',3:'Happy',4:'Neutral',5:'Sad',6:'Surprise'}

        #lists of videos
        happy=os.listdir('static/videos/Happy/Cleaned')
        energetic=os.listdir('static/videos/Energetic/Cleaned')
        neutral=os.listdir('static/videos/Neutral/Cleaned')
        sad=os.listdir('static/videos/Sad/Cleaned')

        #mapping videos to prediction
        if emote[out]=='Angry':
            user_video=os.path.join('static/videos/Happy/Cleaned/',happy[random.randint(0,len(happy)-1)])
        if emote[out]=='Disgust':
            user_video=os.path.join('static/videos/Happy/Cleaned/',happy[random.randint(0,len(happy)-1)])
        if emote[out]=='Fear':
            k=random.randint(0,1)
            if k==0:
                user_video=os.path.join('static/videos/Happy/Cleaned/',happy[random.randint(0,len(happy)-1)])
            if k==1:
                user_video=os.path.join('static/videos/Energetic/Cleaned/',energetic[random.randint(0,len(energetic)-1)])
        if emote[out]=='Happy':
            k=random.randint(0,3)
            if k==0:
                user_video=os.path.join('static/videos/Happy/Cleaned/',happy[random.randint(0,len(happy)-1)])
            if k==1:
                user_video=os.path.join('static/videos/Energetic/Cleaned/',energetic[random.randint(0,len(energetic)-1)])
            if k==2:
                user_video=os.path.join('static/videos/Neutral/Cleaned/',neutral[random.randint(0,len(neutral)-1)])
            if k==3:
                user_video=os.path.join('static/videos/Sad/Cleaned/',sad[random.randint(0,len(sad)-1)])
        if emote[out]=='Neutral':
            k=random.randint(0,2)
            if k==0:
                user_video=os.path.join('static/videos/Happy/Cleaned/',happy[random.randint(0,len(happy)-1)])
            if k==1:
                user_video=os.path.join('static/videos/Energetic/Cleaned/',energetic[random.randint(0,len(energetic)-1)])
            if k==2:
                user_video=os.path.join('static/videos/Neutral/Cleaned/',neutral[random.randint(0,len(neutral)-1)]) 
        if emote[out]=='Sad':
            k=random.randint(0,1)
            if k==0:
                user_video=os.path.join('static/videos/Happy/Cleaned/',happy[random.randint(0,len(happy)-1)])
            if k==1:
                user_video=os.path.join('static/videos/Energetic/Cleaned/',energetic[random.randint(0,len(energetic)-1)])
        if emote[out]=='Surprise':
            k=random.randint(0,1)
            if k==0:
                user_video=os.path.join('static/videos/Happy/Cleaned/',happy[random.randint(0,len(happy)-1)])
            if k==1:
                user_video=os.path.join('static/videos/Energetic/Cleaned/',energetic[random.randint(0,len(energetic)-1)])
    #returning template at end of function                
    return render_template('page1.html', prediction=emote[out], user_image = filename1, user_video=user_video) #filepath can be passed to render images or videos
#main code
if __name__=='__main__':
    app.run(debug=True)