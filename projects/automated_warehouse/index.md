---
layout: mathjax
nav_order: 1
title: Automated Warehouse Administration
parent: Projects
---
{% include mathjax.html %}
# AUTOMATED WAREHOUSE ADMINISTRATION
---

## Overview


We are in a simulated warehouse with $$N$$ robots at our disposal,  all of
them controlled from a central server.

Our task is to make use of these robots to pick packages from the racks and
place them in their designated conveyor belts, helping in a (out of
scope) package delivery process.


## Technical Overview


1. The simulation starts in a pre-set environment or warehouse, where there 
are $$M$$ fixed conveyor belts and $$N$$ resting locations. The (central)
server discretizes the warehouse layout and computes the optimal navigation
policy to (independently) reach each belt and resting location, from any
location in the map.

2. Sometimes an order arrives, to pick $$K$$ packages available in the  racks,
each meant to be placed in a particular conveyor  belt. The  server computes
the optimal navigation policy to (independently) reach each of them from any
location in the warehouse.  

3. Each of the $$N$$ robots, distributed around the warehouse, is assigned a
package to pick up and place in their assigned belt. The server computes
the assignations based on:
   1. For each package, it computes the cost of reaching such item from the
     current robot location + the cost of reaching the target belt from the
     package location.
   2. Then, the robot is assigned the package of minimal cost.
   3. It picks another robot and repeats.

4. Once a robot's been assigned a package to transport, it starts
navigating the warehouse, according to the pre-computed policies, caring about
collisions against walls and other robots.

5. When a robot has delivered its package, it is assigned a new one, if
available; otherwise, it goes to any resting location until a new order
arrives, and it's assigned a new package to transport.


## Tasks


1. ~~The simulation starts in a pre-set environment or warehouse, where there 
are $$M$$ fixed conveyor belts and $$N$$ resting locations~~. The (central)
server discretizes the warehouse layout ~~and computes the optimal navigation
policy to (independently) reach each belt and resting location, from any
location in the map.~~

2. ~~Sometimes an order arrives, to pick $$K$$ packages available in the racks,
each meant to be placed in a particular conveyor  belt. The  server computes
the optimal navigation policy to (independently) reach each of them from any
location in the warehouse.~~

3. ~~Each of the $$N$$ robots, distributed around the warehouse, is assigned a
package to pick up and place in their assigned belt. The server computes
the assignations based on:~~
   1. ~~For each package, it computes the cost of reaching such item from the
     current robot location + the cost of reaching the target belt from the
     package location.~~
   2. ~~Then, the robot is assigned the package of minimal cost.~~
   3. ~~It picks another robot and repeats.~~

4. ~~Once a robot's been assigned a package to transport, it starts
navigating the warehouse, according to the pre-computed policies,~~ caring
about collisions against walls and other robots.

5. ~~When a robot has delivered its package, it is assigned a new one, if
available; otherwise, it goes to any resting location until a new order
arrives, and it's assigned a new package to transport.~~
