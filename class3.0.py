import random
import speech_recognition as sr
import pyttsx3
import openai

# OpenAIのトークンを設定
openai.api_key = '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'

# マイクと音声合成エンジンの初期化
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# 生徒の回答タイプと確率分布
answer_types = ['正確な回答', 'あいまいな回答', '間違った回答', 'トイレに行きたい']
answer_probs = [0.3, 0.4, 0.1, 0.1]

def generate_student_answer(question):
    # 生徒の回答タイプをランダムに選択
    answer_type = random.choices(answer_types, answer_probs)[0]

    if answer_type == '正確な回答':
        # 正確な回答を生成
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "Please make sure your text is 30 words or less"},
                      {"role": "user", "content": question}]
        )
        answer = response.choices[0].message.content.strip()
    elif answer_type == 'あいまいな回答':
        # あいまいな回答を生成
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "Please say the question using user input in 30 words or less"},
                      {"role": "user", "content": question}]
        )
        answer = response.choices[0].message.content.strip()
    elif answer_type == 'トイレに行きたい':
        answer = "すみません。おなかが痛いのでトイレに行っていいですか？"
    else:
        # 間違った回答を生成
        answer = "すみません。わからないです。"

    return answer

def speak(text):
    # テキストを音声に変換して出力
    engine.say(text)
    engine.runAndWait()

def main():
    while True:
        # マイクからの音声入力
        with sr.Microphone() as source:
            print("質問を入力してください...")
            audio = recognizer.listen(source)

        try:
            # 音声をテキストに変換
            question = recognizer.recognize_google(audio, language='ja-JP')
            print("質問:", question)

            # 生徒の回答生成
            answer = generate_student_answer(question)
            print("回答:", answer)

            # 回答を音声で出力
            speak(answer)

        except sr.UnknownValueError:
            print("聞き取れませんでした。もう一度お願いします。")
        except sr.RequestError as e:
            print("エラーが発生しました:", str(e))

if __name__ == '__main__':
    main()
