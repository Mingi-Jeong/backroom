from flask import Flask, render_template, request, jsonify
from saju.calculator import calculate_saju, format_saju
from saju.elements import analyze_saju_elements, get_harmony_advice
from saju.daeun import calculate_daeun
from saju.compatibility import analyze_compatibility

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    name = data.get('name', '')
    year = int(data['year'])
    month = int(data['month'])
    day = int(data['day'])
    hour = int(data.get('hour', 12))
    minute = int(data.get('minute', 0))
    gender = data.get('gender', '남')
    current_year = int(data.get('current_year', 2026))

    saju = calculate_saju(year, month, day, hour, minute)
    saju_text = format_saju(saju)
    elements = analyze_saju_elements(saju)
    harmony = get_harmony_advice(elements)
    daeun = calculate_daeun(saju, gender, current_year)

    return jsonify({
        'name': name,
        'saju': saju,
        'saju_text': saju_text,
        'birth': f"{year}년 {month}월 {day}일 {hour}시",
        'elements': elements,
        'harmony': harmony,
        'daeun': daeun,
    })

@app.route('/compatibility', methods=['POST'])
def compatibility():
    data = request.get_json()['data']
    results = []
    for p in data:
        saju = calculate_saju(p['year'], p['month'], p['day'], p.get('hour', 12), p.get('minute', 0))
        results.append({
            'name': p['name'],
            'saju': saju,
            'saju_text': format_saju(saju),
        })

    compat = analyze_compatibility(results[0]['saju'], results[1]['saju'])
    return jsonify({
        'person1': results[0],
        'person2': results[1],
        'compatibility': compat,
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
