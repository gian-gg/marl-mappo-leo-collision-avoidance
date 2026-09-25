#!/usr/bin/env bash
# One ablation model, seed 42. Usage: run_ablations.sh <radius|control|global>
cd ~/thesis/orbit_zoo
MODEL=$1
SEED=${2:-42}

train () {   # config, output, extra
  echo "=== $2 started $(date '+%H:%M:%S')"
  nice -n 10 .venv/bin/oz train --config "$1" --output "$2" --seed "$SEED" $3 || true
  if [ ! -f "$2/checkpoints/latest.pt" ]; then echo "FAILED: $2"; exit 1; fi
  echo "=== $2 done $(date '+%H:%M:%S')"
}

case "$MODEL" in
  radius)   # fixed width, so it keeps the 16 -> 64 -> 150 curriculum
    train configs/mappo_radius_stage1.json runs/radius_stage1 ""
    train configs/mappo_radius_stage2.json runs/radius_stage2 "--initial-actor runs/radius_stage1/checkpoints/latest.pt"
    train configs/mappo_radius_stage3.json runs/radius_stage3 "--initial-actor runs/radius_stage2/checkpoints/latest.pt"
    ;;
  control|global)   # 150 agents only; entropy 0.05 for 125 updates, then 0.01 for 245
    train "configs/mappo_${MODEL}_phase1.json" "runs/${MODEL}_phase1" ""
    train "configs/mappo_${MODEL}_phase2.json" "runs/${MODEL}_phase2" "--initial-actor runs/${MODEL}_phase1/checkpoints/latest.pt"
    ;;
  *) echo "usage: $0 <radius|control|global> [seed]"; exit 1 ;;
esac
echo "=== $MODEL complete $(date '+%H:%M:%S')"
