from flask import Flask, render_template_string, request
import os
import random
from datetime import datetime, timedelta

app = Flask(__name__)

# 模擬生成歷史數據與統計指標
def generate_market_data(asset_name, base_price, volatility):
    random.seed(42) # 固定隨機種子，確保數據穩定
    data = []
    current_price = base_price
    start_date = datetime.now() - timedelta(days=30)
    
    for i in range(30):
        date_str = (start_date + timedelta(days=i)).strftime('%Y-%m-%d')
        change = current_price * random.uniform(-volatility, volatility)
        current_price = round(current_price + change, 2)
        data.append({"date": date_str, "price": current_price})
    
    # 計算統計指標
    prices = [x["price"] for x in data]
    avg_price = round(sum(prices) / len(prices), 2)
    max_price = max(prices)
    min_price = min(prices)
    
    # 簡單的移動平均 (MA5)
    ma5 = round(sum(prices[-5:]) / 5, 2)
    
    return {
        "asset_name": asset_name,
        "history": data,
        "metrics": {
            "avg_price": avg_price,
            "max_price": max_price,
            "min_price": min_price,
            "ma5": ma5,
            "latest_price": prices[-1]
        }
    }

# HTML 樣式範本 (Bootstrap 5 包裝，展現前端產品經理的審美)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>金融數據分析系統</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.css" rel="stylesheet">
    <style>
        body { background-color: #f8f9fa; font-family: 'Helvetica Neue', Arial, sans-serif; }
        .card { border: none; box-shadow: 0 4px 6px rgba(0,0,0,0.1); border-radius: 12px; }
        .hero-section { background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); color: white; padding: 40px 0; border-radius: 0 0 24px 24px; }
    </style>
</head>
<body>

    <div class="hero-section text-center mb-4">
        <div class="container">
            <h1 class="display-5 fw-bold">📈 股票/虛擬貨幣統計分析系統</h1>
            <p class="lead">資訊數學組期末專題 - 結合數學統計與資訊開發的量化平台</p>
            <span class="badge bg-success fs-6">雲端後端引擎：Flask 運作中</span>
        </div>
    </div>

    <div class="container">
        <!-- 選擇資產 -->
        <div class="row mb-4 justify-content-center">
            <div class="col-md-6 text-center">
                <form method="GET" action="/">
                    <label for="asset" class="form-label fw-bold">請選擇要分析的金融資生：</label>
                    <select name="asset" id="asset" class="form-select form-select-lg mb-3" onchange="this.form.submit()">
                        <option value="TSMC" {% if selected == 'TSMC' %}selected{% endif %}>台灣股市：台積電 (2330)</option>
                        <option value="MEDIATEK" {% if selected == 'MEDIATEK' %}selected{% endif %}>台灣股市：聯發科 (2454)</option>
                        <option value="BTC" {% if selected == 'BTC' %}selected{% endif %}>虛擬貨幣：比特幣 (BTC)</option>
                        <option value="ETH" {% if selected == 'ETH' %}selected{% endif %}>虛擬貨幣：乙太幣 (ETH)</option>
                    </select>
                </form>
            </div>
        </div>

        <!-- 統計數據卡片 -->
        <div class="row g-3 mb-4">
            <div class="col-md-3">
                <div class="card p-3 text-center bg-white">
                    <div class="text-muted small">最新收盤價</div>
                    <div class="fs-3 fw-bold text-primary">${{ res.metrics.latest_price }}</div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card p-3 text-center bg-white">
                    <div class="text-muted small">30日平均價 (μ)</div>
                    <div class="fs-3 fw-bold text-success">${{ res.metrics.avg_price }}</div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card p-3 text-center bg-white">
                    <div class="text-muted small">5日移動平均 (MA5)</div>
                    <div class="fs-3 fw-bold text-warning">${{ res.metrics.ma5 }}</div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card p-3 text-center bg-white">
                    <div class="text-muted small">30日最高 / 最低</div>
                    <div class="fs-4 fw-bold text-danger">${{ res.metrics.max_price }} / ${{ res.metrics.min_price }}</div>
                </div>
            </div>
        </div>

        <!-- 歷史數據表格 -->
        <div class="row">
            <div class="col-12">
                <div class="card p-4 bg-white mb-5">
                    <h3 class="card-title h5 mb-3 fw-bold">📊 歷史價格走勢數據 (近 30 天)</h3>
                    <div class="table-responsive" style="max-height: 300px; overflow-y: auto;">
                        <table class="table table-hover align-middle">
                            <thead class="table-dark sticky-top">
                                <tr>
                                    <th>日期</th>
                                    <th>資產名稱</th>
                                    <th>收盤價格 (USD/TWD)</th>
                                </tr>
                            </thead>
                            <tbody>
                                {% for item in res.history | reverse %}
                                <tr>
                                    <td>{{ item.date }}</td>
                                    <td><span class="badge bg-secondary">{{ res.asset_name }}</span></td>
                                    <td class="fw-bold">${{ item.price }}</td>
                                </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <footer class="text-center py-4 text-muted bg-light border-top mt-auto">
        <p class="mb-0">輔仁大學 數學系資訊數學組 期末成果發表</p>
    </footer>
</body>
</html>
"""

@app.route('/')
def index():
    selected_asset = request.args.get('asset', 'TSMC')
    
    # 根據選擇的資產給予不同的基底價格與波動度
    if selected_asset == 'TSMC':
        res = generate_market_data("台積電 (2330.TW)", 950, 0.02)
    elif selected_asset == 'MEDIATEK':
        res = generate_market_data("聯發科 (2454.TW)", 1200, 0.025)
    elif selected_asset == 'BTC':
        res = generate_market_data("Bitcoin (BTC)", 65000, 0.04)
    elif selected_asset == 'ETH':
        res = generate_market_data("Ethereum (ETH)", 3500, 0.045)
        
    return render_template_string(HTML_TEMPLATE, res=res, selected=selected_asset)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
