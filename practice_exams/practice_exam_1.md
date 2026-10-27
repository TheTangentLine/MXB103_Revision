# MXB103 Practice Exam 1

> **Format matches the real exam:** 16 questions · 80 marks · 3 hours (+10 min perusal) · any calculator · one A4 sheet of notes.
> Q1–8 cover Topics 1–3 and Q9–16 cover Topics 4–6. Show all working. Use **radian mode**; $\log$ means the natural log.
>
> Solutions: [practice_exam_1_solutions.md](practice_exam_1_solutions.md). Try the paper under timed conditions first.

---

### QUESTION 1
**(a)** Express the decimal number $13.6875$ as a binary number. *(2 marks)*

**(b)** Determine the largest representable positive number in the floating point number system $F(2,4,-2,3)$. Give your answer in decimal. *(2 marks)*

### QUESTION 2
**(a)** Find the Taylor polynomial of degree 2 centred on $x_0=0$ for the function $f(x)=\log(1+x)$. *(3 marks)*

**(b)** Find an upper bound on the absolute error incurred when using the polynomial in (a) to approximate $\log(1+x)$ for $x$ between $0$ and $0.5$. *(3 marks)*

### QUESTION 3
Consider the initial value problem
$$\frac{dy}{dt}=t+y^2,\qquad y(0)=1.$$

**(a)** Estimate $y(0.1)$ using Euler's method with subinterval width $h=0.1$. *(2 marks)*

**(b)** Estimate $y(0.1)$ using the modified Euler method with subinterval width $h=0.1$. *(3 marks)*

**(c)** Do you expect the estimate in (a) or (b) to be more accurate? Justify your answer by referring to any relevant mathematical theory. *(1 mark)*

### QUESTION 4
Consider the initial value problem $\dfrac{dy}{dt}=y-t^2$, $y(0)=0.5$. Using the **modified Euler method** with $n=20$ time steps, the following MATLAB script aims to approximate $y(2)$ by the final value of the variable `w`.

```matlab
1  f = @(t,y) y - t^2;
2  n = 20;
3  h = (2 - 0)*n;
4  t = 0;
5  w = 0.5;
6  for i = 1:n
7      k1 = h*f(t,w);
8      k2 = h*f(t,w+k1);
9      w = w + (k1 + k2);
10     t = t + h;
11 end
```
List 3 errors in the code and explain how they can be corrected so the code works as intended. *(6 marks)*

### QUESTION 5
Consider the ODE $\dfrac{dy}{dt}=f(t,y)$, $a\le t\le b$, with $y(a)=\alpha$. Derive the **second order Taylor method**
$$w_{i+1}=w_i+hf(t_i,w_i)+\frac{h^2}{2}f'(t_i,w_i),$$
where $[a,b]$ is divided into $n$ equal subintervals of width $h=(b-a)/n$, $t_i=a+ih$ and $w_i\approx y_i=y(t_i)$. *(4 marks)*

### QUESTION 6
Let $f(x)=\log(x)$ and consider the abscissas $x_0=1$, $x_1=2$, $x_2=4$.

**(a)** Find the Lagrange form of the interpolating polynomial $P_2(x)$, and use it to estimate $\log(3)$. *(3 marks)*

**(b)** Use the Lagrange form of the remainder to find an upper bound on the absolute error in your estimate of $\log(3)$. Verify that the actual error satisfies this bound. *(3 marks)*

### QUESTION 7
Consider the data points $(0,1)$, $(1,2)$, $(2,4)$ and $(3,8)$.

**(a)** Find the Newton forward difference form of the interpolating polynomial passing through all four data points. *(3 marks)*

**(b)** Given that the data come from $f(x)=2^x$, estimate $\sqrt2=2^{0.5}$ using your polynomial from (a). *(1 mark)*

### QUESTION 8
**(a)** Construct the divided difference table for the data $(-1,3)$, $(0,1)$, $(2,3)$ and hence find the Newton divided difference form of the interpolating polynomial $P_2(x)$. *(3 marks)*

**(b)** With as little extra work as possible, include the additional data point $(1,2)$ and find $P_3(x)$. *(1 mark)*

### QUESTION 9
Consider $f(x)=x^3-3x-1$, for which it is desired to solve $f(x)=0$.

**(a)** Show that the interval $[1,2]$ is a bracketing for $f(x)$. *(2 marks)*

**(b)** Apply two iterations of the bisection method using the bracketing from (a). *(2 marks)*

**(c)** Apply one iteration of Newton's method, starting with $x_0=2$. *(2 marks)*

### QUESTION 10
The MATLAB script below aims to solve $x^3-3x-1=0$ using the **secant method** with initial iterates $x_0=1$ and $x_1=2$. It should iterate until either the absolute difference between consecutive iterates is less than or equal to $10^{-8}$, or 50 iterations have been taken.

```matlab
1  f = @(x) x^3 - 3*x - 1;
2  x0 = 1; x1 = 2;
3  tol = 1e-8;
4  for n = 1:50
5      x2 = x1 - f(x1)*(x1 - x0)/(f(x0) - f(x1));
6      x1 = x0;
7      x1 = x2;
8      if abs(x1 - x0) > tol
9          break;
10     end
11 end
```
List 3 errors in the code and explain how they can be corrected so the code works as intended. *(6 marks)*

### QUESTION 11
Let $a$ be any positive number. By applying Newton's method to an appropriate equation of the form $f(x)=0$, derive the following iteration for approximating $\sqrt[4]{a}$:
$$x_{n+1}=\frac{3x_n}{4}+\frac{a}{4x_n^3},\qquad n=0,1,2,\dots$$
*(4 marks)*

### QUESTION 12
The values of a function $f(x)$ are known at three points:

| $x$ | 2.0 | 2.2 | 2.4 |
|---|---|---|---|
| $f(x)$ | 1.3863 | 1.7346 | 2.1011 |

**(a)** Using just two values of $f(x)$, approximate $f'(2.4)$. *(2 marks)*

**(b)** Using all three values of $f(x)$, approximate $f''(2.2)$. *(2 marks)*

### QUESTION 13
The MATLAB script below aims to apply the **composite Simpson's rule** with $n=8$ subintervals to approximate $I=\int_0^2\sqrt{1+x^3}\,dx$.

```matlab
1  f = @(x) sqrt(1 + x.^3);
2  a = 0; b = 2; n = 7;
3  h = (b-a)/n;
4  x = a:h:b;
5  S = f(x(1)) + f(x(n+1));
6  for i = 2:n
7      if mod(i,2) == 0
8          S = S + 2*f(x(i));
9      else
10         S = S + 4*f(x(i));
11     end
12 end
13 I = h/2*S;
```
List 3 errors in the code and explain how they can be corrected so the code works as intended. *(6 marks)*

### QUESTION 14
Let $f(x)=\dfrac{1}{1+x^2}$. Rounded to 4 decimal places, $f(0)=1.0000$, $f(0.25)=0.9412$, $f(0.5)=0.8000$, $f(0.75)=0.6400$ and $f(1)=0.5000$.

**(a)** Use the trapezoidal rule with $n=4$ subintervals to approximate $\int_0^1f(x)\,dx$. *(2 marks)*

**(b)** Use Simpson's rule with $n=4$ subintervals to approximate the same integral. *(2 marks)*

**(c)** The exact value is $\pi/4$. Which approximation is more accurate, and is this what you expected? Explain. *(1 mark)*

### QUESTION 15
Consider
$$A=\begin{bmatrix}2&-1&3\\4&1&7\\-2&7&1\end{bmatrix}=\begin{bmatrix}1&0&0\\2&1&0\\-1&\ell_{32}&1\end{bmatrix}\begin{bmatrix}2&-1&3\\0&u_{22}&1\\0&0&u_{33}\end{bmatrix},\qquad \mathbf b=\begin{bmatrix}-3\\-1\\11\end{bmatrix}.$$

**(a)** Determine $u_{22}$, $\ell_{32}$ and $u_{33}$. *(3 marks)*

**(b)** Use the LU factorisation to solve $A\mathbf x=\mathbf b$. *(2 marks)*

### QUESTION 16
**(a)** To use Cholesky factorisation to solve $A\mathbf x=\mathbf b$, what properties must $A$ have? *(1 mark)*

**(b)** Determine $\ell_{21}$, $\ell_{32}$ and $\ell_{33}$ in the following partially complete Cholesky factorisation:
$$\begin{bmatrix}25&15&-5\\15&18&0\\-5&0&11\end{bmatrix}=\begin{bmatrix}5&0&0\\\ell_{21}&3&0\\-1&\ell_{32}&\ell_{33}\end{bmatrix}\begin{bmatrix}5&\ell_{21}&-1\\0&3&\ell_{32}\\0&0&\ell_{33}\end{bmatrix}$$
*(3 marks)*

---
**END OF PAPER** (Total: 80 marks)
