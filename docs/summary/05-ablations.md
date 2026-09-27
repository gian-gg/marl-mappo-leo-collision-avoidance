# How the ablations were trained

## Fixed radius

- **Training:** same 16 → 64 → 150 curriculum as v4. Only the observation changes.
- **What happened:** it never became confident. Entropy stopped at 0.53 against v4's 0.07, and the last stage added nothing.
- **Result:** avoids 7.4% of no-op's close approaches, against v4's 92.6%.
- **Why:** the object about to hit you is usually far away and closing fast. v4's chosen threat is a median of 4,457 km away and falls inside 1,000 km only 7.6% of the time.

## Global observability

- **Training:** its input size depends on the number of satellites, so it cannot use the curriculum. It was trained at a fixed 150 satellites in two phases.
- **Attempt 1:** did not learn. Settings tuned for v4's 22 inputs do not suit a network with 2,707. This counts as a failed run, not a result.
- **Attempt 2:** lower entropy bonus and higher learning rate. It trained cleanly, but learned only to stop burning. All of the improvement was saved fuel.
- **Result:** never maneuvers in evaluation. Avoids 0%, identical to no-op.

## Takeaways

- Picking neighbours by distance misses the threats that matter.
- Seeing everything does not help. The policy cannot learn which object to act on, so it does nothing.
- A training run can look healthy and still produce a useless policy. Safety is judged by close approaches, not training return.

**Control:** a copy of v4's setup, trained in the same two phases as global, scores the same as v4 (6.65 vs 7.45 close approaches). The ablations lose because of what they see, not how they were trained.
