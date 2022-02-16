import pymongo
client = pymongo.MongoClient("mongodb+srv://root:666666cs@cluster0.h9pli.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.member_system
print("Database successfully connected")

from flask import *
app=Flask(__name__,static_folder="static",static_url_path="/")
app.secret_key="anystringbutsecret"

#處理路由
@app.route("/")
def index():
    
    # print("請求方法",request.method)
    # print("通訊協定",request.scheme)
    # print("主機名稱",request.host)
    # print("路徑",request.path)
    # print("完整的網址",request.url)
    # print("瀏覽器和作業系統",request.headers.get("user-agent"))
    # print("語言偏好",request.headers.get("accept-language"))
    # print("引薦網址",request.headers.get("referrer"))

    # lang=request.headers.get("accept-language")
    # if lang.startswith("en"):
    #     return "Hello World"
    # else:
    #     return "你好，歡迎光臨"
    return render_template("index.html")

@app.route("/member")
def member():
    if "nickname" in session:
        return render_template("member.html")
    else:
        return redirect("/")

@app.route("/error")
def error():
    message=request.args.get("msg","發生錯誤，請聯繫客服!")
    return render_template("error.html",message=message)

@app.route("/signup",methods=["POST"])
def signup():
    #從前端接收資料
    nickname=request.form["nickname"]
    email=request.form["email"]
    passward=request.form["passward"]
    #根據接收到的資料和資料互動
    collection=db.user
    #檢查會員集合中是否有相同email的文件資料
    result=collection.find_one({
        "email":email
    })
    if result !=None:
        return redirect("/error?msg=信箱已被註冊")
    #把資料放進資料庫，完成註冊
    collection.insert_one({
        "nickname":nickname,
        "email":email,
        "passward":passward
    })
    return redirect("/")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/signin",methods=["POST"])
def signin():
    #從前端取得使用者的輸入
    email=request.form["email"]
    passward=request.form["passward"]
    #和資料庫互動
    collection=db.user
    #檢查信箱密碼是否正確
    result=collection.find_one({
        "$and":[
            {"email":email},
            {"passward":passward}
        ]
    })
    #找不到對應的資料，登入失敗，導向到錯誤頁面
    if result==None:
        return redirect("/error?msg=帳號或密碼輸入錯誤")
    #登入成功，在 Session 紀錄會員資訊，導向到會員頁面
    session["nickname"]=result["nickname"]
    return redirect("/member")

@app.route("/signout")
def signout():
    #移除Session中的會員資訊
    del session["nickname"]
    return redirect("/")

# @app.route("/user/<username>")
# def handleUser(username):
#     if username=="justin":
#         return "你好" + username
#     else:
#         return "Hello" +username

app.run(port=3000)