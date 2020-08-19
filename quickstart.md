### Quickstart für schulReddit

Zunächst solltet ihr ein virtual environment für das Projekt anlegen.
Einen kurzen Screenshot, wie das funktionieren kann, habe ich schon in
den Discord-Channel gepostet.

Dann starten wir ein neues Projekt:

    django-admin startproject tutorial

Danach sollte die directory structure so aussehen:

    .
    ├── manage.py
    └── tutorial
        ├── asgi.py
        ├── \__init__.py
        ├── settings.py
        ├── urls.py
        └── wsgi.py

*Der Punkt steht dabei für das current working directory, also in diesem Fall auch "tutorial"*

Dann erstellen wir eine Application:

    python manage.py startapp bulletinBoard

    .
    ├── bulletinBoard
    │   ├── admin.py
    │   ├── apps.py
    │   ├── __init__.py
    │   ├── migrations
    │   │   └── __init__.py
    │   ├── models.py
    │   ├── tests.py
    │   └── views.py
    ├── manage.py
    └── tutorial
        ├── asgi.py
        ├── __init__.py
        ├── __pycache__
        │   ├── __init__.cpython-38.pyc
        │   └── settings.cpython-38.pyc
        ├── settings.py
        ├── urls.py
        └── wsgi.py

Jetzt sieht die directory structure schon anders aus.
Die App bulletinBoard kommt hinzu und ist der Dreh- und
Angelpunkt unserer Website.

Danach öffnen wir die Datei __settings.py__.
In dieser Datei suchen wir nach __INSTALLED_APPS__.

__tutorial/settings.py__

    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'bulletinBoard', # hier am Ende fügen wir die gerade erstellte App hinzu, damit
                         # wir global darauf zugreifen, HTTP-Request routen und noch viele
                         # weitere Sachen machen können.
    ]

In der gleichen Datei suchen wir auch noch nach __TIME_ZONE__.

    TIME_ZONE = 'Europe/Berlin' # Hier gleichen wir an unsere lokale Zeitzone an.

Wie im Tutorial der Mozilla Foundation fürgen wir urlpatterns hinzu, 
die im Folgenden die HTTP-Requests auffangen und an die richtige Stelle leiten.

__tutorial/urls.py__

    from django.urls import include
    from django.conf import settings
    from django.conf.urls.static import static
    from django.views.generic import RedirectView


    urlpatterns = [
        path('admin/', admin.site.urls),
        path('bulletinBoard/', include('bulletinBoard.urls')), # die URL für die App
        path('', RedirectView.as_view(url='bulletinBoard/', permanent=True)), 
    
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) # das hier ist für
                                                                    # static files
Wir verweisen hier bei der zweiten path-Funktion auf **bulletinBoard.urls**.
Da es die Datei noch nicht gibt, müssen wir diese erstellen.

    from django.urls import path
    from . import views

    urlpatterns = [
            #path('', views.index, name='index'),
        ]


Dann wenden wir uns den __models__ zu. Wie ich ja schon in der Video-Session
erzählt habe, sind __models__ sozusagen das *Datenbank-Mapping*, also so eine
Art Schnittstelle zwischen django und der jeweils verwendeten Datenbank.

Dort definieren wir die Einträge, die django dann in die Datenbank schreiben
können soll.

Das hier ist jetzt ein **template** für ein durchschnittliches model:

__bulletinBoard/models.py__

    class MyModelName(models.Model):
        """A typical class defining a model, derived from the Model class."""
    
        # Fields
        my_field_name = models.CharField(max_length=20, help_text='Enter field documentation')
        ...
    
        # Metadata
        class Meta: 
            ordering = ['-my_field_name']
    
        # Methods
        def get_absolute_url(self):
            """Returns the url to access a particular instance of MyModelName."""
            return reverse('model-detail-view', args=[str(self.id)])
        
        def __str__(self):
            """String for representing the MyModelName object (in Admin site etc.)."""
            return self.my_field_name

Wir müssen nun überlegen was wir brauchen. Also für ein absolutes Minimum benötigen wir
zumindest ein model für **User** und ein model für **Posts**.

Das User-Model hat im Beispiel jetzt die Datenbankfelder last_name und first_name.

    class User(models.Model):
        
        last_name = models.CharField(max_length = 666, help_text = "Last name of user")
        first_name = models.CharField(max_length = 1000, help_text = "First name of user")
        ordering = ['last_name', 'first_name']
    
        def __str__(self):
            return "{0} {1}".format(self.first_name, self.last_name)

Die __CharFields__ haben eine Maximallänge von 666 und 1000 Zeichen.
Ich hab einfach mal gegoogled, wie lang die längsten Vor- und Nachnamen der Welt
sind und diese dementsprechend eingetragen. Der __help_text__ ist hier für die Erfassung hilfreich.

Beim Post-Model wird es etwas komplizierter.

    class Post(models.Model):
    
        title = models.CharField(max_length = 80, help_text = "Title of post")
        content = models.TextField(max_length = 8000, help_text = "Content of post")
        author = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
    
        def __str__(self):
            return "{0} {1} {2}".format(self.title, self.content, self.author)

Wir haben hier ein Char- und ein TextField. Beides sind Textfelder, in die strings
eingegeben werden können. Dann haben wir einen author als ForeignKey. Dieser "Key" ist das
User Model. Der ForeignKey ist eine one-to-many-Beziehung. Es können also viele Posts den
selben Autor haben. 

Die __\__str_\___ Funktionen geben das ganze Objekt zurück. Hier im Format Titel, Content, Autor.

Um die Kommentare und deren Model kümmern wir uns später, da das eine kompliziertere Geschichte werden wird.

Wenn wir die Erstellung der Models abgeschlossen haben müssen wir die geplanten column-Einträge noch schreiben und dann in die Datenbank "migrieren".

Also:

    python manage.py makemigrations

und dann: 

    python manage.py migrate

Nachdem wir die Migration durchgeführt haben, müssen wir die Models noch im Admin-Interface
registrieren:

__bulletinBoard/admin.py__

    from .models import User, Post

    admin.site.register(User)
    admin.site.register(Post)

Danach sollten wir einen Administrator-Account generieren:

    python manage.py createsuperuser

Der fragt ein paar Daten ab, Email und Passwort sind aber noch egal.

Danach können wir mit:

    python manage.py runserver

den development server starten und uns auf http://127.0.0.1:8000/admin
die Models in Aktion anschauen.

Erstellt am Besten gleich ein paar Einträge. Es sollte gleich deutlich werden, 
dass jeder Post einen User hat, und ein User viele Posts haben kann.

Jetzt kommt der spannende Part. Jetzt holen wir nämlich mithilfe von django 
wieder Einträge aus der Datenbank heraus und geben sie in unsere Website aus.


Jetzt schreiben wir die erste view, also die Datei, die den ganzen Python Code enthält,
der später für die Funktionalität der Website sorgen wird.

__bulletinBoard/views.py__

    from django.shortcuts import render, get_object_or_404
    from bulletinBoard.models import User, Post
    
    def index(request): # Diese Funktion ist die index view, also sozusagen der Code für die
                        # Homepage
        
        num_posts = Post.objects.all().count() # Hier holen wir uns alle Einträge im Post-Objekt
        num_users = User.objects.all().count() # und zählen sie, wie auch im User-Objekt
        post = Post.objects.all() # hier laden wir alle Posts in eine Liste
    
        context = {
            'num_posts': num_posts,
            'num_users': num_users,
            'post': post, 
            
        } # der context mappt die objekte zu variablen, auf die wir später zugreifen können
    
        return render(request, 'index.html', context=context) 
    
Jetzt brauchen wir noch einen template-Ordner im bulletinBoard directory, da das der Standard-Lookup-Pfad in django ist.

In diesem template-Ordner erstellen wir eine Datei namens base_generic.html.

__bulletinBoard/templates/base_genric.html__

    <!DOCTYPE html>
    <html lang="en">
    <head>
      {% block title %}<title>schul-Reddit</title>{% endblock %}
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/    bootstrap.min.css" integrity="sha384-MCw98/    SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">
      <!-- Add additional CSS in static file -->
      {% load static %}
      <link rel="stylesheet" href="{% static 'css/styles.css' %}">
    </head>
    <body>
      <div class="container-fluid">
        <div class="row">
          <div class="col-sm-2">
          {% block sidebar %}
            <ul class="sidebar-nav">
              <li><a href="{% url 'index' %}">Home</a></li>
              <li><a href="">Users</a></li>
              <li><a href="">Posts</a></li>
            </ul>
         {% endblock %}
          </div>
          <div class="col-sm-10 ">{% block content %}{% endblock %}</div>
        </div>
      </div>
    </body>
    </html>


Für css, das nicht Bootstrap-Klassen entstammt brauchen wir noch einen anderen Ordern, 
nämlich static und in diesem Ordner einen weiteren für das css. 

Also:

__bulletinBoard/static/css/styles.css__

    .sidebar-nav {
        margin-top: 20px;
        padding: 0;
        list-style: none;
    }

Nun brauchen wir auch noch unsere index.html:

__bulletinBoard/templates/index.html__

    {% extends "base_generic.html" %}
    
    {% block content %}
      <h1>schulReddit</h1>
      <p>Welcome to schulReddit, a website developed by <em>HTTF</em>!</p>
      <h2>Dynamic content</h2>
      <p>The site has the following counts for users and posts:</p>
      <ul>
        <li><strong>Users:</strong> {{ num_users }}</li>
        <li><strong>Posts:</strong> {{ num_posts }}</li>
      </ul>
      <p>
        {% for p in post %}
          <h1>{{ p.title }}</h1>
          <p>{{ p.content }}</p>
          <p>{{ p.author }}</p>
        {% endfor %}
      </p>
    
    {% endblock %}

Hier kommt noch mehr, aber ihr könnt es ja schonmal testen.

Wir müssen noch eine Sache ändern:

In unserem settings.py macht ihr einen weiteren Import.

Also:

__tutorial/settings.py__

    import os
    
    Dann schreiben wir in den TEMPLATES in 
    'DIRS': [
        os.path.join(BASE_DIR, 'templates'),
    ]

Jetzt müssen wir noch einen Kommentar in der app-spezifischen __urls.py__ unkommentieren.

__bulletinBoard/urls.py__

    # löschen 

Wenn ihr jetzt den wieder den development server startet, 
solltet ihr sehen, wie die von euch eingetragenen Daten auf
der Website gerendert werden.

### Der Guide ist nicht komplett, aber für heute hab ich keine Kraft mehr ^^
