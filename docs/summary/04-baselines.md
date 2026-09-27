# Baselines

v4 sees only its one most threatening neighbour (22 inputs). Each baseline below is compared against it.

- **No-op** never maneuvers. It shows how many close approaches happen if nobody acts.
- **Collinear** is the traditional method. When a predicted miss is within 1 km, it burns along the orbital track only.
- **Fixed radius** is a trained policy that sees the 4 nearest objects within 1,000 km (67 inputs). It tests picking neighbours by distance instead of by threat.
- **Global observability** is a trained policy that sees every moving object (2,707 inputs at 150 satellites). It tests dropping neighbour selection entirely. Its input size depends on the number of satellites, so it cannot run at other sizes.
