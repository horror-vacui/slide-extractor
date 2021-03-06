import numpy as np
import cv2


class DuplicateHandler:
    entries = []
    n2compare = -5  # lets just compare the last 5 slides

    def __init__(self, thresh):
        self.threshold = thresh

    def check(self, img, add=True):
        # zti 20200805
        # it compares the image to every previous image
        # This way the updated contents/agenda slides will be removed
        # The same slide with different highlights are used in these
        for i in self.entries[self.n2compare:]: 
            d = self.calcDiff(i, img) # zti: for debugging
            # print(f"The difference btw images is: {d}")
            if d < self.threshold:
                return False

        if add:
            self.entries.append(img)

        return True

    def calcDiff(self, img1, img2):
        # convert images to grayscale if needed
        if len(img1.shape) > 2:
            img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        if len(img2.shape) > 2:
            img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

        # bring the two images to the same size
        if img1.shape[0] > img2.shape[0] or img1.shape[1] > img2.shape[1]:
            img1 = img1[0: img2.shape[0], 0: img2.shape[1]]
        elif img2.shape[0] > img1.shape[0] or img2.shape[1] > img1.shape[1]:
            img2 = img2[0: img1.shape[0], 0: img1.shape[1]]

        img1 = cv2.GaussianBlur(img1, (11, 11), 0)
        img2 = cv2.GaussianBlur(img2, (11, 11), 0)

        diff = cv2.absdiff(img1, img2)
        diff = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)[1]

        diff = diff.astype(np.uint8)
        # alternatively: (np.sum(diff) / (diff.size * 255)) * 100
        percent = (np.count_nonzero(diff) / diff.size) * 100

        return percent
