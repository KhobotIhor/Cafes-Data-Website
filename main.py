from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators, BooleanField

cafes_info = []
class Base(DeclarativeBase):
    pass


app = Flask(__name__)
db = SQLAlchemy(model_class=Base)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cafes.db"
app.config['SECRET_KEY'] = 'SECRET_KEY'

db.init_app(app)


def to_dict(self):
    return {column.name: getattr(self, column.name) for column in self.__table__.columns}


class PostCafe(FlaskForm):
    name = StringField('Cafe Name', validators=[validators.DataRequired()])
    map_url = StringField('Google Maps Url for Cafe Location', validators=[validators.DataRequired(), validators.URL()])
    img_url = StringField('URL for Image of the Cafe', validators=[validators.URL()])
    location = StringField('District where the cafe is located')
    seats = StringField('Approximate number of seats e.g 10-20', validators=[validators.DataRequired()])
    wifi = BooleanField('Is there wifi in the cafe?')
    toilet = BooleanField('Is there toilet in the cafe?')
    coffee_price = StringField('How much is a cup of coffee in this cafe? e.g 2.5$')
    submit = SubmitField('Post')
class Cafe(db.Model):
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    name: Mapped[str] = mapped_column(db.String(250), nullable=False)
    map_url: Mapped[str] = mapped_column(db.String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(db.String(500))
    location: Mapped[str] = mapped_column(db.String(250))
    seats: Mapped[str] = mapped_column(db.String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(db.Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(db.Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(db.Boolean)
    can_take_calls: Mapped[bool] = mapped_column(db.Boolean)
    coffee_price: Mapped[str] = mapped_column(db.String(250), nullable=True)



@app.route('/')
def home():
    result = db.session.execute(db.select(Cafe).order_by(Cafe.name))
    data = result.scalars().all()
    return render_template('index.html', cafes=data)

@app.route('/post', methods=['GET', 'POST'])
def post():
    form = PostCafe()

    if form.validate_on_submit():
        new_cafe = Cafe(
            name=request.form.get("name"),
            map_url=request.form.get("map_url"),
            img_url=request.form.get("img_url"),
            location=request.form.get("location"),
            has_sockets=True,
            has_toilet=bool(request.form.get("toilet")),
            has_wifi=bool(request.form.get("wifi")),
            can_take_calls=True,
            seats=request.form.get("seats"),
            coffee_price=request.form.get("coffee_price"),
        )
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for('home'))
    print(form.errors)
    return render_template('index.html', form=form)


@app.route('/delete/<int:cafe_id>')
def delete_cafe(cafe_id):
    cafe = db.get_or_404(Cafe, cafe_id)
    if cafe:
        db.session.delete(cafe)
        db.session.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)

