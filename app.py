from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    uname = request.form['username'].lower()  # Convert to lowercase
    pwd = request.form['password']

    try:
        df = pd.read_csv("csvfile/username.csv")
        user = df.loc[df["username"].str.lower() == uname]  # Case-insensitive comparison

        if user.empty:
            return "Invalid Username or Password"
        elif user['password'].values[0] == pwd:
            return redirect(url_for('menu'))
        else:
            return "Invalid Username or Password"

    except FileNotFoundError:
        return "Username file not found"
    except Exception as e:
        return f"An error occurred: {e}"

        #  except FileNotFoundError:
        #     return "User database not found. Please set up the system."


   
       
@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            patdf = pd.read_csv("csvfile/patientnew.csv", index_col=0)
        except FileNotFoundError:
            patdf = pd.DataFrame(columns=["pid", "name", "age", "weight", "gender", "address", "phoneno", "disease"])
        pid = int(request.form['pid'])
        if not patdf[patdf['pid'] == pid].empty:
            return "Duplicate Patient ID. Please try again with a unique ID."
        name = request.form['name']
        age = request.form['age']
        weight = request.form['weight']
        gender = request.form['gender']
        address = request.form['address']
        phoneno = request.form['phoneno']
        disease = request.form['disease']
        patdf.loc[len(patdf)] = [pid, name, age, weight, gender, address, phoneno, disease]
        patdf.to_csv("csvfile/patientnew.csv")
        return redirect(url_for('menu'))
    return render_template('register.html')

@app.route('/patients')
def list_patients():
    try:
        patdf = pd.read_csv("csvfile/patientnew.csv", index_col=0)
    except FileNotFoundError:
        return "No patient records found."
    return render_template('patients.html', patients=patdf.to_dict(orient='records'))

@app.route('/update/<int:pid>', methods=['GET', 'POST'])
def update_patient(pid):
    try:
        patdf = pd.read_csv("csvfile/patientnew.csv", index_col=0)
        patient = patdf.loc[patdf['pid'] == pid]
        if patient.empty:
            return "Patient not found."
        if request.method == 'POST':
            name = request.form['name']
            age = request.form['age']
            weight = request.form['weight']
            gender = request.form['gender']
            address = request.form['address']
            phoneno = request.form['phoneno']
            disease = request.form['disease']
            patdf.loc[patdf['pid'] == pid, ['name', 'age', 'weight', 'gender', 'address', 'phoneno', 'disease']] = [name, age, weight, gender, address, phoneno, disease]
            patdf.to_csv("csvfile/patientnew.csv")
            return redirect(url_for('list_patients'))
        return render_template('update.html', patient=patient.iloc[0].to_dict())
    except FileNotFoundError:
        return "Patient database not found."

@app.route('/delete/<int:pid>', methods=['POST'])
def delete_patient(pid):
    try:
        patdf = pd.read_csv("csvfile/patientnew.csv", index_col=0)
        patdf = patdf[patdf['pid'] != pid]
        patdf.to_csv("csvfile/patientnew.csv")
        return redirect(url_for('list_patients'))
    except FileNotFoundError:
        return "Patient database not found."

@app.route('/search', methods=['GET', 'POST'])
def search_patient():
    if request.method == 'POST':
        pid = int(request.form['pid'])
        try:
            patdf = pd.read_csv("csvfile/patientnew.csv", index_col=0)
            patient = patdf.loc[patdf['pid'] == pid]
            if patient.empty:
                return "No patient found with the given ID."
            return render_template('search_result.html', patient=patient.iloc[0].to_dict())
        except FileNotFoundError:
            return "Patient database not found."
    return render_template('search.html')

@app.route('/graph/disease_count')
def disease_count_graph():
    try:
        df = pd.read_csv("csvfile/patientnew.csv")
        disease_counts = df['disease'].value_counts()

        graph_path = "static/disease_count_graph.png"
        plt.figure()
        disease_counts.plot(kind='bar', color='skyblue')
        plt.title('Number of Patients for Each Disease')
        plt.xlabel('Disease')
        plt.ylabel('Number of Patients')
        plt.tight_layout()
        plt.savefig(graph_path)
        plt.close()

        return render_template('graph_disease.html', graph='/' + graph_path)
    except FileNotFoundError:
        return "No patient data available to generate graphs."

@app.route('/graph/age_group')
def age_group_graph():
    try:
        df = pd.read_csv("csvfile/patientnew.csv")
        age_groups = pd.cut(df['age'], bins=[0, 18, 35, 50, 65, 100], labels=['0-18', '19-35', '36-50', '51-65', '65+'])
        age_group_counts = df.groupby(['disease', age_groups]).size().unstack(fill_value=0)

        graph_path = "static/age_group_graph.png"
        plt.figure()
        age_group_counts.plot(kind='bar', stacked=True, figsize=(10, 6))
        plt.title('Age Group Distribution for Diseases')
        plt.xlabel('Disease')
        plt.ylabel('Number of Patients')
        plt.tight_layout()
        plt.savefig(graph_path)
        plt.close()

        return render_template('graph_age.html', graph='/' + graph_path)
    except FileNotFoundError:
        return "No patient data available to generate graphs."

if __name__ == '__main__':
    os.makedirs('csvfile', exist_ok=True)
    app.run(debug=True)
