# Fuel trade-off

The adopted policy spends 23–28% more delta-v than the rule. This sweep asks what that
buys, by retraining the whole curriculum at four values of `delta_v_penalty_per_mps`
and measuring where each lands.

## Result

Charging more for fuel does not produce an efficient policy. It removes the behaviour
the policy's advantage depends on.

| Variant | Penalty | Burn costs | Close approaches | Delta-v | Margin over the rule |
| --- | ---: | ---: | ---: | ---: | ---: |
| Rule | — | — | 10.40 | **0.670** | — |
| **v4 (adopted)** | 1.0 | 0.5 | **7.45** | 0.860 | **+2.9 pt** |
| fuel2 | 2.0 | 1.0 | 8.40 | 0.804 | +2.0 pt |
| fuel4 | 4.0 | 2.0 | 13.45 | 0.783 | −3.0 pt |
| fuel8 | 8.0 | 4.0 | 52.05 | 0.513 | −41.2 pt |

150 agents, 20 held-out episodes, `configs/eval_stage3.json`. Margin is the share of
no-op close approaches resolved, against the rule's 89.7%.

The exchange rate is poor throughout. fuel2 saves 0.057 m/s and costs 0.95 close
approaches per episode; fuel4 saves 0.077 and costs 6.00, which puts it behind the
rule on safety while still spending more fuel than it. Only fuel8 reaches the rule's
delta-v, and it resolves less than half of what a coasting constellation suffers.

## The advantage is the extra burning

Repeating the comparison where double threats are 100% of the mix
([MULTITHREAT_BENCHMARK.md](MULTITHREAT_BENCHMARK.md)) shows what the penalty is
actually removing:

| Variant | Penalty | Margin over the rule |
| --- | ---: | ---: |
| v4 | 1.0 | **+7.6 pt** |
| fuel2 | 2.0 | +5.6 pt |
| fuel4 | 4.0 | +1.8 pt |
| fuel8 | 8.0 | −32.2 pt |

The margin falls monotonically with the penalty. Every difference is significant when
paired across the same 20 episodes: fuel2 against v4 gives p = 0.0014 under stress and
p = 0.045 on the standard benchmark; fuel4 gives p = 0.0002 and p = 0.0001.

A burn-level count at 64 agents found that 27% of the actor's burns fire when no
threat is flagged — when the predicted miss is still beyond the safe separation. Those
burns are not waste. They are the policy acting *before* a conjunction develops, which
is something the rule cannot do: its trigger requires the predicted miss to be inside
the threshold already. Charging more for fuel removes exactly those burns, and the
advantage goes with them.

## Pareto frontier

| Policy | Close approaches | Delta-v | Status |
| --- | ---: | ---: | --- |
| Rule | 10.40 | 0.670 | frontier |
| fuel2 | 8.40 | 0.804 | frontier |
| v4 | 7.45 | 0.860 | frontier |
| fuel4 | 13.45 | 0.783 | dominated by the rule |
| fuel8 | 52.05 | 0.513 | frontier, but resolves 48.6% |

fuel4 is strictly worse than the rule on both axes: more close approaches and more
delta-v.

## Adopted

v4 is kept. fuel2 is a legitimate frontier point if propellant ever becomes the
binding constraint — 6.5% less delta-v for 12.7% more close approaches — but it gives
up a quarter of the multi-threat margin for a saving that is small next to what it
costs. No variant reaches the rule's delta-v while remaining safer than it.

## Method

```sh
# one curriculum per variant, three in parallel on 20 cores
./runs/fuel_curriculum.sh 2      # configs/mappo_fuel2_stage{1,2,3}.json
./runs/fuel_curriculum.sh 4
./runs/fuel_curriculum.sh 8

.venv/bin/oz evaluate --config configs/eval_stage3.json \
  --policy noop --policy rule \
  --policy v4=runs/v4_stage3/checkpoints/latest.pt \
  --policy fuel2=runs/fuel2_stage3/checkpoints/latest.pt \
  --policy fuel4=runs/fuel4_stage3/checkpoints/latest.pt \
  --policy fuel8=runs/fuel8_stage3/checkpoints/latest.pt \
  --episodes 20 --output runs/fuel_eval_stage3
```

Each variant differs from the adopted configuration only in
`rewards.delta_v_penalty_per_mps`; seed, entropy, scenario mix and every other weight
are identical. Artifacts: `runs/fuel{2,4,8}_stage3`, `runs/fuel_eval_stage3`,
`runs/fuel_eval_mt100`.

## Limitations

- **One seed per variant.** Seeds 42 and 7 of the adopted configuration differ by 0.40
  close approaches per episode, so differences smaller than that are not resolvable.
  fuel2's gap of 0.95 is above it; the ordering of fuel2 against v4 is not.
- **One lever.** Only the delta-v penalty was varied. The flat close-approach penalty,
  the shaping weight and the maneuver magnitude would each move the frontier
  differently.
- **Fixed maneuver size.** Every burn is 0.5 m/s. A policy able to choose smaller burns
  might reach parts of the frontier none of these variants can.
