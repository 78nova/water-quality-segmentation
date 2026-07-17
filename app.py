from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# =========================
# LOAD DATA
# =========================

df = pd.read_excel("data/hasil_cluster_kmedoids_2025.xlsx")
df_medoid = pd.read_excel("data/medoid_cluster_2025.xlsx")

# =========================
# KETERANGAN CLUSTER
# =========================

keterangan_cluster = {
    0: {
        "karakteristik": "Dominan TSS dan Sulfat",
        "interpretasi": "Cluster ini memiliki rata-rata TSS dan Sulfat tertinggi dibandingkan cluster lainnya sehingga lokasi-lokasi pada cluster ini mempunyai karakteristik yang serupa berdasarkan kedua parameter tersebut."
    },

    1: {
        "karakteristik": "Parameter relatif seimbang",
        "interpretasi": "Seluruh parameter memiliki nilai rata-rata yang relatif sedang tanpa parameter yang paling menonjol."
    },

    2: {
        "karakteristik": "Dominan TDS, Klorida, dan Sulfat relatif lebih rendah",
        "interpretasi": "Cluster ini memiliki nilai rata-rata TDS, Klorida, dan Sulfat yang relatif lebih rendah dibandingkan beberapa cluster lainnya."
    },

    3: {
        "karakteristik": "Dominan TDS dan Klorida",
        "interpretasi": "Cluster ini memiliki rata-rata TDS dan Klorida tertinggi dibandingkan cluster lainnya."
    },

    4: {
        "karakteristik": "Parameter relatif paling rendah",
        "interpretasi": "Cluster ini memiliki rata-rata TSS, TDS, Klorida, dan Sulfat paling rendah dibandingkan cluster lainnya."
    }
}
# =========================
# DASHBOARD
# =========================

@app.route("/")
def dashboard():

    jumlah_lokasi = len(df)
    jumlah_cluster = df["Cluster"].nunique()

    daftar_lokasi = sorted(
        df["LOKASI"].unique()
    )

    lokasi_pilih = request.args.get("lokasi")

    hasil = None

    if lokasi_pilih:

        data_lokasi = df[
            df["LOKASI"] == lokasi_pilih
        ]

        if not data_lokasi.empty:

            hasil = data_lokasi.iloc[0].to_dict()

            cluster = hasil["Cluster"]

            hasil["karakteristik"] = keterangan_cluster[cluster]["karakteristik"]
            hasil["interpretasi"] = keterangan_cluster[cluster]["interpretasi"]

    return render_template(
        "dashboard.html",
        jumlah_lokasi=jumlah_lokasi,
        jumlah_cluster=jumlah_cluster,
        daftar_lokasi=daftar_lokasi,
        hasil=hasil
    )

# =========================
# DATA
# =========================

@app.route("/data")
def data():

    tabel = df.to_dict(
        orient="records"
    )

    return render_template(
        "data.html",
        data=tabel
    )

# =========================
# HASIL
# =========================

@app.route("/hasil")
def hasil():

    tabel = df.to_dict(
        orient="records"
    )

    return render_template(
        "hasil.html",
        data=tabel
    )

# =========================
# VISUALISASI
# =========================

@app.route("/visualisasi")
def visualisasi():

    return render_template(
        "visualisasi.html"
    )

# =========================
# MEDOID
# =========================

@app.route("/medoid")
def medoid():

    tabel_medoid = df_medoid.to_dict(
        orient="records"
    )

    return render_template(
        "medoid.html",
        data=tabel_medoid
    )

# =========================

if __name__ == "__main__":
    app.run(debug=True)