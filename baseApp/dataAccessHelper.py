import datetime
from .models import TestPost

class dataAccessHelper():
    #全件取得データ
    get_posts = []
    #名称検索データ
    get_posts_name = []
    #検索オブジェクト無しエラー
    err_msg_sortnull = 'テストが見つかりませんでした'

    #テストタスク全件取得（条件：募集フラグ==True, 削除フラグ==Falese）
    def getAllTask(cls):
        cls.get_posts = TestPost.objects.filter(TestPost.RecrutingPeriodFlg==True, TestPost.DelFlg==False).order_by(id)
        return cls.get_posts
    
    #--------------以降検索用--------------
    #名称検索（部分一致可:大小区別なし）
    def sortTaskName(cls, sortString):
        cls.get_posts_name = TestPost.objects.filter(PostName__icontains = sortString)
            
    #募集期日検索（期日が近い）
    def sortRecrutingUp(cls):
        #取得データ存在有無
        if cls.get_posts:
            now = datetime.datetime.now()
            #取得データソート
            cls.get_posts.sort(key=lambda post:abs(now - TestPost.RecrutingPeriodSt))
        else:
            #エラー時：エラーメッセージ返却
            return cls.err_msg_sortnull
        
    #募集期日検索（期日が遠い）
    def sortRecrutingDown(cls):
        #取得データ存在有無
        if cls.get_posts:
            now = datetime.datetime.now()
            #取得データソート
            cls.get_posts.sort(key=lambda post:abs(now + TestPost.RecrutingPeriodSt))
        else:
            #エラー時：エラーメッセージ返却
            return cls.err_msg_sortnull
    #