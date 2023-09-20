from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, redirect, url_for, request, flash, session, jsonify
from backend.db import db
from backend.auth import authapp, login_required

app = Flask(__name__, static_folder='static', static_url_path='/static')
app = Flask(__name__, static_folder='static', static_url_path='')
app.secret_key = 'GOOD_SECRET_KEY'

app.register_blueprint(authapp)

# demo5
# 333


@app.route('/', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')


@app.route('/jurusan', methods=['GET', 'POST'])
@login_required
def jurusan():
    if request.method == 'POST':
        dataMajor = {
            'major': request.form['jurusan']
        }
        data = db.collection('jurusan').document(
            dataMajor['major']).get().to_dict()
        if data is None:
            db.collection('jurusan').document(
                dataMajor['major']).set(dataMajor)
            flash('Anda telah berhasil Menambahkan Jurusan', 'primary')
            return redirect(url_for('jurusan'))
        flash('Jurusan yang anda masukkan sudah ada', 'warning')
    docs = db.collection('jurusan').get()
    majors = []
    for doc in docs:
        majors.append(doc.to_dict())
    return render_template('jurusan.html', majors=majors)


@app.route('/jurusan/hapus/<uid>')
@login_required
def jurusanHapus(uid):
    data = db.collection('jurusan').document(uid).delete()
    return redirect(url_for('jurusan'))


@app.route('/mahasiswa', methods=['GET', 'POST'])
@login_required
def mahasiswa():
    if request.method == 'POST':
        dataStudent = {
            'name': request.form['mahasiswa'],
            'email': request.form['email'],
            'phone': request.form['phone'],
            'major': request.form['jurusan']
        }
        db.collection('mahasiswa').document().set(dataStudent)
        flash('Anda telah berhasil Menambahkan Data', 'primary')
        return redirect(url_for('mahasiswa'))
    docs = db.collection('mahasiswa').get()
    students = []
    for doc in docs:
        siswa = doc.to_dict()
        siswa['id'] = doc.id
        students.append(siswa)
    return render_template('mahasiswa/mahasiswa.html', students=students)


@app.route('/mahasiswa/lihat/<uid>')
@login_required
def mahasiswaLihat(uid):
    dataStudent = db.collection('mahasiswa').document(uid).get().to_dict()
    return render_template('mahasiswa/lihat.html', dataStudent=dataStudent)


@app.route('/mahasiswa/edit/<uid>', methods=['GET', 'POST'])
@login_required
def mahasiswaEdit(uid):
    if request.method == 'POST':
        dataStudent = {
            'name': request.form['mahasiswa'],
            'email': request.form['email'],
            'phone': request.form['phone'],
            'major': request.form['jurusan']
        }
        db.collection('mahasiswa').document(uid).set(dataStudent, merge=True)
        print('berhasil')
        flash('Anda Berhasil Mengedit Data', 'primary')
        return redirect(url_for('mahasiswa'))
    students = db.collection('mahasiswa').document(uid).get().to_dict()
    print('gagal')
    return render_template('mahasiswa/edit.html', students=students)


@app.route('/mahasiswa/hapus/<uid>')
@login_required
def mahasiswaHapus(uid):
    dataStudent = db.collection('mahasiswa').document(uid).delete()
    flash('Anda Berhasil Menghapus Data', 'primary')
    return redirect(url_for('mahasiswa'))


@app.route('/user', methods=['GET', 'POST'])
@login_required
def user():
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
                return redirect(url_for('user'))
            flash('Username yang anda masukkan sudah ada', 'warning')
            return redirect(url_for('user'))
        flash('Password dan Konfirmasi Password tidak cocok', 'danger')
    docs = db.collection('user').get()
    users = []
    for doc in docs:
        person = doc.to_dict()
        person['id'] = doc.id
        users.append(person)
    # return users
    return render_template('user/user.html', users=users)


@app.route('/user/lihat/<uid>')
@login_required
def userLihat(uid):
    dataUser = db.collection('user').document(uid).get().to_dict()
    return render_template('user/lihat.html', dataUser=dataUser)


@app.route('/user/edit/<uid>', methods=['GET', 'POST'])
@login_required
def userEdit(uid):
    if request.method == 'POST':
        dataUser = {
            'full_name': request.form['nama_lengkap'],
            'username': request.form['username']
        }
        db.collection('user').document(uid).set(dataUser, merge=True)
        flash('Anda Berhasil Mengedit Data', 'primary')
        return redirect(url_for('user'))
    dataUser = db.collection('user').document(uid).get().to_dict()
    return render_template('user/edit.html', dataUser=dataUser)


@app.route('/user/hapus/<uid>')
@login_required
def userHapus(uid):
    dataUser = db.collection('user').document(uid).delete()
    return redirect(url_for('user'))


if __name__ == '__main__':
    app.run(debug=True)
