from .calculator import CHEONGAN, GANJI, CHEONGAN_OHANG, GANJI_OHANG

DAEUN_TABLE = {
    '양': [6, 16, 26, 36, 46, 56, 66, 76, 86, 96],
    '음': [5, 15, 25, 35, 45, 55, 65, 75, 85, 95],
}

def calculate_daeun(saju, gender='남', year=2026):
    y_stem_idx = saju['year']['stem_idx']
    y_gan = CHEONGAN[y_stem_idx].strip()
    y_umyang = '양' if y_stem_idx % 2 == 0 else '음'

    if gender == '남':
        direction = '순행' if y_umyang == '양' else '역행'
    else:
        direction = '순행' if y_umyang == '음' else '역행'

    birth_year = year - 30
    daeun_start = DAEUN_TABLE[y_umyang][0]

    daeuns = []
    for i in range(10):
        age = daeun_start + i * 10
        d_stem = (saju['month']['stem_idx'] + (i + 1) * (1 if direction == '순행' else -1)) % 10
        d_branch = (saju['month']['branch_idx'] + (i + 1) * (1 if direction == '순행' else -1)) % 12
        daeuns.append({
            'age': f"{age}~{age + 9}세",
            'ganji': f"{CHEONGAN[d_stem]}{GANJI[d_branch]}",
        })

    seun_stem = (saju['year']['stem_idx'] + (year - birth_year)) % 10
    seun_branch = (saju['year']['branch_idx'] + (year - birth_year)) % 12

    return {
        'direction': direction,
        'daeun_start_age': f"{daeun_start}세",
        'daeuns': daeuns,
        'seun': f"{CHEONGAN[seun_stem]}{GANJI[seun_branch]}",
    }
