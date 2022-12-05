from datetime import date, time
from flask import Flask, request, render_template
from helperfunctions import cleanTimetableLink
from main import main
import os



app = Flask(__name__)
appName = "where-got-time-table"


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        modules = request.form.get("modules")

        link = request.form.get("link")

        if link != "":
            try:
                module_list = cleanTimetableLink(link=link)
            except Exception:
                return render_template('error_link.html')
        else:
            module_list = [i.upper() for i in modules.split()]

        starttime = int(float(request.form.get("timestart")))
        endtime = int(float(request.form.get("timeend")))

        semester = int(request.form.get("semester"))

        monday = "Monday" if request.form.get("Monday") == "on" else "off"
        tuesday = "Tuesday" if request.form.get("Tuesday") == "on" else "off"
        wednesday = "Wednesday" if request.form.get("Wednesday") == "on" else "off"
        thursday = "Thursday" if request.form.get("Thursday") == "on" else "off"
        friday = "Friday" if request.form.get("Friday") == "on" else "off"

        freeday_list = list(filter(lambda x: x != "off", [monday, tuesday, wednesday, thursday, friday]))

        interval_input = request.form.get("betweenlessons")
        interval = False if interval_input == "" else int(interval_input)

        lunch = True if request.form.get("lunch") == "on" else False


        if len(module_list) != 0:
            link = main(module_list, semester, starttime, endtime, freeday_list, lunch, interval)

            if link == False:
                return render_template('error_modules.html')

            return render_template('results.html', link=link)
        else:
            return ('', 204)
    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))