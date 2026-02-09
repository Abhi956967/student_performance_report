import os
import uuid
import pandas as pd

from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    redirect,
    send_file
)

from flask_login import (
    LoginManager,
    login_user,
    login_required,
    logout_user,
    UserMixin,
    current_user
)

from werkzeug.security import generate_password_hash, check_password_hash

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Table,
    TableStyle,
    Spacer
)

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

from src.pipeline.predict_pipeline import CustomData, PredictPipeline


# ---------------- CONFIG ---------------- #

UPLOAD_FOLDER = "uploads"
REPORT_FOLDER = "reports"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(REPORT_FOLDER, exist_ok=True)

application = Flask(__name__)
app = application

app.secret_key = "mlops-secret-key"


# ---------------- LOGIN SETUP ---------------- #

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


# demo user
USERS = {
    "admin": generate_password_hash("admin123")
}


class User(UserMixin):
    def __init__(self, username):
        self.id = username


@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


# ---------------- ROUTES ---------------- #

@app.route("/")
def index():
    return render_template("index.html")


# ---------- LOGIN ---------- #
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username in USERS and check_password_hash(
            USERS[username], password
        ):
            login_user(User(username))
            return redirect("/predict")

        return render_template(
            "login.html",
            error="Invalid username or password"
        )

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


# ---------- SINGLE PREDICTION PAGE ---------- #
@app.route("/predict")
@login_required
def predict_page():
    return render_template("predict.html")


# ---------- API PREDICT ---------- #
@app.route("/api/predict", methods=["POST"])
@login_required
def api_predict():

    try:
        data = request.get_json()

        student = CustomData(
            gender=data["gender"],
            race_ethnicity=data["ethnicity"],
            parental_level_of_education=data[
                "parental_level_of_education"
            ],
            lunch=data["lunch"],
            test_preparation_course=data[
                "test_preparation_course"
            ],
            reading_score=float(data["reading_score"]),
            writing_score=float(data["writing_score"])
        )

        df = student.get_data_as_data_frame()

        pipeline = PredictPipeline()
        pred = pipeline.predict(df)[0]

        return jsonify({
            "success": True,
            "prediction": round(pred, 2)
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# ---------- CSV BATCH ---------- #
@app.route("/batch", methods=["GET", "POST"])
@login_required
def batch():

    if request.method == "POST":

        file = request.files["file"]

        path = os.path.join(
            UPLOAD_FOLDER,
            f"{uuid.uuid4()}_{file.filename}"
        )

        file.save(path)

        df = pd.read_csv(path)

        pipeline = PredictPipeline()
        preds = pipeline.predict(df)

        df["math_prediction"] = preds

        out_path = os.path.join(
            REPORT_FOLDER,
            f"{uuid.uuid4()}.csv"
        )

        df.to_csv(out_path, index=False)

        return render_template(
            "batch.html",
            table=df.head().to_html(classes="table"),
            download=out_path
        )

    return render_template("batch.html")


# ---------- PDF REPORT ---------- #
@app.route("/download_pdf/<path:file>")
@login_required
def download_pdf(file):

    df = pd.read_csv(file)

    pdf_path = file.replace(".csv", ".pdf")

    styles = getSampleStyleSheet()

    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4
    )

    table_data = [
        df.columns.tolist()
    ] + df.values.tolist()

    table = Table(table_data)

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
    ]))

    elements = [
        Paragraph(
            "<b>Student Performance Batch Report</b>",
            styles["Title"]
        ),
        Spacer(1, 20),
        table
    ]

    doc.build(elements)

    return send_file(pdf_path, as_attachment=True)


# ---------- ADMIN DASHBOARD ---------- #
@app.route("/admin")
@login_required
def admin():

    if current_user.id != "admin":
        return "Unauthorized", 403

    return render_template("admin.html")


# ---------------- MAIN ---------------- #

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)


























# from flask import Flask, request, render_template, jsonify
# from src.pipeline.predict_pipeline import CustomData, PredictPipeline

# application = Flask(__name__)
# app = application


# @app.route("/")
# def index():
#     return render_template("index.html")


# @app.route("/predict")
# def predict_page():
#     return render_template("predict.html")


# # ---------- API ROUTE ----------
# @app.route("/api/predict", methods=["POST"])
# def api_predict():

#     try:
#         data = request.json

#         student = CustomData(
#             gender=data["gender"],
#             race_ethnicity=data["ethnicity"],
#             parental_level_of_education=data["parental_level_of_education"],
#             lunch=data["lunch"],
#             test_preparation_course=data["test_preparation_course"],
#             reading_score=float(data["reading_score"]),
#             writing_score=float(data["writing_score"])
#         )

#         df = student.get_data_as_data_frame()

#         pipeline = PredictPipeline()
#         result = pipeline.predict(df)[0]

#         return jsonify({
#             "success": True,
#             "prediction": round(result, 2)
#         })

#     except Exception as e:
#         return jsonify({
#             "success": False,
#             "error": str(e)
#         })


# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=8080)

# ----------------------------------------------------------------------------------------------------------------------

# from flask import Flask,request,render_template
# import numpy as np
# import pandas as pd


# from sklearn.preprocessing import StandardScaler
# from src.pipeline.predict_pipeline import CustomData,PredictPipeline

# application=Flask(__name__)

# app=application

# ## Route for a home page

# @app.route('/')
# def index():
#     return render_template('index.html') 

# @app.route('/predictdata',methods=['GET','POST'])
# def predict_datapoint():
#     if request.method=='GET':
#         return render_template('home.html')
#     else:
#         data=CustomData(
#             gender=request.form.get('gender'),
#             race_ethnicity=request.form.get('ethnicity'),
#             parental_level_of_education=request.form.get('parental_level_of_education'),
#             lunch=request.form.get('lunch'),
#             test_preparation_course=request.form.get('test_preparation_course'),
#             reading_score=float(request.form.get('writing_score')),
#             writing_score=float(request.form.get('reading_score')))
        
#         pred_df=data.get_data_as_data_frame()
#         print(pred_df)

#         predict_pipeline=PredictPipeline()
#         results=predict_pipeline.predict(pred_df)
#         return render_template('home.html',results=results[0])
    
# if __name__=="__main__":
#     # app.run(host="0.0.0.0",port=8080)
#     app.run(host='0.0.0.0', port=8080)