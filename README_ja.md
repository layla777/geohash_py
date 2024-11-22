# Geohash Py

地理座標をコンパクトなジオハッシュ文字列にエンコードおよびデコードするための包括的な Python 実装です．このプロジェクトは[このブログ記事](http://mtcn.ko-me.com/%E9%96%A2%E6%95%B0%E3%80%81%E3%83%A9%E3%82%A4%E3%83%96%E3%83%A9%E3%83%AA/geohash%E9%96%A2%E6%95%B0)で説明されているジオハッシュアルゴリズムに基づいています．

## 特徴

- 地理座標をジオハッシュ文字列にエンコード
- ジオハッシュ文字列を緯度と経度にデコード
- 特定のジオハッシュの隣接するジオハッシュを取得
- 座標とジオハッシュ文字列の入力検証
- 緯度と経度の正規化

## インストール

リポジトリをローカルマシンにクローンします：

```sh
git clone https://github.com/layla777/geohash_py.git
cd geohash_py
```

これは純粋な Python 実装のため，追加の依存関係は必要ありません．

## 使い方

`Geohash` クラスを用いてジオハッシュをエンコードおよびデコードする方法を以下に示します．

### ジオハッシュオブジェクトの初期化

ジオハッシュオブジェクトは，地理座標を提供するかジオハッシュ文字列を提供することで初期化できます．

#### 緯度と経度を使用する場合

```python
from geohash import Geohash

# 緯度と経度で初期化
lat_lng = [37.7749, -122.4194]  # サンフランシスコ，CA
length = 8
geohash_obj = Geohash(lat_lng=lat_lng, length=length)
print("生成されたジオハッシュ：", geohash_obj.get_geohash())
```

#### ジオハッシュ文字列を使用する場合

```python
# ジオハッシュ文字列で初期化
geohash_str = '9q8yy'
geohash_obj = Geohash(geohash=geohash_str)
print("ジオハッシュ：", geohash_obj.get_geohash())
```

### 座標のエンコード

既存のジオハッシュオブジェクトに新しい座標をエンコードできます：

```python
# 新しい座標をエンコード
new_lat_lng = [34.0522, -118.2437]  # ロサンゼルス，CA
geohash_obj.encode_with_lat_lng(new_lat_lng, length)
print("新しいジオハッシュ：", geohash_obj.get_geohash())
```

### ジオハッシュのデコード

ジオハッシュ文字列を緯度と経度にデコードできます：

```python
# ジオハッシュをデコード
lat_lng = geohash_obj.decode()
print("デコードされた座標：", lat_lng)
```

### 隣接するジオハッシュの取得

特定のジオハッシュに対して隣接するジオハッシュを取得できます：

```python
# 隣接するジオハッシュを取得
neighbors = geohash_obj.neighbors(order=1)
print("隣接するジオハッシュ：", neighbors)
```

## API リファレンス

### Geohash

#### `__init__` メソッド

```python
__init__(lat_lng: List[Union[float, int]] = None, length: int = 11, geohash: str = 's0000000000')
```

ジオハッシュオブジェクトを初期化します．

- `lat_lng`: 緯度と経度を含むリスト．
- `length`: ジオハッシュ文字列の望ましい長さ．
- `geohash`: ジオハッシュ文字列．

#### `get_geohash` メソッド

```python
get_geohash() -> str
```

現在のジオハッシュ文字列を返します．

#### `set_geohash` メソッド

```python
set_geohash(s: str)
```

新しいジオハッシュ文字列を設定します．

#### `encode_with_lat_lng` メソッド

```python
encode_with_lat_lng(lat_lng: List[Union[float, int]], length: int = 11)
```

指定された緯度と経度を指定された長さのジオハッシュ文字列にエンコードします．

#### `decode_to_interval` メソッド

```python
decode_to_interval() -> List[Tuple[float, float]]
```

ジオハッシュをその緯度と経度の範囲にデコードします．

#### `decode` メソッド

```python
decode() -> List[float]
```

ジオハッシュをその緯度と経度の範囲の中点にデコードします．

#### `neighbors` メソッド

```python
neighbors(order: int = 1) -> List[str]
```

現在のジオハッシュ周辺の隣接するジオハッシュのリストを返します．

## ライセンス

このプロジェクトは MIT ライセンスの下でライセンスされています．詳細は [LICENSE](LICENSE) ファイルを参照してください．

## 謝辞

この実装は[このブログ記事](http://mtcn.ko-me.com/%E9%96%A2%E6%95%B0%E3%80%81%E3%83%A9%E3%82%A4%E3%83%96%E3%83%A9%E3%83%AA/geohash%E9%96%A2%E6%95%B0)で説明されているジオハッシュアルゴリズムに触発されています．

問題を報告したりプルリクエストを提出することで、このプロジェクトに自由に貢献してください．