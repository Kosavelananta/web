from flask import Flask, request, url_for, redirect
from flask import render_template
from mysql import connector

app = Flask(__name__)
db = connector.connect(
    host = "localhost",
    user = "root",
    passwd = "",
    database = "pempek"
)

if db.is_connected():
    print('====Connected====')

@app.route('/')
@app.route('/home')
def home():
    cur = db.cursor()
    cur.execute('select harga_pempek, harga from aneka_pempek, minuman '
                'where aneka_pempek.id_pempek="KLT" and minuman.id_minuman="SJR"')
    harga = cur.fetchone()

    cur.execute("select * from minuman")
    minuman = cur.fetchall()

    cur.execute("select * from aneka_pempek")
    pempek = cur.fetchall()

    cur.close()
    return render_template("erere.html", minuman=minuman, pempek=pempek, harga=harga)


@app.route('/order', methods=['POST'])
def order():
    nama_pemesan = request.form['nama_pemesan']
    pempek_id = request.form['pempek_id']
    minuman_id = request.form['minuman_id']

    cur = db.cursor()
    cur.execute('select harga_pempek, harga from aneka_pempek, minuman '
                'where aneka_pempek.id_pempek=%s and minuman.id_minuman=%s', (pempek_id, minuman_id))
    harga = cur.fetchone()
    total_harga = int(harga[0]) + int(harga[1])
    cur.close()

    cur = db.cursor()
    cur.execute("INSERT INTO `order` (`no_order`, `nama_pemesan`, `pempek_id`, `minuman_id`, `total_harga`) VALUES (NULL, %s, %s, %s, %s);",
                (nama_pemesan, pempek_id, minuman_id, str(total_harga)))
    db.commit()
    return redirect(url_for('home'))

if __name__== '__main__':
    app.run(debug=True)