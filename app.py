from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os

app = Flask(__name__, static_folder='assets')
app.secret_key = "gizli_anahtar"

DATA_FILE = "data/cv_kayitlari.json"
programlama_dilleri_listesi = [
    "HTML", "CSS", "JavaScript", "TypeScript", "React", "Vue.js", "Python", "C++",
    "Java", "C#", "PHP", "Ruby"
]
@app.route("/")
def form():
    return render_template("form.html", diller=programlama_dilleri_listesi)
@app.route("/basvuru", methods=["POST"])
def basvuru():
    ad = request.form.get("ad")
    eposta = request.form.get("eposta")
    telefon = request.form.get("telefon")
    mezuniyet = request.form.get("mezuniyet")
    deneyim = request.form.get("deneyim")
    onyazi = request.form.get("onyazi")
    programlama_dilleri = request.form.getlist("programlama_dilleri")
    yabanci_dil = request.form.get("yabanci_dil")
    pozisyon = request.form.get("pozisyon")

    
    if not (ad and eposta and telefon and mezuniyet and deneyim and pozisyon and onyazi):
        flash("Lütfen tüm zorunlu alanları doldurun!")
        return redirect(url_for("form"))

    try:
        deneyim = int(deneyim)
    except ValueError:
        flash("Deneyim yılı sayı olmalıdır!")
        return redirect(url_for("form"))

    
    yabanci_diller = [yabanci_dil]

    cv = {
        "ad": ad,
        "eposta": eposta,
        "telefon": telefon,
        "mezuniyet": mezuniyet,
        "deneyim_yili": deneyim,
        "onyazi": onyazi,
        "programlama_dilleri": programlama_dilleri,
        "yabanci_diller": yabanci_diller,
        "pozisyon_tercihi": pozisyon
    }

    os.makedirs("data", exist_ok=True)
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=2)

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        kayitlar = json.load(f)

    kayitlar.append(cv)

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(kayitlar, f, ensure_ascii=False, indent=2)

    flash("Başvurunuz Alınmıştır!", "success")
    return redirect(url_for("form"))

if __name__ == "__main__":
    app.run(debug=True)
