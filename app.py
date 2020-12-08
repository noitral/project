
from flask import Flask, send_file, make_response, request
import random,string
from pymysql import *


def go(path):
    # 浏览器适配
    if path[-1] == '/':path=path[:-1]
    return "templates\\" + path


app = Flask(__name__)


# 欢迎页面
@app.route('/')
def hello_world():
    return send_file(go("index.html"))



@app.route("/<string:path>")
def play(path):
    file = send_file(go(path))
    resp = make_response(file)
    # 在选择性别的页面，设置uid
    if path == "1.html":
        uid = ''.join(random.sample(string.ascii_letters + string.digits, 36))
        resp.set_cookie("uid", uid)
    # 性别
    if "boy_.html" in path:     resp.set_cookie("gender", "boy")
    if "girl_.html" in path:    resp.set_cookie("gender", "girl")
    #年龄
    if "introduction" in path:
        age = request.args.get("valus")
        if age: resp.set_cookie("age", age)
    #  题号-分数
    if ("boy_title" in path) or ("girl_title" in path) or ("tip_boy.html" in path):
        qid = request.args.get("QID")
        score = request.args.get("score")
        if qid and score:resp.set_cookie(qid, score)
    # 计算分数
    if ("result.html" in path):
        result = {}
        result['gender'] = request.cookies.get("gender")
        result['age'] = request.cookies.get('age')
        result['uid'] = request.cookies.get('uid')
        for i in range(1,18):
            result[i] = request.cookies.get(str(i))
        result[18] = request.args.get("score")
        # 1,6,8,12,13,17
        scoreA = (int(result[1]) + int(result[6]) - int(result[8]) + int(result[12]) + int(result[13]) - int(result[17])) / 6
        # 4,9.15,3,10,11
        scoreB = (int(result[4]) + int(result[9]) + int(result[15]) + int(result[3]) + int(result[10]) + int(result[11])) / 6
        # 2,5,7,14,16,18
        scoreC = (-int(result[2]) + int(result[5]) - int(result[7]) + int(result[14]) - int(result[16]) - int(result[18])) / 6
        conn = connect(host='127.0.0.1', port=3306, database='wdnmd', user='wdnmd', password='123456', charset='utf8')
        cs = conn.cursor()
        sql = """INSERT INTO `wdnmd`.`data` (`UID`, `GENDER`, `AGE`, `1`, `2`, `3`, `4`, `5`, `6`, `7`, `8`, `9`, `10`, `11`, `12`, `13`, `14`, `15`, `16`, `17`, `18`, `A`, `B`, `C`, `SELECT_SEX`) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s' );"""%(result['uid'], result['gender'], result['age'], result[1], result[2], result[3], result[4], result[5], result[6], result[7], result[8], result[9], result[10], result[11], result[12], result[13], result[14], result[15], result[16], result[17], result[18], scoreA, scoreB, scoreC, "")
        cs.execute(sql)
        conn.commit()
        cs.close()
        conn.close()
        if scoreA >= 3 and scoreB >= 3 and scoreC >= 3:
            if result['gender'] == 'girl': return send_file("girl_py.html")
            else: return send_file(go("boy_py.html"))

        if scoreA >= 3 and scoreB >= 3 and scoreC <= 3:
            if result['gender'] == 'girl': return send_file("girl_java.html")
            else: return send_file(go("boy_java.html"))

        if scoreA <= 3 and scoreB <= 3 and scoreC >= 3:
            if result['gender'] == 'girl': return send_file("girl_cplus.html")
            else: return send_file(go("boy_cplus.html"))

        if scoreA <= 3 and scoreB <= 3 and scoreC <= 3:
            if result['gender'] == 'girl': return send_file("girl_c.html")
            else: return send_file(go("boy_c.html"))
    return resp
@app.errorhandler(404)
def error(e):
    return "你请求的页面不存在，错误信息：%s"%e
@app.errorhandler(500)
def error(e):
    return "非法路径，错误信息：%s"%e
if __name__ == '__main__':
    app.run(debug=True)



