import yfinance as yt

skrot = "AAPL"
try:
    spolka = yt.Ticker(skrot)
    notowania = spolka.history(period="max")
    print(notowania)
except Exception:
    print(f"Nie udało się pobrać danych dla spółki: {skrot} !!!")

print(f"noto {notowania}")
