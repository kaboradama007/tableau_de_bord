##_____________________________________________________________________________________________
##___________importation des bibliotheques_____________________________________________________

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
import geopandas as gdp
import folium
import contextily as ctx

#@st.cache

##_____________________________________________________________________________________________
##___________IMPORTATION DES DONNEES  ET DU NETOYYAGE DES DATASETS_____________________________

########################### Données sur les ressources en santé du BURKINA FASO################
ressource=pd.read_csv("Gouvernance_data.csv",sep=';', decimal=',',encoding='ISO-8859-1')
ressource=ressource.rename(columns={'Rayon daction moyen théorique en km': "Rayon d'action moyen théorique en km" })
#st.write("Donnée brute par district sanitaire")
#st.dataframe(ressource.head(5))

########################### Données district et calcul des indicateurs par région ################
ds=pd.read_csv("Dataset_DS.csv",sep=';', decimal=',',encoding='ISO-8859-1')

#Regroupement des données par région
data_reg=ds.groupby(["region","Annee"]).sum()
data_reg=data_reg.reset_index()
data2=data_reg.drop(["pays", "province","District"], axis=1)

#Calcul des indicateurs
# Soins curatif et hospitalisation
data2["Nouveaux contacts par habitant"] = (data2["CE-Nouveaux consultants"] / data2["GEN - Population total"]).round(2)
data2["Nouveau contact chez les moins de 5 ans"] = (data2["CE-Nouveaux consultants moins de cinq ans"] /
                                                    data2["GEN - Population de moins de 5 ans"]).round(2)
data2["Proportion (%) d’enfants pris en charge selon l'approche PCIME"] = (100*data2["Nombre de enfants pris en charge selon approche PCIME"] /
                                                                           data2["CE-Nouveaux consultants moins de cinq ans"]).round(2)
# Santé maternelle
data2["Taux (%) d'accouchement dans les FS"] = (100* data2["SMI-Accouchement total"] / data2["Accouchements attendus"]).round(1)
data2["Taux (%) de couverture en CPN1"] = (100* data2["Nombre de CPN1"] / data2["Grossesses attendues"]).round(1)
data2["Taux (%) de couverture en CPN4"] = (100* data2["Nombre de CPN4"] / data2["Grossesses attendues"]).round(1)
data2["Pourcentage des femmes enceintes vues au 1er trimestre"] = (100* data2["Nombre de CPN1 vues au 1er trimestre de la grossesse"] /
                                                                   data2["Nombre de CPN1"]).round(1)
data2["Pourcentage des femmes enceintes ayant bénéficié du TPI3"] = (100* data2["Nombre de femmes enceintes ayant recu le TPI3"] /
                                                                     data2["Nombre de CPN1"]).round(1)
data2["Proportion (%) de faible poids de naissance"] = (100* data2["Nouveau-nes a terme de moins de 2500 g  a la naissance"] /
                                                        data2["SMI-total naissance vivante"]).round(1)
data2["Couverture (%) en consultation postnatale 6e semaine"] = (100* data2["Consultations postnatales  6eme-8eme semaine"] /
                                                                 data2["SMI-Nombre de femmes ayant accouche"]).round(1)
data2["Couverture (%) en consultation postnatale 6e heure"] = (100* data2["Consultations postnatales  6eme-8eme heure"] /
                                                               data2["SMI-Nombre de femmes ayant accouche"]).round(1)
data2["Taux (%) de confirmation du paludisme"] = (100* data2["Palu-TDR et GE realises"] /data2["Palu-Cas de paludisme suspect cas"]).round(1)

###création du dataset des indicateurs par région
# Variable a supprimer dans la base region afin d'alleger le dataset
data_brute=['Accouchements attendus', 'CE-Nouveaux consultants',
       'CE-Nouveaux consultants moins de cinq ans',
       'Consultations postnatales  6eme-8eme heure',
       'Consultations postnatales  6eme-8eme semaine',
       'Enfants de 0 -11 mois ayant recu le DTC-HepB-Hib1',
       'Enfants de 0 -11 mois ayant recu le DTC-HepB-Hib3',
       'Femmes vues en CPN au cours du mois et ayant beneficie dun test VIH',
       'GEN - Population de moins de 5 ans', 'GEN - Population total',
       'Grossesses attendues', 'Naissances vivantes attendues',
       'Nombre de CPN1',
       'Nombre de CPN1 vues au 1er trimestre de la grossesse',
       'Nombre de CPN4',
       'Nombre de enfants pris en charge selon approche PCIME',
       'Nombre de femmes enceintes ayant recu le TPI3',
       'Nouveau-nes a terme de moins de 2500 g  a la naissance',
       'Nouveau-nes mis aux seins dans lheure qui suit la naissance',
       'Palu-Cas de paludisme suspect cas', 'Palu-TDR et GE realises',
       'Population < 1 an', 'SMI-Accouchement total',
       'SMI-Nombre de femmes ayant accouche', 'SMI-total naissance vivante']


indic_region=data2.drop(data_brute, axis=1)

########################### Données district et calcul des indicateurs au niveau national ################
data_nat=ds.groupby(["pays","Annee"]).sum()
data_nat=data_nat.reset_index()
data3=data_nat.drop(["region", "province","District"], axis=1)

# Soins curatif et hospitalisation NATIONAL
data3["Nouveaux contacts par habitant"] = (data3["CE-Nouveaux consultants"] / data3["GEN - Population total"]).round(2)
data3["Nouveau contact chez les moins de 5 ans"] = (data3["CE-Nouveaux consultants moins de cinq ans"] /
                                                    data3["GEN - Population de moins de 5 ans"]).round(2)
data3["Proportion (%) d’enfants pris en charge selon l'approche PCIME"] = (100*data3["Nombre de enfants pris en charge selon approche PCIME"] /
                                                                           data3["CE-Nouveaux consultants moins de cinq ans"]).round(2)
# Santé maternelle
data3["Taux (%) d'accouchement dans les FS"] = (100* data3["SMI-Accouchement total"] / data3["Accouchements attendus"]).round(1)
data3["Taux (%) de couverture en CPN1"] = (100* data3["Nombre de CPN1"] / data3["Grossesses attendues"]).round(1)
data3["Taux (%) de couverture en CPN4"] = (100* data3["Nombre de CPN4"] / data3["Grossesses attendues"]).round(1)
data3["Pourcentage des femmes enceintes vues au 1er trimestre"] = (100* data3["Nombre de CPN1 vues au 1er trimestre de la grossesse"] /
                                                                   data3["Nombre de CPN1"]).round(1)
data3["Pourcentage des femmes enceintes ayant bénéficié du TPI3"] = (100* data3["Nombre de femmes enceintes ayant recu le TPI3"] /
                                                                     data3["Nombre de CPN1"]).round(1)
data3["Proportion (%) de faible poids de naissance"] = (100* data3["Nouveau-nes a terme de moins de 2500 g  a la naissance"] /
                                                        data3["SMI-total naissance vivante"]).round(1)
data3["Couverture (%) en consultation postnatale 6e semaine"] = (100* data3["Consultations postnatales  6eme-8eme semaine"] /
                                                                 data3["SMI-Nombre de femmes ayant accouche"]).round(1)
data3["Couverture (%) en consultation postnatale 6e heure"] = (100* data3["Consultations postnatales  6eme-8eme heure"] /
                                                               data3["SMI-Nombre de femmes ayant accouche"]).round(1)
data3["Taux (%) de confirmation du paludisme"] = (100* data3["Palu-TDR et GE realises"] /data3["Palu-Cas de paludisme suspect cas"]).round(1)

indic_nat=data3.drop(data_brute, axis=1)


###_______________________________fusion de dataframe region et national_______________
df_nat=indic_nat
df_nat = df_nat.rename(columns={'pays': 'region'}) ## pour avoir les memes nom de colonnes
df_concat = pd.concat([df_nat, indic_region], ignore_index=True)
df_concat = df_concat.rename(columns={'region': 'organisation_unit'})


##_____________________________________________________________________________________________
##_____________________________DECLARATION DES VARIABLES ______________________________________

# liste des structures du dataframe fuisionner (region et national)
org_unit=['Burkina Faso', 'Boucle du Mouhoun', 'Cascades', 'Centre',
       'Centre Est', 'Centre Nord', 'Centre Ouest', 'Centre Sud', 'Est',
       'Hauts Bassins', 'Nord', 'Plateau Central', 'Sahel', 'Sud Ouest']

# liste des indicateurs du dataframe fuisionner (region et national)

numeric_col=["Nouveaux contacts par habitant",
       "Nouveau contact chez les moins de 5 ans",
       "Proportion (%) d’enfants pris en charge selon l'approche PCIME",
       "Taux (%) d'accouchement dans les FS", "Taux (%) de couverture en CPN1",
       "Taux (%) de couverture en CPN4",
       "Pourcentage des femmes enceintes vues au 1er trimestre",
       "Pourcentage des femmes enceintes ayant bénéficié du TPI3",
       "Proportion (%) de faible poids de naissance",
       "Couverture (%) en consultation postnatale 6e semaine",
       "Couverture (%) en consultation postnatale 6e heure",
       "Taux (%) de confirmation du paludisme"]

###liste des années du daset fusion
#annee=[2024,2023,2022,2021,2020]
annee=ds["Annee"].unique().tolist()

### indicateurs de ressources(personnels et infrastructures)
val_gouv=["Rayon d'action moyen théorique en km",
       "Ratio population/médecin ", "Ratio habitants/infirmier",
       "Ratio population/SFE-ME"]


##_____________________________________________________________________________________________
##___________Titre du dashboard et du context dans streamlit___________________________________
with st.sidebar:
    col7, col8,col9 = st.columns(3)
    
    with col7:
        st.image("armoiries_bfa.png", use_container_width=True)
    
    with col8:
        st.image("armoiries_bfa.png", use_container_width=True)
    with col9:
        st.image("armoiries_bfa.png", use_container_width=True)


##_____________________________________________________________________________________________
##_____________________________CREATION DE LA BARRE LATERALE POUR LE CHOIX DES PARAMETRES _____
st.sidebar.title("choix des parametres")

st.markdown("""
    <style>
        section[data-testid="stSidebar"] {
            background-color: #f0f2f6;  /* Couleur de fond */
        }
        section[data-testid="stSidebar"] h1 {
            color: darkblue; /* Couleur du texte */
        }
    </style>
""", unsafe_allow_html=True)

#st.markdown("<h3 style='color:blue; font-weight:bold;'>Choisis l'indicateur à visualiser:</h3>", unsafe_allow_html=True)
var_y=st.sidebar.selectbox("Choisis l'indicateur à visualise",numeric_col)
structure=st.sidebar.selectbox("Choisis l'unité d'organisation",org_unit)
var_an=st.sidebar.selectbox("Choisis l'année pour la visualisation",annee)

##_____________________________________________________________________________________________
##___________# Créer les onglets dans streamlit___________________________________


titres_onglets = ["TABLEAU DE BORD", "DONNEES DE BASE"]
onglet1, onglet2 = st.tabs(titres_onglets)
 
# Ajouter du contenu à chaque onglet
with onglet1:
##_____________________________________________________________________________________________
##_____________________________DEFINITION DES OBJECTIFS ET DE CERTAINS PARAMETRES______________

    ### objectif par indicateurs par région et national
    objectif=""
    if var_y=="Nouveaux contacts par habitant":
        objectif=1
    elif var_y=="Nouveau contact chez les moins de 5 ans":
        objectif=2
    elif var_y=="Proportion (%) d’enfants pris en charge selon l'approche PCIME":
        objectif=80
    elif var_y=="Taux (%) d'accouchement dans les FS":
        objectif=85
    elif var_y=="Taux (%) de couverture en CPN1":
        objectif=80
    elif var_y=="Taux (%) de couverture en CPN4":
        objectif=50
    elif var_y=="Pourcentage des femmes enceintes vues au 1er trimestre":
        objectif=50
    elif var_y=="Pourcentage des femmes enceintes ayant bénéficié du TPI3":
        objectif=90
    elif var_y=="Proportion (%) de faible poids de naissance":
        objectif=10
    elif var_y=="Couverture (%) en consultation postnatale 6e semaine":
        objectif=50
    elif var_y=="Couverture (%) en consultation postnatale 6e heure":
        objectif=90
    elif var_y=="Taux (%) de confirmation du paludisme":
        objectif=95


    ##_____________________________________________________________________________________________
    ##_____________________________VISUALISATION DES INDICATEURS DE RESSOURCES_____________________
    message2="Choisis l'indicateurs de ressources à visualiser"
    st.markdown(f"<h3 style='font-size:18px; color:navy; text-align:left;'>{message2}</h3>", unsafe_allow_html=True)
    valeur_indic=st.selectbox("",val_gouv)
    norme_PNDS=""
    if valeur_indic=="Rayon d'action moyen théorique en km":
        norme_PNDS=5
    elif valeur_indic=="Ratio population/médecin ":
        norme_PNDS=5000
    elif valeur_indic=="Ratio habitants/infirmier":
        norme_PNDS=2000
    elif valeur_indic=="Ratio population/SFE-ME":
        norme_PNDS=3000


    ####Message en fonction de l'indicateur
    if valeur_indic=="Rayon d'action moyen théorique en km":
        message=f"La vision du Ministère de la santé est de rapprocher de moins de {norme_PNDS} km les centres de santé aux populations "
    elif valeur_indic=="Ratio population/médecin ":
        message=f"La vision du Ministère de la santé est que chaque médecin doit prendre en charge moins de {norme_PNDS} personnes"
    elif valeur_indic=="Ratio habitants/infirmier":
        message=f"La vision du Ministère de la santé est que chaque infirmier doit prendre en charge moins de {norme_PNDS} personnes"
    elif valeur_indic=="Ratio population/SFE-ME":
        message=f"La vision du Ministère de la santé est que chaque sage femme/maieuticien doit prendre en charge moins de {norme_PNDS} personnes"

    st.markdown(f"<h3 style='font-size:18px; color:navy; text-align:left;'>{message}</h3>", unsafe_allow_html=True)

    # création de deux colonne
    col1, col2 = st.columns(2)

    with col1:
    
        st.markdown(f"<h3 style='font-size:14px; color:navy; text-align:left;'>{valeur_indic}</h3>", unsafe_allow_html=True)
        ##### norme pnds pour les indicateurs globaux

        ## choix des indicateurs liés
        var_connex="Centre de sante publique" #par defaut
        if valeur_indic=="Rayon d’action moyen théorique en km":
            var_connex="Centre de sante publique"
        elif valeur_indic=="Ratio population/médecin ":
            var_connex="Effectif Médecins"
        elif valeur_indic=="Ratio habitants/infirmier":
            var_connex="Effectif Infirmiers"
        elif valeur_indic=="Ratio population/SFE-ME":
            var_connex="Effectif de Sage femme"

        ###graph
        fig_sb0,ax_sb0=plt.subplots(figsize=(10,5))
        ax_sb0=sns.barplot(data=ressource, x=ressource["Annee"], y=valeur_indic, palette='hls')
        # Ajouter une barre horizontale pour l'objectif
        plt.axhline(norme_PNDS, color='red', linestyle='--', linewidth=2, label=f"Objectif : {objectif}")
        # Personnalisation
        #plt.title(f"Evolution de {valeur_indic}", fontsize=14)
        plt.xlabel("Année", fontsize=12)
        plt.ylabel("valeur", fontsize=12)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        #plt.xticks(rotation=45)
        #plt.xticks(fontsize=10)
        for container in ax_sb0.containers:
            ax_sb0.bar_label(container, fmt="%.1f", label_type="edge", fontsize=10, color="black")
        st.pyplot(fig_sb0)

    with col2:
        st.markdown(f"<h3 style='font-size:14px; color:navy; text-align:left;'>{var_connex} et du gap par annéé</h3>", unsafe_allow_html=True)
        ###graph
        fig_sb01,ax_sb01=plt.subplots(figsize=(10,5))
        ax_sb01=sns.barplot(data=ressource, x=ressource["Annee"], y=var_connex,hue="Disponibilite")
        #plt.title(f"nombre de {var_connex} et du Gap au fil des années", fontsize=14)
        plt.xlabel("Annee", fontsize=12)
        plt.ylabel("nombre", fontsize=12)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.xticks(rotation=45)
        plt.xticks(fontsize=10)
        for container in ax_sb01.containers:
            ax_sb01.bar_label(container, fmt="%.1f", label_type="edge", fontsize=10, color="black")
        st.pyplot(fig_sb01)



    ## Barre laterale de separation entre les sections
    st.markdown(
    """
    <style>
    .custom-hr {
        border: none;
        height: 3px;
        background: linear-gradient(to right, #2E86C1, #AED6F1);
        margin: 20px 0;
    }
    </style>
    <hr class="custom-hr">
    """,
    unsafe_allow_html=True
    )

    # _____________________________________________________________________________________________
    ##_____________________________VISUALISATION DES INDICATEURS DE REGION ET NATIONAL_____________

    # parametre de l'axe des ordonnées
    if var_y=="Nouveaux contacts par habitant" or var_y=="Nouveau contact chez les moins de 5 ans":
        ordonnee="Nombre"
    else :
        ordonnee="Pourcentage"

    # parametre de l'axe des ordonnées
    if var_y=="Nouveaux contacts par habitant" or var_y=="Nouveau contact chez les moins de 5 ans":
        expression="contacts au moins"
    else :
        expression="%"





    # filtre de l'unité d'organisation
    df_fusion = df_concat.query("organisation_unit == @structure")

    ### EVOLUTION DES INDICATEURS PAR STRUCTURE
    st.markdown(f"##### 🎯 L'objectif **PNDS** de **{var_y}** est de **{objectif} {expression}** ✅")
    fig_sb,ax_sb=plt.subplots(figsize=(10,5))
    ###prendre en compte la forme en aire
    sns.set_theme(style="darkgrid")
    plt.fill_between(df_fusion["Annee"], df_fusion[var_y], color="#f2f4f4", alpha=0.4)


    ax_sb=sns.lineplot(data=df_fusion, x=df_fusion["Annee"], y=var_y, marker="o", linewidth=2)
    # Ajouter une barre horizontale pour l'objectif
    plt.axhline(objectif,color='red', linestyle='--', linewidth=2, label=f"Objectif : {objectif}")
    # ETIQUETTES
    # Ajouter des étiquettes sur chaque point
    for i, row in df_fusion.iterrows():
        plt.text(row["Annee"], row[var_y] + 0.3, str(row[var_y]), ha="center", fontsize=10, color="blue")


    # Personnalisation
    plt.ylim(0, None)
    plt.xticks(df_fusion["Annee"][::1])
    #plt.title(f"Evolution du {var_y} au {structure}", fontsize=14)
    st.markdown(f"<h3 style='font-size:14px; color:navy; text-align:left;'>Evolution du {var_y} au {structure}</h3>", unsafe_allow_html=True)
    plt.xlabel("Année", fontsize=12)
    plt.ylabel(ordonnee, fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    st.pyplot(fig_sb)


    #####presentation par région
    data_an=indic_region.query("Annee== @var_an").sort_values(by=var_y)

    fig_sb2,ax_sb2=plt.subplots(figsize=(10,5))
    ax_sb2=sns.barplot(data=data_an, x=data_an["region"], y=var_y, palette='hls')
    # Ajouter une barre horizontale pour l'objectif
    plt.axhline(objectif, color='red', linestyle='--', linewidth=2, label=f"Objectif : {objectif}")
    # Personnalisation
    #plt.title(f"{var_y} par région en {var_an}", fontsize=14)
    st.markdown(f"<h3 style='font-size:14px; color:navy; text-align:left;'>{var_y} par région en {var_an}</h3>", unsafe_allow_html=True)
    plt.xlabel("Région", fontsize=12)
    plt.ylabel(ordonnee, fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.xticks(rotation=45)
    plt.xticks(fontsize=10)
    for container in ax_sb2.containers:
        ax_sb2.bar_label(container, fmt="%.1f", label_type="edge", fontsize=10, color="black")
    st.pyplot(fig_sb2)


        ## Barre laterale de separation entre les sections
    st.markdown(
    """
    <style>
    .custom-hr {
        border: none;
        height: 3px;
        background: linear-gradient(to right, #2E86C1, #AED6F1);
        margin: 20px 0;
    }
    </style>
    <hr class="custom-hr">
    """,
    unsafe_allow_html=True
    )


    #### SYSTEME D'INFORMATION GEOGRAPHIQUE
    # importation du shapefile
    district=gdp.read_file("district_sanitaire.shp")
    fosa=gdp.read_file("centre_sante.shp")

    # Affichage de la table district
    #district.head()
    ########### carte thematique
    region_sig="BOUCLE DU MOUHOUN"
    if structure=="Boucle du Mouhoun":
        region_sig="BOUCLE DU MOUHOUN"
    elif structure=="Cascades":
        region_sig="CASCADES"
    elif structure=="Centre":
        region_sig="CENTRE"
    elif structure=="Centre Est":
        region_sig="CENTRE-EST"
    elif structure=="Centre Nord":
        region_sig="CENTRE-NORD"
    elif structure=="Centre Ouest":
        region_sig="CENTRE-OUEST"
    elif structure=="Centre Sud":
        region_sig="CENTRE-SUD"
    elif structure=="Est":
        region_sig="EST"
    elif structure=="Hauts Bassins":
        region_sig="HAUTS-BASSINS"
    elif structure=="Nord":
        region_sig="NORD"
    elif structure=="Plateau Central":
        region_sig="PLATEAU-CENTRAL"
    elif structure=="Sahel":
        region_sig="SAHEL"
    elif structure=="Sud Ouest":
        region_sig="SUD-OUEST"

    region=district[district["Region"]==region_sig]
    zoom_level = 12

    if structure=="Burkina Faso":
            #district.plot(figsize=(20,20))
            fig3, ax3=plt.subplots(figsize=(30,30))
            district.plot(column="Completude",cmap="RdYlBu",legend=True, vmin=0, vmax=100,edgecolor="black", linewidth=2,ax=ax3)
            for idx, row in district.iterrows():
                ax3.text(row.geometry.centroid.x,row.geometry.centroid.y,row["Nom_DS"], fontsize=12)
                ax3.set_title(f"Carte: Complétude des RMA du {structure} en 2024 par district", fontsize=40,color="navy",	loc="left",pad=20)
            # Ajouter un fond de carte OpenStreetMap
            ctx.add_basemap(ax3, source=ctx.providers.OpenStreetMap.Mapnik,zoom=zoom_level)
            st.pyplot(fig3)
    else:
            
            ## region selectionner
        #district.plot(figsize=(20,20))
        fig5, ax5=plt.subplots(figsize=(30,30))
        region.plot(column="Completude",cmap="RdYlBu",legend=True, vmin=0, vmax=100, edgecolor="black", linewidth=2,ax=ax5)
        for idx, row in region.iterrows():
            ax5.text(row.geometry.centroid.x,row.geometry.centroid.y,row["Nom_DS"], fontsize=12)
            ax5.set_title(f"Carte: Complétude des RMA de la région du {structure} en 2024 par district", fontsize=40,color="navy",	loc="left",pad=20)
        # Ajouter un fond de carte OpenStreetMap
        ctx.add_basemap(ax5, source=ctx.providers.OpenStreetMap.Mapnik,zoom=zoom_level)
        #st.pyplot(fig3)
        st.pyplot(fig5)


##::::::/::::::::::::DONNEES::::::::::::::::::::::::::::::::::::::::::::::::::
 
with onglet2:
    st.header("Données sur les ressources en santé")
    st.write(ressource.head())
    st.header('Données brute des districts sanitaire')
    st.write(ds.head())
    st.header('Indicateurs par région')
    st.write(data2.head()) 





