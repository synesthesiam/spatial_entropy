spatial\_entropy
================

Computes an entropy profile for an image using moving averages. Inspired by [this StackExchange thread](http://stats.stackexchange.com/questions/17109/measuring-entropy-information-patterns-of-a-2d-binary-matrix).

Description
-----------

The program computes the entropy of a 2D image using moving averages at various window sizes. This produces a "profile" for the image that can be used to rank images by complexity. More complex images have consistently higher entropies over a range of window sizes.

Examples
--------

Consider the following matrices:

<table>
<tr>
<td><strong>A1</strong></td>
<td><strong>A2</strong></td>
</tr>
<tr>
<td>
<img src="https://raw.github.com/synesthesiam/spatial_entropy/master/etc/a1.jpg" />
</td>
<td>
<img src="https://raw.github.com/synesthesiam/spatial_entropy/master/etc/a2.jpg" />
</td>
</tr>
<tr>
<td><strong>A3</strong></td>
<td><strong>A4</strong></td>
</tr>
<tr>
<td>
<img src="https://raw.github.com/synesthesiam/spatial_entropy/master/etc/a3.jpg" />
</td>
<td>
<img src="https://raw.github.com/synesthesiam/spatial_entropy/master/etc/a4.jpg" />
</td>
</tr>
</table>

Print the entropy profiles of the binary matrices (stored in text files) for all window sizes:

    python spatial_entropy.py etc/*.txt --matrix --profile
    # Using size = 4
    # image entropy size
    "etc/a1.txt" 0.970950594455 1
    "etc/a1.txt" 0.988699408288 2
    "etc/a1.txt" 0.918295834054 3
    "etc/a1.txt" 1.5 4
    "etc/a2.txt" 0.998845535995 1
    "etc/a2.txt" 2.12661447181 2
    "etc/a2.txt" 1.53049305676 3
    "etc/a2.txt" 0.811278124459 4
    "etc/a3.txt" 0.942683189255 1
    "etc/a3.txt" 1.5 2
    "etc/a3.txt" 1.39214722366 3
    "etc/a3.txt" -0 4
    "etc/a4.txt" 0.998845535995 1
    "etc/a4.txt" -0 2
    "etc/a4.txt" 0.991076059838 3
    "etc/a4.txt" -0 4
    "etc/a5.txt" 0.970950594455 1
    "etc/a5.txt" 1.0 2
    "etc/a5.txt" 0.918295834054 3
    "etc/a5.txt" -0 4

Plot the profiles of the binary matrices:

    $ python spatial_entropy.py etc/*.txt --plot profile-matrices.png --matrix

![profile-matrices.png](https://raw.github.com/synesthesiam/spatial_entropy/master/profile-matrices.png)

Plot the profiles of actual image files using a maximum window size of 10:

    $ python spatial_entropy.py etc/*.jpg --plot profile-images.png --size 10 --legend "upper left"

![profile-images.png](https://raw.github.com/synesthesiam/spatial_entropy/master/profile-images.png)
