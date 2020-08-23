# 熔融塩ループ計算
## リポジトリ概要
熔融塩ループの正常系、異常系をシミュレートします。

## 環境構築
### 事前準備
pythonおよびpipenvのコマンド実行用にパスを通しておく。
- pipenv…python環境とライブラリの統合管理ツール。

```
python導入後に以下実行でインストール
pip3 install --user pipenv
```

- 導入の確認
```
> python --version
Python 3.7.4
> pipenv --version
pipenv, version 2018.11.26
```

### 開発環境インストール
- 作業用の任意のディレクトリで以下を実行

shell(mac等)の場合
```
PIPENV_VENV_IN_PROJECT=true pipenv sync
```

command prompt(windows)の場合
```
set PIPENV_VENV_IN_PROJECT=true
pipenv sync
```

## パラメータファイル設定

### 値には数式を利用可能。その場合「""」でくくって文字列として設定する。python標準関数の他、numpyの「pi」「sqrt」は使用可能。

| 項目 | 子項目 | 設定内容 | 備考 |
|---|---|---|---|
| system_env | | システム環境パラメータ | |
| | gravity | 重力定数 |
| | initial_degree | 系内初期温度 |
| | kinetic_viscosity | 動粘度 |
| loop_config | | ループパラメータ |
| | max_iteration | 最大ループ回数
| | interval_second | 1ループあたりの経過時間（秒）
| | target_degree | 到達温度
| | heat_input_persec | 秒あたりの投入熱量を指定<br>[time: 投入開始時刻 energy: 投入熱量] | 配列で複数設定可、<br>次の値を設定するまでは毎秒投入され続ける |
| | pressure_of_pump_persec | 秒あたりのポンプ圧力を指定<br>[time: 開始時刻 energy: ポンプ圧力] | 配列で複数設定可、<br>次の値を設定するまでは毎秒投入され続ける |
| | system_error | 異常発生の設定を行う。| type:異常の種類。現在は閉塞（pipe_block）のみ。<br>point_id:異常発生個所（device_idを指定）<br>time:異常発生時間<br>block_rate_of_l_end_area:閉塞する面積の割合。閉塞の場合のみ指定。<br>enable:有効化。設定を消さずに異常発生を無効化したい場合はFalseを指定する。 | 配列で複数指定可。
| system_config | | システム設定パラメータ
| | device_connections | デバイスの接続情報。<br>root:接続元デバイスid<br>dist:接続先デバイスid | 配列で指定し、ループになるように設定する必要がある。
| system_devices | | システム構成デバイスパラメータ | | デバイス個別の属性は元プログラムに準じて設定しているため省略。
| | core | 炉心 | 
| | pump | ポンプ | 
| | heat_exchanger　| 熱交換器 | 
| | pipe | パイプ | 
| log_config | | ログ動作設定
| | outfile | ログファイル保存先フォルダ | デフォルトでは実行ディレクトリに保存
