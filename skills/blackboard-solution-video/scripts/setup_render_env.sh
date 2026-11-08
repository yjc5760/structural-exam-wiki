#!/usr/bin/env bash
# 在 Linux（雲端沙箱／WSL）裝好渲染環境：Manim 0.21、pango、dvisvgm、LaTeX、芫荽 Iansui 字型。
# 已裝好的步驟會自動跳過。用法：bash setup_render_env.sh
set -u
need_apt=()
dpkg -s libpango1.0-dev >/dev/null 2>&1 || need_apt+=(libpango1.0-dev)
dpkg -s libcairo2-dev   >/dev/null 2>&1 || need_apt+=(libcairo2-dev)
command -v dvisvgm >/dev/null || need_apt+=(dvisvgm)
command -v latex   >/dev/null || need_apt+=(texlive-latex-extra texlive-fonts-recommended)
command -v ffmpeg  >/dev/null || need_apt+=(ffmpeg)
if [ ${#need_apt[@]} -gt 0 ]; then
  echo "apt 安裝：${need_apt[*]}"
  (apt-get install -y -q "${need_apt[@]}" || (apt-get update -q; apt-get install -y -q "${need_apt[@]}")) >/tmp/apt.log 2>&1 \
    || echo "⚠ apt 失敗，見 /tmp/apt.log"
fi

if ! python3 -c "import manim" 2>/dev/null; then
  PIP="pip install -q --break-system-packages"
  # manim 依賴的 srt 套件在部分 Debian/Ubuntu 的 setuptools 下 build 失敗（install_layout 錯誤）：
  # 改成直接把 srt.py 放進 site-packages
  if ! python3 -c "import srt" 2>/dev/null; then
    $PIP srt 2>/dev/null || {
      tmp=$(mktemp -d); pip download -q srt==3.5.3 --no-deps --no-binary :all: -d "$tmp"
      tar xzf "$tmp"/srt-3.5.3.tar.gz -C "$tmp"
      SP=$(python3 -c "import site;print(site.getsitepackages()[0])")
      cp "$tmp"/srt-3.5.3/srt.py "$SP"/
      mkdir -p "$SP"/srt-3.5.3.dist-info
      printf "Metadata-Version: 2.1\nName: srt\nVersion: 3.5.3\n" > "$SP"/srt-3.5.3.dist-info/METADATA
      touch "$SP"/srt-3.5.3.dist-info/RECORD
    }
  fi
  $PIP manim numpy
fi
python3 -c "import manim;print('manim', manim.__version__)"

if ! fc-list | grep -qi iansui; then
  mkdir -p ~/.fonts
  tmp=$(mktemp -d)
  git clone -q --depth 1 https://github.com/ButTaiwan/iansui.git "$tmp/iansui" \
    && cp "$tmp"/iansui/fonts/ttf/Iansui-Regular.ttf ~/.fonts/ && fc-cache -f >/dev/null
fi
fc-list | grep -qi iansui && echo "字型 Iansui OK" || echo "⚠ 沒裝到 Iansui，中文會用系統字型"
fc-list | grep -qi "Noto Sans CJK TC" || echo "（提示：燒字幕用 Noto Sans CJK TC，沒有也會退回其他中文字型）"
