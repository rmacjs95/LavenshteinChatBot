import pandas as pd

# 레벤슈타인 거리기반 챗봇 클래스 정의
class LavenshteinChatBot:
    def __init__(self, filepath):
        # 질문 및 답변 리스트 정의
        self.questions, self.answers = self.load_data(filepath)

    def load_data(self, filepath):
        data = pd.read_csv(filepath) # csv 파일을 DataFrame으로 읽어오기
        questions = data['Q'].tolist()  # 질문열만 뽑아 파이썬 리스트로 저장
        answers = data['A'].tolist()   # 답변열만 뽑아 파이썬 리스트로 저장
        return questions, answers

    def find_best_answer(self, input_sentence):
        # 같은 질문이 있다면 같은 답변을 제출
        if input_sentence in self.questions:
            return self.answers[self.questions.index(input_sentence)]
        
        # 레벤슈타인 거리를 저장할 리스트 초기화
        score = []

        # 레벤슈타인 거리를 계산하기 위해 데이터셋의 질문을 루프
        for idx, Q in enumerate(self.questions):
            # 데이터셋의 질문과 입력한 질문의 사이즈 구하기
            Q_len = len(Q)
            I_len = len(input_sentence)
            
            # 질문 혹은 데이터셋 질문이 None인 경우 가장 큰 거리를 측정
            if Q_len == "":
                score.append(I_len)
                break
            if I_len == "":
                score.append(Q_len)
                break
            
            # 레벤슈타인 거리를 저장할 리스트 정의
            matrix = [[] for i in range(Q_len+1)]
            for i in range(Q_len+1):
                matrix[i] = [0 for j in range(I_len+1)]

            # 0일 때 초깃값을 설정
            for i in range(Q_len+1):
                matrix[i][0] = i
            for j in range(I_len+1):
                matrix[0][j] = j
            
            # 표 채우기 --- (※2)
            for i in range(1, Q_len+1):
                ac = Q[i-1]
                for j in range(1, I_len+1):
                    bc = input_sentence[j-1] 
                    cost = 0 if (ac == bc) else 1
                    matrix[i][j] = min([
                        matrix[i-1][j] + 1,     # 문자 제거: 위쪽에서 +1
                        matrix[i][j-1] + 1,     # 문자 삽입: 왼쪽 수에서 +1   
                        matrix[i-1][j-1] + cost # 문자 변경: 대각선에서 +1, 문자가 동일하면 대각선 숫자 복사
                    ])
            score.append(matrix[Q_len][I_len]) # 계산된 레벤슈타인 값 저장
        return self.answers[score.index(min(score))] # 거리가 가장 유사한 인덱스의 답변을 리턴
    
    
# 데이터셋의 위치 정의
filepath = 'ChatbotData.csv'

# 챗봇 인스턴스 정의
chatbot = LavenshteinChatBot(filepath)

# '종료'라는 단어가 입력될 때까지 챗봇과의 대화를 반복
while True:
    input_sentence = input('You: ')
    if input_sentence.lower() == '종료':
        break
    response = chatbot.find_best_answer(input_sentence)
    print('Chatbot:', response)
    
