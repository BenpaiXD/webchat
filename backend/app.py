from flask import Flask, render_template

# create instance of flask app
app = Flask(__name__)

# decorator sets this as root in website
@app.route("/")
def homePage():
    # html that is being run on the page
    return render_template("index.html")

if __name__ == "__main__":
    app.run()