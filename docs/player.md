
# Player

## Attributes

### Fuel Amount

The fuel amount is a constantly decreasing variable which represents how long the train can keep running. Fuel is consumed passively but can be gambled by using a boost which has a lower distance-consumption ratio but grants a speed boost to the player.

### Position

The x-position of the front of the train. Relative to the start of the page.

### Speed

```
(top, bottom) = 30 pixels / 1 second

if tick % bottom == 0
    position += top
```

### Page

The index of the page that the train is currently on.

### Track

The index of the track that the train is on. This also accounts for switches. If the track index is >= the number of tracks then the train is on a switch. `track - number of tracks = switch index`.

### Boost Time

The time that the boost will end. `is_boosted = time < boost_time`

### Max Speed

The top speed (without boost) that the train can get to with its current weight.

### Boost Amount

The multiplier e.g.: 110% That is applied to the [max speed](#max-speed) to get the target speed when boosting.

### Acceleration

The rate that the [speed variable](#speed) is moved towards [top speed](#max-speed)

### Deceleration

The rate that the [speed variable](#speed) is reduced to [top speed](#max-speed)

## Methods

- [Update](#update)
- [Activate](#activate-boost)
- Fuel Height?
  
### Update

Calculate the upper bound for the speed of this frame

```
    target_speed = max_speed

    if boost_time > time then 
        target_speed *= boost_amount
    end if
```

Move the current speed towards the target speed
```
    if speed < target_speed then
        speed += acceleration
    else
        speed -= deceleration
    end if
```
Apply the speed by updating the position
```
    position += speed * delta
```

### Activate Boost



