from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# --- Funkcje obliczeniowe ---
def sum_digits(n):
    return sum(int(d) for d in str(n))

def reduce_to_one_digit(n):
    while n >= 10:
        n = sum_digits(n)
    return n

def process_decimal(decimal_part):
    s = str(decimal_part)
    if len(s) % 2 != 0:
        s += '0'
    total = 0
    for i in range(0, len(s), 2):
        pair = s[i:i+2]
        total += sum_digits(int(pair))
    return reduce_to_one_digit(total)

def calculate_magic_average(grades_count):
    total_grades = sum(grades_count.values())
    if total_grades == 0:
        return None
    sum_grades = sum(grade * count for grade, count in grades_count.items())
    average = sum_grades / total_grades
    dec = str(average).split(".")[1]
    dec = int(dec)
    if not dec == 0:
        average = str(average) + "10101"
        average = float(average)

    integer_part = int(average)
    decimal_str = str(average).split(".")[1]
    processed_decimal = process_decimal(decimal_str)

    final_result = float(f"{integer_part}.{processed_decimal}")
    return final_result

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/calculate", methods=["POST"])
def calculate():
    data = request.json
    grades_count = {int(k): int(v) for k, v in data.items()}
    result = calculate_magic_average(grades_count)
    if result is None:
        return jsonify({"result": "Nie podano ocen."})
    else:
        return jsonify({"result": f"Twoja Średnia: {result}"})

if __name__ == "__main__":
    app.run(debug=True)
