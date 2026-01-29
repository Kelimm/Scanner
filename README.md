# 🕵️‍♂️ Custom Canny Edge Detector (from scratch)

A pure Python implementation of the **Canny Edge Detection** algorithm. This project recreates every mathematical step using **NumPy** vectorization, moving away from black-box library functions to understand the underlying computer vision principles.

---

## 🚀 The Mathematical Pipeline

The algorithm follows a rigorous four-stage process powered by linear algebra and calculus.

### 1. Noise Reduction (Gaussian Blur)
To prevent the algorithm from detecting noise as edges, we apply a $5 \times 5$ Gaussian kernel $H$. Each pixel value is recomputed as a weighted average of its neighbors:

$$
H = \frac{1}{159} 
\begin{bmatrix} 
2 & 4 & 5 & 4 & 2 \\ 
4 & 9 & 12 & 9 & 4 \\ 
5 & 12 & 15 & 12 & 5 \\ 
4 & 9 & 12 & 9 & 4 \\ 
2 & 4 & 5 & 4 & 2 
\end{bmatrix}
$$

### 2. Gradient Calculation (Sobel Operators)
We calculate the intensity gradient of the image using Sobel kernels. This highlights regions with high luminous spatial frequency.

* **Horizontal Gradient ($G_x$):** $G_x = I * K_x$
* **Vertical Gradient ($G_y$):** $G_y = I * K_y$

Where the kernels are defined as:

$$
K_x = \begin{bmatrix} 
-1 & 0 & 1 \\ 
-2 & 0 & 2 \\ 
-1 & 0 & 1 
\end{bmatrix}
\quad , \quad
K_y = \begin{bmatrix} 
-1 & -2 & -1 \\ 
0 & 0 & 0 \\ 
1 & 2 & 1 
\end{bmatrix}
$$

The **Magnitude ($G$)** and **Direction ($\theta$)** are then computed:

$$G = \sqrt{G_x^2 + G_y^2}$$

$$\theta = \arctan\left(\frac{G_y}{G_x}\right)$$

### 3. Non-Maximum Suppression (NMS)
To obtain thin edges, we only preserve pixels that are local maxima in the direction of the gradient $\theta$. If a pixel's magnitude $G(i,j)$ is not greater than its neighbors along the gradient vector, it is suppressed ($G = 0$).

### 4. Hysteresis Thresholding
We use two thresholds, $T_{high}$ and $T_{low}$, to classify pixels:
* **Strong edges**: $G \geq T_{high}$ (Keep)
* **Weak edges**: $T_{low} \leq G < T_{high}$ (Keep only if connected to a strong edge)
* **Suppressed**: $G < T_{low}$ (Discard)

---
## 🖼️ Example Results

Comparison between the input image and the custom Canny output:

| Original Image | Custom Canny Output |
| :---: | :---: |
| ![Original Image](./example.jpg) | ![Canny Output](./example_canny.jpg) |

*(Replace the paths above with your actual image filenames)*

---
## 🚧 Work In Progress: Document Scanner

The project is currently evolving into an **Automatic Document Scanner**. 

**Current development focus:**
* [ ] **Quadrilateral Detection**: Implementing contour approximation to find the document's four corners.
* [ ] **Perspective Warp**: Applying a homography matrix to transform the document into a top-down view.
* [ ] **Adaptive Binarization**: Enhancing text readability after scanning.

---
*Developed with ☕ and Linear Algebra.*
