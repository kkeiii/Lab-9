from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='templ')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reviews.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    rate = db.Column(db.Integer, nullable=False)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text = request.form.get('text')
        rate = request.form.get('rate')
        if text and rate and rate.isdigit():
            rate_int = int(rate)
            if 1 <= rate_int <= 5:
                new_review = Review(text=text, rate=rate_int)
                db.session.add(new_review)
                db.session.commit()
                return redirect(url_for('veb') + '?thanks=1')
        return redirect(url_for('veb'))
    reviews = Review.query.all()
    thanks = request.args.get('thanks')
    return render_template('veb.html', reviews=reviews, thanks=thanks)

@app.route('/clear', methods=['POST'])
def clear():
    Review.query.delete()
    db.session.commit()
    return redirect(url_for('veb'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    #print("Откройте в браузере: http://127.0.0.1:5000/")
    app.run(debug=True)
