from scipy import ndimage
from scipy import datasets
import matplotlib
matplotlib.use('TkAgg')
import pylab as pl
ascent = datasets.ascent()

shifted_ascent = ndimage.shift(ascent, (50, 50))
shifted_ascent2 = ndimage.shift(ascent, (50, 50), mode="nearest")
rotated_ascent = ndimage.rotate(ascent, 30)

pl.subplot(2, 2, 1)
pl.imshow(ascent, cmap=pl.cm.gray)
pl.subplot(2, 2, 2)
pl.imshow(shifted_ascent, cmap=pl.cm.gray)
pl.subplot(2, 2, 3)
pl.imshow(shifted_ascent2, cmap=pl.cm.gray)
pl.subplot(2, 2, 4)
pl.imshow(rotated_ascent, cmap=pl.cm.gray)
pl.show()
