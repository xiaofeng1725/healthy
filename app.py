from flask import Flask, render_template, request
import matplotlib.pyplot as plt
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'static'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    height = float(request.form['height'])
    weight = float(request.form['weight'])
    age = int(request.form['age'])
    history = request.form['history']

    # 计算 BMI
    bmi = round(weight / (height / 100) ** 2, 2)

    # 标准体重（简单算法：身高(cm) - 105）
    std_weight = round(height - 105, 2)
    diff_weight = round(weight - std_weight, 2)

    if bmi < 18.5:
        status = "偏瘦"
        exercise = "建议进行力量训练，如哑铃、深蹲等，每周3次以上。"
        diet = "增加蛋白质摄入，如鸡蛋、牛奶、坚果等。"
    elif 18.5 <= bmi < 24:
        status = "正常"
        exercise = "维持现有运动量，建议每周跑步3-5次，每次30分钟。"
        diet = "均衡饮食，蔬菜水果比例合理。"
    else:
        status = "超重"
        exercise = "增加有氧运动，如游泳、骑行、快走等，每周4-5次。"
        diet = "控制碳水，减少油炸食品，多吃粗粮。"

    # 生成图表
    labels = ['标准体重', '偏离体重']
    values = [std_weight, abs(diff_weight)]  # 确保为正数
    colors = ['#36a2eb', '#ff6384']

    plt.figure(figsize=(5,5))
    import matplotlib
    matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 支持中文字体
    matplotlib.rcParams['axes.unicode_minus'] = False  # 正常显示负号

    plt.pie(values, labels=labels, autopct='%1.1f%%', colors=colors, startangle=140)

    plt.axis('equal')
    chart_path = os.path.join(UPLOAD_FOLDER, 'chart.png')
    plt.savefig(chart_path)
    plt.close()

    return render_template('result.html', bmi=bmi, status=status, std_weight=std_weight,
                           diff_weight=diff_weight, exercise=exercise, diet=diet,
                           history=history, chart_url='/' + chart_path)

#if __name__ == '__main__':
    #app.run(debug=True)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
