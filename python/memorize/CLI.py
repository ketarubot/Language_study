import sys
import re
import random

word_dict = {}
weights = {}
correct = set()
performance = [0, 0, 0]
random_mode = False
english = False
turned = False

# 단어 파일 읽기 및 초기화
def start():
    global word_dict
    global weights
    global correct
    global performance
    global random_mode
    global english
    
    word_dict = {}
    weights = {}
    correct = set()
    performance = [0, 0, 0]
    random_mode = False
    choose = input('읽어올 텍스트파일의 이름을 입력하세요: ').strip()
    try:
        with open(f"{choose}.txt", 'r', encoding='utf-8') as file:
            for line in file:
                word, meaning = map(str.strip, line.split('/', 1))
                word_dict[word] = meaning.strip()
                weights[word] = 1
        print("-" * 50)
    except FileNotFoundError:
        print(f"Error: '{choose}.txt' 파일을 찾을 수 없습니다.")
        sys.exit()

    while True:
        category = input('문제 유형을 선택하세요(한글, 영어, 랜덤): ').strip()
        if category == '영어':
            english = True
            print("-" * 50)
            break
        elif category == '한글':
            english = False
            print("-" * 50)
            break
        elif category == '랜덤':
            random_mode = True
            print("-" * 50)
            break
        else:
            print('올바른 입력이 아닙니다. 다시 입력해주세요.')
    turned = True

def clean_input(input_str):
    # 입력 받은 문자열에서 괄호 안 내용과 '~'을 제거하고 공백을 정리
    return re.sub(r'\(.*?\)|~', '', input_str).replace(' ', '').strip().lower()

def is_correct(user_input, correct_answer):
    # 사용자가 입력한 뜻이 여러 개일 때, 하나라도 맞으면 정답으로 인정
    possible_answers = correct_answer.replace(' ', '').split(',')  # 여러 뜻을 ','로 구분했다고 가정
    return any(clean_input(user_input) == clean_input(answer.strip()) for answer in possible_answers)

def ask_question():
    remaining_words = [word for word in word_dict.keys() if word not in correct]  # 맞춘 단어를 제외한 남은 단어만
    weighted_choices = [word for word in remaining_words for _ in range(weights[word])]
    
    if not weighted_choices:
        print("모든 단어를 학습하셨습니다.")
        if input('다시 학습하시겠습니까(y/*)? ') == 'y':
            start()
            print('-' * 50)
        else:
            sys.exit()

    question_word = random.choice(weighted_choices)
    answer = word_dict[question_word]

    # 문제 유형을 무작위로 선택: 영어 맞추기 (True) 또는 뜻 맞추기 (False)
    if random_mode:
        is_english_question = random.choice([True, False])
    else:
        is_english_question = english
        
    if is_english_question:
        question = answer + f'[{question_word[0]}]'  # 뜻을 주고 영어 단어를 맞추게 함
        correct_answer = question_word  # 정답은 영어 단어
    else:
        question = question_word  # 영어 단어를 주고 뜻을 맞추게 함
        correct_answer = answer  # 정답은 뜻

    user_answer = input(f"'{question}': ").strip()

    performance[1] += 1  # 총 문제 수 증가

    # 정답 확인
    if is_correct(user_answer, correct_answer):
        correct.add(question_word)  # 맞춘 단어를 correct에 추가
        performance[0] += 1
        performance[2] += 1
        weights[question_word] = max(1, weights[question_word] - 1)  # 가중치 감소
        print(f"정답입니다!: '{correct_answer}'")
    else:
        performance[0] = 0
        weights[question_word] += 1  # 가중치 증가
        print(f"틀렸습니다. 정답은 '{correct_answer}'입니다.")

    # 학습 성과 출력
    accuracy = (performance[2] / performance[1]) * 100
    print(f"정답률: {accuracy:.2f}%")
    print(f"연속 정답 수: {performance[0]}")
    print(f"남은 문제 수: {len(remaining_words)-1}")
    print("-" * 50)

start()
while True:
    ask_question()
