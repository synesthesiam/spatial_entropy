spatial\_entropy
================

Computes an entropy profile for an image using moving averages.

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

Plot the profiles of the binary matrices stored in text files:

    $ python spatial_entropy.py etc/*.txt --plot profile-matrices.png --matrix

![profile-matrices.png](https://raw.github.com/synesthesiam/spatial_entropy/master/profile-matrices.png)

Plot the profiles of actual image files using a maximum window size of 10:

    $ python spatial_entropy.py etc/*.jpg --plot profile-images.png --size 10 --legend "upper left"

![profile-images.png](https://raw.github.com/synesthesiam/spatial_entropy/master/profile-images.png)
