import os
import uuid
import sqlite3
from flask import Flask, request, render_template, redirect, url_for, flash, session, g
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from PIL import Image


def save_resized_profile_pic(uploaded_file, upload_folder):
    filename = secure_filename(uploaded_file.filename)
    unique_name = f"{uuid.uuid4().hex}_{filename}"
    filepath = os.path.join(upload_folder, unique_name)

    img = Image.open(uploaded_file)
    img = img.convert("RGB")
    img.thumbnail((256, 256))  # Keep aspect ratio within 256x256

    # Center it in a 256x256 white square
    square_img = Image.new('RGB', (256, 256), (255, 255, 255))
    x = (256 - img.width) // 2
    y = (256 - img.height) // 2
    square_img.paste(img, (x, y))
    square_img.save(filepath, format='JPEG', quality=85)

    return unique_name

app = Flask(__name__)
app.secret_key = "your_secret_key"

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

DATABASE = 'pawsitive.db'

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

# --- Create tables if not exists ---
with sqlite3.connect(DATABASE) as conn:
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            name TEXT,
            phone TEXT,
            email TEXT,
            bio TEXT,
            account_type TEXT,
            profile_pic TEXT
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            media TEXT,
            caption TEXT,
            FOREIGN KEY (username) REFERENCES users(username)
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS mypets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            photo TEXT,
            name TEXT,
            breed TEXT,
            age TEXT,
            birthday TEXT,
            vaccination TEXT,
            deworming TEXT,
            vet TEXT
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS adoptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            photo TEXT,
            details TEXT,
            contact_name TEXT,
            contact_number TEXT,
            location TEXT
        )
    ''')
    conn.execute('''
    CREATE TABLE IF NOT EXISTS likes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        post_id INTEGER,
        username TEXT,
        UNIQUE(post_id, username),
        FOREIGN KEY(post_id) REFERENCES posts(id),
        FOREIGN KEY(username) REFERENCES users(username)
    )
''')
    conn.execute('''
    CREATE TABLE IF NOT EXISTS comments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        post_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        comment_text TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (post_id) REFERENCES posts(id),
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
''')
    conn.execute('''
    CREATE TABLE IF NOT EXISTS reminders (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       user_id INTEGER,
       pet_id INTEGER,
       reminder_type TEXT,
       reminder_date DATE,
       notified INTEGER DEFAULT 0,
       FOREIGN KEY (user_id) REFERENCES users(id),
       FOREIGN KEY (pet_id) REFERENCES mypets(id)  -- ✅ corrected table name
    )
''')



@app.route('/')
def home():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        username = request.form['username']
        password = generate_password_hash(request.form['password'])  # 🔒 Hash password
        bio = request.form['bio']
        account_type = request.form['account_type']
        profile_pic = request.files['profile_pic']

        unique_name = None
        if profile_pic:
            filename = secure_filename(profile_pic.filename)
            unique_name = f"{uuid.uuid4().hex}_{filename}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_name)
            profile_pic.save(filepath)

        try:
            db = get_db()
            db.execute('''
                INSERT INTO users (username, password, name, phone, email, bio, account_type, profile_pic)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (username, password, name, phone, email, bio, account_type, unique_name))
            db.commit()
            flash('Registration successful! Please log in.')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username already taken.')
            return redirect(url_for('register'))

    return render_template('register.html')  # 👈 correct return for GET request


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db = get_db()
        user = db.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()

        if user and check_password_hash(user['password'], password):  # ✅ Secure check
            session['user'] = user['username']
            flash('Login successful!', 'login')
            response = redirect(url_for('feed'))
            response.set_cookie('darkMode', '', expires=0)  # clear cookie
            return response
        else:
            flash('Invalid username or password.', 'login')
            return redirect(url_for('login'))

    return render_template('login.html')  # 👈 correct return for GET

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out.', 'login')  # Also login-related
    return redirect(url_for('login'))

@app.route('/profile')
def profile():
    if 'user' not in session:
        return redirect(url_for('login'))

    db = get_db()
    user = db.execute('SELECT * FROM users WHERE username = ?', (session['user'],)).fetchone()
    posts = db.execute('SELECT * FROM posts WHERE username = ? ORDER BY id DESC', (session['user'],)).fetchall()

    updated_posts = []
    for post in posts:
        post_id = post['id']
        like_count = db.execute('SELECT COUNT(*) FROM likes WHERE post_id = ?', (post_id,)).fetchone()[0]
        liked = db.execute('SELECT 1 FROM likes WHERE post_id = ? AND username = ?', (post_id, session['user'])).fetchone()
        updated_posts.append({**post, 'like_count': like_count, 'liked': bool(liked)})

    return render_template('profile.html', user=user, posts=updated_posts)

@app.route('/mypets')
def mypets():
    if 'user' not in session:
        return redirect(url_for('login'))

    db = get_db()
    pets = db.execute('SELECT * FROM mypets WHERE username = ?', (session['user'],)).fetchall()
    return render_template('mypets.html', pets=pets)

@app.route('/adoptions')
def adoptions():
    if 'user' not in session:
        return redirect(url_for('login'))

    db = get_db()
    adoptions = db.execute('SELECT * FROM adoptions ORDER BY id DESC').fetchall()
    return render_template('adoptions.html', adoptions=adoptions)

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if 'user' not in session:
        return redirect(url_for('login'))

    db = get_db()
    user = db.execute('SELECT * FROM users WHERE username = ?', (session['user'],)).fetchone()

    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        bio = request.form['bio']
        profile_pic = request.files.get('profile_pic')

        if profile_pic and profile_pic.filename != "":
            from werkzeug.utils import secure_filename
            import uuid, os
            filename = secure_filename(profile_pic.filename)
            unique_name = f"{uuid.uuid4().hex}_{filename}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_name)
            profile_pic.save(filepath)
            db.execute('''
                UPDATE users SET name = ?, phone = ?, email = ?, bio = ?, profile_pic = ? WHERE username = ?
            ''', (name, phone, email, bio, unique_name, session['user']))
        else:
            db.execute('''
                UPDATE users SET name = ?, phone = ?, email = ?, bio = ? WHERE username = ?
            ''', (name, phone, email, bio, session['user']))

        db.commit()
        flash("Settings updated.")
        return redirect(url_for('settings'))

    return render_template('settings.html', user=user)
@app.route('/feed')
def feed():
    if 'user' not in session:
        return redirect(url_for('login'))

    db = get_db()

    # Get current user info
    user = db.execute('SELECT * FROM users WHERE username = ?', (session['user'],)).fetchone()

    # Fetch posts
    posts = db.execute('SELECT * FROM posts ORDER BY id DESC').fetchall()

    # Fetch all usernames used in posts
    usernames = list(set(post['username'] for post in posts))
    user_rows = db.execute(f'''
        SELECT username, profile_pic FROM users WHERE username IN ({','.join(['?'] * len(usernames))})
    ''', usernames).fetchall()

    # Create mapping: username => user info
    users_map = {row['username']: {'profile_pic': row['profile_pic'], 'username': row['username']} for row in user_rows}

    # Add like info to each post
    updated_posts = []
    for post in posts:
        post_id = post['id']
        like_count = db.execute('SELECT COUNT(*) FROM likes WHERE post_id = ?', (post_id,)).fetchone()[0]
        liked = db.execute('SELECT 1 FROM likes WHERE post_id = ? AND username = ?', (post_id, session['user'])).fetchone()
        updated_posts.append({**post, 'like_count': like_count, 'liked': bool(liked)})

    # ✅ Fetch comments for all posts
    comments_by_post = {}
    for post in posts:
        post_id = post['id']
        comments = db.execute('''
            SELECT comments.comment_text, users.username
            FROM comments
            JOIN users ON comments.user_id = users.id
            WHERE comments.post_id = ?
            ORDER BY comments.timestamp ASC
        ''', (post_id,)).fetchall()
        comments_by_post[post_id] = comments

    return render_template(
        'feed.html',
        posts=updated_posts,
        user=user,
        users_map=users_map,
        comments_by_post=comments_by_post
    )


@app.route('/createpost', methods=['GET'])
def create_post_page():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('create-post.html')  # This is your form page

@app.route('/createpost', methods=['POST'])
def create_post():
    if 'user' not in session:
        return redirect(url_for('login'))

    caption = request.form['caption']
    media = request.files['media']

    unique_name = None
    if media:
        filename = secure_filename(media.filename)
        unique_name = f"{uuid.uuid4().hex}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_name)
        media.save(filepath)

    db = get_db()
    db.execute(
        'INSERT INTO posts (username, media, caption) VALUES (?, ?, ?)',
        (session['user'], unique_name, caption)
    )
    db.commit()
    flash('Post created!', 'post')
    return redirect(url_for('feed'))



@app.route('/add-mypet', methods=['GET', 'POST'])
def add_mypet():
    if 'user' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        photo = request.files['photo']
        pet_name = request.form['pet_name']
        breed = request.form['breed']
        age = request.form['age']
        birthday = request.form['birthday']
        vaccination = request.form['vaccination']
        deworming = request.form['deworming']
        vet = request.form['vet']

        if photo:
            filename = secure_filename(photo.filename)
            unique_name = f"{uuid.uuid4().hex}_{filename}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_name)
            photo.save(filepath)
        else:
            unique_name = None

        db = get_db()
        db.execute('''
            INSERT INTO mypets (username, photo, name, breed, age, birthday, vaccination, deworming, vet)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (session['user'], unique_name, pet_name, breed, age, birthday, vaccination, deworming, vet))
        db.commit()
        flash('Pet added successfully!')
        return redirect(url_for('mypets'))

    return render_template('add-mypet.html')

@app.route('/add-adoption', methods=['GET', 'POST'])
def add_adoption():
    if 'user' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        photo = request.files['photo']
        details = request.form['details']
        contact_name = request.form['contact_name']
        contact_number = request.form['contact_number']
        location = request.form['location']

        if photo:
            filename = secure_filename(photo.filename)
            unique_name = f"{uuid.uuid4().hex}_{filename}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_name)
            photo.save(filepath)
        else:
            unique_name = None

        db = get_db()
        db.execute('''
            INSERT INTO adoptions (username, photo, details, contact_name, contact_number, location)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (session['user'], unique_name, details, contact_name, contact_number, location))
        db.commit()
        flash('Pet listed for adoption successfully!')
        return redirect(url_for('adoptions'))

    return render_template('add-adoption.html')

@app.route('/delete_account', methods=['POST'])
def delete_account():
    if 'user' not in session:
        return redirect(url_for('login'))

    db = get_db()
    db.execute('DELETE FROM users WHERE username = ?', (session['user'],))
    db.execute('DELETE FROM posts WHERE username = ?', (session['user'],))
    db.execute('DELETE FROM mypets WHERE username = ?', (session['user'],))
    db.execute('DELETE FROM adoptions WHERE username = ?', (session['user'],))
    db.commit()

    session.clear()
    flash("Your account and all related data have been deleted.", 'account')
    return redirect(url_for('register'))

@app.route('/delete_post/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    if 'user' not in session:
        return redirect(url_for('login'))

    db = get_db()
    db.execute('DELETE FROM posts WHERE id = ? AND username = ?', (post_id, session['user']))
    db.commit()
    flash('Post deleted!', 'post')
    return redirect(url_for('feed'))

@app.route('/delete_pet/<int:pet_id>', methods=['POST'])
def delete_pet(pet_id):
    if 'user' not in session:
        return redirect(url_for('login'))

    db = get_db()
    db.execute('DELETE FROM mypets WHERE id = ? AND username = ?', (pet_id, session['user']))
    db.commit()
    flash("Pet deleted.", 'pet')
    return redirect(url_for('mypets'))

@app.route('/delete_adoption/<int:adoption_id>', methods=['POST'])
def delete_adoption(adoption_id):
    if 'user' not in session:
        return redirect(url_for('login'))

    db = get_db()
    db.execute('DELETE FROM adoptions WHERE id = ? AND username = ?', (adoption_id, session['user']))
    db.commit()
    flash("Adoption listing deleted.", 'adoption')
    return redirect(url_for('adoptions'))


@app.route('/like/<int:post_id>', methods=['POST'])
def like(post_id):
    if 'user' not in session:
        return redirect(url_for('login'))

    db = get_db()

    liked = db.execute(
        'SELECT 1 FROM likes WHERE post_id = ? AND username = ?', (post_id, session['user'])
    ).fetchone()

    if liked:
        db.execute('DELETE FROM likes WHERE post_id = ? AND username = ?', (post_id, session['user']))
    else:
        db.execute('INSERT OR IGNORE INTO likes (post_id, username) VALUES (?, ?)', (post_id, session['user']))
    
    db.commit()
    return redirect(request.referrer or url_for('feed'))

@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/comment', methods=['POST'])
def comment():
    if 'user' not in session:
        return redirect('/login')

    post_id = request.form['post_id']
    comment_text = request.form['comment_text']

    db = get_db()
    user_id = db.execute('SELECT id FROM users WHERE username = ?', (session['user'],)).fetchone()['id']

    db.execute("INSERT INTO comments (post_id, user_id, comment_text) VALUES (?, ?, ?)",
               (post_id, user_id, comment_text))
    db.commit()

    return redirect('/feed')

def get_db_connection():
    
    conn = sqlite3.connect('pawsitive.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/view_profile/<username>')
def view_profile(username):
    db = get_db()
    profile_user = db.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    posts = db.execute('SELECT * FROM posts WHERE username = ? ORDER BY id DESC', (username,)).fetchall()

    if not profile_user:
        flash('User not found.')
        return redirect(url_for('feed'))

    return render_template('view_profile.html', profile_user=profile_user, posts=posts)



if __name__ == '__main__':
    app.run(debug=True)
