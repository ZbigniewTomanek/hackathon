#!/bin/bash

# Base command
BASE_CMD="PYTHONPATH=./:$PYTHONPATH uv run biohack_attack/generate_hypothesis.py"
INPUT_FILE="../data/C_Reactive_Protein__CRP_.json"
OUTPUT_BASE="biohack_attack/output"

# Different configurations to test
configs=(
    "--threads 8 --hypotheses 3 --top-k 2"
    "--threads 16 --hypotheses 5 --top-k 2"
    "--threads 32 --hypotheses 7 --top-k 3"
    "--threads 64 --hypotheses 10 --top-k 3"
)

# Run each configuration
for config in "${configs[@]}"; do
    echo "Running configuration: $config"
    timestamp=$(date +%Y-%m-%d-%H-%M-%S)
    output_dir="${OUTPUT_BASE}/benchmark_${timestamp}"
    
    $BASE_CMD -f "$INPUT_FILE" -o "$output_dir" $config
    
    echo "Completed configuration: $config"
    echo "----------------------------------------"
done
