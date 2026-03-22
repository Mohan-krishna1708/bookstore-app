import os

from flask import Flask, render_template, request, Response, url_for,redirect
import pymysql
from email.message import EmailMessage
import smtplib
import random
from werkzeug.security import generate_password_hash, check_password_hash


db_config = {
    'host': 'localhost',
    'database': 'bookstore',
    'user': 'root',
    'password': os.getenv("DB_PASS")
}
app = Flask(__name__)

#EMAIL CONFIGURATION
EMAIL_ADDRESS = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASS")
def send_email(to_mail, subject, body):
    msg = EmailMessage()
    msg['To'] = to_mail
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg.set_content(body)
   
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)


@app.route('/')
def home():    
    return render_template('home.html')
    

@app.route('/adminlogin1')
def adminlogin1():
    return render_template('admin_login.html')

@app.route('/adminlogin2', methods = ['GET', "POST"] )
def adminlogin2():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')        
        if username == "admin" and password == "admin":
            return render_template('admin_dashboard.html')        
        else:
            message = "Invalid credentials"
            return render_template('errorpage.html', message = message)
    
    return render_template('admin_login.html')

@app.route('/forgot_password1', methods=['POST'])
def forgot_password1():
    email = request.form['email']
    otp = random.randint(1111,9999)

    subject = "OTP for password reset"
    body = f"Your OTP is {otp}"

    send_email(email, subject, body)

    return render_template('forgot_password1.html', email=email, otp=otp)


@app.route('/forgot_password3', methods=['POST'])
def forgot_password3():
    email = request.form['email']
    otp = request.form['otp']
    cotp = request.form['cotp']

    if otp == cotp:
        return render_template('forgot_password2.html', email=email)
    else:
        return render_template('errorpage.html', message="Invalid OTP")


@app.route('/forgot_password4', methods=['POST'])
def forgot_password4():
    email = request.form['email']
    password = request.form['password']
    cpassword = request.form['cpassword']

    if password != cpassword:
        return render_template('errorpage.html', message="Passwords do not match")

    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()

    query = "UPDATE USERS SET USER_PASSWORD=%s WHERE USER_EMAIL=%s"
    hashed_password = generate_password_hash(password)
    cursor.execute(query, (hashed_password, email)) 
    conn.commit()

    cursor.close()
    conn.close()

    return render_template('user_login.html')

@app.route('/home')
def landing():
    
    return render_template('home.html')
@app.route('/admin_addproducts1')
def admin_addproducts1():
    return render_template('admin_addproducts.html')

@app.route('/add_products', methods=["GET", "POST"])
def add_products():
    if request.method == "POST":
        pname = request.form["product_name"]
        pimage = request.files["product_image"]
        pgenere = request.form["product_genre"]
        paprice = request.form["actual_price"]
        pdprice = request.form["discounted_price"]
        pquantity = request.form["quantity"]

        pimage = pimage.read()

        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        query = '''INSERT INTO PRODUCTS 
                (PNAME, PIMAGE, PGENERE, PAPRICE, PDPRICE, PQUANTITY)
                VALUES (%s,%s,%s,%s,%s,%s)'''
        cursor.execute(query,(pname, pimage, pgenere, paprice, pdprice,pquantity))
        conn.commit()
        cursor.close()
        conn.close()

        return render_template('admin_dashboard.html', data="YES")

    return redirect('/admin_addproducts1')    

@app.route('/admin_manageproducts1')
def admin_manageproducts1():
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    query = 'SELECT * FROM PRODUCTS'
    cursor.execute(query)
    products = cursor.fetchall()
    details = []
    for i in products:
        i = list(i)        
        i[2] = url_for('product_image', pid = i[0] )        
        details.append(i)
            
    return render_template("admin_manageproducts.html", details = details)

@app.route('/product_image/<int:pid>')
def product_image(pid):
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    query = "SELECT PIMAGE FROM PRODUCTS WHERE PID = %s"
    cursor.execute(query, (pid,))
    image = cursor.fetchone()
    if image and image[0]:
        return Response(image[0], mimetype='image/png')
    else:
        return redirect('/static/images/default.png')
    
@app.route('/admin_deleteproduct/<int:pid>')    
def admin_deleteproduct(pid):
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    query = "DELETE FROM PRODUCTS WHERE PID = %s "
    cursor.execute(query, (pid,))
    conn.commit()
    
    query = 'SELECT * FROM PRODUCTS'
    cursor.execute(query)
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    
    details = []
    for i in products:
        i = list(i)        
        i[2] = url_for('product_image', pid = i[0] )        
        details.append(i)            
    return render_template("admin_manageproducts.html", details = details)
    


@app.route('/user_signup1')
def user_signup1():
    return render_template('user_signup.html')

@app.route('/user_signup2', methods = ['POST', 'GET'])
def user_signup2():
    
    name = request.form["name"]
    email = request.form["email"]
    mobile = request.form["mobile"]
    upassword = request.form["password"]
    cpassword = request.form["cpassword"]    
    if upassword != cpassword:
        return render_template('errorpage.html', message = "Password does not match")    
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    query = "SELECT * FROM USERS WHERE USER_EMAIL = %s"
    cursor.execute(query, (email,))   
    entries = cursor.fetchone()    
    if entries == None:
        otp = random.randint(1111,9999)
        subject = "OTP for verification"
        body = f'''Your OTP for verification is {otp}. 
        Do not share with others.'''
        send_email(email,subject, body )
        return render_template('otpverify.html',name=name,email=email,mobile=mobile,password=upassword,otp=otp)    
    else:
        return render_template('errorpage.html', message = "Email already exists")

@app.route("/user_signup3",methods=["POST","GET"])
def user_signup3():
    name = request.form["name"]
    email = request.form["email"]
    mobile = request.form["mobile"]
    password = request.form["password"]
    otp = request.form["otp"]
    cotp = request.form["cotp"]
    
    if otp == cotp:
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        query = "INSERT INTO USERS (USER_NAME,USER_EMAIL,USER_MOBILE,USER_PASSWORD) VALUES (%s,%s,%s,%s)"
        hashed_password = generate_password_hash(password)
        cursor.execute(query,(name,email,mobile,hashed_password))
        conn.commit()
        return render_template("user_login.html")
    else:
        return render_template("errorpage.html",message="Invalid OTP")

@app.route('/user_login1')
def user_login1():
    return render_template('user_login.html')

@app.route('/user_login2', methods = ['POST', 'GET'])
def user_login2():
    email = request.form.get('email')
    password = request.form.get('password')
    
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    query = 'SELECT * FROM USERS WHERE USER_EMAIL = %s '
    cursor.execute(query, (email,))
    details = cursor.fetchone()  
    if details == None:
        return render_template('errorpage.html', message = 'email not registered') 
    details = list(details)
    user_id = details[0]
    if check_password_hash(details[4], password):
        query = 'SELECT * FROM PRODUCTS'
        cursor.execute(query)
        products = cursor.fetchall()
        cursor.close()
        conn.close()
            
        details = []
        for i in products:
            i = list(i)        
            i[2] = url_for('product_image', pid = i[0] )  
            if i[-1]  > 0:    
                details.append(i) 
        return render_template('user_home.html', products = details, user_id = user_id)    
    else:
        return render_template('errorpage.html', message = "Invalid Password")


@app.route('/add_to_cart/<int:pid>/<int:userid>')
def add_to_cart(pid, userid):

    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()

    # 1. check stock first
    cursor.execute("SELECT PQUANTITY FROM PRODUCTS WHERE PID = %s", (pid,))
    result = cursor.fetchone()

    if result is None:
        return render_template('errorpage.html', message="Product not found")

    p_quantity = result[0]

    if p_quantity <= 0:
        return render_template('errorpage.html', message="Out of stock")

    # 2. check if item already in cart
    cursor.execute(
        "SELECT QUANTITY FROM CART WHERE PRODUCT_ID = %s AND USER_ID = %s",
        (pid, userid)
    )
    quantity = cursor.fetchone()

    if quantity is None:
        cursor.execute(
            "INSERT INTO CART (USER_ID, PRODUCT_ID, QUANTITY) VALUES (%s, %s, %s)",
            (userid, pid, 1)
        )
    else:
        cursor.execute(
            "UPDATE CART SET QUANTITY = %s WHERE PRODUCT_ID = %s AND USER_ID = %s",
            (quantity[0] + 1, pid, userid)
        )

    # 3. update product stock
    cursor.execute(
        "UPDATE PRODUCTS SET PQUANTITY = %s WHERE PID = %s",
        (p_quantity - 1, pid)
    )

    conn.commit()

    # 4. reload products
    cursor.execute("SELECT * FROM PRODUCTS")
    products = cursor.fetchall()

    cursor.close()
    conn.close()

    details = []
    for i in products:
        i = list(i)
        i[2] = url_for('product_image', pid=i[0])
        if i[-1] > 0:
            details.append(i)

    return render_template('user_home.html', products=details, user_id=userid, msg="YES")

@app.route("/shopping_cart/<int:user_id>")
def shopping_cart(user_id):    
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()    
    query = 'SELECT * FROM CART WHERE USER_ID = %s'
    cursor.execute(query, (user_id,))
    cart_products = cursor.fetchall()
    
    final_data = [] 
    for each in cart_products:
        product_id = each[1]
        quantity = each[2]
        query = '''SELECT PID, PNAME, PIMAGE, PDPRICE FROM PRODUCTS
        WHERE PID = %s 
        '''
        cursor.execute(query, (product_id,))
        product_details = cursor.fetchone()

        if product_details:  # Only proceed if the product exists
            product_details = list(product_details)
            product_details[2] = url_for('product_image', pid = product_id)
            final_data.append([product_details, quantity])
    
    cursor.close()
    conn.close() 
     
    total = 0
    for each in final_data:
        total += each[0][3] * each[1]

    return render_template('shopping_cart.html', data=final_data, user_id=user_id, total=total)

              
@app.route('/user_login_updated/<int:user_id>')  
def user_login_updated(user_id):
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    query = 'SELECT * FROM PRODUCTS'
    cursor.execute(query)
    products = cursor.fetchall()
    cursor.close()
    conn.close()
            
    details = []
    for i in products:
        i = list(i)        
        i[2] = url_for('product_image', pid = i[0] )  
        if i[-1]  > 0:    
            details.append(i) 
    return render_template('user_home.html', products = details, user_id = user_id) 


@app.route('/delete_cart_item/<int:pid>/<int:userid>/<int:quantity>')
def delete_cart_item(pid, userid, quantity):
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    
    query = '''DELETE FROM CART WHERE PRODUCT_ID = %s AND USER_ID = %s
    '''
    cursor.execute(query, (pid, userid))
    conn.commit()

    query = '''SELECT PQUANTITY FROM PRODUCTS 
    WHERE PID = %s
    '''
    cursor.execute(query, (pid,))
    current_quantity = cursor.fetchone()[0]
    query = '''UPDATE PRODUCTS SET PQUANTITY = %s  WHERE PID = %s'''
    cursor.execute(query, (current_quantity + quantity,pid))
    conn.commit()


    return redirect(url_for('shopping_cart', user_id = userid))


@app.route('/success', methods=['POST', 'GET'])
def success():
    razorpay_payment_id = request.form.get('razorpay_payment_id')
    userid = request.form.get('userid')

    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()

    query = '''INSERT INTO ORDER_DETAILS VALUES (%s, %s)'''
    cursor.execute(query, (userid, razorpay_payment_id))
    conn.commit()

    query = '''INSERT INTO ORDERS SELECT * FROM CART'''
    cursor.execute(query)
    conn.commit()

    cursor.execute('DELETE FROM CART')
    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for('user_login_updated', user_id=userid))

if __name__ == "__main__":
    app.run(debug = True, port = 5006)

