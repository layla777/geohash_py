
# GeohashPy

包括的な Python 実装としての Geohash．この実装では，地理座標をコンパクトな Geohash 文字列にエンコードおよびデコードすることができます．本プロジェクトは，[このブログ記事](http://mtcn.ko-me.com/%E9%96%A2%E6%95%B0%E3%80%81%E3%83%A9%E3%82%A4%E3%83%96%E3%83%A9%E3%83%AA/geohash%E9%96%A2%E6%95%B0) で説明されている Geohash アルゴリズムに基づいています．

## このプロジェクトについて
このプロジェクトは，**オブジェクト指向プログラミング（OOP）のサンプル実装**および**Geohash アルゴリズムを理解するための教育ツール**として設計されています．最適化や速度よりも一貫性のある設計とアルゴリズムの透明性を重視しています．

#### 主な特徴：
- OOP の原則をわかりやすく，直感的に示すクリーンな例を提供．
- 読みやすさと明確さを重視して，学習者が Geohash アルゴリズムを理解しやすくする．

## Geohash とは？

Geohash は，地理座標をコンパクトな文字列にエンコードするために使用される階層的な空間データ構造です．Geohash の主な特徴は以下の通りです：

- **再帰的な分割**：地球の表面が小さな長方形の領域に再帰的に分割され，それぞれの分割によって精度が向上します．
- **長方形の領域**：各 Geohash 文字列は地球上の長方形の領域に対応しています．しかし，アルゴリズムの構造上，一部の領域は不規則な形状になることがあります．
- **コンパクトな表現**：Geohash 文字列は非常に簡潔で，その長さが精度を決定します．

### 不規則な長方形の例

例えば，赤道をまたぐ領域を表す Geohash 文字列を考えると，極付近に移動するに従ってかなりサイズが異なる長方形になる場合があり，不規則性が特徴的です．

### 精度テーブル

以下の表は，異なる長さの Geohash 文字列に対応するおおよその解像度を示しています：
> **注意**：この表に記載されている解像度は赤道付近でのおおよその値を表しています．緯度が高くなり極に近づくにつれて，地球の曲率の影響で経度方向（東西方向）の解像度が細かくなります．
| 長さ    | 解像度（緯度 x 経度）        |
|---------|------------------------------|
| 1       | ±2500 km x ±5000 km          |
| 2       | ±630 km x ±1250 km           |
| 3       | ±78 km x ±156 km             |
| 4       | ±20 km x ±39 km              |
| 5       | ±2.4 km x ±4.9 km            |
| 6       | ±610 m x ±1.2 km             |
| 7       | ±76 m x ±152 m               |
| 8       | ±19 m x ±38 m                |
| 9       | ±2.4 m x ±4.8 m              |
| 10      | ±0.6 m x ±1.2 m              |
| 11      | ±0.07 m x ±0.15 m            |

ライブラリではデフォルトで精度が 11 に設定されていますが，ユーザーが要件に応じてカスタムの長さを指定することも可能です．

### ライブラリ設計の理念

このライブラリは，不規則な長方形を表現するものを含む，全ての有効な Geohash 文字列を受け入れます．この不規則性はアルゴリズムの自然な結果であり，地理的空間を柔軟に表現できる点で重要な特性です．

## 機能

- 地理座標を Geohash 文字列にエンコード
- Geohash 文字列を緯度・経度の座標にデコード
- 与えられた Geohash の近接する Geohash を取得
- 処理中に緯度と経度を正規化
- 座標や Geohash 文字列の入力検証を実施
- 緯度と経度の正規化
- 緯度・経度が処理中にどのように正規化されるかを示す明確な例を提供

## インストール

以下の手順でリポジトリをローカルマシンにクローンしてください：

```sh
git clone https://github.com/layla777/geohash_py.git
cd geohash_py
```

この実装は純粋な Python に基づいているため，追加の依存関係は必要ありません．
## Usage
Here's how you can use the `Geohash` class to encode, decode, and normalize geohashes, initialize them with specific values, and understand latitude and longitude normalization.

### Initializing a Geohash Object

The `Geohash` object should be initialized using one of the recommended methods:

#### **Recommended**: Using Latitude and Longitude (`init_with_lat_lng`)

```python
from geohash import Geohash

# Initialize with latitude and longitude
lat_lng = [37.7749, -122.4194]  # San Francisco, CA
length = 8
gh = Geohash.init_with_lat_lng(lat_lng=lat_lng, length=length)
print('Generated geohash:', gh.get_geohash())
```

#### **Recommended**: Using a Geohash String (`init_with_geohash`)

```python
# Initialize with a geohash string
geohash_str = '9q8yy'
gh = Geohash.init_with_geohash(geohash_str)
print('Geohash:', gh.get_geohash())
```

### Encoding Coordinates

You can encode new coordinates into the existing geohash object:

```python
# Encode new coordinates
new_lat_lng = [34.0522, -118.2437]  # Los Angeles, CA
gh.encode_with_lat_lng(new_lat_lng, length)
print('New geohash:', gh.get_geohash())
```

### Decoding a Geohash

You can decode a geohash string back into latitude and longitude:

```python
# Decode geohash
lat_lng = gh.decode()
print('Decoded coordinates:', lat_lng)
```

### Latitude and Longitude Normalization

Latitude and longitude values are automatically adjusted to ensure they fall within valid ranges. See [Technical Details](#technical-details).

### Getting Neighboring Geohashes

You can retrieve neighboring geohashes for a given geohash:

```python
# Get neighbors
neighbors = gh.neighbors(order=1)
print('Neighboring geohashes:', neighbors)
```

## API Reference

### Geohash

#### `__init__` method *(Internal Use Only)*

```python
__init__()
```

This internal constructor initializes a Geohash object with the default geohash value `'s0000000000'`. Direct usage is discouraged; use `init_with_lat_lng` or `init_with_geohash` for custom initialization.

#### `get_geohash` method

```python
get_geohash() -> str
```

Returns the current geohash string.

#### `set_geohash` method

```python
set_geohash(s: str)
```

Sets a new geohash string.

#### `encode_with_lat_lng` method

```python
encode_with_lat_lng(lat_lng: List[Union[float, int]], length: int = 11)
```

Encodes the provided latitude and longitude into a geohash string of the specified length.

#### `decode_to_interval` method

```python
decode_to_interval() -> List[Tuple[float, float]]
```

Decodes the geohash to its latitude and longitude interval.

#### `decode` method

```python
decode() -> List[float]
```

Decodes the geohash to the midpoint of its latitude and longitude interval.

#### `neighbors` method

```python
neighbors(order: int = 1) -> List[str]
```

Returns a list of neighboring geohashes around the current geohash.

## Technical Details

### Latitude and Longitude Normalization

- **Longitude Normalization**: Longitude values are wrapped within the range of -180 to 180 degrees using modular arithmetic. For example:
  - A longitude of `190` normalizes to `-170`.
  - A longitude of `-200` normalizes to `160`.

- **Latitude Normalization**: Latitude values are wrapped within the range of -90 to 90 degrees. If the value exceeds these bounds, it "bounces back" toward the center by reflecting over the boundary. For example:
  - A latitude of `-95` normalizes to `-85`.
  - A latitude of `100` normalizes to `80`.

This ensures realistic and accurate representation of geographic coordinates on the globe.

## License


This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

This implementation is inspired by the Geohash algorithm explained in [this blog post](http://mtcn.ko-me.com/%E9%96%A2%E6%95%B0%E3%80%81%E3%83%A9%E3%82%A4%E3%83%96%E3%83%A9%E3%83%AA/geohash%E9%96%A2%E6%95%B0).

Feel free to contribute to this project by opening issues or submitting pull requests.
