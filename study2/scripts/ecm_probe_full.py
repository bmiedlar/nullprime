"""Pre-registered ECM probe: each hard item, ecm(n, B1=100000, B2=1000000, max_curve=100, seed=42), 60 s. Runs in the sandbox."""
import csv, multiprocessing as mp, time
from sympy.ntheory.ecm import ecm


def run(n, q):
    q.put(sorted(ecm(n, B1=100000, B2=1000000, max_curve=100, seed=42)))


if __name__ == "__main__":
    rows = [r for r in csv.DictReader(open("/items.csv")) if r["split"] == "hard"]
    with open("/out/ecm-probe.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["n", "result", "seconds"])
        for r in rows:
            q = mp.Queue()
            p = mp.Process(target=run, args=(int(r["n"]), q))
            t = time.time()
            p.start()
            p.join(60)
            if p.is_alive():
                p.terminate()
                res = "timeout"
            else:
                res = "factored" if not q.empty() and len(q.get()) > 1 else "no factor"
            w.writerow([r["n"], res, round(time.time() - t, 1)])
            fh.flush()
            print(res, flush=True)
