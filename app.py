import requests
from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQALCHEMY_DATABASE_URI']='sqlite:///weather.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class City(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50),nullable=False)

@app.route("/", methods=["GET","POST"])
def index():
    if request.method=='POST':
        new_city=request.form.get('city')

        if new_city:
            new_city_obj=City(name=new_city)

            db.session.add(new_city_obj)
            db.session.commit()

    cities= City.query.all()
    
    url= 'http://api.openweathermap.org/data/2.5/weather?q={}&APPID=dcb9b872954f2d5711ca01bef174cde7'
    city = 'New Delhi'

    weather_data=[]

    for city in cities:

        r= requests.get(url.format(city.name)).json()
        print(r)

        temp=r['main']['temp']
        tempc= temp-273.15
        tempc=round(tempc,2)


        weather ={
            'city' : city.name,
            'temperature' : tempc,
            'description' : r['weather'][0]['description'] ,
            'icon' : r['weather'][0]['icon'],
        }

        weather_data.append(weather)
    return render_template('weather.html', weather_data=weather_data)

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)