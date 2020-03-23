# Website content extractor

Repository contains Django application with microservice getting URL from user with parameters to get text or 
images or both and saves it to database. Next periodically celery worker extracts given URL for those parameters and 
saves it in database. All tasks, saved images and saved texts are visible in REST API.

### Procedures

Firstly copy file with environ variables `.env_template` with new name `.env`. You can do it by command:
```bash
cp .env_template .env
```
Because of whole environment is containerized by Docker. You have to make sure that docker and docker-compose are installed.
To run pull all images, create database store directory and finally run all service run command:
```bash
docker-compose up -d
```

### Tasks
To add new task to extract texts or/and images go to webpage `localhost:8000` and add some URL and click "Extract".

All tasks are visible on `localhost:8000/api/tasks/` which can be filtering and ordering. For example if you want to see
only completed tasks add parameter `?state=success`.

### Images extractor
All completed tasks which extract images are visible on `localhost:8000/api/images/` where you can download image clicking
on path value of `image` key.

### Texts extractor
All completed tasks which extract texts are visible on `localhost:8000/api/texts/`. Texts are saved in database in json
list, because this type of structure should be more helpful for ML developers than joined one huge string.


#### Comment from author
Co poszło ok:
  1. Ponieważ Postgres bardzo długo się uruchamia, już po wystartowaniu kontenera, po raz pierwszy zaczął mi nie 
  wystarczać 'dockerowy' atrybut usługi `depends_on`, przez co zacząłem szukać metody opóźnienia startu pozostałych usług. 
  W ten sposób znalazłem skrypt na w dokumentacji dockera `wait_for_it.sh`. Prosty kawałek kodu, a z pewnością nie raz 
  z niego w przyszłości skorzystam. 

Co poszło nie tak:
  1. Przede wszystkim mogłem zrobić więcej testów modeli, widoków oraz samych funkcji do ektrakcji zawartości stron.
  Ze względu na czas i na to, że korzystałem z generycznych komponentów Django, zrobiłem testy tylko najbardziej krytycznych
  elementów i z całą pewnością zrobiłem ich za mało.

Do zmiany:
  1. Dodanie testów modeli, widoków, formularza oraz funkcji z katalogu `utils/` oraz zmiana struktury plików, tak żeby
  wszystkie powyżej testy znajdowały się w osobnych plikach w nieutworzonym katalogu `tests/`.
  1. Wygodne w przeglądaniu API byłoby bezpośrednie przechodzenie z widoku listy tasków/obrazów/tekstów do widoku 
  szczegółowego danego tasku, obrazu czy tekstu
  1. Jako użytkownik takiego API chciałbym mieć również jakieś parametry, jak na przykład wymiary, oraz sam podgląd pobranego
  zdjęcia
  1. Jako użytkownik chciałbym mieć również widoczne tagi HTML do wszystkich pobranych tekstów, pomogłoby to odsiać często
  mniej potrzebną zawartość, jak na przykład tytuły
  1. Wszystkie teksty teraz zapisuję do listy. W przypadku gdy w jednym artykule mamy link, to zapis wygląda następująco:
  [pierwsza_część_tekstu, słowo_wcześniej_zawierające_hiperłącze, druga_część_tekstu]
  Jako, że to jeden artykuł, to moim zdaniem powinno to być jako jeden element w liście, a nie trzy. 
 