from django import forms

from .models import Post

#投稿フォームで受け取る情報
class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = (
            'gender',
            'brand',
            'temp',
            'category',
            'image',
            'purpose',
            'comment',
        )
        labels = {
            'gender': ('性別'),
            'brand': ('ブランド'),
            'temp': ('気温'),
            'category': ('ジャンル'),
            'purpose': ('目的'),
            'comment': ('コメント'),
        }

# 検索フォームで受け取る情報
class SearchForm(forms.Form, forms.ModelForm):
    
    class Meta:
        model = Post
        fields = ('gender', 'category', 'purpose')
        labels = {
            'gender': ('性別'),
            'category': ('ジャンル'),
            'purpose': ('目的'),
        }
    
    KEN_CHOICES = (
        (u'Sapporo', u'北海道'),
        (u'Aomori', u'青森県'),
        (u'Iwate', u'岩手県'),
        (u'Miyagi', u'宮城県'),
        (u'Akita', u'秋田県'),
        (u'Yamagata', u'山形県'),
        (u'Fukushima', u'福島県'),
        (u'Ibaraki', u'茨城県'),
        (u'Tochigi', u'栃木県'),
        (u'Gunma', u'群馬県'),
        (u'Saitama', u'埼玉県'),
        (u'Chiba', u'千葉県'),
        (u'Tokyo', u'東京都'),
        (u'Kanagawa', u'神奈川県'),
        (u'Niigata', u'新潟県'),
        (u'Toyama', u'富山県'),
        (u'Ishikawa', u'石川県'),
        (u'Fukui', u'福井県'),
        (u'Yamanashi', u'山梨県'),
        (u'Nagano', u'長野県'),
        (u'Gifu', u'岐阜県'),
        (u'Shizuoka', u'静岡県'),
        (u'Aichi', u'愛知県'),
        (u'Mie', u'三重県'),
        (u'Shiga', u'滋賀県'),
        (u'Kyoto', u'京都府'),
        (u'Osaka', u'大阪府'),
        (u'Kobe', u'兵庫県'),
        (u'Nara', u'奈良県'),
        (u'Wakayama', u'和歌山県'),
        (u'Tottori', u'鳥取県'),
        (u'Shimane', u'島根県'),
        (u'Okayama', u'岡山県'),
        (u'Hiroshima', u'広島県'),
        (u'Yamaguchi', u'山口県'),
        (u'Tokushima', u'徳島県'),
        (u'Kagawa', u'香川県'),
        (u'Ehime', u'愛媛県'),
        (u'Kouchi', u'高知県'),
        (u'Fukuoka', u'福岡県'),
        (u'Saga', u'佐賀県'),
        (u'nagasaki', u'長崎県'),
        (u'Kumamoto', u'熊本県'),
        (u'Oita', u'大分県'),
        (u'Miyazaki', u'宮崎県'),
        (u'Kagoshima', u'鹿児島県'),
        (u'Okinawa', u'沖縄県'),
    )
    ken = forms.CharField(max_length=10, widget=forms.Select(choices=KEN_CHOICES), label='行き先')
