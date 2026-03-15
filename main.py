from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

stations = pd.read_csv("data_small\stations.txt", skiprows=17)
stations = stations[["STAID" , "STANAME                                 "]]


@app.route("/")
def home():
    return render_template("home.html", data=stations.to_html())

@app.route("/api/v1/<station>/<date>")
def temperature(station, date):
    filename = "data_small/TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])
    temperatue = df.loc[df['    DATE'] == date]['   TG'].squeeze() / 10
    return {"station": station,
            "date": date,
            "temperature": temperatue}

@app.route("/api/v1/<station>")
def station(station):
    file = "data_small/TG_STAID" + str(station).zfill(6) + ".txt"
    sd = pd.read_csv(file, skiprows=20)
    return render_template("home.html", data=sd.to_html())

@app.route("/api/v1/year/<station>/<year>")
def year(station, year):
    file = "data_small/TG_STAID" + str(station).zfill(6) + ".txt"
    sd = pd.read_csv(file, skiprows=20)
    sd['    DATE'] = sd['    DATE'].astype(str)
    sd = sd[sd['    DATE'].str.startswith(str(year))]
    return render_template("home.html", data=sd.to_html())


if __name__ == "__main__":
    app.run(debug=True) 