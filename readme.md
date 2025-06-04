# Finance Manager

**Finance Manager** to desktopowa aplikacja napisana w Pythonie z wykorzystaniem frameworka PyQt6 oraz bazy SQLite, której głównym zadaniem jest wsparcie w zarządzaniu finansami osobistymi lub domowymi.

## Spis treści

1. [Opis](#opis)  
2. [Funkcje](#funkcje)  
3. [Instalacja](#instalacja)  
4. [Użycie](#użycie)  
5. [Struktura zakładek](#struktura-zakładek)  
6. [Kontrybucja](#kontrybucja)  
7. [Licencja](#licencja)  

## Opis

Finance Manager umożliwia użytkownikowi:

- Zarządzanie kontami finansowymi  
- Prowadzenie rejestru przychodów i wydatków  
- Planowanie nadchodzących transakcji  
- Ustalanie budżetów na poszczególne kategorie wydatków  
- Przegląd historii transakcji z możliwością filtrowania  
- Import i eksport danych do plików PDF oraz XLS  
- Opcjonalne zabezpieczenie dostępu do aplikacji hasłem  

## Funkcje

- **Zarządzanie kontami**: Tworzenie, edycja i usuwanie kont bankowych/oszczędnościowych, wraz z bieżącą aktualizacją sald w oparciu o wykonywane transakcje.  
- **Rejestr transakcji**: Dodawanie, edycja i usuwanie przychodów oraz wydatków. Spójność salda kont jest zachowywana automatycznie. Przy przekroczeniu budżetu dla danej kategorii wyświetlane jest ostrzeżenie.  
- **Planowanie transakcji**: Kalendarz z podświetlonymi dniami, w których zaplanowano przynajmniej jedną pozycję. Użytkownik może zarządzać (CRUD) planowanymi transakcjami, a także przeglądać listę pozycji przypisanych do wybranej daty.  
- **Budżetowanie**: Definiowanie limitów wydatków dla poszczególnych kategorii na określony miesiąc i rok. System automatycznie sprawdza, czy bieżące wydatki nie przekraczają ustalonych limitów.  
- **Historia transakcji**: Zaawansowane filtry (zakres dat, kategorie, fragment opisu) pozwalają na szybkie wyszukiwanie oraz przeglądanie archiwalnych transakcji.  
- **Przelicznik walut**: Prosty interfejs umożliwiający wybór waluty źródłowej i docelowej oraz pobieranie aktualnych kursów walut z API Narodowego Banku Polskiego (NBP).  
- **Import/Eksport**: Eksport wszystkich danych (kont i transakcji) do plików PDF lub XLS oraz możliwość importu z wcześniej wygenerowanych raportów.  
- **Zabezpieczenie hasłem**: Opcjonalne ustawienie hasła blokującego dostęp do aplikacji.  

