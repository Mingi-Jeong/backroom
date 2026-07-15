from .calculator import CHEONGAN_OHANG, GANJI_OHANG
from .elements import ELEMENT_PRODUCING, ELEMENT_CONTROLLING

def analyze_compatibility(saju1, saju2):
    pillars = ['year', 'month', 'day', 'hour']
    score = 0
    details = []

    for p in pillars:
        s1 = saju1[p]['stem'].strip()
        s2 = saju2[p]['stem'].strip()
        b1 = saju1[p]['branch'].strip()
        b2 = saju2[p]['branch'].strip()

        e1_s = CHEONGAN_OHANG[s1]
        e2_s = CHEONGAN_OHANG[s2]
        e1_b = GANJI_OHANG[b1]
        e2_b = GANJI_OHANG[b2]

        for e1, e2, part in [(e1_s, e2_s, f"{p}천간"), (e1_b, e2_b, f"{p}지지")]:
            if e1 == e2:
                score += 2
                details.append(f"{part}: {e1}←→{e2} 동일 (조화)")
            elif ELEMENT_PRODUCING.get(e1) == e2:
                score += 3
                details.append(f"{part}: {e1}→{e2} 상생 (좋음)")
            elif ELEMENT_PRODUCING.get(e2) == e1:
                score += 1
                details.append(f"{part}: {e1}←{e2} 역생 (보통)")
            elif ELEMENT_CONTROLLING.get(e1) == e2:
                score -= 1
                details.append(f"{part}: {e1}克制{e2} 상극 (주의)")
            elif ELEMENT_CONTROLLING.get(e2) == e1:
                score -= 1
                details.append(f"{part}: {e1}被{e2}克制 역극 (주의)")

    if score >= 40:
        level = '매우 좋음'
    elif score >= 30:
        level = '좋음'
    elif score >= 20:
        level = '보통'
    elif score >= 10:
        level = '주의'
    else:
        level = '어려움'

    return {
        'score': score,
        'level': level,
        'max_score': 48,
        'details': details,
    }
