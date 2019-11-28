# Python and Neo4j project
  Example project utilizing Neo4j database in software, that is supposed to manage drone cargo around districts of Poznań City.
  App was written in a haste and I had much less skills in Python.
  Take it as an example app, not as a model.
  
  Currently code is total mess and fubar, but somehow works.
  You'll require Neo4j database installed on your machine.
  Name it 'Graph', and fill-in passwords in code variable 'driver'.


# Original requirements (PL)
-- python_neo4j_projekt

Dodać do API:
- parametryzacja
- dodawanie i usuwanie danych z bazy
- traversal framework
- zapis danych do obiektu, pliku

Sprawozdanie:
Implementacja: schemat jako typy węzłów, atrybuty i połączenia

-- oryginał wymagań:

Projekt
• Wersja 1-osobowa
– Baza danych – skrypt tworzący struktury + dane
– Interfejs dostępu bazy danych – 5-10 funkcji/metod,
które
  • mają mieć określoną funkcjonalność (np. logowanie
    użytkownika, rejestracja użytkownika, wydobycie określonej
    informacji, dodanie nowej informacji)
  • mogą być napisane w dowolnym podstawowym API dla danej
    bazy danych np. node.js
  • nie wykorzystują mapowania np. obiektowo-dokumentowego
  • korzystające ze specyficznych własności bazy danych
