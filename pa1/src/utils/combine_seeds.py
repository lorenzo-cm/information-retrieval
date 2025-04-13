import glob

arquivos = glob.glob("seeds/seeds-*.txt")

seeds = set()

for arquivo in arquivos:
    with open(arquivo, "r", encoding="utf-8") as f:
        for linha in f:
            link = linha.strip()
            if link:
                seeds.add(link)

with open("seeds-all.txt", "w", encoding="utf-8") as f:
    for seed in sorted(seeds):
        f.write(seed + "\n")