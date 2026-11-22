"""SM-2018-3 geometry: finite-difference head and stream function (for the lecture's flow-net illustration).
Domain: soil from ground (y=0) to impervious layer (y=-17.2); dam base at y=-1.6 for 0<=x<=50; cutoff at x=0 from -1.6 to -9.4.
Upstream ground (x<0, y=0): h = 6.3; downstream ground (x>50, y=0): h = 0; no-flow elsewhere. Lateral truncation at x=-60, 110."""
import numpy as np, scipy.sparse as sp, scipy.sparse.linalg as spl
DX = 0.2
X0, X1, Y0, Y1 = -60.0, 110.0, -17.2, 0.0
nx = int(round((X1 - X0)/DX)) + 1; ny = int(round((Y1 - Y0)/DX)) + 1
xs = X0 + DX*np.arange(nx); ys = Y0 + DX*np.arange(ny)
I0 = int(round((0 - X0)/DX)); I50 = int(round((50 - X0)/DX))
JB = int(round((-1.6 - Y0)/DX)); JW = int(round((-9.4 - Y0)/DX)); JT = ny - 1
def active(i, j):  # soil node?
    if I0 <= i <= I50 and j > JB: return False   # inside dam
    return True
def blocked(i1, j1, i2, j2):  # flux blocked between neighbours (thin cutoff between columns I0-1 and I0)
    if j1 == j2 and {i1, i2} == {I0 - 1, I0} and JW <= j1 <= JB: return True
    return False
def solve(dirichlet):
    idx = -np.ones((nx, ny), int); n = 0
    for i in range(nx):
        for j in range(ny):
            if active(i, j): idx[i, j] = n; n += 1
    A = sp.lil_matrix((n, n)); b = np.zeros(n)
    for i in range(nx):
        for j in range(ny):
            k = idx[i, j]
            if k < 0: continue
            dv = dirichlet(i, j)
            if dv is not None:
                A[k, k] = 1; b[k] = dv; continue
            diag = 0
            for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                i2, j2 = i + di, j + dj
                if not (0 <= i2 < nx and 0 <= j2 < ny) or idx[i2, j2] < 0 or blocked(i, j, i2, j2): continue
                A[k, idx[i2, j2]] = -1; diag += 1
            A[k, k] = diag
    sol = spl.spsolve(A.tocsr(), b)
    F = np.full((nx, ny), np.nan)
    for i in range(nx):
        for j in range(ny):
            if idx[i, j] >= 0: F[i, j] = sol[idx[i, j]]
    return F
def head():
    def d(i, j):
        if j == JT and i < I0: return 6.3
        if j == JT and i > I50: return 0.0
        return None
    return solve(d)
def stream():
    # psi = 0 on dam base and both faces of the cutoff (the inner impervious boundary), psi = 1 on impervious bottom and lateral sides;
    # ground surfaces are equipotentials -> Neumann for psi (natural).
    def d(i, j):
        if j == 0 or i == 0 or i == nx - 1: return 1.0
        if JB == j and I0 <= i <= I50: return 0.0
        if i in (I0 - 1, I0) and JW <= j <= JB: return 0.0
        return None
    return solve(d)
if __name__ == '__main__':
    import time; t = time.time(); H = head(); P = stream(); print(nx, ny, time.time() - t)
    np.savez('/tmp/fn.npz', H=H, P=P, xs=xs, ys=ys)
    # equivalent shape factor: q/(k dH) from flux through downstream surface
    j = JT; q = 0
    for i in range(I50 + 1, nx):
        q += (H[i, j - 1] - H[i, j])/DX*DX
    print('shape factor q/(k*dH) =', q/6.3)
    for nm, x in zip('abcde', [0.0 + DX, 12.5, 25, 37.5, 50]):
        i = int(round((x - X0)/DX)); print(nm, x, 'h =', round(H[i, JB], 3))
