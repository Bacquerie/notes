---
layout: mathjax
nav_order: 1
title: Rodent Control
parent: Practices
---
{% include mathjax.html %}
# RODENT CONTROL


---
## Topics

* Linear Kalman filters for tracking.


---
## Overview


We are in a mouse-infested (continuous) house. Your task is to program a robot to catch them all
using a trap gun.


---
## High-Level Expected Behavior


1. The program starts with $$N$$ mice running around the house, under near-linear velocity, which
   is assumed to be Gaussian. The agent must try to keep track of their movement.
   
2. When the agent is confident enough about its tracking abilities, it predicts (estimates) the
   next $$K$$ locations of each tracked mouse.

3. From these estimated locations, it filters out those locations that are too far away from a given
   shooting range, those that are too far or too close time-wise, and those locations where the
   trap wouldn't fall near enough the mouse.

4. From the remaining viable locations, it estimates its best shot and shoots a trap. If it
   fails, it goes back to step (2).

5. As the mice are running in a house of limited dimensions, they will change their direction once
   reaching a wall. This will insert noise into the tracking devices. To handle these, and maybe
   other error scenarios, the agent keeps record of the difference between the actual sensed
   location of each mouse and its estimated location. If this difference is greater than a
   threshold, it will count a mistake. If there occurs $$M$$ consecutive tracking mistakes, the
   agent will drop the current filter for the *erred* mouse and create a new one, going back to
   step (2).

6. Once all mice are trapped, the program starts over again.


---
## Short Demo

<video width="100%" autoplay controls>
  <source src="demo.mp4" type="video/mp4">
Your browser does not support the video tag.
</video>
