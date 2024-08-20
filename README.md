1. ルートフォルダ作成
2. ルートにvenv作成
3. ルートにリポジトリクローン
4. venvに入る[ xxx/Scripts/Activate.ps1 ] xxxはvenvの名前
5. cdでクローンしたリポジトリへ入る
6. [ pip install -r requirements.txt ]でパッケージインストール
7. [ python manage.py makemigrations ]でマイグレーションファイルを作成
8. [ python manage.py migrate ]でDBへマイグレーション情報を反映
9. [ python manage.py createsuperuser ] でスーパーユーザー（管理者アカウント）を作成
10. [python manage.py runserver ] でサーバー起動（エラー表記が出るがgcpデプロイ用の処理がコケてるだけなので無視）
11. 遊ぶ
