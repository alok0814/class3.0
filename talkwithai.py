import speech_recognition as sr
from gtts import gTTS
import os
import tempfile
import subprocess
import pygame
import openai

##############
# 音声認識関数 #
##############
def recognize_speech():

    recognizer = sr.Recognizer()    
    # Set timeout settings.
    recognizer.dynamic_energy_threshold = False

    
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
    
        while(True):
            print(">> Please speak now...")
            audio = recognizer.listen(source, timeout=1000.0)

            try:
                # Google Web Speech API を使って音声をテキストに変換
                text = recognizer.recognize_google(audio, language="ja-JP")
                print("[You]")
                print(text)
                return text
            except sr.UnknownValueError:
                print("Sorry, I could not understand what you said. Please speak again.")
            except sr.RequestError as e:
                print(f"Could not request results; {e}")

#############################
# 音声ファイル(mp3)再生用の関数 #
#############################
def play_mp3_blocking(file_path):

    pygame.init()
    pygame.mixer.init()
    mp3_file = pygame.mixer.Sound(file_path)    # MP3ファイルをロード
    
    print(">> Ready to Sppeach!")
    mp3_file.play()     # MP3ファイルを再生

    # 再生が終了するまで待つ(ブロッキング処理)
    while pygame.mixer.get_busy():
        pygame.time.Clock().tick(10)  # 10msごとに再生状態をチェック

    pygame.mixer.quit()


####################################################################################
# Google Text-to-Speech(gTTS)を用いてChatGPTによるレスポンス(テキスト)を.mp3形式に変換する #
####################################################################################
def text_to_speech(text):

    tts = gTTS(text=text, lang='ja', slow=False)
    
    with tempfile.NamedTemporaryFile(delete=True) as fp:
        temp_filename = f"{fp.name}.mp3"
        tts.save(temp_filename)

        # 音声ファイル再生（ブロッキング処理）
        play_mp3_blocking(temp_filename)



# メインの関数
if __name__ == '__main__':

    # ChatGPTのセットアップ
    openai.api_key="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"
    # UserとChatGPTとの会話履歴を格納するリスト
    conversationHistory = []

    # Ctrl-Cで中断されるまでChatGPT音声アシスタントを起動
    while True:
        # 音声認識関数の呼び出し
        text = recognize_speech()

        if text:
            print(" >> Waiting for response from ChatGPT...")
            # ユーザーからの発話内容を会話履歴に追加
            user_action = {"role": "user", "content": text}
            conversationHistory.append(user_action)
            
            # ChatGPTからの応答を取得
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=conversationHistory, 
            )
            responce = response["choices"][0]["message"]["content"]
            
            # ChatGPTからの応答内容を会話履歴に追加
            chatGPT_responce = {"role": "assistant", "content": responce}
            conversationHistory.append(chatGPT_responce) 

            print("[ChatGPT]") #応答内容をコンソール出力
            print(responce.strip()) #応答内容をコンソール出力
            # # (step3) 音声合成関数の呼び出し("ChatGPTのレスポンス"を"mp3ファイル"に変換して再生)
            print(">> Generating audio file....")
            text_to_speech(responce)