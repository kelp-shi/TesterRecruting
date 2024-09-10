- main - main（docker, docker-compose使用したもの）
- ~~Rr-gcp - gcpデプロイテスト用ブランチ（gcp操作になれるためのブランチ）~~ （2024.09.02削除）
- defalt_django - 純粋にvenvとmysqlで動かすだけのブランチ（簡易閲覧、dockerエラー時用）
- docker-compose - docker-composeを用いてdjango, mysql, nginxを動かすため

docker使用環境であれば[docker-compose]を使用

docker非使用環境であれば[defalt_django]を使用

docker非使用環境かつMysql非使用環境であれば[defalt_django]を使用した後、sqlite3使用手順に沿って修正
