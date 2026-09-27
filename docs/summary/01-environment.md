# Environment

Each controlled satellite is an agent. All agents share one policy (the actor) and act at the same time every 120 s. Orbits are propagated with Orekit. An episode is 25 decisions, about 50 minutes.

During training, a critic sees the whole scene and helps the actor learn. Only the actor is used after training.

## What the actor sees (22 inputs)

- **Itself (7):** position, velocity, and fuel left.
- **Its most threatening neighbour (15):** relative position and velocity, time to closest approach, predicted miss distance, combined size, whether the neighbour can maneuver, its fuel, a valid flag, and the direction the miss will fall in.

Threats are ranked by predicted miss and time to closest approach. The top one is predicted along curved orbits (gravity plus Earth's flattening, J2). The input size does not depend on how many satellites there are, which is what lets v4 run at 10,000 satellites.

## What it can do (7 actions)

- No burn
- Prograde or retrograde (along the track)
- Radial out or in
- Cross-track either way

Each burn is 0.5 m/s at up to 7 N, finished within 60 s.

## What it is rewarded for

| Term | Reward |
|---|---|
| Collision | −100, and the episode ends |
| Close approach under 1 km | −10, plus −30 × how deep inside 1 km it got |
| Fuel | −1 per m/s burned |
| Impossible burn | −2 |
| Shaping | reward for widening the predicted miss, penalty for narrowing it |

Shaping gives feedback before the encounter happens, and it does not change which policy is best.
