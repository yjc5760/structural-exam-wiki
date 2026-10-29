# API 速查

## 目錄

- [座標系與 Canvas](#座標系與-canvas)
- [基本圖元](#基本圖元)
- [文字與數學符號](#文字與數學符號)
- [力與箭頭](#力與箭頭)
- [支承符號](#支承符號)
- [尺寸線、座標軸、圖例](#尺寸線座標軸圖例)
- [撓曲形狀](#撓曲形狀)
- [多聯圖 compose](#多聯圖-compose)
- [recipes 高階產生器](#recipes-高階產生器)
- [色票](#色票)

---

## 座標系與 Canvas

內部使用**數學座標（y 向上）**，輸出時自動翻轉成 SVG 座標。

```python
Canvas(w, h, sx=1.0, ox=0.0, oy=0.0, bg=None)
```

| 參數 | 意義 |
|---|---|
| `w, h` | 畫布像素尺寸 |
| `sx` | 每 1 模型單位 = 幾像素（等向縮放，x/y 共用） |
| `ox` | 模型原點的像素 x（由左緣起算） |
| `oy` | 模型原點的像素 y（**由底緣起算**） |
| `bg` | 背景色；`None` 為透明 |

版面配置的標準做法：先決定四邊留白，再由留白反推 `sx` 與 `ox/oy`，
不要先寫死 `sx` 再祈禱塞得下。

```python
L, R, T, B = 64, 190, 74, 58          # 左/右標註槽/上/下留白
sx = min((W - L - R) / x_range, (H - T - B) / y_range)
cv = Canvas(W, H, sx=sx, ox=L - x_min*sx, oy=B - y_min*sx)
```

輔助方法：

```python
cv.X(x) / cv.Y(y) / cv.P((x, y))     # 模型座標 → 像素
cv.svg()                              # 回傳 SVG 字串
cv.save(path)                         # 寫檔（自動建目錄）
```

---

## 基本圖元

```python
cv.line(p0, p1, color, w=2, dash=None, cap="round", op=1.0)
cv.poly(pts, color, w=2, dash=None, fill="none", op=1.0)   # 折線／曲線
cv.polygon(pts, fill, stroke="none", w=1, op=1.0)          # 填色多邊形
cv.circle(p, r, fill="none", stroke, w=2, dash=None)       # r 為模型單位
cv.dot(p, r=4.5, fill, stroke="#FFFFFF", w=1.6)            # 節點；r 為像素
cv.rect_px(x, y, w, h, fill, rx=10, stroke="none", sw=1)   # 像素座標矩形
cv.panel(title=None, sub=None, pad=6, radius=14)           # 子圖外框＋標題
```

`cap="butt"` 用於構材（端點不圓角，接頭才會對齊）；`cap="round"` 用於力線。

---

## 文字與數學符號

```python
cv.text(p, s, size=15, color, anchor="middle", weight="400",
        italic=False, dx=0, dy=0, font=None, baseline="middle")
cv.text_px(x, y, s, ...)          # 像素座標版
cv.math(p, s, ...)                # 襯線斜體，數學符號用
cv.math_px(x, y, s, ...)
```

上下標語法：`_{下標}`、`^{上標}`，單字元可省大括號。

```python
cv.math_px(x, y, "K_{33} = 24EI/L^{3}", 15, C["bmd"], weight="700")
```

含上下標且 `anchor` 為 `middle`/`end` 時，會自動改為 `start` 並以 `est_width()`
估算寬度補償位移——因為部分渲染器（含 WeasyPrint）對 `text-anchor` + `tspan dy`
的處理不一致。

**不要使用 `²` `³` `₁` `₂` 這類 Unicode 上下標字元**，數學襯線字型常缺字。

文字內容含 `&` `<` `>` 時用 `esc()` 跳脫。

---

## 力與箭頭

```python
cv.arrow(p0, p1, color, w=3.2, head=10, dash=None)   # p0 起點 → p1 箭頭端
cv.double_arrow(p0, p1, color, w=3.0, head=10)       # 雙箭頭（力偶、對稱標示）
cv.moment_arrow(p, r=22, ccw=True, color, w=2.8, span=250, start=110)
```

`moment_arrow` 的 `start` 為起始角（數學角，度；0° 指向 +x，逆時針增加），
`span` 為跨越角度。門型構架節點常用 `r=26, span=235, start=205`。

```python
cv.udl(p0, p1, height, n=9, color, w=2.0, taper=None, label=None)
```

均佈／梯形載重。`height` 為載重高度（模型單位），法向為 `(-dy, dx)/L`；
`taper=(h0, h1)` 畫梯形。`height` 建議取跨度的 0.08～0.12，太大會撞到子圖標題。

---

## 支承符號

```python
cv.fixed_support(p, ang=0, size=20, color)
cv.pin_support(p, ang=0, size=16, color, ground=True)
cv.roller_support(p, ang=0, size=16, color)
cv.support(p, kind, ang=0, size=None, color)     # kind: 'fixed'|'pin'|'roller'
```

`ang=0` 支承面在下方；`ang=90` 為左側牆面；`ang=-90` 為右側牆面。
桁架題常見的「銷接於右側牆面」用 `cv.support(p, 'pin', -90)`。

---

## 尺寸線、座標軸、圖例

```python
cv.dim(p0, p1, label, off=0, color, size=14, label_off=13)
```

`off` 沿法線 `(-dy, dx)/L` 偏移（像素）。方向速記：

| 量測方向 | `off > 0` 落在 |
|---|---|
| 水平（左→右） | 下方 |
| 垂直（下→上） | 右方 |

`label_off` 同一法線方向的標註偏移，正負與 `off` 一致。

```python
cv.axes(origin, lx=1.0, ly=1.0, labels=("x", "y"), color, w=1.8)
cv.legend(x, y, items, size=12.5, gap=20, swatch=22)   # items: [(color, '說明')]
```

---

## 撓曲形狀

以三次 Hermite 形狀函數取樣，回傳整體座標點列，直接餵給 `cv.poly()`。

```python
hermite(v1, t1, v2, t2, Lm, n=60)    # → [(ξ, w)]；底層函式
column_shape(base, Lm, delta_top, theta_top, delta_bot=0.0, theta_bot=0.0, n=60)
beam_shape(left, Lm, theta_L, theta_R, v_L=0.0, v_R=0.0, n=60)
member_shape(p0, p1, w_of_xi, n=60)  # 任意方向構材，自訂撓度函數
```

**轉角一律為整體逆時針正。** 垂直桿件內部換算為 `du/dy = -θ`。

門型構架側移模式的標準寫法：

```python
D  = 0.185                     # 繪圖用側移量（模型單位）
th = -0.6 * D                  # θ_ccw = -3Δ/(5L)，L=1；解題用順時針正故取負
cv.poly(column_shape((0, 0), 1.0, D, th), C["deform"], 5.4)
cv.poly(column_shape((1, 0), 1.0, D, th), C["deform"], 5.4)
cv.poly(beam_shape((D, 1), 1.0, th, th), C["deform"], 5.4)
```

反曲點位置應由彎矩內插算出後再標，不要目測：

```python
xi = M_base / (M_base + M_top)          # = 4/7
u  = D * (2.4*xi**2 - 1.4*xi**3)        # 該處的側向位移
cv.dot((u, xi), 5.4, fill="#FFFFFF", stroke=C["accent"], w=2.9)
```

---

## 多聯圖 compose

```python
compose(panels, title=None, sub=None, note=None, cols=None,
        pad_top=None, pad_bottom=46, bg="#FFFFFF", path=None)
```

`panels` 為尺寸相同的 `Canvas` 串列。`cols=1` 為直向堆疊。
每格會自動套 `clipPath`，防止溢出侵入鄰格。回傳 SVG 字串；給 `path` 則同時寫檔。

---

## recipes 高階產生器

全部位於 `scripts/recipes.py`。共同參數：`title`、`note`、`path`、`W`、`H`。

```python
plot_function(cv, xs, ys, scale, base_y=0.0, x0=0.0, color, fill,
              w=2.2, marks=None, zero_line=True)
```
沿水平方向畫填色函數圖（SFD／BMD／撓度通用）。`marks` 為 `[(x, '文字', dy_px)]`。

```python
beam_vm(span, xs, V, M, supports=(), point_loads=(), udls=(),
        title, note, path, W=760, PH=210, v_unit="", m_unit="", key_V=(), key_M=())
```
梁三聯圖：載重／SFD／BMD。`supports=[(x,'pin')]`、`udls=[(x0,x1,'w')]`、
`point_loads=[(x,'P')]`。**`V` 與 `M` 必須由解題算出**，不可由本函式代算。
各聯的基線位置與比例會依數值正負範圍自動配置。

```python
mohr3(s1, s2, s3, unit="MPa", names=("σ_{1}","σ_{2}","σ_{3}"), ...)
mohr2(sx_, sy_, txy, unit="MPa", ...)
```
三圓／二維莫爾圓。`mohr3` 自動排序主應力並標出三個 $\tau_{ij}$；
`mohr2` 標出 X／Y 點、主應力、$\tau_{max}$ 與 $2\theta_p$。

```python
rc_flexure(b, h, d, c, a, labels=None, ..., PW=330, PH=420, bars=3)
```
RC 斷面／應變／等值應力塊三聯圖。`c`、`a` 由解題提供。
垂直尺度三格共用（故 c、a、d 的相對位置為真），水平尺度為示意。
`labels` 可覆寫 `eps_cu`／`eps_s`／`fc`／`Cc`／`T`／`c`／`a`／`b`／`h`／`d`。

```python
pm_interaction(M, P, marks=(), m_unit="kN·m", p_unit="kN", ...)
```
P-M 交互曲線。`marks=[(M, P, '標籤')]` 標示純壓、平衡點、拉力控制等關鍵點。

```python
truss_forces(nodes, members, supports=(), loads=(), margin=110, fmt="{:+.3g}", ...)
```
桁架力流圖。`nodes={'A':(x,y)}`、`members=[('A','B',N)]`（N>0 受拉、N<0 受壓、
N=0 畫灰虛線零桿）。線寬隨 |N| 變化。`loads=[('A',(dx,dy),'P')]`，
畫布邊界會自動涵蓋箭頭尾端。

```python
bar_compare(cases, sketch=None, W=1020, row_h=86, ...)
```
量級比較長條圖，用於「答案應落在什麼區間」的合理性檢核。
`cases=[(名稱, 說明, 數值, 標示式, 顏色)]`，數值最大者為 100%。
`sketch=f(mini_canvas, i)` 可在左側畫迷你示意圖。

---

## 色票

只能使用 `structdraw.C` 中的顏色，不要自行調色。

| 鍵 | 用途 | 鍵 | 用途 |
|---|---|---|---|
| `member` | 構材 | `tension` | 受拉（同 load 紅） |
| `member2` | 次要構材 | `compr` | 受壓（同 deform 藍） |
| `ghost` | 原始未變形位置 | `accent` | 重點標記（反曲點等） |
| `load` | 外力 | `dim` | 尺寸線 |
| `deform` | 變形、位移、自由度 | `text` / `muted` | 文字 |
| `bmd` | 彎矩圖 | `panel` / `border` | 子圖底色與外框 |
| `sfd` | 剪力圖 | `fill_t/c/m/s` | 對應的半透明填色 |
