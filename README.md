# EC_site_by_Django
 
これらのコードは私が作製したECサイトです。
 
# DEMO
 
トップページ
https://user-images.githubusercontent.com/76026039/159591492-42474f31-aa0b-4cc1-8c82-14cedd596589.png

カートページ
https://user-images.githubusercontent.com/76026039/159591584-c7a050b0-c2cb-4868-b1f9-3a2db9a06aac.png

決済ページ
https://user-images.githubusercontent.com/76026039/159591704-3ce4fd2a-0aeb-4265-b764-295fc9555c79.png

購入後、在庫や売上も変更し、人気商品ランキングも変更していく
https://user-images.githubusercontent.com/76026039/159592219-a169d87f-9689-48cb-8b65-8602f0b7b580.png

 
# Features
 
Djangoで簡単なブログサイトをUdemyの教材を通して作製してきたが、今回は
決済機能のあるECサイト(ショッピングサイト)を作成した。
ログイン・サインアップ機能、アカウントごとに注文履歴などを管理。

# Requirement
 
* python 3.x
* pillow
* stripe
* django
 
# Installation
 
Requirementで列挙したライブラリなどのインストール方法を説明する
 
```zsh
pip install pillow
pip install django
pip install stripe
```
 
# Usage
 
これらを機能させるにはまず
・Stripeのページへ行きアカウントを作成・シークレットキーを取得(テスト版)
・本プロジェクト直下に"secrets"フォルダを作成し、".env.div"ファイルを作成
・そのファイル内にsettings.pyにおけるSECRET_KEY, DEBUG, ALLOWED_HOSTSを記載
・次いで、STRIPE_API_SECRET_KEYにStripeのシークレットキーを設定、MY_DOMAINに"http://127.0.0.1:8000"と記載
 
# Note
 
※本プロジェクトはデプロイをしていない
※カード決済の際、番号は4242 4242 4242 4242としてください。
 
# Author
  
* Logarithm
* Univercity
* kosuke.eng@gmail.com
