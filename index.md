---
layout: default
title: Home
nav_order: 1
permalink: /
---
# Keep Your Distance
Here you can find basic information on the Keep Your Distance game, developed over the course of the EU Research Project [Suitceyes](www.suitceyes.eu).

## About
Keep Your Distance (previously *Police Chase*) is a game designed with the aim of teaching deafblind individuals to navigate with the haptic wearable (Haptic Intelligent Personalized Interface) safely. The game involves two players where one player assumes the role of a secret agent (player wearing a haptic wearable) and the other acts as a suspect. The goal of the secret agent is to keep within an optimal distance to the suspect. While getting too close to the suspect will expose the secret agent's cover, staying too far from the suspect will enable him/her to escape. At the end of the game, we provide a cue that the agent can catch the suspect to win the game.

The application uses a wide-angle camera to track ArUco markers which represent the suspect. Through computer vision algorithms we are able to estimate the distance and the angle to the marker. Depending on these two parameters we can provide different cues to the wearer of the haptic wearable:

* Varying frequency levels of vibration (quicker pulses mean the agent is getting too close to the suspect, slower pulses mean the agent is too far from the suspect)

* Local vibrations on the tactile belt of the haptic wearable: These indicate the direction the wearer must move towards in order to follow the suspect.
We use a Wizard of Oz style application to provide signals to the user, e.g., when the agent can catch the suspect. This application can be found [here](https://github.com/AffectiveCognitiveInstitute/Keep-Your-Distance-Unity-App).

The following video gives a brief overview of the game. 

[![Keep Your Distance Overview Video](http://img.youtube.com/vi/bwPG-lzKVoc/0.jpg)](https://www.youtube.com/watch?v=bwPG-lzKVoc)

## Publications
* James Gay, Moritz Umfahrer, Arthur Theil, Lea Buchweitz, Eva Lindell, Li Guo, Nils-Krister Persson, and Oliver Korn. 2020. Keep Your Distance: A Playful Haptic Navigation Wearable for Individuals with Deafblindness. The 22nd International ACM SIGACCESS Conference on Computers and Accessibility. Association for Computing Machinery, New York, NY, USA, Article 93, 1–4. DOI: [https://doi.org/10.1145/3373625.3418048](https://doi.org/10.1145/3373625.3418048)

## Contributors
The following individuals made contributions to the Keep Your Distance game:

**Concept**: Arthur Theil, James Gay, Lea Buchweitz, Moritz Umfahrer

**Programming**: Lea Buchweitz, James Gay

**Hardware**: James Gay, Moritz Umfahrer

**Textile**: Eva Lindell, Li Guo, Nils-Krister Persson

## Authors
* James Gay