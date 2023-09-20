from functools import wraps
from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from backend.db import db, storage
from werkzeug.security import generate_password_hash, check_password_hash

authapp = Blueprint('authapp', __name__)


# ini adalah fungsi untuk melakukan pengecekan apakah session ada atau tidak
def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'user' in session:
            return f(*args, **kwargs)
        else:
            flash('Anda harus login', 'danger')
            return redirect(url_for('authapp.login'))
    return wrapper


@authapp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        dataUser = {
            'username': request.form['username'],
            'password': request.form['password']
        }
        data = db.collection('user').document(
            dataUser['username']).get().to_dict()
        if data is not None:
            if check_password_hash(data['password'], dataUser['password']):
                session['user'] = data
                return redirect(url_for('dashboard'))
        flash(
            'Akun anda tidak dapat ditemukan, silahkan register terlebih dahulu', 'danger')
        return redirect(url_for('authapp.login'))
    if session.get('user') is not None:
        return redirect(url_for('dashboard'))
    return render_template('login.html')


@authapp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if request.form['password'] == request.form['password-confirm']:
            dataUser = {
                'full_name': request.form['full-name'],
                'username': request.form['username'],
                'password': request.form['password']
            }
            data = db.collection('user').document(
                dataUser['username']).get().to_dict()
            if data is None:
                dataUser['password'] = generate_password_hash(
                    request.form['password'], 'sha256')
                db.collection('user').document(
                    dataUser['username']).set(dataUser)
                flash('Anda telah berhasil Membuat Akun', 'primary')
                return redirect(url_for('authapp.login'))
            flash('Username yang anda masukkan sudah ada', 'warning')
            return redirect(url_for('authapp.register'))
        flash('Password dan Konfirmasi Password tidak cocok', 'danger')
    if session.get('user') is not None:
        return redirect(url_for('dashboard'))
    return render_template('register.html')


@authapp.route('/password', methods=['GET', 'POST'])
@login_required
def changePass():
    if request.method == 'POST':
        if request.form['password'] != request.form['validatePass']:
            flash('Password dan Konfirmasi Password tidak cocok', 'danger')
            return redirect(url_for('authapp.changePass'))
        data = db.collection('user').document(
            session['user']['username']).get().to_dict()

        if check_password_hash(data['password'], request.form['currentPass']):
            newPass = generate_password_hash(
                request.form['password'], 'sha256')
            db.collection('user').document(data['username']).update(
                {'password': newPass})
            return redirect(url_for('dashboard'))
        else:
            flash('Password yang anda masukkan salah', 'danger')
            return redirect(url_for('authapp.changePass'))
    return render_template('change-pass.html')


@authapp.route('/profileImage', methods=['GET', 'POST'])
def profileImage():
    data = session['user']
    if request.method == 'POST':
        # pengecekan apakah gambar ada atau tidak
        if 'gambar' in request.files and request.files['gambar']:
            # simpan dalam veriable image
            image = request.files['gambar']
            # buat syarat ekstension file
            ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
            # simpan nama file
            filename = image.filename
            # buat lokasi penympanan di storage
            lokasi = f'user/{filename}'

            # ini memisahkan nama file dengan ekstension
            ext = filename.rsplit('.', 1)[1].lower()
            # cek ekstension file
            if ext in ALLOWED_EXTENSIONS:
                storage.child(lokasi).put(image)
                data['gambar'] = storage.child(lokasi).get_url(None)
            else:
                flash("Gambar tidak diperbolehkan", "danger")
                return redirect(url_for('profileImage'))

        db.collection('user').document(data['username']).set(data)
        session['user'] = data

        return redirect(url_for('dashboard'))

    # 1. tampilkan foto profil sekarang berdasarkan data gambar pada session['user'] (jika baru pertama kali login, maka gambar secara otomatis adalah default image)
    # 2. input data gambarnya dengan membatasi bentuk dan ekstensi filenya pada setingan form
    # 3. lakukan pengecekan pada data gambar, jika TRUE maka set (data)
    return render_template('change-profileImage.html')


@authapp.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('authapp.login'))
