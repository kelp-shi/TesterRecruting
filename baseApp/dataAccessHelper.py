import datetime
from .models import TestPost

class dataAccessHelper():
    #全件取得データ
    get_posts = []
    #名称検索データ
    get_posts_name = []
    #検索オブジェクト無しエラー
    err_msg_sortnull = '募集中のテストが見つかりませんでした'

    #テストタスク全件取得（条件：募集フラグ==True, 削除フラグ==Falese）
    #新規クエリ
    def getAllTask(cls):
        cls.get_posts = TestPost.objects.filter(TestPost.RecrutingPeriodFlg==True, TestPost.DelFlg==False).order_by(id)

        #取得データ存在有無
        if cls.get_posts:
            #取得データ返却
            return cls.get_posts
        #取得データ無し：エラーメッセージ返却
        else:
            return cls.err_msg_sortnull
    
    #--------------以降検索用--------------
    #名称検索（部分一致可:大小区別なし）
    #新規クエリ
    def sortTaskName(cls, sortString):
        cls.get_posts_name = TestPost.objects.filter(PostName__icontains = sortString)
        return cls.get_post_name
            
    #募集期日検索（期日が近い）
    #全件取得データをソート
    def sortRecrutingUp(cls):
        #取得データ存在有無
        if cls.get_posts:
            now = datetime.datetime.now()
            #取得データソート
            cls.get_posts.sort(key=lambda post:abs(now - TestPost.RecrutingPeriodSt))
        else:
            #エラー時：エラーメッセージ返却（取得データなし）
            return cls.err_msg_sortnull
        
    #募集期日検索（期日が遠い）
    #全件取得データをソート
    def sortRecrutingDown(cls):
        #取得データ存在有無
        if cls.get_posts:
            now = datetime.datetime.now()
            #取得データソート
            cls.get_posts.sort(key=lambda post:abs(now + TestPost.RecrutingPeriodSt))
        else:
            #エラー時：エラーメッセージ返却
            return cls.err_msg_sortnull
    #募集期日検索（期日終了）
    #新規クエリ
    
    #テスト期日検索（期日が近い）
    #全件データをソート
    def sortTestUp(cls):
        if cls.get_posts:
            now = datetime.datetime.now()
            cls.get_posts.sort(key=lambda post:abs(now + TestPost.TestStart))
        else:
            #エラー時：エラーメッセージ返却（取得データなし）
            return cls.err_msg_sortnull
            
    #テスト期日検索（期日が遠い）
    #全件データソート
    def sortTestDown(cls):
        if cls.get_posts:
            now = datetime.datetime.now()
            cls.get_posts.sort(key=lambda post:abs(now + TestPost.TestStart))
        else:
            #エラー時：エラーメッセージ返却（取得データなし）
            return cls.err_msg_sortnull
    
    #テスト種類検索
    #新規クエリ
    
    #削除検索（条件：削除フラグ==True）
    #新規クエリ
    def getDelPost(cls):
        get_delPosts = TestPost.objects.filter(TestPost.DelFlg==True).order_by(id)
        return get_delPosts
    
    #