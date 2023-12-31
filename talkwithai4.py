import random
import speech_recognition as sr
import pyttsx3
import openai

# OpenAIのトークンを設定
openai.api_key = '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'

# マイクと音声合成エンジンの初期化
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# 会話の履歴
conversation_history = []

# 生徒の回答タイプと確率分布
answer_types = ['正確な回答', 'あいまいな回答',  'トイレに行きたい']
answer_probs = [2.0, 4.0, 4.0]

def generate_student_answer(question):
    # 生徒の回答タイプをランダムに選択
    answer_type = random.choices(answer_types, answer_probs)[0]
    print("IN")
    if answer_type == '正確な回答':
        print("正確な回答")
        # 正確な回答を生成
        messages = [
            {"role": "system", "content": "高校生の言葉づかいで質問に対して30文字以内で答えてください"}
        ]
        for i, (q, a) in enumerate(conversation_history[-5:], start=1):
            messages.append({"role": "user", "content": f"{i}: {q}"})
            messages.append({"role": "assistant", "content": f"{i}: {a}"})

        messages.append({"role": "user", "content": question})

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
        )
        answer = response.choices[0].message.content.strip()
    elif answer_type == 'あいまいな回答':
        # あいまいな回答を生成
        print("あいまいな回答")
        messages = [
            {"role": "system", "content": "見当違いの回答を30文字で答えてください"}
        ]
        for i, (q, a) in enumerate(conversation_history[-5:], start=1):
            messages.append({"role": "user", "content": f"{i}: {q}"})
            messages.append({"role": "assistant", "content": f"{i}: {a}"})

        messages.append({"role": "user", "content": question})

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
        )
        answer = response.choices[0].message.content.strip()
    elif answer_type == 'トイレに行きたい':
        print("トイレに行きたい回答")
        answer = "すみません。おなかが痛いのでトイレに行っていいですか？"
    else:
        # 間違った回答を生成
        print("すみません。わからないです。")
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

            # 会話の履歴に追加
            conversation_history.append((question, answer))

        except sr.UnknownValueError:
            print("聞き取れませんでした。もう一度お願いします。")
        except sr.RequestError as e:
            print("エラーが発生しました:", str(e))

if __name__ == '__main__':
    main()
