from flask import Flask, render_template, request
from data_analyze import AttendanceAnalyzer

app = Flask(__name__)

# Initialize the analyzer
analyzer = AttendanceAnalyzer("logs.csv", "registration_users.csv")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        target_date = request.form["date"]
        results = analyzer.analyze_date(target_date)
        return render_template(
            "results.html",
            date=target_date,
            absent_users=results["absent_users"],
            late_early_data=results["late_early_data"],
        )
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
