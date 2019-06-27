from django.db import models
from django.utils import timezone

import os
import uuid
from PIL.Image import Image
from hackathon.settings import MEDIA_ROOT

# Create your models here.

def get_image_path(self, filename):
    """
    カスタマイズした画像pathを取得する
    UUIDにして画像ファイル名をhash化
    :param self: インスタンス(model)
    :param filename:  元の画像ファイル
    :return: カスタマイズしたファイル名を含む画像パス
    """

    prefix = 'images/'
    name = str(uuid.uuid4()).replace('-', '')
    extension = os.path.splitext(filename)[-1]

    return prefix + name + extension
        
def delete_previous_file(function):
    """
    不要となる古い画像ファイルを削除する為のデコレータ実装
    :param function: メイン関数
    :return: wrapper
    """

    def wrapper(*args, **kwargs):
        self = args[0]
        #保存前の画像ファイル名取得
        result = Post.objects.filter(pk=self.pk)
        previous = result[0] if len(result) else None
        super(Post, self).save()
        #関数実行
        result = function(*args, **kwargs)
        #保存前のファイルがあったら削除
        if previous:
            os.remove(MEDIA_ROOT + '/' + previous.image.name)
        return result
    return wrapper

class Post(models.Model):
    
    GENDER_CHOICES = (
        (u'M', u'Men'),  #(データベースに保存される値, 管理インターフェイスで表示される値)
        (u'W', u'Women'),
    )
    CATEGORY_CHOICES = (
        (u'outdoor', u'アウトドア'),
        (u'amekaji', u'アメカジ'),
        (u'kuranji', u'クランジ'),
        (u'surf', u'サーフ'),
        (u'salon', u'サロン'),
        (u'street', u'ストリート'),
        (u'sports', u'スポーツMIX'),
        (u'toratto', u'トラット'),
        (u'noomukoa', u'ノームコア'),
        (u'business', u'ビジネス'),
        (u'hiphop', u'ヒップホップ'),
        (u'host', u'ホスト'),
        (u'mode', u'モード'),
        (u'rock', u'ロック'),
        (u'onee', u'お姉'),
        (u'girlish', u'ガーリッシュ'),
        (u'gyaru', u'ギャル'),
        (u'kireime', u'きれいめカジュアル'),
        (u'gosurori', u'ゴスロリ'),
        (u'marine', u'マリン'),
        (u'harajuku', u'原宿'),
        (u'morigirl', u'森ガール'),
    )
    TEMP_CHOICES = (
        (u'~5', u'~5℃'),
        (u'6~10', u'6~10℃'),
        (u'11~15', u'11~15℃'),
        (u'16~20', u'16~20℃'),
        (u'21~25', u'21~25℃'),
        (u'26~30', u'26~30℃'),
        (u'31~', u'31℃~'),
    )
    PURPOSE_CHOICES = (
        (u'date', u'デート'),
        (u'party', u'パーティ'),
        (u'outdoor', u'アウトドア'),
        (u'business', u'ビジネス'),
        (u'nochoice', u'選択なし'),
    )
    created_date = models.DateTimeField(default = timezone.now)
    gender = models.CharField(max_length = 2, choices = GENDER_CHOICES)
    brand = models.CharField(max_length = 30)
    category = models.CharField(max_length = 10, choices = CATEGORY_CHOICES)
    temp = models.CharField(max_length = 8, choices = TEMP_CHOICES)
    purpose = models.CharField(max_length = 10, choices = PURPOSE_CHOICES)
    image = models.ImageField(upload_to=get_image_path)
    comment = models.TextField(blank = True)
    
    og_image = image.upload_to
    
    @delete_previous_file
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super(Post, self).save()
    
    @delete_previous_file
    def delete(self, using=None, keep_parents=False):
        super(Post, self).delete()
    
    def __str__(self):
        return u'Post Object' + str(self.id)
    
    def admin_og_image(self):
        if self.og_image:
            return '<img src="{}" style="width:100px;height:auto;">'.format(self.og_image)
        else:
            return 'no image'
    
    admin_og_image.allow_tags = True
