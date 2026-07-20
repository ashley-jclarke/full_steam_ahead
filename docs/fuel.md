# Fuel


**let S** *= starting mass of fuel*

**let** R *= rate that fuel is burnt*

**let u** *= base speed without burning fuel*


**The distance the train can travel in the given time.**

$$s\left(t\right)=\{S-Rt\geq0: ut+ \frac{1}{2}Rt^2, s\left(\frac{S}{R}\right)\}\{t\geq\}$$

**The max distance a train can travel (if going at top speed for the duration)**

$$s_{\mathrm{max}}=s\left(\frac{S}{R}\right)$$

**The distance the train can travel in the given time.**

$$v(t)=\{S-Rt\geq0: S-max(S-Rt, 0) + u, 0\} \{t\geq0\}$$


## What does this mean?

- Refuel locations need to have a distance much less than $s_{\mathrm{max}}$ apart. 

[distance-time/speed-time](fuel_graph.png)