from .calculator import CHEONGAN, GANJI, CHEONGAN_OHANG, GANJI_OHANG, CHEONGAN_UMYANG, GANJI_UMYANG

ELEMENTS_ORDER = ['목', '화', '토', '금', '수']
ELEMENT_COLORS = {'목':'초록', '화':'빨강', '토':'노랑', '금':'하양', '수':'검정'}
ELEMENT_SEASONS = {'목':'봄', '화':'여름', '토':'환절기', '금':'가을', '수':'겨울'}
ELEMENT_DIRECTIONS = {'목':'동', '화':'남', '토':'중앙', '금':'서', '수':'북'}
ELEMENT_ORGANS = {'목':'간·담', '화':'심장·소장', '토':'비·위', '금':'폐·대장', '수':'신장·방광'}
ELEMENT_EMOTIONS = {'목':'분노', '화':'기쁨', '토':'생각', '금':'슬픔', '수':'두려움'}

ELEMENT_PRODUCING = {'목':'화', '화':'토', '토':'금', '금':'수', '수':'목'}
ELEMENT_CONTROLLING = {'목':'토', '토':'수', '수':'화', '화':'금', '금':'목'}

def analyze_saju_elements(saju):
    pillars = ['year', 'month', 'day', 'hour']
    element_count = {'목':0, '화':0, '토':0, '금':0, '수':0}
    umyang = {'양':0, '음':0}

    for p in pillars:
        s = saju[p]['stem']
        b = saju[p]['branch']
        e1 = CHEONGAN_OHANG[s.strip()]
        e2 = GANJI_OHANG[b.strip()]
        element_count[e1] += 1
        element_count[e2] += 1
        u1 = CHEONGAN_UMYANG[s.strip()]
        u2 = GANJI_UMYANG[b.strip()]
        umyang[u1] += 1
        umyang[u2] += 1

    present = [e for e in ELEMENTS_ORDER if element_count[e] > 0]
    missing = [e for e in ELEMENTS_ORDER if element_count[e] == 0]
    strong = max(element_count, key=element_count.get)
    weak = min(element_count, key=element_count.get)
    balance = '음' if umyang['음'] > umyang['양'] else '양' if umyang['양'] > umyang['음'] else '중립'

    return {
        'counts': element_count,
        'present': present,
        'missing': missing,
        'strongest': strong,
        'weakest': weak,
        'balance': balance,
        'umyang': umyang,
    }

def get_harmony_advice(elements):
    lines = []
    counts = elements['counts']
    present = elements['present']

    for e in present:
        produced = ELEMENT_PRODUCING[e]
        if counts[produced] > 0:
            lines.append(f"{e}이(가) {produced}을(를) 생성하여 좋은 흐름입니다.")
        else:
            lines.append(f"{e}이(가) 있지만 {produced}이(가) 없어 생성 관계가 약합니다.")

    for e in present:
        controlled = ELEMENT_CONTROLLING[e]
        if counts[controlled] > 0:
            lines.append(f"{e}이(가) {controlled}을(를) 제어하여 균형을 잡아줍니다.")

    if elements['missing']:
        lines.append(f"부족한 오행: {', '.join(elements['missing'])} - 해당 오행을 보완하는 것이 좋습니다.")

    lines.append(f"가장 강한 오행: {elements['strongest']}")
    lines.append(f"음양 균형: {elements['balance']} (양:{elements['umyang']['양']}, 음:{elements['umyang']['음']})")
    return lines
