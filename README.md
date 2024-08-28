# 起動手順
## 事前準備
1. Mysqlをインストール

## リポジトリクローンからrunserver
1. ルートフォルダ作成
2. ルートにvenv作成
3. ルートにリポジトリクローン
4. venvに入る[ xxx/Scripts/Activate.ps1 ] xxxはvenvの名前
5. cdでクローンしたリポジトリへ入る
6. [ pip install -r requirements.txt ]でパッケージインストール
7. settings.pyのDB関連情報をインストールしたMysqlに沿って修正（userやpass）
   
※mysqlではなくsqlite3を使用する場合は下記に書き換え（mysqlではなくベースディレクトリにdbを作成する）

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

8. [ python manage.py makemigrations ]でマイグレーションファイルを作成
9. [ python manage.py migrate ]でDBへマイグレーション情報を反映
10. [ python manage.py createsuperuser ] でスーパーユーザー（管理者アカウント）を作成
11. [python manage.py runserver ] でサーバー起動（エラー表記が出るがgcpデプロイ用の処理がコケてるだけなので無視）
12. 遊ぶ

### ファイル構成図
```ini
roor
 ├─venv
 └─testerRecruting
      ├─baseApp(appF)
      ├─templates
      ├─testerRecruting(projectF)
      ├─.env
      ├─.gitignore
      ├─manage.py
      └─requirements.txt
```
### .envのなかみ（使用環境に沿って都度修正）
```.env
#---------------デプロイ環境の値---------------
MYSQL_ROOT_PASSWORD=********（適当な値）
MYSQL_DATABASE=terec-mysql001sample
MYSQL_USER=terec-admin
MYSQL_PASSWORD=********（適当な値）
MYSQL_HOST=********（適当な値）
MYSQL_PORT=5432

#---------------開発環境の値---------------
D_MYSQL_ROOT_PASSWORD=********（適当な値）
D_MYSQL_DATABASE=terecmysql001sample（環境のDB名）
D_MYSQL_USER=root
D_MYSQL_PASSWORD=********（適当な値）
D_MYSQL_HOST=localhost
D_MYSQL_PORT=3306
D_DJANGO_ALLOWED_HOSTS=127.0.0.1

#---------------django関連の値---------------
DJANGO_SECRET_KEY=********（適当な値）
DJANGO_ALLOWED_HOSTS=testerrecruitment.com
DJANGO_DEBUG=True

#---------------メール送信関連の値---------------
DJANGO_EMAIL=********
DJANGO_EMAIL_PORT=587
DJANGO_EMAIL_USE_TLS =True
DJANGO_EMAIL_HOST_USER=support@testerrecruitment.com
DJANGO_EMAIL_HOST_PASSWORD=********（適当な値）
DJANGO_DEFAULT_FROM_EMAIL=noreply@testerrecruitment.com
DJANGO_CONTACT_EMAIL=support@testerrecruitment.com

#---------------デプロイ環境の値---------------
GOOGLE_CLOUD_PROJECT=********
SETTINGS_NAME=********
USE_GCP_SECRETS=True
```
