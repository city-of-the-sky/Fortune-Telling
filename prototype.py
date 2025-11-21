# -*- encoding: UTF-8 -*-

def get_yearly_pillar(year): # type: (int) -> str
    '주어진 서기 년을 즉 연간으로 변환합니다.'
    stems = ['갑', '을', '병', '정', '무', '기', '경', '신', '임', '계']
    branches = ['자', '축', '인', '묘', '진', '사', '오', '미', '신', '유', '술', '해']
    return stems[(year - 4) % 10] + branches[(year - 4) % 12]

def get_monthly_pillar(stem, month): # type: (str, int) -> str
    '주어진 천간과 월을 월간으로 변환합니다.'
    branches = {
        ('갑', '기'): ('병인', '정묘', '무진', '기사', '경오', '신미', '임신', '계유', '갑술', '을해', '병자', '정축'),
        ('을', '경'): ('무인', '기묘', '경진', '신사', '임오', '계미', '갑신', '을유', '병술', '정해', '무자', '기축'),
        ('병', '신'): ('경인', '신묘', '임진', '계사', '갑오', '을미', '병신', '정유', ' 무술', '기해', '경자', '신축'),
        ('정', '임'): ('임인', '계묘', '갑진', '을사', '병오', '정미', '무신', '기유', ' 경술', '신해', '임자', '계축'),
        ('무', '계'): ('갑인', '을묘', '병진', '정사', '무오', '기미', '경신', '신유', ' 임술', '계해', '갑자', '을축'),
    }
    key = filter(lambda key: stem in key, branches)
    return branches[next(key)][month - 2]

def get_daily_pillar():
    raise NotImplementedError

yearly = get_yearly_pillar(2025)
print(yearly)
monthly = get_monthly_pillar(yearly[0], 5)
print(monthly)
