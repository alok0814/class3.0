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
answer_types = ['正確な回答', 'あいまいな回答', '間違った回答', '逆質問','トイレに行きたい']
answer_probs = [1.0, 0.0, 0.0, 0.0, 0.0]

def generate_student_answer(question):
    # 生徒の回答タイプをランダムに選択
    answer_type = random.choices(answer_types, answer_probs)[0]

    if answer_type == '正確な回答':
        print("正確な回答")
        # 正確な回答を生成
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "高校生の言葉づかいで質問に対して20文字以内で答えてください"},
                      {"role": "user", "content": question}]
        )
        answer = response.choices[0].message.content.strip()
    elif answer_type == 'あいまいな回答':
        # あいまいな回答を生成
        print("あいまいな回答")
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "一部あってる情報を入れて、間違った回答を20文字以内で答えてください"},
                      {"role": "user", "content": question}]
        )
        answer = response.choices[0].message.content.strip()
    elif answer_type == '間違った回答':
        # 間違った回答を生成
        print("間違った回答")
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "見当違いな回答を25文字で答えてください"},
                      {"role": "user", "content": question}]
        )
        answer = response.choices[0].message.content.strip()
    elif answer_type == '逆質問':
        print("逆質問")
        responses = [
            "理解できないので、もう少し具体的な説明をお願いします。",
            "よくわからないので、もうちょっと詳しく教えていただけませんか？",
            "私には理解できないので、もう少し具体的な説明をお願いできますか？",
            "理解できないので、もう少し詳細な情報を教えてもらえませんか？",
            "よく分からないので、もう少し詳しい説明をお願いします。",
            "わからないので補足してください。"
        ]
        answer = random.choice(responses)
    elif answer_type == 'トイレに行きたい':
        print("トイレ")
        responses = [
            "先生、すみませんがトイレに行きたいのですが、許可していただけますか？",
            "先生、ちょっとトイレに行きたいんですけど、いいですか？",
            "先生、すいませんがトイレに行きたくて…。",
            "先生、トイレに行きたいのですが、お願いしてもいいですか？",
            "先生、トイレに行ってもいいですか？お願いします。",
            "すみません。おなかが痛いのでトイレに行っていいですか？"
        ]
        answer = random.choice(responses)
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
