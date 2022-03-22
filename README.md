# EC_site_by_Django
 
これらのコードは私が作製したECサイトです。
 
# DEMO
 

 
# Features
 
Djangoで簡単なブログサイトをUdemyの教材を通して作製してきたが、今回は
決済機能のあるECサイト(ショッピングサイト)を作成した。

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
 
# Author
  
* Logarithm
* Univercity
* kosuke.eng@gmail.com
