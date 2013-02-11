#!/usr/bin/python

# Copyright (C) 2013 Michael Hansen (mihansen@indiana.edu)

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import numpy as np, argparse
from operator import itemgetter
from scipy import ndimage
from PIL import Image

def shannon_entropy(array):
  """Computes the base 2 Shannon entropy of array"""
  array = array.flatten()
  bins = np.unique(array)
  counts = np.bincount(np.digitize(array, bins) - 1)
  total_counts = np.sum(counts)
  probs = counts / float(total_counts)

  return -np.sum(probs * np.log2(probs))

def norm(array):
  """Returns a normalized version of array"""
  return array / np.amax(array)

def moving_average(array, size):
  """Computes the moving average of a 2d array using a size x size neighborhood around each pixel."""
  assert array.ndim > 1
  assert size > 0
  assert size <= min(array.shape[0], array.shape[1])

  # Result is centered in the matrix, with a preference for upper-left on
  # odd-numbered dimensions.
  slice_left = int(size - 1) / 2
  slice_right = -(int(size) / 2)

  # Average over cell neighbors
  filter_size = np.copy(array.shape)
  filter_size[0] = size
  filter_size[1] = size
  result = ndimage.filters.convolve(array, np.ones(shape=filter_size), mode="mirror")

  # Slice out result (centered)
  if slice_right == 0:
    result = result[slice_left:, slice_left:]
  else:
    result = result[slice_left:slice_right, slice_left:slice_right]

  # Normalize
  return norm(result)

def entropy_profile(array, sizes):
  """Returns the entropy of the moving average of array of all given sizes."""
  return [shannon_entropy(moving_average(array, s)) for s in sizes]

def plot_profiles(arrays, names, max_size, legend_loc="upper right"):
  """Returns a Matplotlib figure with the plotted entropy profiles of arrays for sizes [1..max_size]."""

  # Avoid loading MPL unless we're plotting
  from matplotlib import pyplot as mpl 

  fig = mpl.figure()

  sizes = range(1, max_size + 1)
  profiles = [entropy_profile(a, sizes) for a in arrays]
  
  for (profile, name) in zip(profiles, names):
    mpl.plot(sizes, profile, "o-", label=name)

  mpl.xlabel("Window size")
  mpl.ylabel("Entropy")
  mpl.title("Array entropies for different window sizes")
  mpl.legend(loc=legend_loc)
  mpl.grid()

  mpl.xticks(sizes)

  return fig

def rank_arrays(arrays, indices, size):
  """Ranks arrays by descending entropy, starting at size. 
  If entropies are equal, arrays are ordered by entropies at size - 1 (down to size 1 at a minimum).
  Returns an ordered list of tuples of the form:
    (array, entropy, size)
  where entropy has been computed for the array at size.

  NOTE: arrays are not necessarily in absolute descending entropy order.
  Arrays with the same entropy at higher size are ordered according to their entropies at the next size down.
  """
  assert size > 0

  # Compute entropy profiles for all sizes from 1 to max_size
  profiles = np.array([entropy_profile(a, [size]) for a in arrays]).flatten()

  # Rank tentatively by entropy
  tentative_rank = sorted(zip(profiles, indices), key=itemgetter(0), reverse=True)

  if size == 1:
    return [(r[1], r[0], size) for r in tentative_rank]

  final_rank = []
  cur_equiv_list = []

  last_entropy = None
  for (entropy, index) in tentative_rank:
    if entropy != last_entropy:
      if len(cur_equiv_list) > 0:
        final_rank = final_rank + rank_arrays([arrays[i] for i in cur_equiv_list], cur_equiv_list, size - 1)
        cur_equiv_list = []

      final_rank.append((index, entropy, size))
      last_entropy = entropy
    else:
      last_index = final_rank.pop()[0]
      cur_equiv_list = cur_equiv_list + [last_index, index]

  if len(cur_equiv_list) > 0:
    final_rank = final_rank + rank_arrays([arrays[i] for i in cur_equiv_list], cur_equiv_list, size - 1)

  return final_rank

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Computes spatial proximity entropy")
    parser.add_argument("files", metavar="image", type=str, nargs="+",
                        help="path to grayscale image file")

    parser.add_argument("--size", type=int, default=0,
                        help="maximum size of window in moving average (default: no maximum)") 

    parser.add_argument("--rank", action="store_true",
                       help="rank the images by entropy and print out the details") 

    parser.add_argument("--plot", type=str, default="",
                       help="write entropy profile plot of images to the given path") 

    parser.add_argument("--legend", type=str, default="upper right",
                        help="location of legend in plot (default: upper right)") 

    parser.add_argument("--profile", action="store_true",
                       help="print entropy profiles for all images and window sizes up to --size (inclusive)") 

    parser.add_argument("--matrix", action="store_true",
                       help="interpret images as NumPy matrices stored in text files") 

    args = parser.parse_args()

    files = list(args.files)
    images = []

    if args.matrix:
      images = [np.loadtxt(f) for f in files]
    else:
      images = [np.array(Image.open(f)) for f in files]

    if args.size < 1:
      args.size = min([max(img.shape[0], img.shape[1]) for img in images]) - 1
      print "# Using size =", args.size

    if len(args.plot) > 0:
      fig = plot_profiles(images, files, args.size, legend_loc=args.legend)
      fig.savefig(args.plot)
      print "# Wrote", args.plot

    if args.rank:
      rank = rank_arrays(images, range(len(images)), args.size)

      print "# image entropy size"
      for r in rank:
        print "\"{0}\"".format(files[r[0]]), str.join(" ", [str(x) for x in r[1:]])

    if args.profile:
      sizes = range(1, args.size + 1)
      profiles = [entropy_profile(img, sizes) for img in images]

      print "# image entropy size"
      for (f, p) in zip(files, profiles):
        for (size, entropy) in zip(sizes, p):
          print "\"{0}\"".format(f), entropy, size

