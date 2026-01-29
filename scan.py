import cv2
import canny as cny

wc = cv2.VideoCapture(0)

while True:
    ret, frame = wc.read()
    if not ret:
        break


    edges = cny.cannyEdge(0.08,frame)


    cv2.namedWindow("Contours Canny", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Contours Canny", 1080, 720)
    cv2.imshow('Contours Canny', edges)

    # Quitter avec la touche 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

wc.release()
cv2.destroyAllWindows()