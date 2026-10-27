# Exam Playbook

> The 2023, 2024 and 2025 papers use **almost the same 16-question template**. If you can do every row of the table below, you can do the exam.

**Timing:** 180 min for 80 marks is about **2.2 min per mark**. A 6-mark question deserves about 13 minutes. Use the 10 min of perusal to find the MATLAB questions and the derivations you know cold.

---

## 1. Question map (what each number has been, 2023 → 2025)

| Q | Topic | Marks | 2023 | 2024 | 2025 | Notes |
|---|---|---|---|---|---|---|
| 1 | Floating point | 4 | decimal→binary; smallest + | binary→decimal; unit roundoff | smallest +; **cancellation rearrangement** | [Wk 1](week01_errors_floating_point.md), [Wk 2](week02_cancellation_taylor.md) |
| 2 | Taylor + error bound | 6 | $\sin$, $n=1$, $x_0=\pi/6$ | $\sin$, $n=3$ | $\cos$, $n=2$ | [Wk 2](week02_cancellation_taylor.md) |
| 3 | ODE: 1 step × 2 methods + "which is better" | 6 | Euler + Mod Euler | Euler + Mod Euler | Euler + Taylor 2 | [Wk 3](week03_odes_euler.md), [Wk 4](week04_higher_order_ode_methods.md) |
| 4 | **MATLAB: ODE code** | 6 | Taylor 2 | Taylor 2 | RK4 | [Wk 4 §5](week04_higher_order_ode_methods.md) |
| 5 | **Derive** an ODE method | 4 | Taylor 2 | **Mod Euler** | **Mod Euler** | [Wk 4](week04_higher_order_ode_methods.md) |
| 6 | Lagrange (or **MATLAB Lagrange**) | 6 | MATLAB | Lagrange + bound | MATLAB | [Wk 5](week05_interpolation_lagrange.md) |
| 7 | Newton forward difference + estimate | 4 | $\sqrt x$ | $\log x$ | $\sin x$ | [Wk 7](week07_newton_forward_differences.md) |
| 8 | Divided difference algebra | 4 | expand $f[x_0..x_3]$ | prove $=\Delta^2y_0/2h^2$ | expand $f[x_0..x_3]$ | [Wk 6](week06_newton_divided_differences.md), [Wk 7](week07_newton_forward_differences.md) |
| 9 | Bracket + bisection / Newton / secant | 6 | bracket, bisect ×2, secant | bracket, Newton, secant | bracket, bisect ×2, Newton | [Wk 8](week08_bisection_fixed_point.md), [Wk 9](week09_newton_secant.md) |
| 10 | **MATLAB root code** or derive Newton | 3–6 | MATLAB Newton | MATLAB bisection | derive Newton | [Wk 8](week08_bisection_fixed_point.md), [Wk 9](week09_newton_secant.md) |
| 11 | Derive iteration / derive $f''$ formula | 4–6 | derive central $f''$ + choice of $h$ | Newton → $\sqrt[3]a$ | secant → $\sqrt a$ | [Wk 9](week09_newton_secant.md), [Wk 10](week10_numerical_differentiation.md) |
| 12 | Finite differences from table | 4 | backward, central $f'$ | backward, central $f''$ | forward, central $f''$ | [Wk 10](week10_numerical_differentiation.md) |
| 13 | Derive Trap/Simpson **or MATLAB trapezoid** | 5–6 | derive Trap | derive Simpson | MATLAB Trap | [Wk 11](week11_numerical_integration.md) |
| 14 | Trap + Simpson, $n=4$ | 4–6 | + which is better | from table | from table | [Wk 11](week11_numerical_integration.md) |
| 15 | LU fill-in (+ solve / explain) | 5 | fill + explain | fill + backward solve | forward solve + fill | [Wk 12](week12_lu_factorisation.md) |
| 16 | SPD / Cholesky | 4–6 | properties + fill | fill + is it SPD? | show PD + fill | [Wk 13](week13_cholesky.md) |

**Topics NOT examined in those 3 papers** (still examinable, but lower risk): fixed point iteration by hand, RK4 by hand, IEEE derivations, overflow/underflow, the full Newton divided difference construction, convergence-rate theory. Have a quick look at each anyway.

---

## 2. MATLAB bug catalogue (18 marks every year)

Each question asks for **3 errors**, worth 1 mark to identify + 1 to fix each. State the **line number**, **what's wrong**, and **the corrected line**.

### The 10 bug types that have actually appeared

| # | Bug type | Example | Fix |
|---|---|---|---|
| 1 | Variable never initialised | no `t = 2;` / no `w = 3;` before loop | add it before the loop |
| 2 | Wrong initial value | `w = 2` when $y(0)=1$ | `w = 1` |
| 3 | Arguments swapped | `f(w,t)`, `fdash(w,t)` | `f(t,w)` |
| 4 | Missing chain rule in $f'$ | `fdash = @(t,y) 4 + 2*y` | `4 + 2*y*f(t,y)` |
| 5 | Wrong coefficient in a scheme | RK4 `w+k3/2` in `k4`; trapezoid missing `2*` | `w+k3`; `2*f(x(i))` |
| 6 | Wrong `h` / midpoint | `h=(a+b)/n`; `p=(b-a)/2` | `(b-a)/n`; `(a+b)/2` |
| 7 | Off-by-one index | `f(x(n))` as the last point | `f(x(n+1))` |
| 8 | Reversed stopping logic | `while abs(x-x_old) < tol`; `if (b-a) > tol, break` | `> tol`; `<= tol` |
| 9 | Formula upside down / wrong update | `x - fdash(x)/f(x)`; bisection `a = b` | `x - f(x)/fdash(x)`; `b = p` |
| 10 | Vector ops / denominators / relative error | `exp(x)*sin(5*x)` on a vector; wrong `(x(i)-x(j))`; `rel = .../P2(a)` | `.*`; fix the index; `.../abs(f(a))` |

### Reading strategy
1. Write the **correct algorithm** in your head (or in the margin) first.
2. Go **line by line**: is every variable defined before it's used? Do the argument orders match the definitions?
3. Check **loop bounds and indices** (MATLAB starts at 1, and $n$ intervals means $n+1$ points).
4. Check **loop and stop conditions** ("keep going while NOT converged").
5. Check **`.*` `./` `.^`** wherever a vector is passed.

---

## 3. Derivations you must be able to reproduce

| Derivation | Appeared | Key move |
|---|---|---|
| Euler | (template) | degree-1 Taylor at $t_i$, evaluate at $t_{i+1}$, $y'=f$, drop $O(h^2)$ |
| **Taylor 2** | 2023 Q5 | degree-2 Taylor, $y''=f'$ |
| **Modified Euler** | 2024, 2025 Q5 | Taylor 2 + $f'\approx\frac{f_{i+1}-f_i}{h}$, then Euler for $w_{i+1}$ on the RHS |
| **Newton's method** | 2025 Q10 | tangent line, set $=0$ |
| **Newton → $\sqrt[3]a$**, **Secant → $\sqrt a$**, Heron | every Q11 | choose $f=x^k-a$; difference of squares for secant |
| Expand $f[x_0,x_1,x_2,x_3]$ | 2023, 2025 Q8 | apply the definition recursively, one line per level |
| $f[x_0,x_1,x_2]=\Delta^2y_0/(2h^2)$ | 2024 Q8 | substitute $x_{i+1}-x_i=h$ |
| **Central $f''$ + error** | 2023 Q11 | add the degree-3 Taylor expansions at $\pm h$, then IVT |
| Central $f'$, forward $f'$ | lectures | subtract the degree-2 expansions / degree-1 Taylor |
| **Trapezoid** from $P_1$, composite | 2023 Q13 | $x=x_0+sh$, $\int_0^1$, sum over strips |
| **Simpson** from $P_2$ | 2024 Q13 | $\int_0^2$, substitute the $\Delta$'s |
| Cancellation rearrangement | 2025 Q1 | multiply by the conjugate |
| Positive definite via $\mathbf x^TA\mathbf x$ | 2025 Q16 | complete the square |

---

## 4. "Which is more accurate? Justify" templates

- **ODE:** "(b), since [Mod Euler / Taylor 2 / RK4] is a **second [fourth] order** method (global error $O(h^2)$ [$O(h^4)$]) whereas Euler is **first order** ($O(h)$)."
- **Quadrature:** "Simpson, since it is **fourth order** ($O(h^4)$) whereas the trapezoidal rule is **second order** ($O(h^2)$)."
- **Finite differences:** "the central difference, since it is **second order** ($O(h^2)$) whereas forward/backward are **first order** ($O(h)$)."
- **Root finding:** "Newton converges **quadratically** (correct digits roughly double each step), secant at order ≈1.618, bisection and fixed point **linearly**."
- **Choice of $h$:** "too large gives **truncation** error, too small gives **roundoff** error (catastrophic cancellation)."

---

## 5. ⚠️ Errors in the official solutions (don't let them confuse you)

| Paper | Question | Official solution says | Correct |
|---|---|---|---|
| 2025 | Q3a Euler | $w_1=1.2$ | $w_1=1+0.25(1+1/1)=\mathbf{1.5}$ (consistent with their own Q3b answer of 1.53125) |
| 2025 | Q4 RK4 code | "initial value of w should be 2, not 1" | the code has `w = 2` but $y(0)=1$, so it should be **`w = 1`** |
| 2025 | Q9b bisection | $f(2.5)$ negative; answer 1.5 | $f(2.5)=+3.625$, so $b=2.5$; approximation after 2 iterations is **2.5** |
| 2025 | Q12a | calls it "backward difference" | it's a **forward** difference (left end of the table) |
| 2025 | Q14 | writes $\int_0^1$ | $\int_0^2$ (the numbers are correct) |
| 2024 | Q6a | $y_1=0.5$, $y_2=-1$ | $y_1=\cos\frac\pi6=\frac{\sqrt3}2$, $y_2=\cos\frac\pi2=0$ |
| 2024 | Q3 | writes $y(0.1)$ | $y(2.1)$ (the numbers are correct) |
| 2023 | Q6 | fix: `exp(-x).*(5*x)` | `exp(-x).*cos(5*x)` |

---

## 6. Suggested A4 sheet (double-sided)

**Side 1 (Qianqian: Topics 1–3)**
- $F(\beta,k,m,M)$: $S=\beta^m$, $L=(\beta-\beta^{1-k})\beta^M$, $u=\frac12\beta^{1-k}$; binary conversion method
- Cancellation fixes table (conjugate, log rules, $1-\cos x$)
- Taylor $P_n$, $R_n=\frac{f^{(n+1)}(c)}{(n+1)!}(x-x_0)^{n+1}$, and the 5-step bound recipe
- Euler, Taylor 2 (+ chain rule $f'=f_t+f_y f$), Mod Euler ($k_1,k_2$), RK4 ($k_1..k_4$), order table
- Mod Euler derivation skeleton (4 lines)
- Lagrange $L_{n,i}$, remainder with $\prod(x-x_i)$
- Divided difference definition + table shape; forward difference table, $\binom sk$, $s=(x-x_0)/h$, $f[\dots]=\Delta^ky_0/(k!h^k)$

**Side 2 (Elliot: Topics 4–6)**
- IVT/bracketing sentence; bisection table layout; fixed point theorem conditions
- Newton, secant formulas; convergence orders (1, 1, 1.618, 2)
- Q11 strategy: $f=x^k-a$; difference of squares
- Finite difference table (5 formulas + errors); which to use at the ends; $h$ trade-off sentence
- Trapezoid ($\frac h2[1,2,\dots,2,1]$), Simpson ($\frac h3[1,4,2,\dots,4,1]$); errors; exactness
- Trapezoid/Simpson derivation skeleton ($x=x_0+sh$)
- LU 3×3 formulas + order; "explain in words" 3 lines
- Cholesky 3×3 formulas; SPD definition; completing the square
- MATLAB bug checklist (the 10 types)

---

## 7. Final-week plan

1. **Day 1:** read [00_big_picture_methods.md](00_big_picture_methods.md), then do the 2023 paper **timed** and mark it.
2. **Day 2:** work through the weak topics with the week files and their practice questions; write out every derivation in §3 from memory.
3. **Day 3:** do the 2024 paper timed; drill the MATLAB catalogue.
4. **Day 4:** do the 2025 paper timed (watch for the solution errors in §5); finalise the A4 sheet.
5. **Day 5:** do [Practice Exam 1](../practice_exams/practice_exam_1.md) timed, mark it with [its solutions](../practice_exams/practice_exam_1_solutions.md), and revisit the step-by-step sections for anything you dropped marks on.
6. **Day 6:** do [Practice Exam 2](../practice_exams/practice_exam_2.md) timed, then mark it with [its solutions](../practice_exams/practice_exam_2_solutions.md).
7. **Night before:** reread the traps sections and the A4 sheet. **Check that your calculator is in radian mode.**
