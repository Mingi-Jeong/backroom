from datetime import datetime, date

CHEONGAN = ['갑', ' 을', ' 병', ' 정', ' 무', ' 기', ' 경', ' 신', ' 임', ' 계']
GANJI = ['자', '축', '인', '묘', '진', '사', '오', '미', '신', '유', '술', '해']

CHEONGAN_OHANG = {'갑':'목','을':'목','병':'화','정':'화','무':'토','기':'토','경':'금','신':'금','임':'수','계':'수'}
GANJI_OHANG = {'자':'수','축':'토','인':'목','묘':'목','진':'토','사':'화','오':'화','미':'토','신':'금','유':'금','술':'토','해':'수'}
CHEONGAN_UMYANG = {'갑':'양','을':'음','병':'양','정':'음','무':'양','기':'음','경':'양','신':'음','임':'양','계':'음'}
GANJI_UMYANG = {'자':'양','축':'음','인':'양','묘':'음','진':'양','사':'음','오':'양','미':'음','신':'양','유':'음','술':'양','해':'음'}

MONTH_STEM_START = {0:2, 2:4, 4:6, 6:8, 8:0}

HOURLY_BRANCHES = [3,4,5,6,7,8,9,10,11,0,1,2]

SOLAR_TERMS_DAY = [4, 6, 6, 5, 6, 6, 7, 8, 8, 8, 7, 6]

def _days_from_1900(y, m, d):
    total = 0
    for year in range(1900, y):
        total += 366 if (year % 4 == 0 and year % 100 != 0) or year % 400 == 0 else 365
    for month in range(1, m):
        if month in [1,3,5,7,8,10,12]:
            total += 31
        elif month in [4,6,9,11]:
            total += 30
        else:
            total += 29 if (y % 4 == 0 and y % 100 != 0) or y % 400 == 0 else 28
    total += d - 1
    return total

def _year_stem_branch(y):
    stem = (y - 4) % 10
    branch = (y - 4) % 12
    return stem, branch

def _month_stem_branch(y, m):
    y_stem = (y - 4) % 10
    start_stem = MONTH_STEM_START[y_stem // 2 * 2]
    month_idx = (m + 1) % 12
    stem = (start_stem + (m - 1)) % 10
    return stem, month_idx

def _day_stem_branch(y, m, d):
    days = _days_from_1900(y, m, d)
    stem = (days + 6) % 10
    branch = days % 12
    return stem, branch

def _hour_stem_branch(d_stem, h):
    h_branch = HOURLY_BRANCHES[h // 2 if h % 2 == 0 else (h - 1) // 2]
    h_stem = (d_stem % 5 * 2 + h_branch % 10) % 10
    return h_stem, h_branch

def calculate_saju(year, month, day, hour=12, minute=0):
    ipchun_day = 4
    if month == 1 or (month == 2 and day < ipchun_day):
        sj_year = year - 1
    else:
        sj_year = year

    m_start_day = SOLAR_TERMS_DAY[month - 1]
    adj_month = month - 1 if day < m_start_day else month
    if adj_month == 0:
        sm_year = sj_year - 1 if sj_year > 1900 else sj_year
        adj_month = 12
    else:
        sm_year = sj_year
    if month == 1 and day < ipchun_day:
        adj_year = year - 1
    elif month == 12 and day >= SOLAR_TERMS_DAY[11]:
        adj_year = year + 1
    else:
        adj_year = year

    y_stem, y_branch = _year_stem_branch(sj_year)
    m_stem, m_branch = _month_stem_branch(sm_year, adj_month)
    d_stem, d_branch = _day_stem_branch(year, month, day)
    h_stem, h_branch = _hour_stem_branch(d_stem, hour)

    return {
        'year': {'stem': CHEONGAN[y_stem], 'branch': GANJI[y_branch], 'stem_idx': y_stem, 'branch_idx': y_branch},
        'month': {'stem': CHEONGAN[m_stem], 'branch': GANJI[m_branch], 'stem_idx': m_stem, 'branch_idx': m_branch},
        'day': {'stem': CHEONGAN[d_stem], 'branch': GANJI[d_branch], 'stem_idx': d_stem, 'branch_idx': d_branch},
        'hour': {'stem': CHEONGAN[h_stem], 'branch': GANJI[h_branch], 'stem_idx': h_stem, 'branch_idx': h_branch},
    }

def format_saju(saju):
    return f"{saju['year']['stem']}{saju['year']['branch']}년 {saju['month']['stem']}{saju['month']['branch']}월 {saju['day']['stem']}{saju['day']['branch']}일 {saju['hour']['stem']}{saju['hour']['branch']}시"
