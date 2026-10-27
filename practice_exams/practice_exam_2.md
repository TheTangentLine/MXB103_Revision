# MXB103 Practice Exam 2

> **Format matches the real exam:** 16 questions · 80 marks · 3 hours (+10 min perusal) · any calculator · one A4 sheet of notes.
> Q1–8 cover Topics 1–3 and Q9–16 cover Topics 4–6. Show all working. Use **radian mode**; $\log$ means the natural log.
>
> Solutions: [practice_exam_2_solutions.md](practice_exam_2_solutions.md). Try the paper under timed conditions first.

---

### QUESTION 1
**(a)** Express the binary number $101.101_2$ as a decimal number. *(2 marks)*

**(b)** Rearrange the expression $\sqrt{x^2+1}-x$ so that it does not exhibit catastrophic cancellation when $x$ is large and positive. *(2 marks)*

### QUESTION 2
**(a)** Find the Taylor polynomial of degree 2 centred on $x_0=1$ for the function $f(x)=\dfrac1x$. *(3 marks)*

**(b)** Find an upper bound on the absolute error incurred when using the polynomial in (a) to approximate $\dfrac1x$ for $x$ between $1$ and $1.2$. *(3 marks)*

### QUESTION 3
Consider the initial value problem
$$\frac{dy}{dt}=y-t,\qquad y(0)=2.$$

**(a)** Estimate $y(0.2)$ using Euler's method with subinterval width $h=0.2$. *(2 marks)*

**(b)** Estimate $y(0.2)$ using the second order Taylor method with subinterval width $h=0.2$. *(3 marks)*

**(c)** Do you expect the estimate in (a) or (b) to be more accurate? Justify your answer by referring to any relevant mathematical theory. *(1 mark)*

### QUESTION 4
Consider the initial value problem $\dfrac{dy}{dt}=y\cos t$, $y(0)=1$. Using the **fourth order Runge–Kutta method** with $n=50$ time steps, the following MATLAB script aims to approximate $y(1)$ by the final value of the variable `w`.

```matlab
1  f = @(t,y) y*cos(t);
2  a = 0; b = 1; n = 50;
3  h = (b-a)/n;
4  t = a; w = 1;
5  for i = 1:n-1
6      k1 = h*f(t,w);
7      k2 = h*f(t+h/2, w+k1/2);
8      k3 = h*f(t+h/2, w+k1/2);
9      k4 = h*f(t+h, w+k3);
10     w = w + (k1 + 2*k2 + 2*k3 + k4)/4;
11     t = t + h;
12 end
```
List 3 errors in the code and explain how they can be corrected so the code works as intended. *(6 marks)*

### QUESTION 5
Consider the ODE $\dfrac{dy}{dt}=f(t,y)$, $a\le t\le b$, with $y(a)=\alpha$. Derive the **modified Euler method**
$$w_{i+1}=w_i+\frac h2\Big[f(t_i,w_i)+f\big(t_{i+1},\,w_i+hf(t_i,w_i)\big)\Big],$$
where $[a,b]$ is divided into $n$ equal subintervals of width $h=(b-a)/n$, $t_i=a+ih$ and $w_i\approx y_i=y(t_i)$. *(4 marks)*

### QUESTION 6
Let $f(x)=\sqrt{x+1}$ and let $P_2(x)$ be the Lagrange form of the interpolating polynomial through $(0,f(0))$, $(1,f(1))$ and $(3,f(3))$. The MATLAB script below aims to calculate the absolute and relative errors when approximating $f(2)$ by $P_2(2)$.

```matlab
1  f = @(x) sqrt(x+1);
2  xd = [0, 1, 3];
3  yd = f(xd);
4  a = 2;
5  P2 = (a-xd(2))*(a-xd(3))/((xd(1)-xd(2))*(xd(1)-xd(3)))*yd(1) + ...
6       (a-xd(1))*(a-xd(3))/((xd(2)-xd(1))*(xd(2)-xd(3)))*yd(1) + ...
7       (a-xd(1))*(a-xd(2))/((xd(3)-xd(1))*(xd(3)-xd(2)))*yd(3);
8  abs_err = P2 - f(a);                  % absolute error
9  rel_err = abs(P2 - f(a))/abs(P2);     % relative error
```
List 3 errors in the code and explain how they can be corrected so the code works as intended. *(6 marks)*

### QUESTION 7
The following values of $f(x)=\sin(x)$ are given to 4 decimal places:

| $x$ | 0 | 0.2 | 0.4 | 0.6 |
|---|---|---|---|---|
| $f(x)$ | 0.0000 | 0.1987 | 0.3894 | 0.5646 |

**(a)** Find the Newton forward difference form of the interpolating polynomial passing through all four data points. *(3 marks)*

**(b)** Use your polynomial to estimate $\sin(0.3)$. *(1 mark)*

### QUESTION 8
**(a)** Using the definition of divided differences, express $f[x_0,x_1,x_2]$ in terms of the abscissas $x_0,x_1,x_2$ and function values $y_0,y_1,y_2$. *(2 marks)*

**(b)** Compute $f[1,2,4]$ for the data $(1,1)$, $(2,4)$, $(4,16)$. Explain why the answer is exactly $1$. *(2 marks)*

### QUESTION 9
Consider $f(x)=e^x-3x$, for which it is desired to solve $f(x)=0$.

**(a)** Show that the interval $[0,1]$ is a bracketing for $f(x)$. *(2 marks)*

**(b)** Apply one iteration of the secant method, starting with $x_0=0$ and $x_1=1$. *(2 marks)*

**(c)** Apply one iteration of Newton's method, starting with $x_0=0$. *(2 marks)*

### QUESTION 10
The MATLAB script below aims to solve $e^x-3x=0$ using **fixed point iteration** $x_{n+1}=g(x_n)$ with $g(x)=e^x/3$ and $x_0=0.5$. It should iterate until either $|x_{n+1}-x_n|\le10^{-6}$ or 100 iterations have been taken.

```matlab
1  g = @(x) exp(x)/3;
2  x = 0.5;
3  tol = 1e-6;
4  for n = 1:100
5      xnew = g(xnew);
6      if abs(xnew - x) > tol
7          break;
8      end
9      xnew = x;
10 end
```
List 3 errors in the code and explain how they can be corrected so the code works as intended. *(6 marks)*

### QUESTION 11
Let $a$ be any positive number. By applying the **secant method** to an appropriate equation of the form $f(x)=0$, derive the following iteration for approximating $\sqrt[3]a$:
$$x_{n+1}=x_n-\frac{x_n^3-a}{x_n^2+x_nx_{n-1}+x_{n-1}^2},\qquad n=1,2,3,\dots$$
*(4 marks)*

### QUESTION 12
**(a)** Use a Taylor polynomial to derive the first order forward difference approximation, including its error term:
$$f'(x_0)=\frac{f(x_0+h)-f(x_0)}{h}-\frac h2f''(c).$$
*(2 marks)*

**(b)** For $f(x)=e^{-x^2}$, approximate $f'(0.5)$ using the second order central difference approximation with $h=0.1$. *(2 marks)*

### QUESTION 13
**(a)** Let $P_2(x)$ be the interpolating polynomial for $f(x)$ at the equally spaced abscissas $x_0,x_1,x_2$ (spacing $h$). Show that
$$\int_{x_0}^{x_2}P_2(x)\,dx=\frac h3\big[f(x_0)+4f(x_1)+f(x_2)\big].$$
*(4 marks)*

**(b)** For polynomials of what degree is Simpson's rule exact? Explain briefly. *(1 mark)*

### QUESTION 14
The values of $f(x)=\log(x)$ to 4 decimal places are $0$, $0.2231$, $0.4055$, $0.5596$, $0.6931$ at $x=1,\ 1.25,\ 1.5,\ 1.75,\ 2$.

**(a)** Use the trapezoidal rule with $n=4$ subintervals to approximate $\int_1^2\log(x)\,dx$. *(2 marks)*

**(b)** Use Simpson's rule with $n=4$ subintervals to approximate the same integral. *(2 marks)*

**(c)** The exact value is $2\log2-1$. Compute the absolute error of each approximation. *(1 mark)*

### QUESTION 15
Consider
$$A=\begin{bmatrix}1&2&-1\\3&8&1\\-2&0&5\end{bmatrix}=\begin{bmatrix}1&0&0\\3&1&0\\-2&\ell_{32}&1\end{bmatrix}\begin{bmatrix}1&2&-1\\0&u_{22}&4\\0&0&u_{33}\end{bmatrix},\qquad\mathbf b=\begin{bmatrix}-1\\-1\\1\end{bmatrix}.$$

**(a)** Determine $u_{22}$, $\ell_{32}$ and $u_{33}$. *(3 marks)*

**(b)** Use the LU factorisation to solve $A\mathbf x=\mathbf b$. *(2 marks)*

### QUESTION 16
**(a)** Show that the symmetric matrix $\begin{bmatrix}4&-2\\-2&3\end{bmatrix}$ is positive definite. *(3 marks)*

**(b)** Determine $\ell_{22}$ and $\ell_{33}$ in the following partially complete Cholesky factorisation:
$$\begin{bmatrix}4&-2&2\\-2&10&-7\\2&-7&9\end{bmatrix}=\begin{bmatrix}2&0&0\\-1&\ell_{22}&0\\1&-2&\ell_{33}\end{bmatrix}\begin{bmatrix}2&-1&1\\0&\ell_{22}&-2\\0&0&\ell_{33}\end{bmatrix}$$
*(2 marks)*

---
**END OF PAPER** (Total: 80 marks)
