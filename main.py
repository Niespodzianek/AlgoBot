import yfinance as yt
import pandas as pd
import os

def zapis_surowych_danych(tiker: str, notowania: pd.DataFrame, verbose=True) -> bool:
    sciezka: str = f"{tiker}_raw.csv"
    if verbose:
        os.system("clear")
        print("Rozpoczynam zapis surowych notowań do pliku...")
        input("Naciśnij ENTER aby kontynuować...")
    notowania.to_csv(sciezka)
    return True

def zapis_poprawionych_danych(tiker: str, notowania: pd.DataFrame, verbose=True) -> bool:
    sciezka: str = f"{tiker}_clean.csv"
    if verbose:
        os.system("clear")
        print("Rozpoczynam zapis poprawionych notowań do pliku...")
        input("Naciśnij ENTER aby kontynuować...")
    notowania.to_csv(sciezka)
    return True

def poprawa_danych(tiker: str, notowania: pd.DataFrame, verbose=True) -> (bool, pd.DataFrame):
    if verbose:
        os.system("clear")
        print("Rozpoczynam poprawę danych...")
        input("Naciśnij ENTER aby kontynuować...")
    notowania["Data"] = notowania.index
    notowania = notowania[["Open", "High", "Low", "Close", "Volume"]]
    notowania.columns = ["Otwarcie", "Najwyzszy", "Najnizszy", "Zamkniecie", "Wolumen"]
    if verbose:
        os.system("clear")
        print("Oto skorygowany fragment notowań")
        print(notowania.head())
        input("Naciśnij ENTER aby kontynuować...")
    return True, notowania

def pobranie_surowych_danych(tiker: str, verbose) -> (bool, pd.DataFrame):
    if verbose:
        os.system("clear")
        print("Rozpoczynam pobieranie danych z serwera Yahoo Finance...")
        input("Naciśnij ENTER aby kontynuować...")
    try:
        spolka = yt.Ticker(tiker)
        notowania: pd.DataFrame = spolka.history(period="max")
        if len(notowania) > 0:
            if verbose:
                os.system("clear")
                print("Pobrano dane z serwera Yahoo Finance.")
                print(notowania)
                input("Naciśnij ENTER aby kontynuować...")
            return True, notowania
        elif notowania.empty and verbose:
            os.system("clear")
            print("Nie udało się pobrać danych z serwera Yahoo Finance. Sprawdź poprawność wpisanego tikera !!!")
            input("Naciśnij ENTER aby kontynuować...")
            return False, None
    except Exception:
        os.system("clear")
        print(f"Nie udało się pobrać danych dla spółki: {tiker} z powodu braku połączenia z serwerem !!!")
        return False, None

def main(verbose=True) -> None:
    status: bool = False
    notowania: pd.DataFrame
    tiker: str = input("Podaj tiker spółki: ").upper()
    status, surowe_notowania = pobranie_surowych_danych(tiker=tiker, verbose=verbose)
    if status and verbose:
        os.system("clear")
        print("Dane zostały pobrane poprawnie.")
        print(surowe_notowania)
        input("Naciśnij ENTER aby kontynuować...")
    status = zapis_surowych_danych(tiker=tiker, notowania=surowe_notowania, verbose=verbose)
    if status and verbose:
        os.system("clear")
        print("Dane zostały zapisane poprawnie.")
        input("Naciśnij ENTER aby kontynuować...")
    status, poprawione_notowania = poprawa_danych(tiker=tiker, notowania=surowe_notowania, verbose=verbose)
    if status and verbose:
        os.system("clear")
        print("Dane zostały poprawione poprawnie.")
        print(poprawione_notowania)
        input("Naciśnij ENTER aby kontynuować...")
    status = zapis_poprawionych_danych(tiker=tiker, notowania=poprawione_notowania, verbose=verbose)
    if status and verbose:
        os.system("clear")
        print("Dane skorygowane zostały zapisane poprawnie.")
        print(poprawione_notowania)
        input("Naciśnij ENTER aby kontynuować...")
    return None
    
if __name__ == "__main__":
    os.system("clear")
    print("Witaj w programie do analizy danych giełdowych!")
    input("Naciśnij ENTER aby kontynuować...")
    main(verbose=False)
    os.system("clear")
    print("Dziękuję za skorzystanie z programu!\nDo zobaczenia !!!")
    input("Naciśnij ENTER aby zakończyć...")
    exit(0)
