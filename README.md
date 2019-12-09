# Create Update Node
Houdiniで指定したバージョンから更新のあったノードをまとめて作成するツールです。

![Get New Nodes](https://dl.dropboxusercontent.com/s/01q7a13djx3165n/NodeCompare.gif?dl=0)

このツールの紹介は下記ページをご覧ください。

[新しいバージョンで追加、更新されたノードの一覧を取得、作成する](https://qiita.com/d658t/private/33170d0e625d76effcde)

# インストールとスクリプトの登録方法
1. **Clone or download > Download ZIP**からZIPファイルをダウンロードします。

2. 解凍したフォルダ内の**python2.7libs**をPythonが認識される場所にコピーしてください。  
Windowsの場合は`%HOMEDRIVE%%HOMEPATH%\Documents\houdiniバージョン`にコピーすると自動で認識されます。
![Script Place](https://dl.dropboxusercontent.com/s/nzidjyjb93ud2yu/ScriptPlace.jpg?dl=0)

3. Houdiniを起動し、シェルフの+をクリック>New Shelf...をクリックします。
![Shelf Set01](https://dl.dropboxusercontent.com/s/vvjmo3q8hhwawe0/NewShelfSet01.jpg?dl=0)

4. シェルフセットの設定ウィンドウが開くので、適当な名前を付け、Acceptを押します。
![Shelf Set02](https://dl.dropboxusercontent.com/s/borw48j2heyzwle/NewShelfSet02.jpg?dl=0)

5. 新しく作ったシェルフ上で右クリック>New Tool...をクリックします。
![Shelf New Tool](https://dl.dropboxusercontent.com/s/8jejzujehy6u1ke/ShelfNewTool.jpg?dl=0)

6. OptionsタブのNameをcreate_update_nodeにし、LabelをCreate Update Nodeにします。
![Self Tool Setting](https://dl.dropboxusercontent.com/s/pudqm3e7cv4sa3b/ShelfToolSetting.jpg?dl=0)

7. Scriptタブに下記コードを記入します。
```Python
from create_update_node import core
core.main()
```  
![Self Tool Script](https://dl.dropboxusercontent.com/s/lbqty4et69f1auj/ShelfToolScript.jpg?dl=0)

# スクリプトの実行
- 登録したシェルフツールをクリックすることでスクリプトが実行されます。

- スクリプトを実行すると、どのバージョンと比較するかを選ぶウィンドウが出てきて、選ぶとノードの比較処理が走ります。

# 機能
- ノード自体が追加された物は**NewNodes**、パラメータが追加されたノードは**NewParmNodes**という**Subnet**が作成され、中に**Sop**などカテゴリごとにノードが出来ます。
![New Sop](https://dl.dropboxusercontent.com/s/exs9g6r51nj4hhx/NewSop.jpg?dl=0)

- 追加されたパラメータには**constant**というエクスプレッションが入っているので、パラメータのフィルターから**Parameters with Non-Default Values**を選ぶと追加されたパラメータのみ表示出来るようになっています。  
※一部のパラメータにはエクスプレッションをセット出来ないので、全てではありません
![Parameter Filter](https://dl.dropboxusercontent.com/s/9d7p5n2jmr7dmpx/ParmFilter.jpg?dl=0)
