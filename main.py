import os, sys
import yfinance as yt
import pandas as pd

APP_NAME: str = "AlgoBot"
VERSION: str = "0.0.1"
DEBUG: bool = "--debug" in sys.argv
INFO: bool = "--info" in sys.argv
symbol: str = ""

def debug_print(tekst: str) -> None:
    if DEBUG:
        input(f"\nDEBUG: {tekst} Naciśnij ENTER aby kontynuować !!!")
    return None

def info_print(tekst: str):
    if INFO:
        input(f"\nINFO: {tekst} Naciśnij ENTER aby kontynuować !!!")
    return None

def zapis_surowych_danych(tiker: str, notowania: pd.DataFrame) -> bool:
    sciezka: str = f"{tiker}_raw.csv"
    if verbose:
        os.system("clear")
        print("Rozpoczynam zapis surowych notowań do pliku...")
        input("Naciśnij ENTER aby kontynuować...")
    notowania.to_csv(sciezka)
    return True

def zapis_poprawionych_danych(tiker: str, notowania: pd.DataFrame) -> bool:
    sciezka: str = f"{tiker}_clean.csv"
    if verbose:
        os.system("clear")
        print("Rozpoczynam zapis poprawionych notowań do pliku...")
        input("Naciśnij ENTER aby kontynuować...")
    notowania.to_csv(sciezka)
    return True

def poprawa_danych(tiker: str, notowania: pd.DataFrame) -> (bool, pd.DataFrame):
    notowania["Data"] = notowania.index
    notowania = notowania[["Open", "High", "Low", "Close", "Volume"]]
    notowania.columns = ["Otwarcie", "Najwyzszy", "Najnizszy", "Zamkniecie", "Wolumen"]
    return True, notowania

def pobranie_surowych_danych(tiker: str) -> (bool, pd.DataFrame):
    try:
        spolka = yt.Ticker(tiker)
        notowania: pd.DataFrame = spolka.history(period="max")
        if len(notowania) > 0:
            return True, notowania
        elif notowania.empty:
            return False, None
    except Exception:
        os.system("clear")
        print(f"Nie udało się pobrać danych dla spółki: {tiker} z powodu braku połączenia z serwerem !!!")
        return False, None

def main(tiker: str) -> None:
    status: bool = False
    notowania: pd.DataFrame
    print(f"Rozpoczynam sprawdzanie spółki:{tiker}.")
    # todo sprawdzenie czy spółka jest już w bazie pobranych notowań
    # todo jeżeli jest to rozpoczynamy analizę
    # todo jeżeli nie ma to pobieram surowe dane
    # status, surowe_notowania = pobranie_surowych_danych(tiker=tiker)
    # status = zapis_surowych_danych(tiker=tiker, notowania=surowe_notowania)
    # status, poprawione_notowania = poprawa_danych(tiker=tiker, notowania=surowe_notowania)
    # status = zapis_poprawionych_danych(tiker=tiker, notowania=poprawione_notowania)
    return None
    
if __name__ == "__main__":
    os.system("cls" if os.name == "nt" else "clear")
    if "--help" in sys.argv:
        print(f"""
        Pomoc dla programu {APP_NAME}:
        
        Funkcje programu:
        Pobieranie danych i notowań wybranej spółki z serwisu Yahoo Finance a następnie analiza pobranych danych.
            
        Użycie programu w CLI:
            python3 main.py
            python3 main.py --flaga
        
        rodzaje flag:
            --help - pomoc,
            --version - wypisuje wersję programu,
            --history - historia wersji,
            --debug - uruchamia program w trybie debug,
            --info - uruchamia program w trybie z komentarzami,
            --ticker symbol - uruchamia program analizując spółkę, której symbol, zgodnie z nomenklaturą Yahoo Finance,
                został wpisany.
        """)
        sys.exit()
    if "--version" in sys.argv:
        print(f"Program {APP_NAME}, wersja: {VERSION}")
        sys.exit()
    if "--history" in sys.argv:
        print(f"""
        Historia dotychczasowych wersji programu {APP_NAME}. Aktualna wersja ma numer: {VERSION}:
         
        0.0.2.
        Pobieranie danych i notowań spółki z serwisu Yahoo Finance.
        
        0.0.1.
        Obsługa flag.
        
        0.0.0.
        Rozpoczęcie pracy nad programem.
        """)
        sys.exit()
    if "--info" and "--debug" in sys.argv:
        INFO = True
        DEBUG = True
    if "--info" in sys.argv:
        DEBUG = False
    if "--debug" in sys.argv:
        INFO = True
    if "--ticker" in sys.argv:
        index = sys.argv.index("--ticker")
        try:
            if sys.argv[index + 1].startswith("--"):
                print(f"Uwaga błąd. W miejsce symbolu spółki wpisano flagę {sys.argv[index + 1]}")
                sys.exit(1)
            elif index + 1 < len(sys.argv):
                symbol = sys.argv[index + 1].upper()
                debug_print(f"Przy uruchamianiu programu, ustalono symbol analizowanej spółki na: {symbol}.")
            else:
                print("Uwaga błąd. Użyto flagi --ticker, ale zapomniano wpisać symbol spółki !!!")
                sys.exit(1)
        except IndexError as error:
            debug_print(f"Wystąpił błąd związany z wyjątkiem {error}, ale to nie ma znaczenia.")
            print("Uwaga błąd. Użyto flagi --ticker, ale zapomniano wpisać symbol spółki !!!")
            sys.exit(1)
    info_print("Witaj w programie do analizy danych giełdowych!")
    main(tiker=symbol)
    info_print("Do zobaczenia !!!")
    exit(0)
