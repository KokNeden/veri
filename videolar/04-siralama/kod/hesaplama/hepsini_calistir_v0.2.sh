#!/usr/bin/env bash
# Sıralama v0.2 (24 madde, plan açığı birincil ölçüt). 05-siralama-sonucu/ klasöründen:  bash kod/hepsini_calistir_v0.2.sh
set -euo pipefail
cd "$(dirname "$0")/.."
PY=../04-siralama-yontemi/kod/.venv/bin/python
export PYTHONPATH=../04-siralama-yontemi/kod
$PY kod/plan_hedefleri_03.py                          # veri/plan_hedefleri.csv (birincil ölçüt)
$PY kod/girdileri_hazirla.py                          # veri/ : sorunlar, matris, gerekçeler, göstergeler
$PY -m kokneden_siralama.calistir --girdi veri --cikti cikti --n 10000 --etiket v0.2
echo "Tamam: cikti/*_v0.2.*"
