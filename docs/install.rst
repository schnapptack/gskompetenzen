GS-Kompetenzen Installation
================================


Diese Installationsanleitung setzt ein installiertes Linux-Serversystem vorraus.
Die Anleitung geht dabei auf Debian 7.0 ein, sollte aber ohne große Anpassungen auch auf andere Distributionen übertragbar sein.
Windows wird für den Betrieb der Webanwendung derzeit nicht offiziell unterstützt.

GS-Kompetenzen ist in Python auf Basis des Webframeworks Django umgesetzt.
Zum Betrieb wird ein Webserver und eine relationale Datenbank benötigt.
Hier wird auf dem Betrieb mit dem Webserver Apache und der Datenbank PostgreSQL eingegangen.
Auf Alternativen zur hier beschriebenen Installation wird in der Django-Dokumentation eingegangen:

- https://docs.djangoproject.com/en/1.5/ref/databases/
- https://docs.djangoproject.com/en/1.5/howto/deployment/



apt-get install git


Installation der Datenbank
------------------------------

Falls noch nicht vorhanden, PostgreSQL installieren::

    apt-get install postgresql-9.1

Legen Sie einen Datenbank-User und eine Datenbank an::

    su postgres
    psql

Zum Anlegen müssen Sie nun die Folgenden SQL-Statements eingeben. Ersetzen Sie dabei ``<dbuser>``,
``<dbpassword>`` und ``<database>`` durch Werte Ihrer Wahl (diese werden später noch benötigt).

::

    CREATE USER <dbuser> WITH PASSWORD '<dbpassword>';
    CREATE DATABASE <database> WITH OWNER <dbuser> TEMPLATE template0 ENCODING 'UTF-8';


Installation des Webservers
------------------------------


Falls noch nicht vorhanden, den Webserver Apache und benötigte Zusatzmodule installieren::

    apt-get install apache2 apache2-mpm-prefork libapache2-mod-wsgi


Installation von GS-Kompetenzen
----------------------------------

Python ist unter Debian meist bereits installiert. Falls nicht muss Python in Version 2.6 oder 2.7 nachinstalliert werden.

Basispakete
'''''''''''''''''

Zusätzlich nötige Python-Module via Paketmanager installieren::

    apt-get install python-virtualenv python-psycopg2


Installation des Produktlinienmanagers ``ape``
'''''''''''''''''''''''''''''''''''''''''''''''

(Vgl. hierzu: http://django-productline.readthedocs.org/en/latest/install.html)

``ape`` lässt sich wie folgt installieren::

    cd /opt
    wget -O - https://raw.github.com/henzk/ape/master/bin/bootstrape | python - webapps

Danach ist ``ape`` unter ``/opt/webapps`` installiert.

Zur Benutzung muss zunächst die Produktlinienumgebung ``ape`` aktiviert werden::

    cd /opt/webapps
    . _ape/activape

.. note::

    Die Umgebung kann jederzeit mit dem Befehl ``deactivape`` wieder verlassen werden.
    ``ape`` verwendet ein ``virtualenv``(https://pypi.python.org/pypi/virtualenv),
    um Python-Pakete unabhängig vom restlichen System zu verwalten. Damit die folgenden
    Pakete mittels ``pip`` korrekt installiert werden, muss die Produktlinienumgebung
    aktiviert sein.


Anschließend wird mit folgendem Befehl das Basisfeature für GS-Kompetenzen installiert::

    pip install git+https://github.com/henzk/django-productline.git#egg=django-productline





Installation des Containers für GS-Kompetenzen
'''''''''''''''''''''''''''''''''''''''''''''''

Für diesen Schritt muss ``ape`` installiert sein.

Nun wird der GS-Kompetenzen Container installiert::

    cd /opt/webapps
    mkdir _var
    cd _var
    git clone https://github.com/schnapptack/gskompetenzen.git
    ln -s /opt/webapps/_var/gskompetenzen/gsk /opt/webapps/


Anschließend sollte die Ausgabe von ``ape info`` wie folgt aussehen::


    root directory  : /opt/webapps

    active container:
    containers and products:
    ------------------------------

    gsk
        gsk


Danach müssen noch weitere benötigte Features und Abhängigkeiten installiert werden::


    pip install django-mptt
    pip install django-jsonfield

    pip install -e git+https://github.com/schnapptack/djpl-emailing.git#egg=djpl-emailing
    pip install -e git+https://github.com/schnapptack/djpl-cssbasics.git#egg=djpl-cssbasics
    pip install -e git+https://github.com/schnapptack/djpl-jsbasics.git#egg=djpl-jsbasics
    pip install -e git+https://github.com/tonimichel/djpl-schnadmin.git#egg=djpl-schnadmin
    pip install -e git+https://github.com/tonimichel/djpl-schnadmin-sidenav.git#egg=djpl-schnadmin-sidenav
    pip install -e git+https://github.com/tonimichel/djpl-users.git#egg=djpl-users

    pip install -e git+https://github.com/tonimichel/djpl-schnippjs.git#egg=djpl-schnippjs
    cd /opt/webapps/_ape/venv/src/djpl-schnippjs
    git submodule init
    git submodule update


Konfiguration des Produktkontexts
-----------------------------------


Zunächst muss die Produktumgebung ``gsk:gsk`` ausgewählt werden (das Produkt ``gsk`` im Container ``gsk``)::

::

    ape teleport gsk:gsk


Sie gelangen dadurch automatisch in das Produktverzeichnis ``/opt/webapps/gsk/products/gsk``.

Legen Sie dort eine Datei namens ``context.json`` mit folgendem Inhalt an(eine Vorlage finden Sie in ``sample_context.json``)::

    {
        "SECRET_KEY": "<secretkey>",
        "SITE_ID": 1,
        "DATA_DIR": "/opt/webapps/gsk/products/gsk/__data__",
        "DATABASES": {
            "default": {
                "ENGINE": "django.db.backends.postgresql_psycopg2",
                "HOST": "localhost",
                "PORT": "5432",
                "USER": "<dbuser>",
                "PASSWORD": "<dbpassword>",
                "NAME": "<database>"
            }
        }
    }

Ersetzen Sie dabei ``<secretkey>`` durch 50 oder mehr zufällige Zeichen (vgl. https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-SECRET_KEY).
``<dbuser>``, ``<dbpassword>`` und ``<database>`` ersetzen Sie bitte durch die zuvor beim Anlegen der Datenbank verwendeten Werte.


Einrichten der Datenbank
-----------------------------

Das anfangs über den Paketmanager installierte Python-Paket ``psycopg2`` muss noch durch symbolische Links in die Umgebung eingebunden werden::

    ln -s /usr/lib/python2.7/dist-packages/psycopg2 /opt/webapps/_ape/venv/lib/python2.7/site-packages/
    ln -s /usr/lib/python2.7/dist-packages/mx /opt/webapps/_ape/venv/lib/python2.7/site-packages/


Einspielen des Datenbankschemas
--------------------------------

Stellen Sie sicher, dass Sie ``ape`` aktiviert haben und sich im Produktkontext ``gsk:gsk`` befinden.

Anschließend können Sie das Schema wie folgt einspielen::

    ape select_features
    ape prepare


Anlegen eines Administrators
--------------------------------

::

    ape manage createsuperuser


Sie können nun den Nutzernamen, die Email-Adresse und das Passwort des Administrators festlegen.


Konfiguration des Webservers
--------------------------------


-wsgi file
-vhost conf



