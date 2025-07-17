import pandas as pd
from flask import Flask, render_template, request, url_for
import joblib   
model = joblib.load('insurance_model.joblib')
import os
app = Flask(__name__)
search_history = []
@app.route('/',methods=['GET'])
def home():
    return render_template('index.html')
@app.route('/project', methods=['GET', 'POST'])
def project():
    image_url = None
    if request.method == 'POST':
        age = request.form.get('age')
        sex = request.form.get('sex')
        BMI = request.form.get('bmi')
        children = request.form.get('children')
        smoker = request.form.get('smoker')
        profile_image = request.files.get('profile_image')
        if profile_image and profile_image.filename:
            upload_folder = os.path.join('static', 'uploads')
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)
            image_path = os.path.join(upload_folder, profile_image.filename)
            profile_image.save(image_path)
            image_url = url_for('static', filename=f'uploads/{profile_image.filename}')
        sex_dict = {'female' : 0, 'male' : 1}
        smoker_dict = {'no' : 0, 'yes' : 1}
        sex_num = sex_dict.get(sex or '', 0)
        smoker_num = smoker_dict.get(smoker or '', 0)
        age_num = int(age or 0)
        BMI_num = float(BMI or 0)
        children_num = int(children or 0)
        lst = [[age_num,sex_num,BMI_num,children_num,smoker_num]]
        prediction = model.predict(lst)
        rounded_prediction = round(prediction[0], 2)
        print("prediction >>>>>>>>>>", prediction)
        import datetime
        search_history.append({ 'age': age,
                                'sex': sex,
                                'BMI': BMI,
                                'children': children,
                                'smoker': smoker,
                                'prediction': rounded_prediction,
                                'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                'image_url': image_url})
        return render_template('project.html', prediction=rounded_prediction,
                                age=age,
                                sex=sex,
                                BMI=BMI,
                                children=children,
                                smoker=smoker,
                                image_url=image_url)
    return render_template('project.html', image_url=image_url)
@app.route('/history')
def history():
    return render_template('history.html', search_history=search_history)
@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        
        # Print contact form data to terminal
        print("\n" + "="*50)
        print("📧 CONTACT FORM SUBMISSION")
        print("="*50)
        print(f"👤 Name: {name}")
        print(f"📧 Email: {email}")
        print(f"💬 Message: {message}")
        print("="*50)
        
        
        # Here you can handle the contact form submission, e.g., save to a database or send an email
        return render_template('contact.html', name=name, email=email, message=message)
    return render_template('contact.html')
@app.route('/generate_card')
def generate_card():
    return render_template('generate_card.html', entries=search_history[::-1])  # Latest first
if __name__ == '__main__':
    app.run(debug=True)