from flask import Flask, request , jsonify , make_response , render_template
from flask_cors import CORS
from dotenv import load_dotenv
load_dotenv()
import google.generativeai as genai
import os
from PIL import Image
import requests
from io import BytesIO



app = Flask(__name__)
CORS(app)

api_secret_key = os.getenv("api_secret_key")

os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input,image):
    model = genai.GenerativeModel('gemini-pro-vision')
    print(f"input_def = {input}")
    if input!="" and input!= None:
       print("if")
       response = model.generate_content([input,image])
    else:
       print("else")
       response = model.generate_content(image)
    return str(response.text)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/image_description_generator", methods=['GET','POST'])
def image_description_generator():
    try:
        if request.method == "POST" or request.method == "GET":
            if 'image' in request.files and request.files['image'].filename != '':
                # If an image file is uploaded directly
                uploaded_file = request.files['image']
                # if uploaded_file.filename == '':
                #     return jsonify({"error": "No file provided"}), 400
                image = Image.open(uploaded_file)
            elif 'url' in request.form:
                # If an S3 URL is provided
                url = request.form['url']
                response = requests.get(url)
                if response.status_code != 200:
                    return jsonify({"error": "Failed to fetch image from provided URL"}), 400
                image = Image.open(BytesIO(response.content))
            else:
                return jsonify({"error": "No image or URL provided"}), 400
            
            prompt = request.form.get("prompt")
            res = get_gemini_response(prompt, image)
            return jsonify({"product_description": res})
            
        return render_template('index.html')
    except Exception as e:
        return jsonify({"error": str(e)}), 500     
    
@app.route('/health')
def health_checkup():
    """
    Return: json
    """
    return jsonify({ 'status': 'UP' }), 200
    
if __name__ == "__main__":
    app.run(host="0.0.0.0" , port = 5556, debug = True)

