---
layout: default
title: Systems
nav_order: 4
---
# Architecture
This page goes into detail about the architecture of the game.
## Game-Loop
The game loop can be found in the `police-chase.py` file. The following diagram gives an overview of application:

<img src="{{site.baseurl}}/assets/images/game-loop.png" width="300" />

## State Machine
The game uses a state machine to manage states. It is possible to switch to any given state at any given time.
There are three states that govern the game. These are:

* **Navigation State**: The navigation state, the default state, is responsible for guiding the agent in the direction of the suspect using vibrations. It also provides information via differing frequency levels whether the agent is in an *optimal* distance to the suspect or whether he/she is too close or too far from the suspect.

* **Catch Suspect State**: The game enters this state via the game's internal messaging system. When this occurs a vibration pattern is played on the 4x4 matrix on the back of the haptic wearable signalling to the wearer that they should now catch the suspect to win the game.

* **Request Progress State**: This state is entered each time the agent presses a button. Upon pressing this button the user is informed on their progress along the route (25%, 50%, 75%). 

See `StateMachine.py` and `States.py` for further implementation details.

## Systems
The game is made up of various systems, each responsible for a certain aspect of the game logic. Each of these systems are updated once per frame. The following table gives an overview of these systems and which role they play.

|System|Description|
|------|-----------|
|CameraRenderingSystem|When the game is run without `headless` mode enabled, this system takes care of displaying captured camera frames in a window with debug information (e.g. markers detected). This is used for debugging purposes only.|
|LoggingSystem|The logging system writes captured markers, the calculated distances and angles into a csv file.|
|MarkerDetectionSystem|The marker detection system retrieves the current frame captured by the camera and tries to detect aruco markers. For any detected marker the system calculates the distance and the angle to the marker, and then proceeds to stores these values in the `MarkerService`.|
|MarkerTransformationSystem|The marker transformation system retrieves the current detected markers and calculates its translation and forward vector.|
|ProgressRequestSystem|The progress request system detects if a button press was detected on the configured gpio pin. If so, it triggers a change in the state machine.|
|ProximityConditionSystem|The proximity condition system takes care of detecting whether the suspect is in a so called "danger zone". The agent is considered to be in a danger zone when the wearer of the haptic wearable is too close or too far from the average position of all detected markers.|
|StateMachine|Updates the current state of the state machine.|
|TargetLookAtSystem|The target look at system tracks whether the suspect is facing the agent. This occurs when the designated "front" marker (see [Configuration](configuration.md)) is facing the camera in a given threshold. If this occurs a response is triggered on the haptic wearable.|