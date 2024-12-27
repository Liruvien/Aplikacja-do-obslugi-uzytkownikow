# Warsztat – Aplikacja do obsługi użytkowników

## Opis

Aplikacja konsolowa do obsługi użytkowników, przyjmująca argumenty wprowadzone przez użytkownika. Obsługa argumentów jest realizowana za pomocą biblioteki argparse.

## Funkcjonalności

Aplikacja umożliwia wykonywanie następujących operacji na użytkownikach:

- Tworzenie użytkowników
- Edycja haseł użytkowników
- Usuwanie użytkowników
- Listowanie wszystkich użytkowników

## Instalacja

1. **Sklonuj repozytorium:**

   ```bash
   git clone https://github.com/TwojeRepozytorium.git
   cd TwojeRepozytorium

## Uruchomienie aplikacji

Aplikację można uruchomić z poziomu terminala, używając polecenia:

```bash
python app.py
```

## Parametry

Aplikacja obsługuje następujące parametry:

- `-u`, `--username` – nazwa użytkownika.
- `-p`, `--password` – hasło użytkownika.
- `-n`, `--new_pass` – nowe hasło (min. 8 znaków).
- `-l`, `--list` – listowanie wszystkich użytkowników.
- `-d`, `--delete` – usuwanie użytkownika.
- `-e`, `--edit` – edycja użytkownika.

## Scenariusze obsługi

### Tworzenie użytkownika

Jeśli podczas wywołania aplikacji podane zostaną tylko parametry `username` i `password`:

1. Sprawdź, czy użytkownik o podanej nazwie istnieje.
   - Jeśli tak – zgłoś błąd (`UniqueViolation`).
   - Jeśli nie:
     - Jeśli hasło ma co najmniej 8 znaków, utwórz użytkownika i zapisz go do bazy danych.
     - Jeśli hasło jest za krótkie, wyświetl odpowiedni komunikat.

### Edycja hasła użytkownika

Jeśli podczas wywołania aplikacji podane zostaną parametry:

- `username`
- `password`
- `--edit`
- `new_pass`

Wykonaj następujące kroki:

1. Sprawdź, czy użytkownik istnieje.
2. Sprawdź, czy hasło jest poprawne:
   - Jeśli tak, sprawdź długość nowego hasła (`new_pass`):
     - Jeśli hasło jest krótsze niż 8 znaków, wyświetl komunikat.
     - Jeśli hasło jest odpowiedniej długości, ustaw nowe hasło.
   - Jeśli hasło jest niepoprawne, wyświetl komunikat o błędzie.

> **Podpowiedź:** Do sprawdzenia poprawności hasła można wykorzystać funkcję `check_password` z biblioteki `clcrypto`.

### Usuwanie użytkownika

Jeśli podczas wywołania aplikacji podane zostaną parametry:

- `username`
- `password`
- `--delete`

Wykonaj następujące kroki:

1. Sprawdź poprawność hasła:
   - Jeśli jest poprawne, usuń użytkownika z bazy danych.
   - Jeśli jest niepoprawne, wyświetl komunikat: **"Incorrect Password!"**

### Listowanie użytkowników

Jeśli podczas wywołania aplikacji podany zostanie parametr `-l` (`--list`):

1. Wypisz listę wszystkich użytkowników.

### Pomoc

Jeśli podany zostanie inny zestaw parametrów, wyświetl panel pomocy. Panel pomocy można wywołać za pomocą metody `print_help` obiektu parsera.

#### Przykład:

```python
import argparse

parser = argparse.ArgumentParser()
parser.print_help()
```