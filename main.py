from flask import Flask, render_template, request, redirect, url_for
import ast, datetime
web_site = Flask(__name__)






@web_site.route('/', methods=["GET", "POST"])
def login():
    error = None

    with open('userdata.txt','r') as f:
        f_user = f.read()
        user = ast.literal_eval(f_user)
        username_list = user.keys()

        if request.method =="POST":
            if request.form["username"] not in username_list: 
                error = "Sorry, you haven't signed up yet."
            elif request.form["username"] in username_list: 
                userpassword = user[request.form["username"]]
                if request.form["password"] == userpassword: 
                    return redirect(url_for("user_page") + request.form["username"]) 

                else:
                    error = "Oops, password is incorrect, try again please."

    return render_template('login.html', error=error, title="Login")

@web_site.route('/register', methods=["GET", "POST"])
def register():
    un_error = None
    pw_error = None
    with open('userdata.txt','r') as f:
        f_user = f.read()
        user = ast.literal_eval(f_user)
        username_list = user.keys()
        
        if request.method == "POST":
            if request.form["username"] in username_list:
                un_error = "Sorry, this name has been taken, try another one please."
            if len(request.form["password"])<6:
                pw_error = "At least 6 digits"
            else:
                user[str(request.form["username"])] = str(request.form["password"])
                with open('userdata.txt','w') as f:
                    f.write(str(user))
                with open('user_diary.txt','r') as f:
                    f_diary = f.read()
                    diary = ast.literal_eval(f_diary)
                    diary[request.form["username"]]={}
                with open('user_diary.txt','w') as f:
                    f.write(str(diary))

                return redirect(url_for("login"))# show a JS alert says "XXX, congratulations! Now try to login, I want to know more about you!"
    return render_template('register.html', un_error=un_error, pw_error=pw_error, title="Register")
    



@web_site.route('/user/', defaults={'username':None})
@web_site.route('/user/<username>')
def user_page(username):
    error = None

    with open('user_diary.txt','r') as f:
        f_diary = f.read()
        diary = ast.literal_eval(f_diary)
    
        diaries = diary[username]
        sorted_diary = {}  
        # show diaries in time sequence, newest first. maybe in html.
        int_key = []
        for key in diaries.keys():
            key = int(key)
            int_key.append(key)
        sorted_id = sorted(int_key, reverse = True)
        
        for id in sorted_id:
            sorted_diary[str(id)] = diaries[str(id)]
        diaries = sorted_diary

        if not diaries:
            error = "Sorry, you haven't create any achievement yet. You can write one now! " 
    
    return render_template('user.html', username=username, diaries=diaries, error=error)


@web_site.route('/user/<username>/create_diary', methods=["GET", "POST"])
def new_diary(username):
    error = None
    if request.method =="POST":
        content = request.form["diary content"]
        date = datetime.datetime.now().strftime("%m/%d/%Y")    #str
        diary_id = 1    #int
        if content:
            with open('user_diary.txt','r') as f:
                f_diary = f.read()
                diary = ast.literal_eval(f_diary)
                # create a new diary_id for the new diary 
                for id in range(1,1000):
                    if str(id) not in diary[username].keys():
                        diary_id = str(id)
                        break
                # diary_id as a key, date:content dict as value
                diary[username][diary_id] = {date:content}
            with open('user_diary.txt','w') as f:
                f.write(str(diary))    
            return redirect(url_for('user_page') + username) # show a JS alert says "Good for you! You've done a great job today, I'm so proud of you!"
        if not content:
            error = "You haven't add anything yet. I believe you can add something for the day. "  # maybe add a JS alert
    return render_template('create_diary.html', error=error, username=username )        
        











RUN_LOCAL_SERVER = True 

host_ip = '127.0.0.1'

if not RUN_LOCAL_SERVER:
  host_ip = '0.0.0.0'

web_site.run(debug=True, host=host_ip, port=8080)