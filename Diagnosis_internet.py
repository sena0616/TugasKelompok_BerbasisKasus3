"""Tugas 3 - Sistem Pakar Diagnosis Gangguan Internet
Forward chaining + backward chaining + conflict resolution.
Urutan resolusi: salience -> specificity -> rule order. Refractoriness berlaku.
"""

SALIENCE = {"Rendah": 1, "Sedang": 2, "Tinggi": 3, "Tertinggi": 4}

# (id, [premis], konklusi, salience)
RULES = [
    ("R1", ["Semua Situs Tidak Bisa Dibuka"], "Cek Router", "Rendah"),
    ("R2", ["Lampu Internet Router Merah"], "Gangguan Provider", "Sedang"),
    ("R3", ["Kecepatan Sangat Lambat"], "Gangguan Provider", "Sedang"),
    ("R4", ["Gangguan Provider", "Tagihan Sudah Dibayar"], "Lapor ke Provider", "Tinggi"),
    ("R5", ["Perangkat Lain Juga Offline"], "Gangguan Provider", "Sedang"),
    ("R6", ["Semua Situs Tidak Bisa Dibuka", "Hanya Laptop Ini Bermasalah"], "Masalah pada Laptop", "Tinggi"),
    ("R7", ["Gangguan Provider"], "Gunakan Tethering Sementara", "Rendah"),
    ("R8", ["Cek Router", "Router Terasa Panas"], "Matikan Router 10 Menit", "Tertinggi"),
]

FACTS = ["Semua Situs Tidak Bisa Dibuka", "Perangkat Lain Juga Offline", "Tagihan Sudah Dibayar"]


def rnum(r):
    return int(r[0][1:])


def forward_chaining(facts, verbose=True):
    wm = list(facts)
    fired = set()  # refractoriness: rule hanya boleh fire sekali dengan data sama
    trace = []
    it = 0
    while True:
        it += 1
        # 1. Match: conflict set = rule yang LHS-nya terpenuhi dan belum pernah fire
        cs = [r for r in RULES if all(p in wm for p in r[1]) and r[0] not in fired]
        # Rule yang konklusinya sudah ada di WM tetap masuk CS (refractoriness hanya
        # melarang fire ulang), sehingga jejaknya mengikuti slide "Jejak Lengkap Iterasi".
        if not cs:
            trace.append((it, [], None, None, None))
            break
        # 2. Choose: salience (desc) -> specificity (jumlah premis, desc) -> nomor rule (asc)
        chosen = sorted(cs, key=lambda r: (-SALIENCE[r[3]], -len(r[1]), rnum(r)))[0]
        # 3. Apply
        new = chosen[2] not in wm
        if new:
            wm.append(chosen[2])
        fired.add(chosen[0])
        trace.append((it, [r[0] for r in cs], chosen, chosen[2], new))
    return wm, trace


def explain_choice(cs_ids):
    """Jelaskan alasan pemilihan jika conflict set > 1 rule."""
    cs = [r for r in RULES if r[0] in cs_ids]
    best = sorted(cs, key=lambda r: (-SALIENCE[r[3]], -len(r[1]), rnum(r)))[0]
    top = [r for r in cs if SALIENCE[r[3]] == SALIENCE[best[3]]]
    if len(top) == 1:
        return f"{best[0]} dipilih karena salience {best[3]} tertinggi di conflict set."
    spec = [r for r in top if len(r[1]) == len(best[1])]
    if len(spec) == 1:
        return f"Salience sama ({best[3]}); {best[0]} paling spesifik ({len(best[1])} premis)."
    return (f"Salience sama ({best[3]}) dan spesifisitas sama ({len(best[1])} premis); "
            f"{best[0]} dipilih karena nomor rule terkecil.")


def backward_chaining(goal, facts, depth=0, log=None, visiting=None):
    """Kembalikan (terbukti?, log). Fakta yang tidak ada di WM dianggap tidak diketahui (gagal)."""
    if log is None:
        log = []
    if visiting is None:
        visiting = set()
    pad = "  " * depth
    if goal in facts:
        log.append(f"{pad}FindOut({goal}): ada di Fakta Awal -> TERBUKTI")
        return True, log
    if goal in visiting:
        log.append(f"{pad}FindOut({goal}): sedang ditelusuri (siklus) -> gagal")
        return False, log
    visiting = visiting | {goal}
    cands = [r for r in RULES if r[2] == goal]
    if not cands:
        log.append(f"{pad}FindOut({goal}): bukan fakta awal & tidak ada rule yang menyimpulkannya -> GAGAL")
        return False, log
    log.append(f"{pad}FindOut({goal}): rule kandidat (RHS) = {{{', '.join(r[0] for r in cands)}}}")
    for r in cands:
        log.append(f"{pad}  Monitor({r[0]}): JIKA {' DAN '.join(r[1])}")
        ok = True
        for p in r[1]:
            res, _ = backward_chaining(p, facts, depth + 2, log, visiting)
            if not res:
                ok = False
                log.append(f"{pad}  {r[0]} gagal karena '{p}' tidak terbukti")
                break
        if ok:
            log.append(f"{pad}  {r[0]} TERPENUHI -> '{goal}' TERBUKTI")
            return True, log
    log.append(f"{pad}FindOut({goal}): semua rule gagal -> GAGAL")
    return False, log


if __name__ == "__main__":
    print("=== (a) FORWARD CHAINING ===")
    print("Fakta awal:", FACTS)
    wm, trace = forward_chaining(FACTS)
    print(f"{'Iter':<5}{'Conflict set':<18}{'Dipilih':<9}{'Perubahan Working Memory'}")
    for it, cs, ch, concl, new in trace:
        if ch is None:
            print(f"{it:<5}{'{ }':<18}{'-':<9}berhenti, tidak ada aturan yang cocok")
        else:
            cs_s = "{" + ", ".join(cs) + "}"
            ch_s = ch[0]
            chg = f"+ ({concl})" if new else f"(tidak ada fakta baru: '{concl}' sudah ada)"
            print(f"{it:<5}{cs_s:<18}{ch_s:<9}{chg}")
    print("Working Memory akhir:")
    for f in wm:
        print("  -", f)

    print("\n=== (b) BACKWARD CHAINING: goal 'Lapor ke Provider' ===")
    ok, log = backward_chaining("Lapor ke Provider", FACTS)
    print("\n".join(log))
    print("HASIL:", "TERBUKTI" if ok else "TIDAK TERBUKTI")

    print("\n=== (c) CONFLICT RESOLUTION ===")
    for it, cs, ch, concl, new in trace:
        if len(cs) > 1:
            print(f"Iterasi {it}: CS = {cs}")
            for rid in cs:
                r = next(x for x in RULES if x[0] == rid)
                print(f"   {rid}: salience={r[3]}, jumlah premis={len(r[1])}")
            print("   ->", explain_choice(cs))