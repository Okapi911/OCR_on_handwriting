# OCR_on_handwriting
Ce projet a pour objectif de s'attaquer au problème de la reconnaissance optique des objets (OCR) généralement appliquée à l'écriture manuscrite. En effet, il vise à intégrer l'OCR dans le traitement d'images provenant de caméras RGB, permettant ainsi de détecter et d'analyser du texte manuscrit en temps réel. 

# Fonctionnalités et utilisations 
Bibliothèque EasyOCR: 
EasyOCR offre une reconnaissance précise et performante de l'écriture manuscrite du fait qu'il est conçu pour être facile à utiliser. En plus, il fournit une interface conviviale pour intégrer la reconnaissance de texte dans des projets de traitement d'images.

Bibliothèque OpenCV: 
Bibliothèque de traitement d'images offrant des fonctionnalités de capture d'images, de prétraitement et d'analyse.

Intégration de PyRealSense2: 
Cette bibliothèque permet d'exploiter la puissance des caméras RGB pour capturer des images en temps réel, alimentant ainsi le processus d'OCR.

Publication via MQTT: 
Les résultats de l'OCR, tels que le texte détecté et sa position, sont publiés via le protocole MQTT. Ce mode de communication asynchrone garantit une transmission fluide et flexible des données. Les utilisateurs reçoivent les résultats affichés par le modèle OCR dès qu'ils sont publiés, ce qui assure une distribution en temps réel.

# Fonctionnement 


Dans notre projet, nous avons conçu deux modèles d'intelligence artificielle pour la reconnaissance de texte en nous basant sur des projets open source existants. 

Le premier modèle : s'appuie sur une architecture GNN (Graph Neural Network) et se caractérisait par un temps de latence minimal. Cependant, il ne permettait pas d'effectuer un fine-tuning, ce qui limitait ses performances pour la reconnaissance des minuscules attachées.

Le deuxième modèle : entraîné à partir de zéro sur le jeu de données IAM words, en adaptant le code et en modifiant la structure du réseau. Bien qu'il fournisse d'excellents résultats pour des mots, même en minuscules, il présentait des limitations pour le traitement des lignes et ne fonctionnait pas pour les paragraphes.

Nous avons choisi le premier modèle afin de réaliser notre projet => En effet, nous avons intégré une caméra indépendante du robot pour traiter le flux vidéo à intervalles réguliers et éviter les perturbations permanentes du texte résultant. Nous avons écrit du texte sur un fond blanc et sous forme de paragraphe, le modèle renvoie au format ligne tous les mots manuscrits tout en préservant l'ordre et la ponctuation. Enfin, ce texte est envoyé à l'application développée avec Expo ce qui permet à l'utilisateur de lire le résultat en temps réel dès qu'ils sont publiés.

# Dépendances et outils utilisés
Pour arriver à configurer l'environnement de développement nécessaire pour le projet OCR sur écriture manuscrite. Il s'assurer d'installer : 

Python 3.x

OpenCV

EasyOCR

PyRealSense2

Matplotlib

MQTT Broker

Ce projet ouvre la voie à une interaction plus fluide et intuitive avec les robots contenant des caméras, en exploitant la puissance de l'OCR pour décrypter et analyser l'écriture manuscrite en temps réel. Les applications potentielles sont vastes et prometteuses, avec un impact positif sur de nombreux aspects de notre vie quotidienne.


