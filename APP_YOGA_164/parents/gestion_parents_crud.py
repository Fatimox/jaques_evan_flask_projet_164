"""Gestion des "routes" FLASK et des données pour les parents.
Fichier : gestion_parents_crud.py
Auteur : OM 2021.03.16
"""
from pathlib import Path

from flask import redirect
from flask import request
from flask import session
from flask import url_for

from APP_YOGA_164 import app
from APP_YOGA_164.database.database_tools import DBconnection
from APP_YOGA_164.erreurs.exceptions import *
from APP_YOGA_164.parents.gestion_parents_wtf_forms import FormWTFAjouterGenres
from APP_YOGA_164.parents.gestion_parents_wtf_forms import FormWTFDeleteGenre
from APP_YOGA_164.parents.gestion_parents_wtf_forms import FormWTFUpdateGenre

"""
    Auteur : OM 2021.03.16
    Définition d'une "route" /genres_afficher
    
    Test : ex : http://127.0.0.1:5575/genres_afficher
    
    Paramètres : order_by : ASC : Ascendant, DESC : Descendant
                id_parent_sel = 0 >> tous les parents.
                id_parent_sel = "n" affiche le genre dont l'id est "n"
"""


@app.route("/genres_afficher/<string:order_by>/<int:id_parent_sel>", methods=['GET', 'POST'])
def genres_afficher(order_by, id_parent_sel):
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                if order_by == "ASC" and id_parent_sel == 0:
                    strsql_genres_afficher = """SELECT t_parents.id_parents, t_parents.Nom, t_parents.Prenom,
                                                    GROUP_CONCAT(t_mail.NomMail) AS ParentsMail,
                                                    GROUP_CONCAT(t_telephone.NumTel) AS ParentsTel,
                                                    GROUP_CONCAT(CONCAT_WS(' ', t_adresse.NomRue, t_adresse.NumeroRue, t_adresse.Ville, t_adresse.Npa)) AS ParentsAdresse FROM t_parents
                                                    LEFT JOIN t_parents_mail ON t_parents.id_parents = t_parents_mail.fk_parents
                                                    LEFT JOIN t_mail ON t_mail.id_mail = t_parents_mail.fk_mail
                                                    LEFT JOIN t_parents_telephone ON t_parents.id_parents = t_parents_telephone.fk_parents
                                                    LEFT JOIN t_telephone ON t_telephone.id_telephone = t_parents_telephone.fk_telephone
                                                    LEFT JOIN t_parents_adresse ON t_parents.id_parents = t_parents_adresse.fk_parents
                                                    LEFT JOIN t_adresse ON t_adresse.id_adresse = t_parents_adresse.fk_adresse
                                                    GROUP BY t_parents.id_parents, t_parents.Nom, t_parents.Prenom;"""

                    mc_afficher.execute(strsql_genres_afficher)
                elif order_by == "ASC":
                    # C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
                    # la commande MySql classique est "SELECT * FROM t_parents"
                    # Pour "lever"(raise) une erreur s'il y a des erreurs sur les noms d'attributs dans la table
                    # donc, je précise les champs à afficher
                    # Constitution d'un dictionnaire pour associer l'id du genre sélectionné avec un nom de variable
                    valeur_id_parent_selected_dictionnaire = {"value_id_parent_selected": id_parent_sel}
                    strsql_genres_afficher = """SELECT * FROM t_parents WHERE id_parents = %(value_id_parent_selected)s"""

                    mc_afficher.execute(strsql_genres_afficher, valeur_id_parent_selected_dictionnaire)
                else:
                    strsql_genres_afficher = """SELECT * FROM t_parents"""

                    mc_afficher.execute(strsql_genres_afficher)

                data_genres = mc_afficher.fetchall()

                print("data_genres ", data_genres, " Type : ", type(data_genres))

                # Différencier les messages si la table est vide.
                if not data_genres and id_parent_sel == 0:
                    flash("""La table "t_parents" est vide. !!""", "warning")
                elif not data_genres and id_parent_sel > 0:
                    # Si l'utilisateur change l'id_parents dans l'URL et que le genre n'existe pas,
                    flash(f"L'enfant demandé n'existe pas !!", "warning")
                else:
                    # Dans tous les autres cas, c'est que la table "t_parents" est vide.
                    # OM 2020.04.09 La ligne ci-dessous permet de donner un sentiment rassurant aux utilisateurs.
                    flash(f"Données parents affichés !!", "success")

        except Exception as Exception_genres_afficher:
            raise ExceptionGenresAfficher(f"fichier : {Path(__file__).name}  ;  "
                                          f"{genres_afficher.__name__} ; "
                                          f"{Exception_genres_afficher}")

    # Envoie la page "HTML" au serveur.
    return render_template("parents/parents_afficher.html", data=data_genres)


"""
    Auteur : OM 2021.03.22
    Définition d'une "route" /genres_ajouter
    
    Test : ex : http://127.0.0.1:5575/genres_ajouter
    
    Paramètres : sans
    
    But : Ajouter un genre pour un film
    
    Remarque :  Dans le champ "montant_facture_html" du formulaire "parents/parents_ajouter.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""


@app.route("/genres_ajouter", methods=['GET', 'POST'])
def genres_ajouter_wtf():
    form = FormWTFAjouterGenres()
    if request.method == "POST":
        try:
            if form.validate_on_submit():
                montant_facture_wtf = form.nom_genre_wtf.data
                montant_facture = montant_facture_wtf

                name_parents_wtf = form.prenom_parents_wtf.data
                name_parents = name_parents_wtf

                valeurs_insertion_dictionnaire = {"value_intitule_genre": montant_facture, "value_intitule_parents": name_parents, "value_intitule_telephone": name_telephone}
                print("valeurs_insertion_dictionnaire ", valeurs_insertion_dictionnaire)

                strsql_insert_genre = """INSERT INTO t_parents (id_parents,Nom,Prenom) VALUES (NULL,%(value_intitule_genre)s,%(value_intitule_parents)s)"""
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_insert_genre, valeurs_insertion_dictionnaire)

                flash(f"Données insérées !!", "success")
                print(f"Données insérées !!")

                # Pour afficher et constater l'insertion de la valeur, on affiche en ordre inverse. (DESC)
                return redirect(url_for('genres_afficher', order_by='DESC', id_parent_sel=0))

        except Exception as Exception_genres_ajouter_wtf:
            raise ExceptionGenresAjouterWtf(f"fichier : {Path(__file__).name}  ;  "
                                            f"{genres_ajouter_wtf.__name__} ; "
                                            f"{Exception_genres_ajouter_wtf}")

    return render_template("parents/parents_ajouter_wtf.html", form=form)


"""
    Auteur : OM 2021.03.29
    Définition d'une "route" /genre_update
    
    Test : ex cliquer sur le menu "parents" puis cliquer sur le bouton "EDIT" d'un "genre"
    
    Paramètres : sans
    
    But : Editer(update) un genre qui a été sélectionné dans le formulaire "factures_afficher.html"
    
    Remarque :  Dans le champ "nom_genre_update_wtf" du formulaire "parents/factures_update_wtf.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""


@app.route("/genre_update", methods=['GET', 'POST'])
def genre_update_wtf():
    # L'utilisateur vient de cliquer sur le bouton "EDIT". Récupère la valeur de "id_parents"
    id_genre_update = request.values['id_genre_btn_edit_html']

    # Objet formulaire pour l'UPDATE
    form_update = FormWTFUpdateGenre()
    try:
        print(" on submit ", form_update.validate_on_submit())
        if form_update.validate_on_submit():
            # Récupèrer la valeur du champ depuis "factures_update_wtf.html" après avoir cliqué sur "SUBMIT".
            # Puis la convertir en lettres minuscules.
            montant_facture_update = form_update.nom_genre_update_wtf.data
            montant_facture_update = montant_facture_update
            date_genre_essai = form_update.date_genre_wtf_essai.data

            valeur_update_dictionnaire = {"value_id_genre": id_genre_update,
                                          "value_montant_facture": montant_facture_update,
                                          "value_date_genre_essai": date_genre_essai
                                          }
            print("valeur_update_dictionnaire ", valeur_update_dictionnaire)

            str_sql_update_intitulegenre = """UPDATE t_parents SET Prenom = %(value_montant_facture)s, 
            Nom = %(value_date_genre_essai)s WHERE id_parents = %(value_id_genre)s """
            with DBconnection() as mconn_bd:
                mconn_bd.execute(str_sql_update_intitulegenre, valeur_update_dictionnaire)

            flash(f"Donnée mise à jour !!", "success")
            print(f"Donnée mise à jour !!")

            # afficher et constater que la donnée est mise à jour.
            # Affiche seulement la valeur modifiée, "ASC" et l'"id_genre_update"
            return redirect(url_for('genres_afficher', order_by="ASC", id_parent_sel=id_genre_update))
        elif request.method == "GET":
            # Opération sur la BD pour récupérer "id_parents" et "intitule_genre" de la "t_parents"
            str_sql_id_genre = "SELECT id_parents, Prenom, Nom FROM t_parents " \
                               "WHERE id_parents = %(value_id_genre)s"
            valeur_select_dictionnaire = {"value_id_genre": id_genre_update}
            with DBconnection() as mybd_conn:
                mybd_conn.execute(str_sql_id_genre, valeur_select_dictionnaire)
            # Une seule valeur est suffisante "fetchone()", vu qu'il n'y a qu'un seul champ "nom genre" pour l'UPDATE
            data_nom_genre = mybd_conn.fetchone()
            print("Nom ", data_nom_genre, " type ", type(data_nom_genre), " genre ",
                  data_nom_genre["Prenom"])

            # Afficher la valeur sélectionnée dans les champs du formulaire "factures_update_wtf.html"
            form_update.nom_genre_update_wtf.data = data_nom_genre["Prenom"]
            form_update.date_genre_wtf_essai.data = data_nom_genre["Nom"]

    except Exception as Exception_genre_update_wtf:
        raise ExceptionGenreUpdateWtf(f"fichier : {Path(__file__).name}  ;  "
                                      f"{genre_update_wtf.__name__} ; "
                                      f"{Exception_genre_update_wtf}")

    return render_template("parents/parents_update_wtf.html", form_update=form_update)


"""
    Auteur : OM 2021.04.08
    Définition d'une "route" /genre_delete
    
    Test : ex. cliquer sur le menu "parents" puis cliquer sur le bouton "DELETE" d'un "genre"
    
    Paramètres : sans
    
    But : Effacer(delete) un genre qui a été sélectionné dans le formulaire "factures_afficher.html"
    
    Remarque :  Dans le champ "nom_genre_delete_wtf" du formulaire "parents/factures_delete_wtf.html",
                le contrôle de la saisie est désactivée. On doit simplement cliquer sur "DELETE"
"""


@app.route("/genre_delete", methods=['GET', 'POST'])
def genre_delete_wtf():
    data_films_attribue_genre_delete = None
    btn_submit_del = None
    # L'utilisateur vient de cliquer sur le bouton "DELETE". Récupère la valeur de "id_parents"
    id_genre_delete = request.values['id_genre_btn_delete_html']

    # Objet formulaire pour effacer le genre sélectionné.
    form_delete = FormWTFDeleteGenre()
    try:
        print(" on submit ", form_delete.validate_on_submit())
        if request.method == "POST" and form_delete.validate_on_submit():

            if form_delete.submit_btn_annuler.data:
                return redirect(url_for("genres_afficher", order_by="ASC", id_parent_sel=0))

            if form_delete.submit_btn_conf_del.data:
                # Récupère les données afin d'afficher à nouveau
                # le formulaire "parents/factures_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                data_films_attribue_genre_delete = session['data_films_attribue_genre_delete']
                print("data_films_attribue_genre_delete ", data_films_attribue_genre_delete)

                flash(f"Effacer le genre de façon définitive de la BD !!!", "danger")
                # L'utilisateur vient de cliquer sur le bouton de confirmation pour effacer...
                # On affiche le bouton "Effacer genre" qui va irrémédiablement EFFACER le genre
                btn_submit_del = True

            if form_delete.submit_btn_del.data:
                valeur_delete_dictionnaire = {"value_id_genre": id_genre_delete}
                print("valeur_delete_dictionnaire ", valeur_delete_dictionnaire)

                str_sql_delete_fk_telephone = """DELETE FROM t_parents_telephone WHERE fk_telephone = %(value_id_genre)s"""
                str_sql_delete_fk_mail = """DELETE FROM t_parents_mail WHERE fk_mail = %(value_id_genre)s"""
                str_sql_delete_fk_adresse = """DELETE FROM t_parents_adresse WHERE fk_adresse = %(value_id_genre)s"""
                str_sql_delete_fk_factures = """DELETE FROM t_parents_factures WHERE fk_factures = %(value_id_genre)s"""
                str_sql_delete_parents = """DELETE FROM t_parents WHERE id_parents = %(value_id_genre)s"""
                # Manière brutale d'effacer d'abord la "fk_genre", même si elle n'existe pas dans la "t_enfants_sante"
                # Ensuite on peut effacer le genre vu qu'il n'est plus "lié" (INNODB) dans la "t_enfants_sante"
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(str_sql_delete_fk_telephone, valeur_delete_dictionnaire)
                    mconn_bd.execute(str_sql_delete_fk_mail, valeur_delete_dictionnaire)
                    mconn_bd.execute(str_sql_delete_fk_adresse, valeur_delete_dictionnaire)
                    mconn_bd.execute(str_sql_delete_fk_factures, valeur_delete_dictionnaire)
                    mconn_bd.execute(str_sql_delete_parents, valeur_delete_dictionnaire)

                flash(f"Genre définitivement effacé !!", "success")
                print(f"Genre définitivement effacé !!")

                # afficher les données
                return redirect(url_for('genres_afficher', order_by="ASC", id_parent_sel=0))

        if request.method == "GET":
            valeur_select_dictionnaire = {"value_id_genre": id_genre_delete}
            print(id_genre_delete, type(id_genre_delete))

            # Requête qui affiche tous les enfants_sante qui ont le genre que l'utilisateur veut effacer
            str_sql_genres_films_delete = """SELECT id_parents, Nom, Prenom FROM t_parents WHERE id_parents = %(value_id_genre)s"""


            with DBconnection() as mydb_conn:
                mydb_conn.execute(str_sql_genres_films_delete, valeur_select_dictionnaire)
                data_films_attribue_genre_delete = mydb_conn.fetchall()
                print("data_films_attribue_genre_delete...", data_films_attribue_genre_delete)

                # Nécessaire pour mémoriser les données afin d'afficher à nouveau
                # le formulaire "parents/factures_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                session['data_films_attribue_genre_delete'] = data_films_attribue_genre_delete

                # Opération sur la BD pour récupérer "id_parents" et "intitule_genre" de la "t_parents"
                str_sql_id_genre = "SELECT id_parents, Nom, Prenom FROM t_parents WHERE id_parents = %(value_id_genre)s"

                mydb_conn.execute(str_sql_id_genre, valeur_select_dictionnaire)
                # Une seule valeur est suffisante "fetchone()",
                # vu qu'il n'y a qu'un seul champ "nom genre" pour l'action DELETE
                data_nom_genre = mydb_conn.fetchone()
                print("data_nom_genre ", data_nom_genre, " type ", type(data_nom_genre), " genre ",
                      data_nom_genre["Nom"])

            # Afficher la valeur sélectionnée dans le champ du formulaire "factures_delete_wtf.html"
            form_delete.nom_genre_delete_wtf.data = data_nom_genre["Nom"]

            # Le bouton pour l'action "DELETE" dans le form. "factures_delete_wtf.html" est caché.
            btn_submit_del = False

    except Exception as Exception_genre_delete_wtf:
        raise ExceptionGenreDeleteWtf(f"fichier : {Path(__file__).name}  ;  "
                                      f"{genre_delete_wtf.__name__} ; "
                                      f"{Exception_genre_delete_wtf}")

    return render_template("parents/parents_delete_wtf.html",
                           form_delete=form_delete,
                           btn_submit_del=btn_submit_del,
                           data_films_associes=data_films_attribue_genre_delete)
