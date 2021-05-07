---
layout: default
title: Systems
nav_order: 4
---
# Architecture
This page goes into detail about the architecture of the game.
## Game-Loop
## State Machine
## Systems
The game is made up of various systems, each responsible for a certain aspect of the game logic. Each of these systems are updated once per frame. The following table gives an overview of these systems and which role they play.

|System|Description|
|------|-----------|
|CameraRenderingSystem|When the game is run without `headless` mode enabled, this system takes care of displaying captured camera frames in a window with debug information (e.g. markers detected). This is used for debugging purposes only.|
|LoggingSystem|The logging system writes captured markers, the calculated distances and angles into a csv file.|
|MarkerDetectionSystem|The marker detection system retrieves the current frame captured by the camera and tries to detect aruco markers. For any detected marker the system calculates the distance and the angle to the marker, and then proceeds to stores these values in the `MarkerService`.|
|MarkerTransformationSystem|The marker transformation system retrieves the current detected markers and calculates its translation and forward vector.|
|ProgressRequestSystem|The progress request system detects if a button press was detected on the configured gpio pin. If so, it triggers a change in the state machine.|
|ProximityConditionSystem|The proximity condition system takes care of detecting whether the suspect is a so called "danger zone". The agent is considered to be in a danger zone when the wearer of the haptic wearable is too close or too far from the average position of all detected markers.|
|TargetLookAtSystem|The target look at system tracks whether the suspect is facing the agent. This occurs when the designated "front" marker (see [Configuration](configuration.md)) is facing the camera in a given threshold. If this occurs a response is triggered on the haptic wearable.|
|VibrationNavigationSystem|The vibration navigation system is responsible for guiding the agent in the direction of the suspect. It also provides information via differing frequency levels whether the agent is in an *optimal* distance to the suspect.|
