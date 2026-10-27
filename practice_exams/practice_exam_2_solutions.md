# MXB103 Practice Exam 2: Solutions

> Marks in **[brackets]** follow the style of the official marking schemes. Each solution is laid out the way the markers expect, with short notes in *italics* explaining what each step is doing. Every number has been checked numerically.
>
> Question paper: [practice_exam_2.md](practice_exam_2.md)

---

## QUESTION 1 (4 marks)

**(a)** *Multiply each digit by its power of 2: positions left of the point are $2^2,2^1,2^0$, and positions right of it are $2^{-1},2^{-2},2^{-3}$.*
$$101.101_2=1\cdot2^2+0\cdot2^1+1\cdot2^0+1\cdot2^{-1}+0\cdot2^{-2}+1\cdot2^{-3}=4+1+0.5+0.125=\boxed{5.625}\quad\textbf{[1 + 1]}$$

**(b)** *Recognise the danger:* for large $x$, $\sqrt{x^2+1}\approx x$, so this subtracts two nearly-equal numbers, which is catastrophic cancellation.

*Fix: multiply by the conjugate over itself.* **[1]**
$$\sqrt{x^2+1}-x=\frac{(\sqrt{x^2+1}-x)(\sqrt{x^2+1}+x)}{\sqrt{x^2+1}+x}=\frac{(x^2+1)-x^2}{\sqrt{x^2+1}+x}=\boxed{\frac{1}{\sqrt{x^2+1}+x}}\quad\textbf{[1]}$$
The new form **adds** two positive numbers, so there is no cancellation.

---

## QUESTION 2 (6 marks)

**(a)** $P_2(x)=f(x_0)+f'(x_0)(x-x_0)+\dfrac{f''(x_0)}{2}(x-x_0)^2$ **[1]**

- $f(x)=x^{-1}$, so $f(1)=1$
- $f'(x)=-x^{-2}$, so $f'(1)=-1$
- $f''(x)=2x^{-3}$, so $f''(1)=2$ **[1]**

$$P_2(x)=1-(x-1)+\frac{2}{2}(x-1)^2=\boxed{1-(x-1)+(x-1)^2}\quad\textbf{[1]}$$

**(b)** $f'''(x)=-6x^{-4}$, so $R_2(x)=\dfrac{f'''(c)}{3!}(x-1)^3=-\dfrac{(x-1)^3}{c^4}$, where $c$ lies between $1$ and $x$. **[1]**

For $1\le x\le1.2$: $c\ge1$, so $\frac1{c^4}\le1$, and $|x-1|^3\le0.2^3$. **[1]**
$$|R_2(x)|\le1\times0.2^3=\boxed{0.008}\quad\textbf{[1]}$$
(Check: at $x=1.2$, $P_2=0.84$ and $1/1.2=0.8333$, so the actual error is $0.0067\le0.008$ ✓)

---

## QUESTION 3 (6 marks)

$f(t,y)=y-t$, $t_0=0$, $w_0=2$, $h=0.2$

**(a)**
$$y(0.2)\approx w_1=w_0+hf(t_0,w_0)=2+0.2(2-0)=\boxed{2.4}\quad\textbf{[1 setup, 1 answer]}$$

**(b)** $w_{i+1}=w_i+hf(t_i,w_i)+\dfrac{h^2}{2}f'(t_i,w_i)$ **[1]**

*The total derivative: $y$ depends on $t$, so differentiate $y$ to get $y'$, then replace $y'$ with $f$.*
$$f'(t,y)=\frac{d}{dt}(y-t)=y'-1=(y-t)-1\quad\textbf{[1]}$$
At $(0,2)$: $f=2$ and $f'=2-0-1=1$, so
$$w_1=2+0.2(2)+\frac{0.2^2}{2}(1)=2+0.4+0.02=\boxed{2.42}\quad\textbf{[1]}$$
(The exact solution is $y=t+1+e^t$, so $y(0.2)=2.4214$.)

**(c)** (b) should be more accurate: the second order Taylor method has global error $O(h^2)$, while Euler's method is first order, $O(h)$. **[1]**

---

## QUESTION 4 (6 marks)

*Write out RK4 correctly first: $k_2,k_3$ at $t+h/2$ using $k_1/2$ and $k_2/2$ respectively; $k_4$ at $t+h$ using the full $k_3$; weights $\tfrac16(1,2,2,1)$; $n$ steps in total.*

1. **Line 5:** this takes only $n-1$ steps, so it stops at $t=0.98$. It should be `for i = 1:n` **[1 + 1]**
2. **Line 8:** $k_3$ must use $k_2$. It should be `k3 = h*f(t+h/2, w+k2/2);` **[1 + 1]**
3. **Line 10:** the weights $1+2+2+1=6$, so it should be `w = w + (k1 + 2*k2 + 2*k3 + k4)/6;` **[1 + 1]**

---

## QUESTION 5 (4 marks)

*Start from Taylor 2, replace the awkward $f'$ by a difference quotient, then replace the unknown $w_{i+1}$ on the right-hand side by an Euler prediction.*

Taylor polynomial of degree 2 about $t_i$, evaluated at $t_{i+1}$, using $y'=f$ and $y''=f'$: **[1.5]**
$$y_{i+1}=y_i+hf(t_i,y_i)+\frac{h^2}{2}f'(t_i,y_i)+O(h^3)$$
Approximate the derivative by a forward difference: **[0.5]**
$$f'(t_i,y_i)=\frac{f(t_{i+1},y_{i+1})-f(t_i,y_i)}{h}+O(h)$$
Substitute and simplify (the error $\frac{h^2}{2}O(h)$ joins the $O(h^3)$ term): **[1]**
$$y_{i+1}=y_i+hf(t_i,y_i)+\frac h2\big[f(t_{i+1},y_{i+1})-f(t_i,y_i)\big]+O(h^3)=y_i+\frac h2\big[f(t_i,y_i)+f(t_{i+1},y_{i+1})\big]+O(h^3)$$
Drop $O(h^3)$ and replace $y$ with $w$: $w_{i+1}=w_i+\frac h2[f(t_i,w_i)+f(t_{i+1},w_{i+1})]$. Then $w_{i+1}$ appears on both sides, so approximate the one on the right with Euler, $w_{i+1}\approx w_i+hf(t_i,w_i)$: **[1]**
$$w_{i+1}=w_i+\frac h2\Big[f(t_i,w_i)+f\big(t_{i+1},\,w_i+hf(t_i,w_i)\big)\Big]$$

---

## QUESTION 6 (6 marks)

*Check each Lagrange term: is each $y$ multiplied by its own basis polynomial? Then check the two error formulas.*

1. **Line 6:** the second basis polynomial $L_{2,1}$ must multiply $y_1$. It should end `*yd(2) + ...` **[1 + 1]**
2. **Line 8:** the absolute error needs an absolute value. It should be `abs_err = abs(P2 - f(a));` **[1 + 1]**
3. **Line 9:** relative error divides by the **true** value. It should be `rel_err = abs(P2 - f(a))/abs(f(a));` **[1 + 1]**

*(Lines 1–3 are fine: `sqrt` acts element-wise on the vector `xd`. With the fixes, $P_2(2)=1.7475$ versus $\sqrt3=1.7321$.)*

---

## QUESTION 7 (4 marks)

**(a)** $h=0.2$, $s=\dfrac{x-0}{0.2}=5x$

| $x_i$ | $y_i$ | $\Delta y$ | $\Delta^2y$ | $\Delta^3y$ |
|---|---|---|---|---|
| 0 | **0.0000** | | | |
| | | **0.1987** | | |
| 0.2 | 0.1987 | | **−0.0080** | |
| | | 0.1907 | | **−0.0075** |
| 0.4 | 0.3894 | | −0.0155 | |
| | | 0.1752 | | |
| 0.6 | 0.5646 | | | |

**[1.5]**

$$P_3(x)=y_0+s\Delta y_0+\frac{s(s-1)}{2}\Delta^2y_0+\frac{s(s-1)(s-2)}{6}\Delta^3y_0\quad\textbf{[0.5]}$$
$$=0.1987s-0.0040\,s(s-1)-0.00125\,s(s-1)(s-2),\qquad s=5x\quad\textbf{[0.5 + 0.5]}$$

**(b)** $x=0.3$ gives $s=1.5$ *(convert to $s$ first!)*:
$$P_3=0.1987(1.5)-0.0040(1.5)(0.5)-0.00125(1.5)(0.5)(-0.5)=0.29805-0.0030+0.00047=\boxed{0.2955}\quad\textbf{[1]}$$
(The true value is $\sin0.3=0.29552$.)

---

## QUESTION 8 (4 marks)

**(a)** *Apply the definition once, then again to each first divided difference.*
$$f[x_0,x_1,x_2]=\frac{f[x_1,x_2]-f[x_0,x_1]}{x_2-x_0}\quad\textbf{[1]}=\frac{\dfrac{y_2-y_1}{x_2-x_1}-\dfrac{y_1-y_0}{x_1-x_0}}{x_2-x_0}\quad\textbf{[1]}$$

**(b)** $f[1,2]=\frac{4-1}{2-1}=3$, $f[2,4]=\frac{16-4}{4-2}=6$, so $f[1,2,4]=\frac{6-3}{4-1}=\boxed{1}$ **[1]**

*Why:* the data lie on $y=x^2$, so the unique interpolating quadratic is $P_2(x)=x^2$. In the Newton form, $f[x_0,x_1,x_2]$ is the coefficient of $(x-x_0)(x-x_1)$, which is the **leading ($x^2$) coefficient**, here 1. **[1]**

---

## QUESTION 9 (6 marks)

**(a)** $f(0)=e^0-0=1>0$ and $f(1)=e-3=-0.2817<0$. **[0.5 + 0.5]** These have opposite signs and $f$ is continuous, so $[0,1]$ is a bracketing. **[1]**

**(b)** $x_{n+1}=x_n-f(x_n)\dfrac{x_n-x_{n-1}}{f(x_n)-f(x_{n-1})}$ **[0.5]**
$$x_2=1-(-0.2817)\frac{1-0}{-0.2817-1}=1-\frac{0.2817}{1.2817}=\boxed{0.7802}\quad\textbf{[1 + 0.5]}$$

**(c)** $f'(x)=e^x-3$, so $f'(0)=-2$ **[0.5 form, 0.5 derivative]**
$$x_1=0-\frac{f(0)}{f'(0)}=0-\frac{1}{-2}=\boxed{0.5}\quad\textbf{[1]}$$
(The true root is $0.6191$.)

---

## QUESTION 10 (6 marks)

*Correct loop: `xnew = g(x)`, stop if `abs(xnew - x) <= tol`, otherwise move forward with `x = xnew`.*

1. **Line 5:** `xnew` is used before it has a value. It should be `xnew = g(x);` **[1 + 1]**
2. **Line 6:** the stopping test is reversed. It should be `if abs(xnew - x) <= tol` **[1 + 1]**
3. **Line 9:** the assignment is backwards: the new iterate must become the current one. It should be `x = xnew;` **[1 + 1]**

*(Will it converge? On $[0,1]$, $g(x)=e^x/3$ lies in $[\tfrac13,\tfrac e3]\subset[0,1]$, and $|g'(x)|=e^x/3\le e/3\approx0.906<1$, so the fixed point theorem guarantees convergence. It is slow because $\lambda\approx0.62$ near the root.)*

---

## QUESTION 11 (4 marks)

Let $f(x)=x^3-a$ (its root is $\sqrt[3]a$). **[1]** The secant method gives **[1]**
$$x_{n+1}=x_n-f(x_n)\frac{x_n-x_{n-1}}{f(x_n)-f(x_{n-1})}=x_n-(x_n^3-a)\frac{x_n-x_{n-1}}{(x_n^3-a)-(x_{n-1}^3-a)}=x_n-(x_n^3-a)\frac{x_n-x_{n-1}}{x_n^3-x_{n-1}^3}$$
*Key step: difference of cubes, $p^3-q^3=(p-q)(p^2+pq+q^2)$.* **[1]**
$$=x_n-(x_n^3-a)\frac{x_n-x_{n-1}}{(x_n-x_{n-1})(x_n^2+x_nx_{n-1}+x_{n-1}^2)}=x_n-\frac{x_n^3-a}{x_n^2+x_nx_{n-1}+x_{n-1}^2}\quad\textbf{[1]}$$

---

## QUESTION 12 (4 marks)

**(a)** The Taylor polynomial of degree 1 for $f(x_0+h)$ with its remainder ($c$ between $x_0$ and $x_0+h$): **[1]**
$$f(x_0+h)=f(x_0)+hf'(x_0)+\frac{h^2}{2}f''(c)$$
Rearrange for $f'(x_0)$: subtract $f(x_0)$ and $\frac{h^2}2f''(c)$, then divide by $h$: **[1]**
$$f'(x_0)=\frac{f(x_0+h)-f(x_0)}{h}-\frac h2f''(c)$$

**(b)** $f'(x_0)\approx\dfrac{f(x_0+h)-f(x_0-h)}{2h}$ **[1]**, with $f(0.6)=e^{-0.36}=0.697676$ and $f(0.4)=e^{-0.16}=0.852144$:
$$f'(0.5)\approx\frac{0.697676-0.852144}{0.2}=\boxed{-0.7723}\quad\textbf{[1]}$$
(Exact: $-2(0.5)e^{-0.25}=-0.7788$.)

---

## QUESTION 13 (5 marks)

**(a)** Use the Newton forward difference form $P_2(x)=y_0+s\Delta y_0+\frac{s(s-1)}2\Delta^2y_0$ with $s=\frac{x-x_0}{h}$. **[1]**

*Change of variable:* $x=x_0+sh$, so $dx=h\,ds$. Also $x=x_0$ gives $s=0$ and $x=x_2$ gives $s=2$.
$$\int_{x_0}^{x_2}P_2\,dx=h\int_0^2\Big[y_0+s\Delta y_0+\big(\tfrac12s^2-\tfrac12s\big)\Delta^2y_0\Big]ds=h\Big[y_0s+\tfrac12s^2\Delta y_0+\big(\tfrac16s^3-\tfrac14s^2\big)\Delta^2y_0\Big]_0^2\quad\textbf{[1]}$$
$$=h\Big[2y_0+2\Delta y_0+\tfrac13\Delta^2y_0\Big]$$
Substitute $\Delta y_0=y_1-y_0$ and $\Delta^2y_0=y_2-2y_1+y_0$: **[1]**
$$=h\Big[2y_0+2y_1-2y_0+\tfrac13y_2-\tfrac23y_1+\tfrac13y_0\Big]=h\Big[\tfrac13y_0+\tfrac43y_1+\tfrac13y_2\Big]=\frac h3\big[f(x_0)+4f(x_1)+f(x_2)\big]\quad\textbf{[1]}$$

**(b)** Degree $\le3$. The error term is $-\frac{(b-a)h^4}{180}f^{(4)}(c)$, and $f^{(4)}\equiv0$ for any cubic, so the error is zero. **[1]**

---

## QUESTION 14 (5 marks)

$h=0.25$

**(a)**
$$T=\frac{0.25}{2}\big[0+2(0.2231+0.4055+0.5596)+0.6931\big]=0.125\times3.0695=\boxed{0.3837}\quad\textbf{[1 + 1]}$$

**(b)**
$$S=\frac{0.25}{3}\big[0+4(0.2231+0.5596)+2(0.4055)+0.6931\big]=\frac{4.6349}{12}=\boxed{0.3862}\quad\textbf{[1 + 1]}$$

**(c)** Exact: $2\log2-1=0.386294$. The trapezoidal error is $|0.386294-0.383688|\approx0.0026$, and the Simpson error is $|0.386294-0.386242|\approx0.00005$. **[1]**

---

## QUESTION 15 (5 marks)

**(a)**
- $u_{22}=a_{22}-\ell_{21}u_{12}=8-3(2)=\boxed{2}$ **[1]**
- $\ell_{32}=\dfrac{a_{32}-\ell_{31}u_{12}}{u_{22}}=\dfrac{0-(-2)(2)}{2}=\boxed{2}$ **[1]**
- $u_{33}=a_{33}-\ell_{31}u_{13}-\ell_{32}u_{23}=5-(-2)(-1)-2(4)=\boxed{-5}$ **[1]**

**(b)** Forward ($L\mathbf z=\mathbf b$): $z_1=-1$; $3(-1)+z_2=-1\Rightarrow z_2=2$; $-2(-1)+2(2)+z_3=1\Rightarrow z_3=-5$ **[1]**

Backward ($U\mathbf x=\mathbf z$): $-5x_3=-5\Rightarrow x_3=1$; $2x_2+4(1)=2\Rightarrow x_2=-1$; $x_1+2(-1)-1=-1\Rightarrow x_1=2$

$$\mathbf x=[2,\ -1,\ 1]^T\quad\textbf{[1]}$$

---

## QUESTION 16 (5 marks)

**(a)** We must show $\mathbf x^TA\mathbf x>0$ for all $\mathbf x\ne\mathbf0$. **[1]**
$$\mathbf x^TA\mathbf x=\begin{bmatrix}x_1&x_2\end{bmatrix}\begin{bmatrix}4x_1-2x_2\\-2x_1+3x_2\end{bmatrix}=4x_1^2-4x_1x_2+3x_2^2\quad\textbf{[1]}$$
*Complete the square: $4x_1^2-4x_1x_2=(2x_1-x_2)^2-x_2^2$.*
$$=(2x_1-x_2)^2+2x_2^2\quad\textbf{[0.5]}$$
This is a sum of squares, so it is $\ge0$, and it equals 0 only if $x_2=0$ and $2x_1=x_2$, i.e. $\mathbf x=\mathbf0$. So $A$ is positive definite. **[0.5]**

**(b)**
- $\ell_{22}=\sqrt{a_{22}-\ell_{21}^2}=\sqrt{10-1}=\boxed{3}$ **[1]**
- $\ell_{33}=\sqrt{a_{33}-\ell_{31}^2-\ell_{32}^2}=\sqrt{9-1-4}=\boxed{2}$ **[1]**
