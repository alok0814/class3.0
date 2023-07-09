import speech_recognition as sr
from gtts import gTTS
import os
import tempfile
import subprocess
import pygame
import openai
# メインの関数
if __name__ == '__main__':

    # ChatGPTのセットアップ
    openai.api_key = "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"
    # UserとChatGPTとの会話履歴を格納するリスト
    conversationHistory = []

    # Ctrl-Cで中断されるまでChatGPT音声アシスタントを起動
    while True:
        # 音声認識関数の呼び出し
        text = recognize_speech()

        if text:
            print(" >> Waiting for response from ChatGPT...")
            # ユーザーからの発話内容を会話履歴に追加
            user_action = {"role": "user", "content": text + "に対して10文字で返答して"}
            conversationHistory.append(user_action)

            # 最大で最新の5つの会話履歴を保持する
            conversationHistory = conversationHistory[-5:]

            # ChatGPTからの応答を取得
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=conversationHistory,
            )
            response = response["choices"][0]["message"]["content"]

            # ChatGPTからの応答内容を会話履歴に追加
            chatGPT_response = {"role": "assistant", "content": response}
            conversationHistory.append(chatGPT_response)

            print("[ChatGPT]")  # 応答内容をコンソール出力
            print(response.strip())  # 応答内容をコンソール出力
            # # (step3) 音声合成関数の呼び出し("ChatGPTのレスポンス"を"mp3ファイル"に変換して再生)
            print(">> Generating audio file....")
            text_to_speech(response)
