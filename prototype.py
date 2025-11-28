from sqlite3 import Connection
from collections import namedtuple

Element = namedtuple('Element', ['name', 'sign'])

class FourPillarsReading:
    elements = {
        **dict.fromkeys(['갑', '을', '인', '묘'], '목'),
        **dict.fromkeys(['병', '정', '사', '오'], '화'),
        **dict.fromkeys(['무', '기', '진', '술', '축', '미'], '토'),
        **dict.fromkeys(['경', '신', '유'], '금'),
        **dict.fromkeys(['임', '계', '해', '자'], '수'),
    }
    signs = {
        **dict.fromkeys(['갑', '병', '무', '경', '임', '자', '인', '진', '오', '신', '술'], '+'),
        **dict.fromkeys(['을', '정', '기', '신', '계', '축', '묘', '사', '미', '유', '해'], '-'),
    }
    conflictions = (
        ('수', '화'), 
        ('화', '금'), 
        ('금', '목'), 
        ('목', '토'), 
        ('토', '수'),
    )
    mutuals = (
        ('수', '목'),
        ('목', '화'),
        ('화', '토'),
        ('토', '금'),
        ('금', '수'),
    )

    def __enter__(self):
        # 육십갑자 데이터베이스
        self.sexagenaries = Connection('pillars_1960_2009_gyungja_base.db')
        self.sexagenaries = self.sexagenaries.cursor()

        # 십이운성 데이터베이스
        self.stages = Connection('stages.db')
        self.stages = self.stages.cursor()
        return self

    def __exit__(self, *parameters):
        # 어차피 안 써서 삭제 (_는 마음에 안 듦)
        del parameters

        # 데이터베이스 닫기 (메모리 절약? 벤치마킹 해봐야 알 거 같음)
        self.sexagenaries.close()
        self.stages.close()
        return None

    def get_twelve_stages(self, *parameters):
        result = self.stages.execute('SELECT * FROM main WHERE stem=? AND branch=?', parameters)
        return result.fetchone() 

    @classmethod
    def get_ten_stars(cls, standard, element):
        standard = Element(cls.elements[standard], cls.signs[standard])
        element = Element(cls.elements[element], cls.signs[element])

        # 오행과 음양이 모두 같으면 비견
        # 오행이 같지만 음양이 다르면 겁재 
        if standard.name == element.name:
            if standard.sign == element.sign:
                return '비견'
            else:
                return '겁재'

        # 오행이 생하는데 음양이 같으면 식신
        # 오행이 생하는데 음양이 다르면 상관
        elif (standard.name, element.name) in cls.mutuals:
            if standard.sign == element.sign:
                return '식신'
            else:
                return '상관'
        
        # 오행이 극하는데 음양이 같으면 편재
        # 오행이 극하는데 음양이 다르면 정재
        elif (standard.name, element.name) in cls.conflictions: 
            if standard.sign == element.sign:
                return '편재'
            else:
                return '정재'

        # 오행이 생받는데 음양이 같으면 편인
        # 오행이 생받는데 음양이 다르면 정인
        elif (element.name, standard.name) in cls.mutuals:
            if element.sign == standard.sign:
                return '편인'
            else:
                return '정인'
        
        # 오행이 극당하는데 음양이 같으면 편관
        # 오행이 극당하는데 음양이 다르면 정관
        elif (element.name, standard.name) in cls.conflictions:
            if element.sign == standard.sign:
                return '편관'
            else:
                return '정관'

        # 그 외의 경우는 발생할 수 없으므로 예외 처리
        else:
            raise ValueError('발생할 수 없는 경우가 발생했습니다.')

    def get_sexagenary(self, *date):
        result = self.sexagenaries.execute('SELECT * FROM main WHERE year=? AND month=? AND day=?', date)
        return result.fetchone()

with FourPillarsReading() as reader:
    print(reader.get_sexagenary(2009, 5, 7))
# reader.close()
