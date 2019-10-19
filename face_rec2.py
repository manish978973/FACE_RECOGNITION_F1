from PIL import Image , ImageDraw
import face_recognition
import os
from flask import  Flask, render_template, request
from flask_uploads import UploadSet, configure_uploads, IMAGES

app = Flask(__name__)

photos = UploadSet('photos', IMAGES)

app.config['UPLOADED_PHOTOS_DEST'] = '/home/manishrchandran/Downloads/FACE'
configure_uploads(app,photos)



my_list = {}

##Loading Training images

def get_encoded_faces():
    for dirpath, dnames, fnames in os.walk("./faces"):
        for f in fnames:
            if f.endswith(".jpg") or f.endswith(".png"):
                face = face_recognition.load_image_file("faces/" + f)
                encoding = face_recognition.face_encodings(face)[0]
                my_list[f.split(".")[0]] = encoding


    return my_list

## TESTING

def classify(img):


    faces = get_encoded_faces()
    known_faces_encoded = list(faces.values())
    known_face_names = list(faces.keys())


    testing_image = face_recognition.load_image_file(img)
    face_locations = face_recognition.face_locations(testing_image)
    face_encodings = face_recognition.face_encodings(testing_image,face_locations)

    pil_Image = Image.fromarray(testing_image)
    draw = ImageDraw.Draw(pil_Image)

    for (top,right,bottom,left), face_encoding in zip(face_locations,face_encodings):
        matches = face_recognition.compare_faces(known_faces_encoded,face_encoding)

        name = "Unknown"

        if True in (matches):
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]

##Draw Image boxes
        draw.rectangle(((left,top),(right,bottom)),outline=(0,0,0))

        #Draw label

        test_width,test_height = draw.textsize(name)
        draw.rectangle(((left, bottom - test_height - 10),(right,bottom)),fill=(0,0,0),outline=(0,0,0))
        draw.text((left+6,bottom - test_height - 5), name, fill=(255,255,255,255))




    del draw

    pil_Image.show()








@app.route('/upload', methods=['GET', 'POST'])

def upload():
    if request.method == 'POST' and 'photo' in request.files:
        #filename = photos.save(request.files['photo'])
        filename = request.files['photo']
        classify(filename)

        #return filename
        #return "Success"
    return render_template('upload.html')


if __name__ == '__main__':
    app.run(debug=True)











