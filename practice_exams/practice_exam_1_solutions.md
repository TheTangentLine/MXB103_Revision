# MXB103 Practice Exam 1: Solutions

> Marks in **[brackets]** follow the style of the official marking schemes. Each solution is laid out the way the markers expect, with short notes in *italics* explaining what each step is doing. Every number has been checked numerically.
>
> Question paper: [practice_exam_1.md](practice_exam_1.md)

---

## QUESTION 1 (4 marks)

**(a)** *Split the number into its integer part 13 and its fraction 0.6875.*

| Integer part (÷2, read the remainders bottom-up) | | Fraction (×2, read the integer parts top-down) | |
|---|---|---|---|
| 13 ÷ 2 = 6 | r **1** | 0.6875 × 2 = 1.375 | **1** |
| 6 ÷ 2 = 3 | r **0** | 0.375 × 2 = 0.75 | **0** |
| 3 ÷ 2 = 1 | r **1** | 0.75 × 2 = 1.5 | **1** |
| 1 ÷ 2 = 0 | r **1** | 0.5 × 2 = 1.0 | **1** (stop: fraction is now 0) |

$$13.6875=\boxed{1101.1011_2}\quad\textbf{[1 working, 1 answer]}$$
Check: $8+4+1+\tfrac12+\tfrac18+\tfrac1{16}=13.6875$ ✓

**(b)** *The largest number has every digit as large as possible ($d_i=\beta-1=1$) and the largest exponent $M=3$.*
$$L=1.111_2\times2^{3}=1111_2=\boxed{15}\qquad\text{or }L=(\beta-\beta^{1-k})\beta^M=(2-2^{-3})\cdot 8=15\quad\textbf{[1 working, 1 answer]}$$

---

## QUESTION 2 (6 marks)

**(a)** *Compute the derivatives, evaluate them at $x_0=0$, then substitute into the Taylor formula.*

$P_2(x)=f(x_0)+f'(x_0)(x-x_0)+\dfrac{f''(x_0)}{2}(x-x_0)^2$ **[1 form]**

- $f(x)=\log(1+x)$, so $f(0)=0$
- $f'(x)=\dfrac{1}{1+x}$, so $f'(0)=1$
- $f''(x)=-\dfrac{1}{(1+x)^2}$, so $f''(0)=-1$ **[1 working]**

$$P_2(x)=0+1\cdot x-\tfrac12x^2=\boxed{x-\frac{x^2}{2}}\quad\textbf{[1]}$$

**(b)** *Write down the remainder, then bound each factor by its worst case.*

$f'''(x)=\dfrac{2}{(1+x)^3}$, and $R_2(x)=\dfrac{f'''(c)}{3!}x^3=\dfrac{x^3}{3(1+c)^3}$, where $c$ lies between $0$ and $x$. **[1]**

For $0\le x\le0.5$ we have $0\le c\le0.5$, so $(1+c)^3\ge1$ and $|x|^3\le0.5^3$: **[1]**
$$|f(x)-P_2(x)|=|R_2(x)|\le\frac{1}{3}\cdot(0.5)^3=\boxed{0.0417}\quad\textbf{[1]}$$
(Sanity check: at $x=0.5$, $P_2=0.375$ and $\log1.5=0.4055$, so the actual error is $0.0305\le0.0417$ ✓)

---

## QUESTION 3 (6 marks)

$f(t,y)=t+y^2$, $t_0=0$, $w_0=1$, $h=0.1$

**(a)** *Euler: slope at the start × step, added to the start value.*
$$y(0.1)\approx w_1=w_0+hf(t_0,w_0)=1+0.1(0+1^2)=\boxed{1.1}\quad\textbf{[1 setup, 1 answer]}$$

**(b)** Modified Euler: $k_1=hf(t_i,w_i)$, $k_2=hf(t_i+h,w_i+k_1)$, $w_{i+1}=w_i+\tfrac12(k_1+k_2)$ **[1]**

- $k_1=0.1\,f(0,1)=0.1(1)=0.1$ *(the Euler increment: slope at the start)*
- $k_2=0.1\,f(0.1,\ 1.1)=0.1(0.1+1.21)=0.131$ *(slope at the predicted end point)* **[1]**
- $w_1=1+\tfrac12(0.1+0.131)=\boxed{1.1155}$ *(average the two increments)* **[1]**

**(c)** (b) should be more accurate: the modified Euler method is **second order** (global error $O(h^2)$), whereas Euler's method is only **first order** ($O(h)$). **[1]**

---

## QUESTION 4 (6 marks)

*Strategy: write down the correct modified Euler algorithm, then compare it with the code line by line.*

1. **Line 3:** the step size is wrong. It should be `h = (2 - 0)/n;` **[1 + 1]**
2. **Line 8:** $k_2$ must be evaluated at the **end** of the step, $t_i+h$. It should be `k2 = h*f(t+h, w+k1);` **[1 + 1]**
3. **Line 9:** the two increments must be **averaged**. It should be `w = w + (k1 + k2)/2;` **[1 + 1]**

*(Lines 4 and 5 correctly initialise `t` and `w`. Line 1 uses `t^2` on a scalar, which is fine.)*

---

## QUESTION 5 (4 marks)

*Same four moves as Euler, but keep one more Taylor term.*

The Taylor polynomial of degree 2 for $y(t)$ centred on $t_i$: **[1]**
$$y(t)=y(t_i)+y'(t_i)(t-t_i)+\frac{y''(t_i)}{2}(t-t_i)^2+O\big((t-t_i)^3\big)$$
Evaluate at $t=t_{i+1}$, so $t_{i+1}-t_i=h$: **[1]**
$$y_{i+1}=y_i+hy'(t_i)+\frac{h^2}{2}y''(t_i)+O(h^3)$$
From the ODE, $y'=f(t,y)$, so $y''=f'(t,y)$: **[1]**
$$y_{i+1}=y_i+hf(t_i,y_i)+\frac{h^2}{2}f'(t_i,y_i)+O(h^3)$$
Drop the $O(h^3)$ term and replace $y_i$ with the approximation $w_i$: **[1]**
$$w_{i+1}=w_i+hf(t_i,w_i)+\frac{h^2}{2}f'(t_i,w_i)$$

---

## QUESTION 6 (6 marks)

**(a)** $y_0=\log1=0$, $y_1=\log2=0.6931$, $y_2=\log4=1.3863$ **[1]**

*Each basis polynomial: the numerator skips its own node, and the denominator is the numerator with $x$ replaced by that node.*
$$P_2(x)=\frac{(x-2)(x-4)}{(1-2)(1-4)}(0)+\frac{(x-1)(x-4)}{(2-1)(2-4)}(0.6931)+\frac{(x-1)(x-2)}{(4-1)(4-2)}(1.3863)\quad\textbf{[1]}$$
At $x=3$: $L_{2,0}(3)=-\tfrac13$, $L_{2,1}(3)=\frac{(2)(-1)}{(1)(-2)}=1$, $L_{2,2}(3)=\frac{(2)(1)}{(3)(2)}=\tfrac13$
$$\log3\approx P_2(3)=0+0.6931+\tfrac13(1.3863)=\boxed{1.1552}\quad\textbf{[1]}$$

**(b)** $R_2(x)=\dfrac{f'''(c)}{3!}(x-1)(x-2)(x-4)$ with $c\in[1,4]$, and $f'''(x)=\dfrac{2}{x^3}$. **[1]**

*The largest value of $|f'''(c)|=2/c^3$ on $[1,4]$ is at $c=1$, giving 2.*
$$|R_2(3)|\le\frac{2}{6}\,\big|(3-1)(3-2)(3-4)\big|=\frac13\cdot2=\boxed{0.6667}\quad\textbf{[1]}$$
Actual error: $|1.1552-1.0986|=0.0566\le0.6667$ ✓ **[1]**

---

## QUESTION 7 (4 marks)

**(a)** $h=1$, $s=\dfrac{x-0}{1}=x$

| $x_i$ | $y_i$ | $\Delta y$ | $\Delta^2y$ | $\Delta^3y$ |
|---|---|---|---|---|
| 0 | **1** | | | |
| | | **1** | | |
| 1 | 2 | | **1** | |
| | | 2 | | **1** |
| 2 | 4 | | 2 | |
| | | 4 | | |
| 3 | 8 | | | |

**[1.5 table]**

$$P_3(x)=y_0+s\Delta y_0+\frac{s(s-1)}{2}\Delta^2y_0+\frac{s(s-1)(s-2)}{6}\Delta^3y_0\quad\textbf{[0.5]}$$
$$=1+s+\frac{s(s-1)}{2}+\frac{s(s-1)(s-2)}{6},\qquad s=x\quad\textbf{[0.5 + 0.5]}$$

**(b)** $x=0.5$ gives $s=0.5$:
$$P_3=1+0.5+\frac{(0.5)(-0.5)}{2}+\frac{(0.5)(-0.5)(-1.5)}{6}=1+0.5-0.125+0.0625=\boxed{1.4375}\quad\textbf{[1]}$$
(The true value is $\sqrt2=1.4142$.)

---

## QUESTION 8 (4 marks)

**(a)** *Each entry = (lower-left − upper-left) ÷ (outermost $x$'s).*

| $x_i$ | $f[x_i]$ | first | second |
|---|---|---|---|
| −1 | **3** | | |
| | | $\frac{1-3}{0-(-1)}=$ **−2** | |
| 0 | 1 | | $\frac{1-(-2)}{2-(-1)}=$ **1** |
| | | $\frac{3-1}{2-0}=1$ | |
| 2 | 3 | | |

**[1.5]**

*Read the top diagonal: $a_0=3$, $a_1=-2$, $a_2=1$.*
$$P_2(x)=3-2(x+1)+1\cdot(x+1)(x-0)\ \left(=x^2-x+1\right)\quad\textbf{[1.5]}$$

**(b)** *Add a row at the bottom: you only need ONE new entry in each column.*
- $f[2,1]=\frac{2-3}{1-2}=1$
- $f[0,2,1]=\frac{1-1}{1-0}=0$
- $f[-1,0,2,1]=\frac{0-1}{1-(-1)}=-0.5$

$$P_3(x)=P_2(x)-0.5(x+1)x(x-2)\quad\textbf{[1]}$$
(Check: $P_3(1)=1-0.5(2)(1)(-1)=2$ ✓)

---

## QUESTION 9 (6 marks)

**(a)** $f(1)=1-3-1=-3$ and $f(2)=8-6-1=1$. **[0.5 + 0.5]** These have opposite signs, and $f$ is continuous, so $[1,2]$ is a bracketing for $f$. **[1]**

**(b)**

| iter | $a$ | $b$ | $p=\frac{a+b}{2}$ | $f(a)$ | $f(b)$ | $f(p)$ | update |
|---|---|---|---|---|---|---|---|
| 1 | 1 | 2 | 1.5 | − | + | $-2.125$ (−) | $a\leftarrow1.5$ |
| 2 | 1.5 | 2 | 1.75 | − | + | $-0.8906$ (−) | $a\leftarrow1.75$ |

Approximate solution after 2 iterations: $x\approx\boxed{1.75}$ **[1 per iteration]**

**(c)** $x_{n+1}=x_n-\dfrac{f(x_n)}{f'(x_n)}$ **[0.5]** with $f'(x)=3x^2-3$ **[0.5]**:
$$x_1=2-\frac{f(2)}{f'(2)}=2-\frac{1}{9}=\frac{17}{9}=\boxed{1.8889}\quad\textbf{[1]}$$
(The true root is $1.8794$. Newton gets much closer than 2 bisection steps.)

---

## QUESTION 10 (6 marks)

*Correct secant step: $x_2=x_1-f(x_1)\dfrac{x_1-x_0}{f(x_1)-f(x_0)}$, then shift $x_0\leftarrow x_1$, $x_1\leftarrow x_2$.*

1. **Line 5:** the denominator is reversed. It should be `(f(x1) - f(x0))`. **[1 + 1]**
2. **Line 6:** this overwrites `x1` instead of shifting it. It should be `x0 = x1;` **[1 + 1]**
3. **Line 8:** the stopping test is reversed: it breaks while the iterates are still far apart. It should be `if abs(x1 - x0) <= tol`. **[1 + 1]**

---

## QUESTION 11 (4 marks)

*Choose $f$ so that its root is exactly the number we want: $x=\sqrt[4]a$ means $x^4=a$.*

Let $f(x)=x^4-a$ (its root is $\sqrt[4]a$). **[1]** Then $f'(x)=4x^3$, and Newton's method gives **[1]**
$$x_{n+1}=x_n-\frac{f(x_n)}{f'(x_n)}=x_n-\frac{x_n^4-a}{4x_n^3}\quad\textbf{[1]}$$
$$=x_n-\frac{x_n}{4}+\frac{a}{4x_n^3}=\frac{3x_n}{4}+\frac{a}{4x_n^3}\quad\textbf{[1]}$$

---

## QUESTION 12 (4 marks)

$h=0.2$

**(a)** *$x=2.4$ is the right end of the table, so only a backward difference is possible.*
$$f'(x_0)\approx\frac{f(x_0)-f(x_0-h)}{h}\quad\textbf{[1]}\qquad f'(2.4)\approx\frac{2.1011-1.7346}{0.2}=\boxed{1.8325}\quad\textbf{[1]}$$

**(b)** *The middle point can use the second-order central difference.*
$$f''(x_0)\approx\frac{f(x_0-h)-2f(x_0)+f(x_0+h)}{h^2}\quad\textbf{[1]}$$
$$f''(2.2)\approx\frac{1.3863-2(1.7346)+2.1011}{0.04}=\frac{0.0182}{0.04}=\boxed{0.4550}\quad\textbf{[1]}$$
(The data come from $x\log x$, so the exact values are $1.8755$ and $0.4545$.)

---

## QUESTION 13 (6 marks)

*Key fact: MATLAB `x(i)` is $x_{i-1}$. So `x(2), x(4), …` are $x_1,x_3,\dots$, the **odd** abscissas, which get weight **4** in Simpson's rule.*

1. **Line 2:** Simpson's rule needs an **even** number of subintervals (and the question specifies 8). It should be `n = 8;` **[1 + 1]**
2. **Lines 8 and 10:** the weights are swapped. For even `i` (odd abscissas) use `4*f(x(i))`, and otherwise use `2*f(x(i))`. **[1 + 1]**
3. **Line 13:** Simpson's prefactor is $h/3$, not $h/2$ (that's the trapezoidal rule). It should be `I = h/3*S;` **[1 + 1]**

---

## QUESTION 14 (5 marks)

$h=0.25$

**(a)**
$$T=\frac h2\big[f_0+2(f_1+f_2+f_3)+f_4\big]=\frac{0.25}{2}\big[1+2(0.9412+0.8+0.64)+0.5\big]\quad\textbf{[1]}$$
$$=0.125\times6.2624=\boxed{0.7828}\quad\textbf{[1]}$$

**(b)**
$$S=\frac h3\big[f_0+4(f_1+f_3)+2f_2+f_4\big]=\frac{0.25}{3}\big[1+4(0.9412+0.64)+2(0.8)+0.5\big]\quad\textbf{[1]}$$
$$=\frac{9.4248}{12}=\boxed{0.7854}\quad\textbf{[1]}$$

**(c)** $\pi/4=0.785398$, so the trapezoidal error is about $0.0026$ and the Simpson error is about $0.000002$. Simpson's rule is far more accurate, as expected: it is **fourth order** ($O(h^4)$), whereas the trapezoidal rule is **second order** ($O(h^2)$). **[1]**

---

## QUESTION 15 (5 marks)

**(a)** *For each entry: (row of $L$) · (column of $U$) $=a_{ij}$, then solve for the one unknown.*

- $u_{22}=a_{22}-\ell_{21}u_{12}=1-(2)(-1)=\boxed{3}$ **[1]**
- $\ell_{32}=\dfrac{a_{32}-\ell_{31}u_{12}}{u_{22}}=\dfrac{7-(-1)(-1)}{3}=\boxed{2}$ **[1]**
- $u_{33}=a_{33}-\ell_{31}u_{13}-\ell_{32}u_{23}=1-(-1)(3)-(2)(1)=\boxed{2}$ **[1]**

**(b)** *Two triangular solves: first $L\mathbf z=\mathbf b$ (top-down), then $U\mathbf x=\mathbf z$ (bottom-up).*

Forward ($L\mathbf z=\mathbf b$): $z_1=-3$; $2(-3)+z_2=-1\Rightarrow z_2=5$; $-(-3)+2(5)+z_3=11\Rightarrow z_3=-2$ **[1]**

Backward ($U\mathbf x=\mathbf z$): $2x_3=-2\Rightarrow x_3=-1$; $3x_2+(-1)=5\Rightarrow x_2=2$; $2x_1-2+3(-1)=-3\Rightarrow x_1=1$

$$\mathbf x=[1,\ 2,\ -1]^T\quad\textbf{[1]}$$

---

## QUESTION 16 (4 marks)

**(a)** $A$ must be **symmetric** and **positive definite** (SPD). **[0.5 + 0.5]**

**(b)** *Below the diagonal: (entry − dot product so far) ÷ diagonal. On the diagonal: √(entry − sum of squares so far).*

- $\ell_{21}=\dfrac{a_{21}}{\ell_{11}}=\dfrac{15}{5}=\boxed{3}$ **[1]**
- $\ell_{32}=\dfrac{a_{32}-\ell_{31}\ell_{21}}{\ell_{22}}=\dfrac{0-(-1)(3)}{3}=\boxed{1}$ **[1]**
- $\ell_{33}=\sqrt{a_{33}-\ell_{31}^2-\ell_{32}^2}=\sqrt{11-1-1}=\boxed{3}$ **[1]**
