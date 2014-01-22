for i in {1..17}; do  cut -d '       ' -f $i,18 MIC_genus.csv >${i}_genus.txt; done

for f in *genus.txt; do d="$(head -1 "$f" | awk '{print $1}')_genus.txt"; if [ ! -f "$d" ]; then mv "$f" "$d"; else echo "File '$d' already exists! Skiped '$f'"; fi; done

