from flask import Flask, request, send_file
import yagmail

sender_email = "email"
receiver_email = "email"
password = "pw"  # Use an App Password for security

app = Flask(__name__)

@app.route('/ground')
def send_email():
    lat = request.args.get('lat') 
    long = request.args.get('long') 
    result = request.args.get('result')
    powerOutage = request.args.get('powerOutage') 
    probability = request.args.get('probability') 
    try:
        # Initialize yagmail
        yag = yagmail.SMTP(sender_email, password)
        if not powerOutage or result == "failure":
            return
        # Send an email
        yag.send(
            to=receiver_email,
            subject="Power outage test",
            contents=f"coordinates: ({lat}, {long})\nresult: {result}\npower outage: {powerOutage}\nconfidence: {probability}"
        )
        
        return "Email sent successfully!"
    
    except Exception as e:
        return f"Error: {e}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)