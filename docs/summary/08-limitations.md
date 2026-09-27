# Limitations

## Evidence

- **Few seeds.** v4 was trained with two seeds (7.45 and 7.05 close approaches). Each ablation was trained with one.
- **Single runs at scale.** Each scalability size is one 6-hour run, so differences of 1 to 3 conjunctions are not meaningful.
- **Scalability is not held out.** The catalog sweep includes satellites the policy trained against. The benchmarks are the clean held-out test.
- **Global got one retry.** Global observability failed after one retuning attempt, not a full search.

## Data

- **Synthetic threats.** Training and benchmark threats are constructed on real close-call geometry, and satellite-pair partners fly constructed orbits.
- **One catalog snapshot.** Calibration and scalability use one frozen TLE catalog. The catalog's source, download date and labelling rules are not yet documented.
- **Overlapping threats are rare.** They are where v4 does best, but in real LEO threats to one satellite arrive about one orbit apart, even at 8× density.

## Physics

- **No drag** in the training environment. Gravity is point mass plus J2.
- **No uncertainty.** Close approaches use a fixed 1 km miss distance, not collision probability. A pass at 999 m counts as a failure and one at 1,001 m as a success.
- **SGP4 and TLEs** are fine for screening but are not operational conjunction assessment.

## Design choices

- **Δv rule changed after first results.** The first rule assumed a guaranteed 6-minute warning and picked 2 m/s. The adopted rule uses measured warning times and picks 0.5 m/s.
- **Assumed hardware.** Satellite masses (300 and 800 kg) are assumptions. The 7 N thruster is stronger than the electric propulsion most LEO constellations use.
- **No station-keeping.** The policy only avoids. Drift from the slot and the fuel to return are calculated, not flown.
