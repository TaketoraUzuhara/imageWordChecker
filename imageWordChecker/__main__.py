from imageWordChecker import robo

if __name__ == '__main__':
    img_name = input('画像の名前を選択してください:')
    image_path = '../img/' + img_name
    ng_word = input('確認したい単語を入力してください：')
    robo1 = robo.imageWordCheckRobo(image_path=image_path, ng_word=ng_word)
    robo1.job()