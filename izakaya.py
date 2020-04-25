#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import speech
import sound
import dialogs
import time

# constant parameter
staff_action = {
    "menu": {
        "drink": {
            "日本酒": {"price": 800, "alc": 3},
            "ビール": {"price": 500, "alc": 1},
            "ハイボール": {"price": 300, "alc": 1},
            "ウォッカ": {"price": 600, "alc": 5}
        }
    }
}

drunk_threshold = 6

def main():
    # initialize
    drink_status = False
    drunk_level = 0
    bill = 0
    
    while (drink_status == False):
        # display menu
        print("++++")
        print("Menu")
        print("")
        for drink in staff_action["menu"]["drink"].keys():
            print(drink)
        print("++++")

        # take a order
        speech.say("ご注文をどうぞ！", 'ja-JP')
        time.sleep(1.8)
        recorder = sound.Recorder('speech.m4a')
        recorder.record()
        dialogs.alert('注文が終わったらボタンをタップしてください.', '', 'Finish', hide_cancel_button = True)
        recorder.stop()
        
        # replay
        voice = sound.Player('speech.m4a')
        voice.play()
        time.sleep(5.0)

        # recognize order
        try:
            result = speech.recognize('speech.m4a', 'ja-JP')
        except RuntimeError as e:
            print("recognition failed: %s" % (e, ))

        # order done
        hit = False
        for candidate in staff_action["menu"]["drink"].keys():
            if candidate in result[0][0]:
                string = 'お待たせしました、' + candidate + 'です！'
                speech.say(string, 'ja-JP')
                print(string)
                
                # add bill and drunk_level
                bill += staff_action["menu"]["drink"][candidate]["price"]
                drunk_level += staff_action["menu"]["drink"][candidate]["alc"]
                                
                hit = True
                break
        if not hit:
            string = "申し訳ありません、当店には取りあつかいがありません。"
            speech.say(string, 'ja-JP')
            print(string)

        # check drunk_level
        if (drunk_level >= drunk_threshold):
            string = "あ、お茶をお出ししますね。"
            speech.say(string, 'ja-JP')
            string = "お会計は" + str(bill) + "円です。お気をつけておかえりください。"
            speech.say(string, 'ja-JP')
            drink_status = True
            
        time.sleep(2.0)

if __name__ == "__main__":
    main()

