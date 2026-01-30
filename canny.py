import numpy as np
import cv2

import os

def NMS(G, angle) :
    G_droite = np.roll(G,1, 1)
    G_gauche = np.roll(G,-1, 1)
    G_bas = np.roll(G,1, 0)
    G_haut = np.roll(G,-1, 0)

    G_diagDB = np.roll(G_droite,1, 0)
    G_diagDH = np.roll(G_droite,-1, 0)
    G_diagGB = np.roll(G_gauche, 1, 0)
    G_diagGH = np.roll(G_gauche, -1, 0)

    masque0 = (angle == 0)
    masque45 = (angle == 45)
    masque90 = (angle == 90)
    masque135 = (angle == 135)

    G0 = masque0 & (G >= G_droite) & (G >= G_gauche)
    G1 = masque45 & (G >= G_diagDH) & (G >= G_diagGB)
    G2 = masque90 & (G >= G_haut) & (G >= G_bas)
    G3 = masque135 & (G >= G_diagDB) & (G >= G_diagGH)

    masque_nms = G0 | G1 | G2 | G3


    G[0] = 0
    G[-1] = 0
    G[:,0] = 0
    G[:,-1] = 0

    return G * masque_nms

def hysteresis(T, G_nms) :
    Th = T * np.max(G_nms)
    Tb = Th * 0.5
    pFort = G_nms >= Th
    pFaible = (G_nms >= Tb) & (G_nms <= Th)
    
    ctn = True

    while ctn :
        pFort_droite = np.roll(pFort, 1, 1)
        pFort_gauche = np.roll(pFort, -1, 1)
        pFort_bas = np.roll(pFort, 1, 0)
        pFort_haut = np.roll(pFort, -1, 0)

        pFort_diagDB = np.roll(pFort_droite, 1, 0)
        pFort_diagDH = np.roll(pFort_droite, -1, 0)
        pFort_diagpGB = np.roll(pFort_gauche, 1, 0)
        pFort_diagpGH = np.roll(pFort_gauche, -1, 0)
        nv = pFaible & (pFort_bas  |
                      pFort_haut |
                      pFort_gauche |
                      pFort_droite |
                      pFort_diagDB |
                      pFort_diagDH |
                      pFort_diagpGB |
                      pFort_diagpGH)
        if not nv.any() :
            break
        
        pFort = pFort | nv
        pFaible = ~nv & pFaible
        
    return  G_nms * pFort


def cannyEdge(T, frame) :
    # img_path = os.path.join(".",frame)
    # img = cv2.imread(img_path)
    img = frame

    img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    img_gray = img_gray.astype(np.float64)
    noyau = np.array([
    [2, 4, 5, 4, 2],
    [4, 9, 12, 9, 4],
    [5, 12, 15, 12, 5],
    [4, 9, 12, 9, 4],
    [2, 4, 5, 4, 2]
    ])
    noyau_final = noyau / 159

    h,w = img_gray.shape
    img_floue = np.zeros((h,w))

    img_floue = cv2.filter2D(img_gray, cv2.CV_64F, noyau_final)


    '''
    for i in range(2, h-2):
        for j in range(2, w-2):
            zone = img_gray[i-2:i+3,j-2:j+3]
            resultat = np.sum(zone * noyau)
            img_floue[i-2, j-2] = resultat
        print(i)
    '''
    K = np.array([
        [-1, 0, 1],
        [-2, 0, 2],
        [-1, 0, 1]
    ])
    tK =np.array([
        [-1, -2, -1],
        [0, 0, 0],
        [1, 2, 1]
    ])

    Gx = cv2.filter2D(img_floue,cv2.CV_64F, K)
    Gy = cv2.filter2D(img_floue,cv2.CV_64F, tK)
    G = np.sqrt(Gx**2 + Gy**2)
    thetaDir = np.arctan2(Gy, Gx)
    angle = thetaDir * 180 / np.pi

    '''
    for lig in range(h) :
        for col in range(w) :
            print(lig)
            x = (angle[lig][col] + 22.5) % 180
            angle[lig][col] = 45 * (x//45)
    '''
    angle = ((angle + 22.5) % 180 // 45) * 45

    G_nms = NMS(G,angle)
    G = hysteresis(T, G_nms)
    img_floue = img_floue.astype("uint8")

    '''
    cv2.namedWindow("img", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("img", 756, 1008)
    cv2.namedWindow("img_floue", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("img_floue", 756, 1008)
    cv2.imshow("img_floue", G)
    cv2.imshow("img", img)
    
    cv2.waitKey(0)
    '''
    return G



# if __name__ == "__main__" :
#     cannyEdge(10,"exemple.jpg")