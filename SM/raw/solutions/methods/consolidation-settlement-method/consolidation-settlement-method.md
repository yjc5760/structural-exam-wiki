# 方法論：Terzaghi 一維壓密沉陷計算

**method_id：** consolidation-settlement-method
**適用單元：** [[SM-U1-3]]
**適用規範條文：** 大地工程手冊（一維壓密理論章節）

---

## 適用題型

飽和黏土層在附加應力下之長期壓密沉陷量與沉陷-時間關係計算，包含正常壓密與過壓密情況。

## 核心公式

正常壓密：$S_c = \dfrac{C_c H}{1+e_0}\log\dfrac{p_0'+\Delta p}{p_0'}$

過壓密（$p_0'+\Delta p \le p_c'$）：$S_c = \dfrac{C_r H}{1+e_0}\log\dfrac{p_0'+\Delta p}{p_0'}$

過壓密跨越 $p_c'$：$S_c = \dfrac{C_r H}{1+e_0}\log\dfrac{p_c'}{p_0'} + \dfrac{C_c H}{1+e_0}\log\dfrac{p_0'+\Delta p}{p_c'}$

時間關係：$T_v = C_v t / H_{dr}^2$，$U<60\%$ 時 $T_v=\frac{\pi}{4}U^2$；$U\ge60\%$ 時 $T_v = 1.781-0.933\log_{10}(100-U)$。

## 步驟摘要

1. 求初始有效覆土應力 $p_0'$（通常取土層中點深度）與過壓密應力 $p_c'$，判斷 OCR = $p_c'/p_0'$。
2. 求附加應力 $\Delta p$（常用 2:1 應力傳佈法或 Boussinesq 角隅法，見 [[BOUSSINESQ-STRESS-INCREASE]]）。
3. 判斷 $p_0'+\Delta p$ 與 $p_c'$ 的相對位置，選用對應的 $C_c$/$C_r$ 組合公式計算最終沉陷量 $S_c$。
4. 若題目要求沉陷-時間關係，先由已知條件反推壓密係數 $k=T_v/t$ 或直接給定 $C_v$，再依 $H_{dr}$（單向或雙向排水）求任意時刻的 $T_v$ 與對應 $U$。
5. 依 $U<60\%$ 或 $\ge60\%$ 切換公式，避免使用錯誤區間的近似式。

## 常見陷阱

正常壓密與過壓密段誤用同一 Cc；忘記依單向/雙向排水正確設定 $H_{dr}$；U=60%轉折點公式誤用。
