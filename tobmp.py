import cv2
import numpy as np

# https://github.com/SamratSahoo/UT-Arlington-Research/blob/master/Week%206%20-%20Convolutions%20%26%20Wavelet%20Transforms/Convolutions.py
def convolve2D(image, kernel, padding=0, strides=1):
    # Cross Correlation
    kernel = np.flipud(np.fliplr(kernel))

    # Gather Shapes of Kernel + Image + Padding
    xKernShape = kernel.shape[0]
    yKernShape = kernel.shape[1]
    xImgShape = image.shape[0]
    yImgShape = image.shape[1]

    # Shape of Output Convolution
    xOutput = int(((xImgShape - xKernShape + 2 * padding) / strides) + 1)
    yOutput = int(((yImgShape - yKernShape + 2 * padding) / strides) + 1)
    output = np.zeros((xOutput, yOutput))

    # Apply Equal Padding to All Sides
    if padding != 0:
        imagePadded = np.zeros((image.shape[0] + padding*2, image.shape[1] + padding*2))
        imagePadded[int(padding):int(-1 * padding), int(padding):int(-1 * padding)] = image
        # print(imagePadded)
    else:
        imagePadded = image

    # Iterate through image
    for y in range(image.shape[1]):
        # Exit Convolution
        if y > image.shape[1] - yKernShape:
            break
        # Only Convolve if y has gone down by the specified Strides
        if y % strides == 0:
            for x in range(image.shape[0]):
                # Go to next row once kernel is out of bounds
                if x > image.shape[0] - xKernShape:
                    break
                try:
                    # Only Convolve if x has moved by the specified Strides
                    if x % strides == 0:
                        output[x, y] = (kernel * imagePadded[x: x + xKernShape, y: y + yKernShape]).sum()
                except:
                    break

    return output

def add_noise(img, n):
    img2 = img
    for _ in range(n):
        x = int(np.random.random() * img.shape[0])
        y = int(np.random.random() * img.shape[1])
        img2[x, y] = 255 # white in gray scale is 255
    return img2

if __name__ == '__main__':
    # Input original image file
    # To use another image input file, please change the filename
    # Also the downloaded 'standard_test_images/' should be in the same folder
    filename='woman_darkhair'
    img = cv2.imread(f'./standard_test_images/{filename}.tif')
    # Write out original image in bmp format
    cv2.imwrite(f'./{filename}.bmp', img)

    # Add white noise points and write out another bmp file
    noise_img = add_noise(img, 100)
    cv2.imwrite(f'./{filename}_noise.bmp', noise_img)

    # Convert to grayscale image
    image = cv2.cvtColor(src=img, code=cv2.COLOR_BGR2GRAY)

    # Gaussian blur Kernel 5x5
    kernel = np.array([[1, 4, 7, 4, 1], [4, 16, 26, 16, 4], [7, 26, 41, 26, 7], [4, 16, 26, 16, 4], [1, 4, 7, 4, 1]])
    kernel_scale= kernel/273
    # Convolve and Save Output
    output = convolve2D(image, kernel_scale, padding=2)
    # cv2.imwrite(f'{filename}_noise_gaussian.bmp', output)