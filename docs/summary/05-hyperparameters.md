# Hyperparameters

v4's settings, from `configs/mappo_stage{1,2,3}.json`. Seed 42.

## MAPPO

| Setting | Value |
|---|---:|
| Actor hidden layers | 128, 64 |
| Critic hidden layers | 256, 128 |
| Actor learning rate | 1 × 10⁻⁴ |
| Critic learning rate | 1 × 10⁻³ |
| Discount (γ) | 0.99 |
| GAE λ | 0.95 |
| PPO clip | 0.2 |
| Value clip | 0.2 |
| Value loss coefficient | 0.5 |
| Max gradient norm | 0.5 |
| Epochs per update | 4 |
| Minibatch size | 512 |

## By stage

| Setting | Stage 1 | Stage 2 | Stage 3 |
|---|---:|---:|---:|
| Satellites | 16 | 64 | 150 |
| Updates | 125 | 110 | 135 |
| Entropy bonus | 0.05 | 0.01 | 0.01 |
| Environment steps per update | 250 | 100 | 50 |
| Episodes per update | 10 | 4 | 2 |
| Agent samples per update | 4,000 | 6,400 | 7,500 |

Each stage starts from the previous stage's actor and a new critic.

## Environment and reward

| Setting | Value |
|---|---:|
| Decision interval (Δt) | 120 s |
| Episode length | 25 decisions |
| Neighbours (k) | 1 |
| Burn size (Δv) | 0.5 m/s |
| Max thrust | 7 N |
| Max burn duration | 60 s |
| Specific impulse | 300 s |
| Safe separation | 1 km |
| Screening horizon | 30 min |
| Collision penalty | −100 |
| Close-approach penalty | −30 × shortfall |
| Flat close-approach penalty | −10 |
| Fuel penalty | −1 per m/s |
| Impossible-burn penalty | −2 |
| Shaping weight | 30 |
