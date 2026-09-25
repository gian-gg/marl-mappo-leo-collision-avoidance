#!/usr/bin/env bash
# Retuned global-observability ablation: lower entropy, higher phase-1 actor LR.
cd ~/thesis/orbit_zoo
SEED=${1:-42}

train () {
  echo "=== $2 started $(date '+%H:%M:%S')"
  nice -n 10 .venv/bin/oz train --config "$1" --output "$2" --seed "$SEED" $3 || true
  if [ ! -f "$2/checkpoints/latest.pt" ]; then echo "FAILED: $2"; exit 1; fi
  echo "=== $2 done $(date '+%H:%M:%S')"
}

train configs/mappo_global2_phase1.json runs/global2_phase1 ""
train configs/mappo_global2_phase2.json runs/global2_phase2 "--initial-actor runs/global2_phase1/checkpoints/latest.pt"

echo "=== training complete $(date '+%H:%M:%S')"

.venv/bin/oz evaluate --config configs/eval_global.json --episodes 20 \
  --policy noop --policy "global2=runs/global2_phase2/checkpoints/latest.pt" \
  --output runs/abl_eval_global2
.venv/bin/oz evaluate --config configs/eval_global_mt100.json --episodes 20 \
  --policy noop --policy "global2=runs/global2_phase2/checkpoints/latest.pt" \
  --output runs/abl_eval_global2_mt100

echo "=== global2 complete $(date '+%H:%M:%S')"
