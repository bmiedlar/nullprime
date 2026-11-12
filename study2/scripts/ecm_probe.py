import csv, multiprocessing as mp, time
from sympy.ntheory.ecm import ecm

def run(n, q):
    q.put(ecm(n, B1=100000, B2=1000000, max_curve=100, seed=42))

rows = list(csv.DictReader(open("/nl.csv"))) + list(csv.DictReader(open("/pilot.csv")))
hard = [int(r["n"]) for r in rows if r["split"] == "hard"][:6]
for n in hard:
    q = mp.Queue()
    p = mp.Process(target=run, args=(n, q))
    t = time.time()
    p.start()
    p.join(60)
    if p.is_alive():
        p.terminate()
        print(str(n)[:12], "no result in 60s", flush=True)
    else:
        print(str(n)[:12], "exit", p.exitcode, round(time.time() - t, 1), "s", "FOUND" if not q.empty() else "none", flush=True)
