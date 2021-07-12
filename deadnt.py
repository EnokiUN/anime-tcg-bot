from flask import Flask 
from threading import Thread 

app = Flask('')

@app.route('/')
def onlypagelmao():
    return 'whut u doing here :0'
    
def run():
    app.run(host='0.0.0.0', port=8080)
    
def thou_shall_not_die():
    t = Thread(target=run)
    t.start()