# MXB103 Formula Sheet

> Everything you need to **memorise**, week by week. Each formula has a short **meaning** and a quick worked example (**e.g.**) underneath. Each week ends with **Remember** notes: the non-formula facts the exam keeps testing.
> Most examples come from the 2023–2025 exams or the lecture problems, so they double as revision of real questions.
> The full explanations and examples are in each `weekXX_*.md` file.

---

## Week 1: Errors & floating point (4 formulas)

**1.1 Absolute and relative error**
$$\text{abs} = |x-\tilde x|\qquad \text{rel}=\frac{|x-\tilde x|}{|x|}$$
> $x$ = true value, $\tilde x$ = approximation. Relative error ≈ the number of correct digits, and it's the one to trust when numbers are very big or very small.

**e.g.** True value $x=4.0$, approximation $\tilde x=4.1$:
- abs $=|4.0-4.1|=0.1$
- rel $=\frac{0.1}{4.0}=0.025$

Now shrink both: $x=4.0\times10^{-3}$, $\tilde x=4.1\times10^{-3}$:
- abs $=10^{-4}$ (looks tiny!)
- rel $=\frac{10^{-4}}{4.0\times10^{-3}}=0.025$ (exactly as good as before)

**Edge case: the true value is 0.** Relative error is undefined:
- $x=0$, $\tilde x=10^{-5}$: rel $=\frac{10^{-5}}{0}$ is undefined, so report abs $=10^{-5}$ instead
- always divide by the **true** value $|x|$, never by $|\tilde x|$ (a recurring MATLAB bug)

**1.2 Smallest positive number in $F(\beta,k,m,M)$**
$$S=1.00\cdots0\times\beta^{m}=\beta^{m}$$
> Smallest significand (1.000…) times the smallest exponent. Anything smaller underflows to 0.

**e.g.** $F(2,5,-4,4)$, so $\beta=2$ and $m=-4$ (2025 Q1a):
- smallest significand: $1.0000_2=1$
- smallest exponent: $2^{-4}$
- $S=1\times2^{-4}=0.0625$

**Edge case: underflow.** Same system (allowed exponents $-4\le e\le4$):
- $x=0.1=(1.10011\ldots)_2\times2^{-4}$: $e=-4$ is allowed, so it is stored (rounded) ✓
- $x=0.05=(1.10011\ldots)_2\times2^{-5}$: $e=-5<m=-4$, so **underflow** and $fl(x)=0$ ✗
- quick test: $0.05<S=0.0625$, so it was always going to underflow

**1.3 Largest number**
$$L=(\beta-1).(\beta-1)\cdots(\beta-1)\times\beta^{M}=(\beta-\beta^{1-k})\,\beta^{M}$$
> Every digit at its maximum, times the largest exponent. Anything bigger overflows to Inf.

**e.g.** $F(2,4,-2,3)$, so $\beta=2$, $k=4$, $M=3$:
- largest significand: $1.111_2=1+\frac12+\frac14+\frac18=1.875$
- largest exponent: $2^3=8$
- $L=1.875\times8=15$
- formula check: $(2-2^{1-4})\times2^3=(2-0.125)\times8=15$ ✓

**Edge case: overflow.** Same system (allowed exponents $-2\le e\le3$):
- $x=13=1101_2=1.101_2\times2^3$: $e=3$ is allowed, so it is stored exactly ✓
- $x=20=10100_2=1.0100_2\times2^4$: $e=4>M=3$, so **overflow** and $fl(x)=$ Inf ✗
- sneaky case, $x=15.75=1.11111_2\times2^3$: $e=3$ looks fine, but rounding to 4 digits gives $1.111|11\to10.000_2$, so $x$ becomes $1.000_2\times2^4$. Now $e=4>3$, so **overflow** ✗ (it rounded past $L=15$)

**1.4 Unit roundoff**
$$u=\tfrac12\,\beta^{1-k}\qquad\text{so}\qquad\frac{|x-fl(x)|}{|x|}\le u$$
> The worst relative error from rounding a number into $F$. It depends only on the base and the number of digits.

**e.g.** $F(3,6,-7,8)$, so $\beta=3$ and $k=6$ (2024 Q1b):
- $u=\frac12\cdot3^{1-6}=\frac12\cdot3^{-5}=\frac1{486}=0.0021$
- meaning: rounding any number into this system gives a relative error of at most $0.21\%$

**Edge case: the bound fails when you underflow.** In $F(10,2,-1,1)$, $u=\frac12\cdot10^{-1}=0.05$:
- $fl(0.04)=0$ (underflow), so the relative error is $\frac{|0.04-0|}{0.04}=1$, far bigger than $u$
- $u$ only bounds the rounding of numbers **inside** the range $[S,L]$
- a number already in $F$ has zero error, e.g. $fl(0.23)=0.23$

**Remember**
- $F(\beta,k,m,M)$ stores $\pm d_1.d_2\cdots d_k\times\beta^e$ with $d_1\neq0$ and $m\le e\le M$. Here $k$ counts **all** digits, including $d_1$.
- Decimal → binary: divide the integer part by 2 (read remainders **upwards**); multiply the fraction by 2 (read integer parts **downwards**).
- $fl(x)$: convert to base $\beta$ → normalise → check exponent → round to $k$ digits.
- IEEE double = $F(2,53,-1022,1023)$, with $u\approx1.11\times10^{-16}$.

---

## Week 2: Cancellation & Taylor (3 formulas + 1 recipe)

**2.1 Conjugate trick (removes cancellation)**
$$A-B=\frac{A^2-B^2}{A+B}\qquad\text{e.g.}\qquad\frac{-b+\sqrt{b^2-4ac}}{2a}=\frac{-2c}{b+\sqrt{b^2-4ac}}$$
> Subtracting nearly-equal rounded numbers destroys digits. Rewrite the formula so it **adds** instead. Other fixes: $\log A-\log B=\log\frac AB$, and $1-\cos x=\frac{\sin^2x}{1+\cos x}$.

**e.g.** $\sqrt{x+1}-\sqrt x$ for large $x$:
$$\sqrt{x+1}-\sqrt x=\frac{(\sqrt{x+1}-\sqrt x)(\sqrt{x+1}+\sqrt x)}{\sqrt{x+1}+\sqrt x}=\frac{(x+1)-x}{\sqrt{x+1}+\sqrt x}=\frac{1}{\sqrt{x+1}+\sqrt x}$$
Test at $x=1000$ in 3-digit arithmetic ($\sqrt{1001}\to31.6$, $\sqrt{1000}\to31.6$):
- original: $31.6-31.6=0$ ✗ (every digit lost)
- rearranged: $\frac{1}{31.6+31.6}=\frac1{63.2}=0.0158$ ✓ (true $0.015807$)

**Edge case: the sign of $b$ decides which root is dangerous.** Lecture example $a=1$, $b=-(10^8+10^{-8})$, $c=1$ (roots $10^8$ and $10^{-8}$):
- $b<0$ makes $-b>0$, so the **minus** root $\frac{-b-\sqrt{b^2-4ac}}{2a}$ subtracts nearly-equal numbers
- naive formula in MATLAB: $1.49\times10^{-8}$ ✗ (49% wrong)
- safe form $\frac{-2c}{b-\sqrt{b^2-4ac}}$: $10^{-8}$ ✓
- the plus root is fine here, because it adds two positive numbers

**2.2 Taylor polynomial of degree $n$ about $x_0$**
$$P_n(x)=\sum_{k=0}^{n}\frac{f^{(k)}(x_0)}{k!}(x-x_0)^k=f(x_0)+f'(x_0)(x-x_0)+\frac{f''(x_0)}{2}(x-x_0)^2+\cdots$$
> The polynomial that matches $f$ and its first $n$ derivatives at $x_0$. It's a good approximation **near** $x_0$.

**e.g.** $f(x)=\cos x$, degree 2, $x_0=0$:
- $f(x)=\cos x$, so $f(0)=1$
- $f'(x)=-\sin x$, so $f'(0)=0$
- $f''(x)=-\cos x$, so $f''(0)=-1$
- substitute: $P_2(x)=1+0\cdot x+\frac{-1}{2}x^2=1-\frac{x^2}{2}$

**Edge case: missing terms.** For $\cos x$ about $0$, $f'''(0)=\sin0=0$, so:
- $P_3(x)=1-\frac{x^2}2+0\cdot x^3=P_2(x)$
- so you may use the $R_3$ remainder instead, which gives a sharper bound on $[0,\pi/3]$: $\frac{x^4}{24}\le\frac{(\pi/3)^4}{24}=0.0501$ (vs $0.1658$)

**Edge case: $f$ is already a polynomial of degree $\le n$.** Then $P_n=f$ exactly. For $f=x^2+3x$ about $x_0=1$ with $n=2$:
- $f(1)=4$, $f'(1)=5$, $f''(1)=2$
- $P_2=4+5(x-1)+(x-1)^2=x^2+3x=f$ ✓

**2.3 Taylor remainder (error)**
$$R_n(x)=f(x)-P_n(x)=\frac{f^{(n+1)}(c)}{(n+1)!}(x-x_0)^{n+1},\qquad c\text{ between }x_0\text{ and }x$$
> The exact error, but $c$ is unknown. It uses the $(n+1)$th derivative.

**e.g.** Same $f=\cos x$, $n=2$, $x_0=0$:
- the next derivative is $f'''(x)=\sin x$
- $R_2(x)=\frac{\sin c}{3!}(x-0)^3=\frac{\sin c}{6}x^3$, with $c$ between $0$ and $x$

**Edge case: at $x=x_0$ the remainder is 0.** $R_n(x_0)=f^{(n+1)}(c)\cdot0=0$, because $P_n(x_0)=f(x_0)$ by construction.

**Edge case: $c$ changes with $x$.** Every $x$ has its own unknown $c$, so never try to solve for $c$; bound it instead.

**2.4 Error bound recipe**
$$|f(x)-P_n(x)|\le\frac{\max|f^{(n+1)}(c)|}{(n+1)!}\cdot\max|x-x_0|^{n+1}$$
> Replace each unknown by its worst case over the interval. The result is an upper bound on the error.

**e.g.** Same, for $x\in[0,\pi/3]$ (2025 Q2b):
- $c\in[0,\pi/3]$, where $\sin$ is increasing, so $|\sin c|\le\sin\frac\pi3=\frac{\sqrt3}2$
- $|x|^3\le\left(\frac\pi3\right)^3=1.1484$
- error $\le\frac{\sqrt3/2}{6}\times1.1484=0.1658$

**Edge case: the maximum may be inside the interval.** For $|\sin c|$ on $[0,\pi]$:
- endpoints: $\sin0=0$ and $\sin\pi=0$
- but the max is $\sin\frac\pi2=1$ in the middle, so the bound must use $1$

**Edge case: interval on both sides of $x_0$.** For $x_0=0$ on $[-1,2]$: $\max|x-x_0|=\max(1,2)=2$, not 1.

**Remember**
- Truncation error = from cutting maths short (finite terms, finite $h$). Roundoff error = from storing finitely many digits.
- Always state where $c$ lies. Calculator in **radians**.

---

## Week 3: ODEs & Euler (3 formulas)

**3.1 Grid**
$$h=\frac{b-a}{n},\qquad t_i=a+ih,\qquad w_i\approx y(t_i)$$
> Chop $[a,b]$ into $n$ steps of width $h$. The method outputs a **table** of values $w_i$, not a formula.

**e.g.** Solve on $[a,b]=[1,2]$ with $n=2$ steps:
- $h=\frac{2-1}{2}=0.5$
- $t_0=1$, $t_1=1+0.5=1.5$, $t_2=1+2(0.5)=2$
- the method produces $w_0,w_1,w_2\approx y(1),\,y(1.5),\,y(2)$

**Edge case: $h$ must divide the interval evenly.** On $[0,1]$:
- $h=0.25$ gives $n=4$ steps ✓
- $h=0.3$ gives $n=3.33$ ✗: you can't land exactly on $t=b$
- choose $h$ (or $n$) so that $n=\frac{b-a}{h}$ is a whole number

**3.2 Euler's method**
$$w_0=\alpha,\qquad w_{i+1}=w_i+h\,f(t_i,w_i)$$
> New value = old value + step × slope at the old point. You walk along the tangent line.

**e.g.** $y'=t+y^2$, $y(0)=1$, $h=0.1$:
- setup: $f(t,y)=t+y^2$, $t_0=0$, $w_0=1$
- slope at the start: $f(0,1)=0+1^2=1$
- step: $w_1=w_0+h\,f(t_0,w_0)=1+0.1(1)=1.1$
- so $y(0.1)\approx1.1$

**Edge case: zero starting slope.** $y'=-2ty$, $y(0)=1$: $f(0,1)=0$, so $w_1=w_0=1$. Euler doesn't move on the first step, even though the true curve does.

**Edge case: $h$ too large** (stability, good to know). $y'=-20y$, $y(0)=1$ (exact $e^{-20t}\to0$). Euler gives $w_{i+1}=(1-20h)\,w_i$:
- $h=0.1$: factor $-1$, so $w=-1,\,1,\,-1,\,1,\ldots$ (oscillates forever)
- $h=0.15$: factor $-2$, so $w=-2,\,4,\,-8,\,16,\ldots$ (blows up)
- fix: use a smaller $h$ (here $h<0.1$)

**3.3 Local → global error**
$$\text{local }O(h^{p+1})\ \Longrightarrow\ \text{global }O(h^{p})\qquad\text{(Euler: local }O(h^2),\ \text{global }O(h))$$
> Local error = error made in **one** step, if you started that step exactly right; it's the dropped Taylor term. Global error = total error at the end. You take $\frac{b-a}{h}$ steps, so you lose one power of $h$.

**e.g.** $y'=y$, $y(0)=1$ (exact $y=e^t$). Euler gives $w_1=1+h$:
- one step, $h=0.1$: $e^{0.1}-1.1=0.0052$
- one step, $h=0.05$: $e^{0.05}-1.05=0.0013$ (÷4, so the local error is $O(h^2)$)
- to $t=1$, $h=0.1$ (10 steps): $e-1.1^{10}=0.1245$
- to $t=1$, $h=0.05$ (20 steps): $e-1.05^{20}=0.0650$ (÷2, so the global error is $O(h)$)

**Edge case: zero local error.** If the true solution is a straight line, $y''=0$ and Euler is **exact**:
- $y'=2$, $y(0)=1$ (exact $y=1+2t$)
- Euler: $w_{i+1}=w_i+2h$, so $w_i=1+2t_i=y(t_i)$ for any $h$

**Remember**
- "Order of a method" = order of the **global** error. Order $p$ means halving $h$ divides the error by $2^p$.
- Derivation moves (all ODE methods): Taylor expand $y$ about $t_i$ → evaluate at $t_{i+1}$ ($t_{i+1}-t_i=h$) → use $y'=f$ → drop $O(h^{\cdot})$ and replace $y$ with $w$.
- Systems (SIR): apply Euler to every variable, using the **old** values on the right-hand side.

---

## Week 4: Higher-order ODE methods (4 formulas)

**4.1 Second-order Taylor method**
$$w_{i+1}=w_i+h\,f(t_i,w_i)+\frac{h^2}{2}f'(t_i,w_i)$$
> Euler plus a curvature correction (the next Taylor term). Global $O(h^2)$.

**e.g.** $y'=y-t$, $y(0)=2$, $h=0.2$:
- $f(t,y)=y-t$, so $f(0,2)=2$
- $f'(t,y)=y'-1=(y-t)-1$, so $f'(0,2)=1$
- $w_1=2+0.2(2)+\frac{0.2^2}{2}(1)=2+0.4+0.02=2.42$
- exact $y(0.2)=2.4214$

**Edge case: exact for quadratic solutions.** $y'=2t$, $y(0)=0$ (exact $y=t^2$):
- $f=2t$ and $f'=2$
- $w_1=0+h(0)+\frac{h^2}{2}(2)=h^2=y(h)$ ✓
- exact because the dropped term involves $y'''=0$

**4.2 Total derivative (for Taylor 2)**
$$f'(t,y)=\frac{\partial f}{\partial t}+\frac{\partial f}{\partial y}\cdot f(t,y)$$
> $y$ depends on $t$, so use the chain rule and replace $y'$ with $f$. This is the most common lost mark and the most common MATLAB bug.

**e.g.** $f=y-t$:
- $\frac{\partial f}{\partial t}=-1$ and $\frac{\partial f}{\partial y}=1$
- $f'=-1+1\cdot f=-1+(y-t)=y-t-1$

Another: $f=4t+y^2$ (this was a 2023 Q4 bug):
- $\frac{\partial f}{\partial t}=4$ and $\frac{\partial f}{\partial y}=2y$
- $f'=4+2y\cdot f=4+2y(4t+y^2)$, **not** $4+2y$

**Edge case: $f$ depends on only one variable.**
- only $t$: $f=t^2$ gives $f'=2t$ (no chain-rule term, since $\frac{\partial f}{\partial y}=0$)
- only $y$: $f=y^2$ gives $f'=0+2y\cdot f=2y\cdot y^2=2y^3$ (only the chain-rule term)

**4.3 Modified Euler**
$$k_1=hf(t_i,w_i),\qquad k_2=hf(t_i+h,\ w_i+k_1),\qquad w_{i+1}=w_i+\tfrac12(k_1+k_2)$$
> Do a trial Euler step, measure the slope at the predicted end, then average the start and end slopes. Global $O(h^2)$ with no $f'$ needed.

**e.g.** $y'=t+y^2$, $y(0)=1$, $h=0.1$:
- $k_1=0.1\,f(0,1)=0.1(0+1)=0.1$
- predicted end point: $(0+0.1,\ 1+0.1)=(0.1,\ 1.1)$
- $k_2=0.1\,f(0.1,1.1)=0.1(0.1+1.21)=0.131$
- $w_1=1+\frac12(0.1+0.131)=1.1155$

**Edge case: $f$ depends only on $t$.** Then Modified Euler is exactly the **trapezoidal rule** (Week 11): $w_{i+1}=w_i+\frac h2\big[f(t_i)+f(t_{i+1})\big]$. For $y'=2t$, $y(0)=0$, $h=0.5$:
- $k_1=0.5(2\times0)=0$
- $k_2=0.5(2\times0.5)=0.5$
- $w_1=0+\frac12(0+0.5)=0.25=y(0.5)$ ✓ (the trapezoid is exact for linear $f$)

**4.4 RK4**
$$\begin{aligned}k_1&=hf(t_i,w_i), & k_2&=hf\!\left(t_i+\tfrac h2,\ w_i+\tfrac{k_1}2\right)\\ k_3&=hf\!\left(t_i+\tfrac h2,\ w_i+\tfrac{k_2}2\right), & k_4&=hf(t_i+h,\ w_i+k_3)\end{aligned}$$
$$w_{i+1}=w_i+\tfrac16(k_1+2k_2+2k_3+k_4)$$
> Four slope samples (start, midpoint twice, end) weighted $1:2:2:1$. Global $O(h^4)$. Note that $k_4$ uses the **full** $k_3$.

**e.g.** $y'=3t-\frac yt$, $y(1)=2$, $h=0.5$:
- $k_1=0.5\,f(1,\ 2)=0.5(3-2)=0.5$
- $k_2=0.5\,f(1.25,\ 2.25)=0.5(3.75-1.8)=0.975$
- $k_3=0.5\,f(1.25,\ 2.4875)=0.5(3.75-1.99)=0.88$
- $k_4=0.5\,f(1.5,\ 2.88)=0.5(4.5-1.92)=1.29$
- $w_1=2+\frac16\big(0.5+2(0.975)+2(0.88)+1.29\big)=2+\frac{5.5}{6}=2.9167$ (exact $2.9167$)

**Edge case: $f$ depends only on $t$.** Then $k_2=k_3$ and RK4 is exactly **Simpson's rule**: $w_{i+1}=w_i+\frac h6\big[f(t_i)+4f(t_i+\frac h2)+f(t_{i+1})\big]$. For $y'=3t^2$, $y(0)=0$, $h=1$:
- $k_1=3(0)^2=0$
- $k_2=k_3=3(0.5)^2=0.75$
- $k_4=3(1)^2=3$
- $w_1=\frac16(0+1.5+1.5+3)=1=y(1)$ ✓ (Simpson is exact for cubics)

**Edge case (MATLAB):** $k_4$ uses the **full** $k_3$; writing `w+k3/2` was one of the bugs in 2025 Q4.

**Remember**

| Method | Global order | Needs $f'$? |
|---|---|---|
| Euler | 1 | no |
| Taylor 2 | 2 | yes |
| Modified Euler | 2 | no |
| RK4 | 4 | no |

- Modified Euler derivation: Taylor 2 + $f'\approx\frac{f(t_{i+1},y_{i+1})-f(t_i,y_i)}{h}$ → $w_{i+1}=w_i+\frac h2[f_i+f_{i+1}]$ → replace $w_{i+1}$ on the right-hand side with Euler's $w_i+hf_i$.

---

## Week 5: Interpolation, Lagrange (2 formulas)

**5.1 Lagrange form**
$$P_n(x)=\sum_{i=0}^{n}L_{n,i}(x)\,y_i,\qquad L_{n,i}(x)=\prod_{j\ne i}\frac{x-x_j}{x_i-x_j}$$
> $L_{n,i}$ equals 1 at $x_i$ and 0 at every other node. So the sum passes through every data point.

**e.g.** $f=\log x$, nodes $1,2,4$; estimate $\log3$:
- $y$ values: $\log1=0$, $\log2=0.6931$, $\log4=1.3863$
- $L_{2,0}(3)=\frac{(3-2)(3-4)}{(1-2)(1-4)}=\frac{-1}{3}$
- $L_{2,1}(3)=\frac{(3-1)(3-4)}{(2-1)(2-4)}=\frac{-2}{-2}=1$
- $L_{2,2}(3)=\frac{(3-1)(3-2)}{(4-1)(4-2)}=\frac26=\frac13$
- check: $-\frac13+1+\frac13=1$ ✓
- $P_2(3)=-\frac13(0)+1(0.6931)+\frac13(1.3863)=1.1552$ (true $1.0986$)

**Edge case: repeated node.** If $x_i=x_j$, the denominator $(x_i-x_j)=0$, so the nodes must be **distinct**.

**Edge case: "degree at most $n$".** $(0,1),(1,3),(2,5)$ lie on a line, so $P_2(x)=1+2x$ (the $x^2$ coefficient is 0). Three points don't always give a genuine quadratic.

**Edge case: evaluating at a node** returns the data exactly: $P_2(x_1)=y_1$, because $L_{n,1}(x_1)=1$ and the other basis polynomials are 0 there.

**5.2 Interpolation remainder**
$$f(x)-P_n(x)=\frac{f^{(n+1)}(c)}{(n+1)!}(x-x_0)(x-x_1)\cdots(x-x_n),\qquad c\in[a,b]$$
> Like the Taylor remainder, but $(x-x_0)^{n+1}$ becomes a product over **all** nodes, so the error is zero at each node.

**e.g.** Same ($\log x$, nodes $1,2,4$, at $x=3$):
- $f'''(x)=\frac2{x^3}$ is largest on $[1,4]$ at $c=1$, so $|f'''(c)|\le2$
- product: $|(3-1)(3-2)(3-4)|=2$
- bound: $|R_2(3)|\le\frac{2}{3!}\times2=0.667$
- actual error: $|1.1552-1.0986|=0.057\le0.667$ ✓

**Edge case: extrapolation.** Same nodes $1,2,4$, but now at $x=8$ (outside them):
- $P_2(8)=0$, while $\log8=2.079$ (error $2.08$)
- product: $|(8-1)(8-2)(8-4)|=168$, so the bound is $\frac26\times168=56$ (valid, but huge)
- outside the nodes, the product grows fast, and so does the error

**Edge case: polynomial data.** If $f$ is a polynomial of degree $\le n$, then $f^{(n+1)}=0$ and the error is **exactly 0** (e.g. 3 points from $x^2$).

**Remember**
- **Uniqueness:** $n+1$ distinct points give exactly one polynomial of degree $\le n$. Lagrange, divided differences and forward differences all give the **same** polynomial.
- $n+1$ points means degree $n$, which means the bound uses $f^{(n+1)}$.
- Check: $\sum_i L_{n,i}(x)=1$.
- Relative error in code divides by $|f(a)|$ (the true value).

---

## Week 6: Newton divided differences (2 formulas)

**6.1 Divided difference**
$$f[x_i]=y_i,\qquad f[x_i,\dots,x_{i+k}]=\frac{f[x_{i+1},\dots,x_{i+k}]-f[x_i,\dots,x_{i+k-1}]}{x_{i+k}-x_i}$$
> (Drop the first point) minus (drop the last point), divided by (last $x$ minus first $x$). First differences are slopes; second differences are slopes of slopes.

**e.g.** Data $(-1,3),(0,1),(2,3)$:
- $f[-1,0]=\frac{1-3}{0-(-1)}=-2$
- $f[0,2]=\frac{3-1}{2-0}=1$
- $f[-1,0,2]=\frac{f[0,2]-f[-1,0]}{2-(-1)}=\frac{1-(-2)}{3}=1$

**Edge case: order doesn't matter.** $f[2,0]=\frac{y_0-y_2}{0-2}=\frac{y_2-y_0}{2-0}=f[0,2]$. Divided differences are symmetric, but always divide by the last minus the first $x$ **of the same list**.

**Edge case: a repeated $x$** gives division by zero, so the nodes must be distinct.

**6.2 Newton divided difference form**
$$P_n(x)=f[x_0]+f[x_0,x_1](x-x_0)+f[x_0,x_1,x_2](x-x_0)(x-x_1)+\cdots$$
> The coefficients are the **top diagonal** of the table. Adding a point adds **one term**, and the old work is kept.

**e.g.** Same data. The top diagonal is $3,\ -2,\ 1$:
- $P_2(x)=3+(-2)(x+1)+1\cdot(x+1)(x-0)$
- expand: $3-2x-2+x^2+x=x^2-x+1$
- check: $P_2(2)=4-2+1=3$ ✓

**Edge case: the new point is already on the curve.** Add $(1,1)$ to the data above (check: $P_2(1)=1-1+1=1$):
- $f[2,1]=\frac{1-3}{1-2}=2$
- $f[0,2,1]=\frac{2-1}{1-0}=1$
- $f[-1,0,2,1]=\frac{1-1}{1-(-1)}=0$
- the new coefficient is **0**, so $P_3=P_2$

**Remember**
- Nodes can be in any order; always divide by the outermost $x$'s of the span.
- Exam: expand $f[x_0,x_1,x_2,x_3]$ by applying 6.1 repeatedly (one level per line).

---

## Week 7: Newton forward differences (3 formulas)

**7.1 Forward differences**
$$\Delta y_i=y_{i+1}-y_i,\qquad \Delta^2y_i=y_{i+2}-2y_{i+1}+y_i,\qquad\Delta^3y_i=y_{i+3}-3y_{i+2}+3y_{i+1}-y_i$$
> Plain subtractions down the table, with no division. Use them only for **equally spaced** data.

**e.g.** $y=1,2,4,8$ (from $2^x$ at $x=0,1,2,3$):
- $\Delta y$: $2-1=1$, $4-2=2$, $8-4=4$
- $\Delta^2y$: $2-1=1$, $4-2=2$
- $\Delta^3y$: $2-1=1$
- top diagonal: $y_0=1$, $\Delta y_0=1$, $\Delta^2y_0=1$, $\Delta^3y_0=1$

**Edge case: polynomial data.** Degree-$d$ data have constant $\Delta^d$ and zero $\Delta^{d+1}$. For $y=x^2$ at $x=0,1,2,3$:
- $y$: 0, 1, 4, 9
- $\Delta y$: 1, 3, 5
- $\Delta^2y$: 2, 2 (constant)
- $\Delta^3y$: 0

**Edge case: unequal spacing** (e.g. $x=0,1,3$): forward differences don't apply, so use divided differences instead.

**7.2 Newton forward difference form**
$$P_n(x)=\sum_{k=0}^{n}\binom sk\Delta^ky_0=y_0+s\Delta y_0+\frac{s(s-1)}{2!}\Delta^2y_0+\frac{s(s-1)(s-2)}{3!}\Delta^3y_0+\cdots,\qquad s=\frac{x-x_0}{h}$$
> The coefficients are the top diagonal of the difference table. **Convert $x\to s$ before evaluating.**

**e.g.** Same data, $h=1$, so $s=\frac{x-0}{1}=x$:
- $P_3=1+1\cdot s+\frac{s(s-1)}{2}(1)+\frac{s(s-1)(s-2)}{6}(1)$
- to estimate $2^{0.5}$: $x=0.5$, so $s=0.5$
- terms: $1+0.5+\frac{(0.5)(-0.5)}{2}+\frac{(0.5)(-0.5)(-1.5)}{6}=1+0.5-0.125+0.0625$
- $P_3=1.4375$ (true $\sqrt2=1.4142$)

**Edge case: $s$ outside $[0,n]$ means extrapolation.** For the population data 1970–2010 ($s=0,\dots,4$), 1950 is $s=-2$, which gives $P_4=3217$: more than in 1970, so unrealistic.

**Edge case: $x_0$ must be the first node.** $s$ is measured from $x_0$, and the top diagonal belongs to $x_0$.

**7.3 Link to divided differences**
$$f[x_0,x_1,\dots,x_k]=\frac{\Delta^ky_0}{k!\,h^k}$$
> With equal spacing, divided differences become forward differences scaled by $k!\,h^k$. Proving it for $k=2$ is an exam question.

**e.g.** $(1,1),(2,4),(3,9)$ from $y=x^2$, with $h=1$:
- $\Delta^2y_0=y_2-2y_1+y_0=9-8+1=2$
- $f[x_0,x_1,x_2]=\frac{2}{2!\cdot1^2}=1$
- check: $f[1,2]=3$, $f[2,3]=5$, $f[1,2,3]=\frac{5-3}{3-1}=1$ ✓ (the $x^2$ coefficient)

**Edge case: don't forget $h^k$ when $h\ne1$.** For $(0,0),(0.5,0.25),(1,1)$ from $y=x^2$, $h=0.5$:
- $\Delta^2y_0=1-2(0.25)+0=0.5$
- $f[x_0,x_1,x_2]=\frac{0.5}{2!\times0.5^2}=1$ ✓
- forgetting $h^2$ gives $\frac{0.5}{2}=0.25$ ✗

**Remember**
- Interpolation (inside the data) is reliable. **Extrapolation** (outside) is unreliable.
- $\binom sk=\frac{s(s-1)\cdots(s-k+1)}{k!}$ works for non-integer $s$.

---

## Week 8: Bisection & fixed point (4 formulas)

**8.1 Bracketing condition (from the IVT)**
$$f\text{ continuous on }[a,b]\ \text{and}\ f(a)\,f(b)<0\ \Longrightarrow\ \text{a root in }[a,b]$$
> If the function changes sign, it must cross zero. Write: "opposite signs, so $[a,b]$ is a bracketing".

**e.g.** $f(x)=x^3-2x-7$ on $[1,3]$ (2025 Q9a):
- $f(1)=1-2-7=-8<0$
- $f(3)=27-6-7=14>0$
- opposite signs and $f$ is continuous, so $[1,3]$ is a bracketing

**Edge case: sign change but no root.** $f(x)=\frac1x$ on $[-1,1]$: $f(-1)=-1$ and $f(1)=1$, but there's no root, because $f$ jumps at $x=0$. The IVT needs $f$ to be **continuous**.

**Edge case: no sign change, yet roots exist.** $f(x)=x^2-0.25$ on $[-1,1]$: $f(\pm1)=0.75$, both positive, but there are roots at $\pm0.5$ (two crossings cancel out).

**8.2 Bisection**
$$p=\frac{a+b}{2};\quad\text{if }\operatorname{sign}f(p)=\operatorname{sign}f(a)\text{ then }a\leftarrow p\text{, else }b\leftarrow p;\qquad|p_n-\text{root}|\le\frac{b-a}{2^n}$$
> Keep the half that still has the sign change. The approximation after $n$ iterations is the $n$th midpoint. Guaranteed, but slow.

**e.g.** Same $f$, two iterations on $[1,3]$:
- iteration 1: $p=\frac{1+3}2=2$, $f(2)=-3$ (same sign as $f(a)$), so $a\leftarrow2$, giving $[2,3]$
- iteration 2: $p=\frac{2+3}2=2.5$, $f(2.5)=3.625$ (same sign as $f(b)$), so $b\leftarrow2.5$, giving $[2,2.5]$
- estimate after 2 iterations: $2.5$, with error $\le\frac{3-1}{2^2}=0.5$

**Edge case: $f(p)=0$ exactly.** Stop: $p$ is the root.

**Edge case: how many iterations?** For error $\le10^{-3}$ on $[1,3]$:
- you need $\frac{2}{2^n}\le10^{-3}$, i.e. $2^n\ge2000$
- so $n=11$ iterations

**Edge case: several roots in $[a,b]$.** Bisection finds **one** of them, and you can't choose which.

**8.3 Fixed point iteration**
$$x=g(x),\qquad x_{n+1}=g(x_n)$$
> Rewrite $f(x)=0$ as $x=g(x)$ and feed each output back in. The answer is where $y=g(x)$ meets $y=x$.

**e.g.** Solve $x=\cos x$ with $g(x)=\cos x$, $x_0=0.5$:
- $x_1=\cos0.5=0.8776$
- $x_2=\cos0.8776=0.6390$
- $x_3=\cos0.6390=0.8027$
- …it zig-zags slowly in to $0.7391$

**Edge case: same equation, different $g$, opposite outcome.** For $0.9\cos x=\sqrt x$ (lecture), from $x_0=0.5$:
- $g_1(x)=\cos^{-1}\!\left(\frac{\sqrt x}{0.9}\right)$: $0.667,\ 0.444,\ 0.750,\ 0.276,\ 0.948$, then undefined ✗
- $g_2(x)=0.81\cos^2x$: $0.624,\ 0.534,\ 0.600,\ \ldots\to0.57$ ✓

**8.4 Fixed point theorem (convergence)**
$$g(x)\in[a,b]\ \forall x\in[a,b]\quad\text{and}\quad|g'(x)|\le k<1\ \Longrightarrow\ \text{unique fixed point, converges for any }x_0\in[a,b]$$
> $g$ must map the interval into itself and **shrink** distances. If $|g'|>1$ near the root, try another rearrangement.

**e.g.** $g(x)=\cos x$ on $[0,1]$:
- maps into itself: $\cos1=0.54\le g(x)\le1$, so $g(x)\in[0,1]$ ✓
- shrinks distances: $|g'(x)|=|\sin x|\le\sin1=0.84<1$ ✓
- so the iteration converges for any $x_0\in[0,1]$

**Edge case: the theorem is sufficient, not necessary.** Take $g=\cos x$ on $[0,2]$:
- $g(2)=\cos2=-0.42\notin[0,2]$, and $|g'(\frac\pi2)|=1$, which is not $<1$
- so the theorem **doesn't apply**, yet the iteration still converges to $0.7391$
- failing the test means "no guarantee", not "will diverge"

---

## Week 9: Newton & secant (2 formulas + orders)

**9.1 Newton's method**
$$x_{n+1}=x_n-\frac{f(x_n)}{f'(x_n)}$$
> Follow the tangent line at $x_n$ down to the $x$-axis. Derivation: set $0=f(x_n)+f'(x_n)(x_{n+1}-x_n)$.

**e.g.** $f(x)=x^3-2x-7$, $x_0=2$ (2025 Q9c):
- $f(2)=8-4-7=-3$
- $f'(x)=3x^2-2$, so $f'(2)=10$
- $x_1=2-\frac{-3}{10}=2.3$

**Edge case: $f'(x_n)=0$.** For $f=x^2-2$ with $x_0=0$: $f'(0)=0$, so you'd divide by zero (the tangent is horizontal and never meets the axis).

**Edge case: cycling.** For $f=x^3-2x+2$ with $x_0=0$:
- $x_1=0-\frac{f(0)}{f'(0)}=0-\frac{2}{-2}=1$
- $x_2=1-\frac{f(1)}{f'(1)}=1-\frac{1}{1}=0$
- back to the start, so it cycles $0,1,0,1,\ldots$ forever; try another $x_0$

**9.2 Secant method**
$$x_{n+1}=x_n-f(x_n)\,\frac{x_n-x_{n-1}}{f(x_n)-f(x_{n-1})}$$
> Newton with $f'$ replaced by the slope through the last two points. It needs 2 starting values and no derivative.

**e.g.** $f(x)=x^4-4x^3+2x+3$, $x_0=1$, $x_1=2$ (2024 Q9c):
- $f(1)=1-4+2+3=2$
- $f(2)=16-32+4+3=-9$
- $x_2=2-(-9)\cdot\frac{2-1}{-9-2}=2-\frac{9}{11}=\frac{13}{11}=1.1818$

**Edge case: $f(x_n)=f(x_{n-1})$.** For $f=x^2-2$ with $x_0=-1$, $x_1=1$: $f(-1)=f(1)=-1$, so the secant line is horizontal and you'd divide by zero.

**Edge case: no bracket needed, so no guarantee.** Unlike bisection, the secant iterates can leave the starting interval.

**9.3 Convergence orders**
$$|x_{n+1}-p|\approx\lambda|x_n-p|^{r}:\quad r=1\ (\text{bisection, fixed point}),\quad r=\tfrac{1+\sqrt5}{2}\approx1.618\ (\text{secant}),\quad r=2\ (\text{Newton})$$
> $r=2$ means the number of correct digits roughly **doubles** each step. Secant is slower because it approximates the derivative.

**e.g.** Newton on $x-\cos x=0$ from $x_0=0.5$ (root $0.739085$):
- $x_1=0.755222$: error $1.6\times10^{-2}$
- $x_2=0.739142$: error $5.7\times10^{-5}$
- $x_3=0.739085$: error $7\times10^{-10}$
- the error is roughly squared each step, so the correct digits double

**Edge case: a repeated root slows Newton down.** For $f=x^2$ (double root at 0) from $x_0=1$:
- $x_{n+1}=x_n-\frac{x_n^2}{2x_n}=\frac{x_n}{2}$, giving $0.5,\ 0.25,\ 0.125,\ \ldots$
- the error only **halves** each step, so convergence is linear, not quadratic

**Remember**
- Deriving an iteration for $\sqrt[k]a$: choose $f(x)=x^k-a$, apply Newton or secant, simplify.
- For secant, use the identities $p^2-q^2=(p-q)(p+q)$ and $p^3-q^3=(p-q)(p^2+pq+q^2)$.
- Heron: $x_{n+1}=\frac12\left(x_n+\frac a{x_n}\right)$ is Newton on $x^2-a$.
- In code: `while` uses `> tol` (keep going), and `if … break` uses `<= tol` (stop).

---

## Week 10: Numerical differentiation (5 formulas)

**10.1 Forward difference** (1st order)
$$f'(x_0)=\frac{f(x_0+h)-f(x_0)}{h}-\frac h2f''(c)$$
> Slope to the point on the right. Use it at the **left end** of a table.

**e.g.** Table $x$: 0.15, 0.3, 0.45; $f$: 1.3516, 1.3043, 1.2419 (2025 Q12a):
- $x_0=0.15$ is the left end, so use forward with $h=0.15$
- $f'(0.15)\approx\frac{f(0.3)-f(0.15)}{0.15}=\frac{1.3043-1.3516}{0.15}=\frac{-0.0473}{0.15}=-0.3153$

**Edge case: exact for straight lines.** For $f=3x+1$: $\frac{f(x_0+h)-f(x_0)}{h}=\frac{3h}{h}=3$ for **any** $h$ (the error term has $f''=0$).

**Edge case: $h$ too small.** Below about $h\approx10^{-8}$, roundoff (catastrophic cancellation) takes over, so a smaller $h$ is **not** always better.

**10.2 Backward difference** (1st order)
$$f'(x_0)=\frac{f(x_0)-f(x_0-h)}{h}+\frac h2f''(c)$$
> Slope to the point on the left. Use it at the **right end** of a table.

**e.g.** Table $x$: 1, 1.1, 1.2; $f$: 0.5679, 0.6542, 0.7286 (2023 Q12a):
- $x_0=1.2$ is the right end, so use backward with $h=0.1$
- $f'(1.2)\approx\frac{0.7286-0.6542}{0.1}=\frac{0.0744}{0.1}=0.7440$

**Edge case: opposite error signs.** The backward error ($+\frac h2f''$) and the forward error ($-\frac h2f''$) have opposite signs, so their **average is exactly the central difference**. For $\sin x$ at $x_0=1$, $h=0.1$:
- forward $0.4970$, backward $0.5820$
- average $0.5395$ = central difference (true $0.5403$)

**10.3 Central difference for $f'$** (2nd order)
$$f'(x_0)=\frac{f(x_0+h)-f(x_0-h)}{2h}-\frac{h^2}{6}f'''(c)$$
> Slope across both neighbours. More accurate, but needs a point on each side.

**e.g.** Same table; find $f'(1.1)$ (2023 Q12b):
- $x_0=1.1$ has neighbours on both sides, so use central with $h=0.1$
- $f'(1.1)\approx\frac{f(1.2)-f(1.0)}{2(0.1)}=\frac{0.7286-0.5679}{0.2}=0.8035$

**Edge case: exact for quadratics** (the error term has $f'''=0$). For $f=x^2$, $x_0=1$, $h=0.5$:
- central: $\frac{1.5^2-0.5^2}{2(0.5)}=\frac{2}{1}=2=f'(1)$ ✓
- forward: $\frac{1.5^2-1}{0.5}=2.5$ ✗

**Edge case: unequal spacing.** If the points on either side are at different distances from $x_0$, this formula doesn't apply.

**10.4 Central difference for $f''$** (2nd order)
$$f''(x_0)=\frac{f(x_0-h)-2f(x_0)+f(x_0+h)}{h^2}-\frac{h^2}{12}f^{(4)}(c)$$
> The "slope of slopes". Derivation: **add** the degree-3 Taylor expansions at $x_0\pm h$, then merge the two $c$'s with the IVT.

**e.g.** First table ($x$: 0.15, 0.3, 0.45); find $f''(0.3)$ (2025 Q12b):
- $h=0.15$, so $h^2=0.0225$
- numerator: $1.3516-2(1.3043)+1.2419=-0.0151$
- $f''(0.3)\approx\frac{-0.0151}{0.0225}=-0.6711$

**Edge case: exact for cubics** (the error term has $f^{(4)}=0$). For $f=x^3$, $x_0=1$, $h=0.5$:
- $\frac{0.5^3-2(1)+1.5^3}{0.5^2}=\frac{0.125-2+3.375}{0.25}=6=f''(1)$ ✓

**10.5 Second-order forward difference**
$$f'(x_0)\approx\frac{-3f(x_0)+4f(x_0+h)-f(x_0+2h)}{2h}$$
> Second-order accuracy using only points to the right. Derivation: $4f(x_0+h)-f(x_0+2h)$ cancels the $h^2$ terms.

**e.g.** $f(x)=\log x$, $x_0=2$, $h=0.1$ (exact $f'(2)=0.5$):
- values: $f(2)=0.693147$, $f(2.1)=0.741937$, $f(2.2)=0.788457$
- second-order forward: $\frac{-3(0.693147)+4(0.741937)-0.788457}{0.2}=0.49925$
- plain forward: $\frac{0.741937-0.693147}{0.1}=0.4879$ (an error about 16× bigger)

**Edge case: exact for quadratics.** For $f=x^2$, $x_0=1$, $h=0.5$:
- $\frac{-3(1)+4(1.5^2)-2^2}{2(0.5)}=\frac{-3+9-4}{1}=2=f'(1)$ ✓

**Remember**
- Derivations: **subtract** the expansions to get $f'$ (even terms cancel); **add** them to get $f''$ (odd terms cancel).
- Choosing $h$: too large gives **truncation** error; too small gives **roundoff** error (catastrophic cancellation).

---

## Week 11: Numerical integration (4 formulas)

**11.1 Trapezoidal rule (one strip)**
$$\int_{x_0}^{x_1}f\,dx\approx\frac h2\big[f(x_0)+f(x_1)\big]$$
> The area of the trapezoid under the straight line (the degree-1 interpolant).

**e.g.** $\int_1^2\frac1x\,dx$ with one strip ($h=1$):
- $f(1)=1$ and $f(2)=0.5$
- $\frac12\big[1+0.5\big]=0.75$
- exact $\log2=0.6931$: one straight line is crude

**Edge case: convex vs concave.** For one strip, the error is $-\frac{h^3}{12}f''(c)$:
- convex ($f''>0$), e.g. $\frac1x$: the trapezoid **over**-estimates ($0.75>0.6931$)
- concave ($f''<0$), e.g. $\sin x$ on $[0,\pi]$: it **under**-estimates ($1.8961<2$)
- straight line ($f''=0$): **exact**

**11.2 Composite trapezoidal rule**
$$\int_a^bf\,dx=\frac h2\Big[f(x_0)+2\sum_{i=1}^{n-1}f(x_i)+f(x_n)\Big]-\frac{(b-a)h^2}{12}f''(c)$$
> Weights $1,2,2,\dots,2,1$. Second order, and exact for polynomials of degree $\le1$.

**e.g.** Same integral, $n=4$, $h=0.25$:
- $x$: 1, 1.25, 1.5, 1.75, 2
- $f$: 1, 0.8, 0.6667, 0.5714, 0.5
- bracket: $1+2(0.8+0.6667+0.5714)+0.5=5.5762$
- $\frac{0.25}{2}\times5.5762=0.6970$ (error $0.004$)

**Edge case: $n$ counts strips, not points.** 5 points means $n=4$ and $h=\frac{b-a}{4}$; using $n=5$ is a classic slip.

**Edge case: unequal spacing.** The formula needs a single $h$; otherwise add up the individual trapezoids yourself.

**11.3 Simpson's rule (one pair of strips)**
$$\int_{x_0}^{x_2}f\,dx\approx\frac h3\big[f(x_0)+4f(x_1)+f(x_2)\big]$$
> The area under the parabola (the degree-2 interpolant) through 3 points.

**e.g.** Same integral, one pair of strips ($h=0.5$):
- $f(1)=1$, $f(1.5)=\frac23$, $f(2)=0.5$
- bracket: $1+4\left(\frac23\right)+0.5=4.1667$
- $\frac{0.5}{3}\times4.1667=0.6944$

**Edge case: exact for cubics too, not just quadratics.** $\int_0^2x^3\,dx=4$, and with $h=1$:
- $\frac13\big[0+4(1)+8\big]=4$ ✓ (the error term has $f^{(4)}=0$)

**11.4 Composite Simpson's rule ($n$ even)**
$$\int_a^bf\,dx=\frac h3\Big[f(x_0)+4\!\!\sum_{\text{odd }i}\!\!f(x_i)+2\!\!\!\sum_{\text{even interior }i}\!\!\!f(x_i)+f(x_n)\Big]-\frac{(b-a)h^4}{180}f^{(4)}(c)$$
> Weights $1,4,2,4,\dots,4,1$. Fourth order, and exact for polynomials of degree $\le3$.

**e.g.** Same integral, $n=4$, $h=0.25$:
- weights $1,4,2,4,1$ on $f$ = 1, 0.8, 0.6667, 0.5714, 0.5
- bracket: $1+4(0.8+0.5714)+2(0.6667)+0.5=8.3190$
- $\frac{0.25}{3}\times8.3190=0.6933$ (error $0.0001$, against $0.004$ for the trapezoid)

**Edge case: $n$ must be even.**
- 4 points means $n=3$ (odd), so Simpson can't be used; use the trapezoidal rule instead
- 6 points means $n=5$: same problem

**Edge case (MATLAB):** `x(i)` is $x_{i-1}$, so the **even** MATLAB indices `x(2)`, `x(4)`, … are the odd abscissas and get weight **4**.

**Remember**
- Derivations: integrate the Newton forward difference interpolant with $x=x_0+sh$, $dx=h\,ds$, $s$ from $0$ to $1$ (trapezoid) or $0$ to $2$ (Simpson).
- In MATLAB, $n$ subintervals means $n+1$ points: `x(1)` is $x_0$ and `x(n+1)` is $x_n$.

---

## Week 12: Linear systems & LU (4 formulas)

**12.1 Forward substitution** (lower triangular)
$$x_i=\frac{b_i-\sum_{j<i}a_{ij}x_j}{a_{ii}},\qquad i=1,2,\dots,n$$
> Row 1 gives $x_1$ directly. Substitute it into row 2 to get $x_2$, and so on **downwards**.

**e.g.** Solve (2025 Q15a):
$$\begin{bmatrix}3&0\\-2&5\end{bmatrix}\mathbf x=\begin{bmatrix}12\\-23\end{bmatrix}$$
- row 1: $3x_1=12$, so $x_1=4$
- row 2: $-2(4)+5x_2=-23$, so $5x_2=-15$ and $x_2=-3$

**Edge case: zero on the diagonal.** In the system below, row 1 says $0\cdot x_1=1$, which is impossible:
$$\begin{bmatrix}0&0\\1&2\end{bmatrix}\mathbf x=\begin{bmatrix}1\\3\end{bmatrix}$$
- a triangular system has a unique solution only if **every diagonal entry is nonzero**

**12.2 Backward substitution** (upper triangular)
$$x_i=\frac{b_i-\sum_{j>i}a_{ij}x_j}{a_{ii}},\qquad i=n,\dots,1$$
> The last row gives $x_n$ directly. Work **upwards**.

**e.g.** Solve:
$$\begin{bmatrix}2&1\\0&4\end{bmatrix}\mathbf x=\begin{bmatrix}5\\8\end{bmatrix}$$
- last row: $4x_2=8$, so $x_2=2$
- row 1: $2x_1+1(2)=5$, so $x_1=1.5$

**Edge case: zero diagonal entry, infinitely many solutions.**
$$\begin{bmatrix}1&1\\0&0\end{bmatrix}\mathbf x=\begin{bmatrix}2\\0\end{bmatrix}$$
- row 2 says $0=0$ (no information), so $x_2$ is free
- row 1 gives $x_1=2-x_2$, which works for every choice of $x_2$

**12.3 Solving with LU**
$$A=LU:\qquad L\mathbf z=\mathbf b\ (\text{forward}),\quad\text{then}\quad U\mathbf x=\mathbf z\ (\text{backward})$$
> Factorise once (the expensive part), then each new $\mathbf b$ costs only two cheap triangular solves.

**e.g.** 2024 Q15b: $\mathbf z=[2,-8,-4]^T$ is given, so solve $U\mathbf x=\mathbf z$ with
$$U=\begin{bmatrix}2&1&-4\\0&-3&2\\0&0&4\end{bmatrix}$$
- row 3: $4x_3=-4$, so $x_3=-1$
- row 2: $-3x_2+2(-1)=-8$, so $x_2=2$
- row 1: $2x_1+2-4(-1)=2$, so $x_1=-2$
- $\mathbf x=[-2,\ 2,\ -1]^T$

**Edge case: a new right-hand side.** Reuse the **same** $L$ and $U$, and redo only the two substitutions. Never refactorise for a new $\mathbf b$.

**Edge case: order matters.** Solve $L\mathbf z=\mathbf b$ **first** (forward), then $U\mathbf x=\mathbf z$ (backward). $\mathbf z$ is not the answer.

**12.4 Doolittle 3×3** ($L$ has 1s on the diagonal)
$$u_{1j}=a_{1j},\quad \ell_{i1}=\frac{a_{i1}}{u_{11}},\quad u_{22}=a_{22}-\ell_{21}u_{12},\quad u_{23}=a_{23}-\ell_{21}u_{13}$$
$$\ell_{32}=\frac{a_{32}-\ell_{31}u_{12}}{u_{22}},\qquad u_{33}=a_{33}-\ell_{31}u_{13}-\ell_{32}u_{23}$$
> All of these come from one rule: $a_{ij}=(\text{row }i\text{ of }L)\cdot(\text{column }j\text{ of }U)$. Order: row of $U$, column of $L$, row of $U$, …

**e.g.** 2024 Q15a, with $\ell_{21}=-2$ and $\ell_{31}=3$ given:
$$A=\begin{bmatrix}2&1&-4\\-4&-5&10\\6&6&-10\end{bmatrix},\qquad u_{23}=2$$
- $u_{22}=a_{22}-\ell_{21}u_{12}=-5-(-2)(1)=-3$
- $\ell_{32}=\frac{a_{32}-\ell_{31}u_{12}}{u_{22}}=\frac{6-3(1)}{-3}=-1$
- $u_{33}=a_{33}-\ell_{31}u_{13}-\ell_{32}u_{23}=-10-3(-4)-(-1)(2)=4$

**Edge case: zero pivot.** The matrix below is invertible, but $u_{11}=0$, so $\ell_{21}=\frac{1}{0}$ and LU (without pivoting) fails:
$$A=\begin{bmatrix}0&1\\1&1\end{bmatrix}$$
- swapping the two rows (**pivoting**) fixes it

**Remember**
- A zero or tiny pivot $u_{jj}$ makes LU unstable, which **pivoting** (row swaps) fixes (not covered in detail).

---

## Week 13: SPD & Cholesky (3 formulas)

**13.1 Symmetric positive definite**
$$A^T=A\qquad\text{and}\qquad\mathbf x^TA\mathbf x>0\ \ \text{for all }\mathbf x\neq\mathbf0$$
> Show it by expanding $\mathbf x^TA\mathbf x$ and completing the square into a sum of squares. For a 2×2 matrix: $\mathbf x^TA\mathbf x=ax_1^2+2bx_1x_2+cx_2^2$.

**e.g.** $A=\begin{bmatrix}1&-1\\-1&2\end{bmatrix}$ (2025 Q16a):
- $A\mathbf x=\begin{bmatrix}x_1-x_2\\-x_1+2x_2\end{bmatrix}$
- $\mathbf x^TA\mathbf x=x_1(x_1-x_2)+x_2(-x_1+2x_2)=x_1^2-2x_1x_2+2x_2^2$
- complete the square: $=(x_1-x_2)^2+x_2^2$
- this is $>0$ unless $x_1=x_2=0$, so $A$ is positive definite

**Edge case: positive entries don't make a matrix PD.** For $A=\begin{bmatrix}1&2\\2&1\end{bmatrix}$ and $\mathbf x=(1,-1)$:
- $\mathbf x^TA\mathbf x=1-4+1=-2<0$, so $A$ is symmetric but **not** PD

**Edge case: $\ge0$ is not enough.** $\begin{bmatrix}1&1\\1&1\end{bmatrix}$ gives $\mathbf x^TA\mathbf x=(x_1+x_2)^2$, which is $0$ for $\mathbf x=(1,-1)\neq\mathbf0$. That's positive **semi**-definite, not PD.

**13.2 Cholesky 3×3** ($A=LL^T$)
$$\ell_{11}=\sqrt{a_{11}},\quad\ell_{21}=\frac{a_{21}}{\ell_{11}},\quad\ell_{31}=\frac{a_{31}}{\ell_{11}},\quad\ell_{22}=\sqrt{a_{22}-\ell_{21}^2}$$
$$\ell_{32}=\frac{a_{32}-\ell_{31}\ell_{21}}{\ell_{22}},\qquad\ell_{33}=\sqrt{a_{33}-\ell_{31}^2-\ell_{32}^2}$$
> Diagonal entry: $\sqrt{\text{entry}-\text{sum of squares so far}}$. Below the diagonal: $(\text{entry}-\text{dot product so far})\div\text{diagonal}$. Work column by column.

**e.g.** Factorise:
$$A=\begin{bmatrix}16&4&8\\4&5&-4\\8&-4&22\end{bmatrix}$$
- column 1: $\ell_{11}=\sqrt{16}=4$, $\ell_{21}=\frac44=1$, $\ell_{31}=\frac84=2$
- column 2: $\ell_{22}=\sqrt{5-1^2}=2$, $\ell_{32}=\frac{-4-(2)(1)}{2}=-3$
- column 3: $\ell_{33}=\sqrt{22-2^2-(-3)^2}=\sqrt9=3$

**Edge case: Cholesky fails.** For $\begin{bmatrix}1&2\\2&1\end{bmatrix}$:
- $\ell_{11}=1$ and $\ell_{21}=2$
- $\ell_{22}=\sqrt{1-4}=\sqrt{-3}$ ✗, so $A$ is not PD; switch to LU

**Edge case: zero under the root.** For $\begin{bmatrix}1&1\\1&1\end{bmatrix}$: $\ell_{22}=\sqrt{1-1}=0$, and any later entry would divide by it, so $A$ is not PD (it's singular).

**13.3 Solving with Cholesky**
$$L\mathbf z=\mathbf b\ (\text{forward}),\quad\text{then}\quad L^T\mathbf x=\mathbf z\ (\text{backward})$$
> Same idea as LU, with $U=L^T$.

**e.g.** Same $A$ and $L$, with $\mathbf b=[20,17,28]^T$.

Forward, $L\mathbf z=\mathbf b$:
- $4z_1=20$, so $z_1=5$
- $z_1+2z_2=17$, so $z_2=6$
- $2z_1-3z_2+3z_3=28$, so $z_3=12$

Backward, $L^T\mathbf x=\mathbf z$:
- $3x_3=12$, so $x_3=4$
- $2x_2-3x_3=6$, so $x_2=9$
- $4x_1+x_2+2x_3=5$, so $x_1=-3$

**Edge case: the second solve goes bottom-up.** $L^T$ is **upper** triangular, so solve $L^T\mathbf x=\mathbf z$ from the last row up (start with $x_3$). Working top-down is a common slip.

**Remember**
- Cholesky needs $A$ **symmetric and positive definite**. It does about half the work of LU, needs no pivoting, and is always stable.
- Cholesky **succeeds** (every square root has a positive argument) **⇔** $A$ is SPD. A negative under the root means $A$ is not SPD, so switch to LU.

---

## Exam-day extras

**"Which is more accurate?"**
> Name the orders: "(b) is second order, $O(h^2)$, whereas (a) is first order, $O(h)$, so (b) has the smaller error for the same $h$."

**MATLAB bug checklist** (3 questions, 18 marks)
> Variables initialised? · `h=(b-a)/n`? · arguments in order `f(t,w)`? · `.*` `./` `.^` on vectors? · right coefficients ($k_3/2$, `2*`, $h/2$ vs $h/3$, `/6`)? · indices `x(1)`…`x(n+1)`? · stop conditions (`> tol` vs `<= tol`)? · Newton `f/fdash` not upside down? · relative error divides by `abs(true)`?
