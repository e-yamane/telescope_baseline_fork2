# Dockerメモ

## コンテナ作成
Dockerfileとか、requirements.txtを書き直したときに実行

``docker-compose build``

## コンテナ起動
基本的には一度起動したら落とさなくても良い
（コンテナ再生成した時とかは行う）

``docker-compose up -d``

## コンテナ停止
基本的には落とさなくても良い
（コンテナ再生成した時とかは行う）

``docker-compose down``

## Dockerコンテナへのシェル接続
Dockerコンテナに接続してjasmineを動かしたいときに利用

``docker exec -it jasmine /bin/bash``
