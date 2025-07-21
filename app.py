from flask import Flask, render_template, request

app = Flask(__name__)

# Mock database
parts = [
    {
        "id": 1,
        "name": "RoboArm X1",
        "price": 199,
        "image_url": "https://lh3.googleusercontent.com/aida-public/AB6AXuBZCYL3a1lNjG4gaje-7o6QpfLW06E_ga6ckiKa6-xYFirF70ClTZ1vIB2TeWinoqMWHAcoO1A-t9mI2xtnzkhvv4twgaKxkEuHzJVMZksWBxc4Eb7aWdMVO81z4vyOQ45o7-Ps8PwDdYjhZht3UKMubMSrfFWBdoO6vGbRwScwlifgiWzgXFn0R-E3SdaWr2FTCIhzJ0iemNXwz1DUQH2QmBJcKYY3ZAysXjJZYTfcTJvlvBJ0xUXueWREl1Z84QDF6l_ZyKbIbeyy",
        "availability": "In Stock",
        "description": "High-precision robotic arm with six degrees of freedom, ideal for industrial automation and research applications.",
        "specifications": "Six degrees of freedom, 1kg payload, 0.1mm repeatability"
    },
    {
        "id": 2,
        "name": "Sensor Module S2",
        "price": 49,
        "image_url": "https://lh3.googleusercontent.com/aida-public/AB6AXuBgZkX7XRw9NnNbjULUxG-v84M_s1r3toQ18SrfOktvavUIkp_0RqgbFx6JDDjME61adzUZl8vyQWtXCt_GGLPg4G2sJewPT_oKqtavXcxsM4nuM3D8H37OcoC_mrGS_pK5bP4Q_inMuTsOeYDpDuSMBgOFks034eb0eJOFnhHp-kWks6UC-9XTNkwMrblZty-L386tsOqhDUF7pxkEbOZja3vUAdGm4kB5RSMOPLgczskzxhf1lDTUJvzSdvozJcSFM4UkQRSkCTZf",
        "availability": "In Stock",
        "description": "Multi-sensor module with environmental monitoring capabilities",
        "specifications": "Temperature, humidity, pressure, motion detection"
    }
]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/parts')
def parts_list():
    search_query = request.args.get('q', '')
    filtered_parts = [p for p in parts if search_query.lower() in p['name'].lower()] if search_query else parts
    return render_template('parts.html', parts=filtered_parts)

@app.route('/parts/<int:part_id>')
def part_detail(part_id):
    part = next((p for p in parts if p['id'] == part_id), None)
    if not part:
        return "Part not found", 404
    return render_template('part_detail.html', part=part)

if __name__ == '__main__':
    app.run(debug=True)