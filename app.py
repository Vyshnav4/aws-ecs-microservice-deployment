from flask import Flask, request, render_template_string

app = Flask(__name__)

home_page = '''
<!doctype html>
<html lang="en">
<head>
    <title>Welcome</title>
    <style>
        body { font-family: Arial; padding: 2rem; background-color: #f4f4f4; }
        .container { background: white; padding: 2rem; max-width: 600px; margin: auto; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
        h1 { color: #333; }
        input, textarea { width: 100%; padding: 0.5rem; margin-top: 0.5rem; border: 1px solid #ccc; border-radius: 4px; }
        button { margin-top: 1rem; padding: 0.7rem 1.5rem; background: #28a745; color: white; border: none; border-radius: 4px; cursor: pointer; }
        button:hover { background: #218838; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Welcome to My Flask Web App</h1>
        <p>This is a basic form built using Flask only.</p>
        <form method="POST" action="/thankyou">
            <label for="name">Name:</label>
            <input type="text" id="name" name="name" required>

            <label for="message">Message:</label>
            <textarea id="message" name="message" rows="4" required></textarea>

            <button type="submit">Send</button>
        </form>
    </div>
</body>
</html>
'''

thankyou_page = '''
<!doctype html>
<html lang="en">
<head>
    <title>Thank You</title>
    <style>
        body { font-family: Arial; text-align: center; padding: 2rem; background-color: #f4f4f4; }
        .msg-box { background: white; padding: 2rem; display: inline-block; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
    </style>
</head>
<body>
    <div class="msg-box">
        <h2>Thank You, {{ name }}!</h2>
        <p>Your message has been received.</p>
    </div>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(home_page)

@app.route('/thankyou', methods=['POST'])
def thankyou():
    name = request.form.get('name', 'Friend')
    return render_template_string(thankyou_page, name=name)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
