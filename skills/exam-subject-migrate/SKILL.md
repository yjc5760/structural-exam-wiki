---
name: exam-subject-migrate
description: 把某一科的獨立知識庫 repo（exam-wiki-RC／SA／SD／SM）搬進五科合一的 structural-exam-wiki/XX/：盤點、複製、wiki 封存、共用腳本與 skills 併入根目錄、規則寫進 SUBJECT.md、分類稽核、逐檔驗證。說「把 exam-wiki-XX 搬進來」「搬 RC 科」「科目搬入」時使用。
---

# exam-subject-migrate — 科目搬入 structural-exam-wiki

把一科的獨立 repo 搬進五科合一知識庫的 `XX/` 資料夾。根目錄 `CLAUDE.md`「科目搬入」寫的是規則，本 skill 是執行步驟。
第一次完整做過的是 SS（2026-11-08，紀錄見 `SS/SUBJECT.md` §9 與根目錄 CLAUDE.md CHANGELOG），可當範本對照。

## 已定案的原則（不用再問使用者）

- **只搬檔案，不帶 git 歷史**；原 repo 原封不動（不 commit、不改、不刪），當歷史封存。
- **原 repo 的 GitHub Pages 舊網址先維持上線**，頁面內的絕對網址先不改，記成 `SUBJECT.md` §10 的待辦。
- **wiki 封存**：原 repo 的 `wiki/` 除 `queries/` 外整批移到 `XX/archive/wiki/`；`wiki/log.md` 移成 `wiki/queries/log.md`（內容不改）。
- **共用的東西只放一份**：通用腳本進根目錄 `scripts/`、skill 進根目錄 `skills/`，科目資料夾不留副本（規則 11、12）。
- **主副分類只填本科子項**：指向他科的分類列出改歸建議，**使用者確認後**才改索引。
- **不 git commit**：寫完檔就停，列出動到的路徑交給使用者。

遇到原則沒涵蓋、又難以回頭的事（例如原 repo 有尚未 commit 的變更、兩邊同一檔各自改過、原 repo 的規則和根目錄衝突）→ 停下來問。

## 環境須知（SS 搬家時踩過的坑）

- 兩個資料夾都要先連上：原 repo（如 `C:\Users\yjc57\Downloads\exam-wiki-RC`）與 `structural-exam-wiki`。用 device_bash 操作，路徑在 `$HOME/mnt/<資料夾名>/`。
- **device_bash 背景程序在指令結束時會被終止**：rsync 不能 `nohup … &`，要在前景分批跑（每次 ≤ 180 秒，大資料夾一個一個來）。
- **device_commit_files 一次傳很多檔會逾時**：超過十來個檔就先在雲端打包成 zip，傳一個檔，再在使用者電腦上用 Python 解開（解完刪 zip）。
- **掛載有延遲**：commit 回報成功後，用 device_bash `grep`／`ls -l` 確認內容真的換了；沒換就再 commit 一次。
- **刪除要授權**：用 `device_request_delete_permission` 對 structural-exam-wiki 申請一次；絕不對原 repo 申請。

## 流程

### 1. 盤點（只讀，不改）

```bash
S=$HOME/mnt/exam-wiki-XX; M=$HOME/mnt/structural-exam-wiki
cd $S && git status --short | wc -l; git log -1 --format='%ci %s'; git remote -v
du -sh $S $S/.git; ls -A $S
find $S -path $S/.git -prune -o -type f -size +50M -print   # GitHub 單檔 100 MB 上限
ls -A $M/XX; cd $M && git status --short | head
```

- 原 repo 有未 commit 的變更 → **停**，請使用者先 commit 或決定要不要帶。
- `M/XX/` 目前是 scaffold 骨架（10-29 建的空頁、七層 wiki 空殼）還是已有內容？有實質內容 → 停下來問。
- 列一張「原 repo 根目錄每一項 → 去處」對照表（見步驟 2），每一項都要有交代。

### 2. 決定每一項的去處

| 原 repo | 去處 |
|---------|------|
| `raw/`、`study/`、`影片講義/`、`解題過程影片/`、`start.html` | `XX/` 同名 |
| `wiki/queries/` | `XX/wiki/queries/` |
| `wiki/` 其餘各層、`wiki/index.md`、`by-year.md` | `XX/archive/wiki/` |
| `wiki/log.md` | `XX/wiki/queries/log.md`（`queries/` 已有 log 時先問） |
| `index.html`、`dashboard-data.js` | 先比對：與根目錄 `scripts/templates/dashboard-index.html` 相容 → 用共用樣板＋`refresh_dashboard.py XX` 重產；原 repo 有自訂改動 → 先沿用原版，記 §10 待辦 |
| `scripts/` 通用腳本 | 與根目錄 `scripts/` 同名檔逐一 `diff`：原 repo 較新且向下相容 → 併入根目錄（並在 SS 上重跑確認不壞）；只是舊版 → 丟棄 |
| `scripts/` 本科一次性腳本（`fixes/` 等） | `XX/scripts/` |
| `skills/` | 與根目錄 `skills/` 逐一比對（**也要和使用者帳號安裝版比**，帳號版可能更新）：取最新的放根目錄，重打包 `.skill`，列入「請使用者重新安裝」清單 |
| `CLAUDE.md`、`CLAUDE-CODE.md`、`CLAUDE-SOLVE.md`、`CLAUDE-SPEC.md`、`xcheck.py` | 參考副本 `XX/archive/exam-wiki-XX-root/`＋一份 README 說明（唯讀） |
| `README.md`、`檔案架構索引表.md`、`知識庫使用說明書.md` | `XX/` 同名，改寫成合併後路徑（範本：`SS/README.md`） |
| `.github/`（勘誤表單、deploy workflow）、`.gitattributes`、`.gitignore`、`.nojekyll` | 根目錄已有就不動；原 repo 有根目錄沒有的（如勘誤表單）才併入 |
| 原 repo 的 `.git/` | 不搬 |

比對帳號安裝版 skill：帳號副本在 `/root/.claude/skills/synced/*/<name>/`（雲端容器內）。比內文時先去掉 `\r` 與 frontmatter 再 `diff`，兩邊各自多出的行都要看。

### 3. 清掉骨架、複製

1. `XX/` 骨架裡 scaffold 產生的七層 wiki 空頁（`wiki/index.md`、`by-year.md`、`concepts/`、`topics/`…）若會和搬入內容衝突，先刪（`SUBJECT.md` 保留）。
2. 分批前景複製，排除不搬的項目：

```bash
rsync -a --exclude='__pycache__/' $S/raw $S/study $M/XX/
rsync -a $S/影片講義 $S/解題過程影片 $S/start.html $M/XX/ 2>/dev/null
mkdir -p $M/XX/wiki $M/XX/archive && rsync -a $S/wiki/queries $M/XX/wiki/
rsync -a --exclude='queries/' --exclude='log.md' $S/wiki/ $M/XX/archive/wiki/
cp -p $S/wiki/log.md $M/XX/wiki/queries/log.md
```

3. 規則檔參考副本、說明文件、腳本、skills 依步驟 2 的表處理。

### 4. 規則寫進 `XX/SUBJECT.md`

- 讀原 repo `CLAUDE.md`／`CLAUDE-CODE.md`／`CLAUDE-SPEC.md`，和根目錄逐項比對，列差異表。
- **本科專屬**（子項表、designMethod 允許值、常見圖解、設計哲學框架、主要規範）→ `SUBJECT.md` §2、§3、§4、§7、§8，並與 `scripts/subject_profiles.json` 同步（規則 10）。
- **看起來該五科通用的差異** → 不要自己改根目錄，列給使用者決定。
- §9 CHANGELOG：加一列搬家紀錄；原 repo CHANGELOG 中 scaffold 日期（2026-10-29）以後的列，原樣放進「獨立 repo 時期的變更紀錄」小節。
- §10：只列仍屬本科專屬或待辦的項目（舊網址、儀表板、一次性腳本…）。

### 5. 分類稽核（要使用者確認）

```bash
cd $M && python scripts/audit_classification.py XX XX --out /tmp/audit-XX.md
```

指向他科的主副分類，每題列「原代號 → 建議本科子項＋理由」，**等使用者確認**再改 `question_index.json`，並在 `wiki/queries/log.md` 記一筆。

### 6. 重產與驗證

```bash
cd $M
python scripts/sync_taxonomy.py
diff -rq -x __pycache__ $S/raw $M/XX/raw && diff -rq -x __pycache__ $S/study $M/XX/study   # 只應有預期差異
python scripts/xcheck.py XX | head -3
python scripts/render_problem_view.py XX-YYYY-N          # 抽一題，和原檔比對應一致
cd XX && python ../scripts/build_frequency.py --check && cd ..
python scripts/build_unit_page.py --all --check --subject XX   # 有 study/data/unit-*.json 才跑
python scripts/build_start.py --repo XX --out /tmp/s.html      # 有 start-links.json 才跑，和原 start.html 比
python scripts/refresh_dashboard.py XX                    # 決定用共用樣板時
```

- 抽查產出頁的站內相對連結都找得到檔案。
- 根目錄 `index.html` 的五科入口讀得到本科題數。
- 有改動根目錄 `scripts/` 時，在 SS 上重跑一次，確認 SS 沒被弄壞。

### 7. 收尾

- 記錄：`XX/SUBJECT.md` §9、根目錄 `CLAUDE.md` CHANGELOG、`XX/wiki/queries/log.md` 各一筆。
- 回報使用者：
  - 搬了什麼、各項去處（一句一類）
  - 驗證結果（逐檔比對、重產一致、xcheck）
  - **需要使用者決定的**：疑似通用的規則差異、分類改歸清單、儀表板與網址待辦
  - **需要重新安裝的 skill**（`.skill` 可用 SendUserFile 傳到對話讓使用者直接按 Save）
  - commit 前須知：`git status` 會出現骨架檔的刪除（正常）；根目錄若有不相干的檔案提醒別一起 commit
  - 動到的路徑清單（不 commit）

## 不要做的事

- 改動、commit 或刪除原 repo 的任何檔案
- 把原 repo 的七層 wiki 放回 `XX/wiki/`，或把通用腳本留一份在 `XX/scripts/`
- 未經使用者確認就改分類、改根目錄通用規則
- 用背景程序跑 rsync；一次 commit 幾十個檔
- 一次搬兩科（規則 9：一個指令只動一科）
