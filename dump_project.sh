#!/bin/bash

# Usage: ./dump_project.sh [project_root] [output_file]
PROJECT_ROOT="${1:-.}"
OUTPUT_FILE="${2:-project_dump.txt}"

# Hard skip these — nothing useful inside
SKIP_DIRS="venv|.venv|env|__pycache__|.git|.mypy_cache|.pytest_cache|dist|build|.next|coverage|.tox|node_modules|*.egg-info"

> "$OUTPUT_FILE"

echo "================================================================" >> "$OUTPUT_FILE"
echo "  PROJECT DUMP: $(realpath $PROJECT_ROOT)" >> "$OUTPUT_FILE"
echo "  Generated: $(date)" >> "$OUTPUT_FILE"
echo "================================================================" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

# Find ALL files, skip only truly useless dirs and binary files
find "$PROJECT_ROOT" -type f \
  | grep -Ev "/($SKIP_DIRS)/" \
  | grep -Ev "\.(pyc|pyo|pyd|so|dylib|dll|exe|bin|jpg|jpeg|png|gif|svg|ico|pdf|zip|tar|gz|lock)$" \
  | sort \
  | while read -r filepath; do

    # Skip files larger than 500KB (likely generated/binary)
    filesize=$(wc -c < "$filepath" 2>/dev/null || echo 0)
    if [ "$filesize" -gt 512000 ]; then
      continue
    fi

    echo "----------------------------------------------------------------" >> "$OUTPUT_FILE"
    echo "FILE: $filepath" >> "$OUTPUT_FILE"
    echo "SIZE: $filesize bytes" >> "$OUTPUT_FILE"
    echo "----------------------------------------------------------------" >> "$OUTPUT_FILE"
    cat "$filepath" >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE"
  done

echo "================================================================" >> "$OUTPUT_FILE"
echo "END OF DUMP" >> "$OUTPUT_FILE"
echo "================================================================" >> "$OUTPUT_FILE"

FILE_COUNT=$(grep -c '^FILE:' "$OUTPUT_FILE")
echo "Done! → $OUTPUT_FILE"
echo "Files captured : $FILE_COUNT"
echo "Total size     : $(du -sh $OUTPUT_FILE | cut -f1)"
