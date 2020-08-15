# Parses form information into Order then adds to database
def addWebOrder():
    from typing import Dict, List

    # Converts string date into datetime object
    from datetime import datetime
    date: datetime = datetime.strptime(request.form["date"], '%Y-%m-%d')

    # Category is a work in progress
    # category= request.form["category"]
    location: str = request.form["loc"]
    subtotals: Dict[str, float] = {
        'Nishant': float(request.form["nishant"]),
        'Arjun': float(request.form["arjun"]),
        'Param': float(request.form["param"]),
    }
    newUserName = request.form["userName"]
    if newUserName:
        subtotals[newUserName] = float(request.form["userTotal"])
    total = float(request.form["total"])

    # Adds order to database
    from DB import DB
    from Order import Order
    excessive: List[Dict] = DB.add(Order(date, location, subtotals, total))

    # Sends member a confirmation message
    Twilio.Communication.send("\nAdded order from %s for a total of $%.2f" % (location, total), "Nishant")
    Twilio.alert(excessive)

# Serves home page
def home():
    if request.method == "POST":
        #addWebOrder()
        location = request.form["loc"]
        total = request.form["total"]
        return render_template("Result.html", loc= location, value=total)
    else:
        return render_template("AddOrder.html")
        # return render_template("test.html")

# Serves data dashboard
def dashboard():
    return render_template("Dashboard.html")

from flask import Flask, request, render_template
#import Twilio

app = Flask(__name__)
app.add_url_rule('/', view_func = home, methods = ['GET', 'POST'])
app.add_url_rule('/Dashboard', view_func = dashboard, methods = ['GET', 'POST'])
#app.add_url_rule('/sms', view_func = Twilio.sms, methods = ['POST'])

from os import environ
if __name__ == "__main__":
    port = int(environ.get("PORT", 5000))
    app.run(host = '0.0.0.0', port = port, debug = True)