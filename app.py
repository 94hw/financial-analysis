from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def index():
    return "<h1>股票/虛擬貨幣統計分析系統已成功啟動！</h1>"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
