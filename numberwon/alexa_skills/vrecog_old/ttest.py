import random
import matplotlib.pyplot as plt

import lbg

NUM_AREAS = 8
NUM_POINTS_PER_AREA = 10
SIZE_CODEBOOK = 8
AREA_MIN_MAX = ((-20, 20), (-20, 20))

random.seed(0)

# create random centroids for NUM_AREAS areas
area_centroids = [(random.uniform(*AREA_MIN_MAX[0]), random.uniform(*AREA_MIN_MAX[1]))
                  for _ in range(NUM_AREAS)]

# display random centroids as orange cicles
plt.scatter([p[0] for p in area_centroids], [p[1] for p in area_centroids], marker='o', color='orange')

# create whole population
population = []
for c in area_centroids:
    # create random points around the centroid c
    area_points = [(random.gauss(c[0], 1.0), random.gauss(c[1], 1.0)) for _ in range(NUM_POINTS_PER_AREA)]
    population.extend(area_points)

# display the population as blue crosses
plt.scatter([p[0] for p in population], [p[1] for p in population], marker='x', color='blue')

# generate codebook
%time cb, cb_abs_w, cb_rel_w = lbg.generate_codebook(population, SIZE_CODEBOOK)

# display codebook as red filled circles
# codevectors with higher weight (more points near them) get bigger radius
plt.scatter([p[0] for p in cb], [p[1] for p in cb], s=[((w+1) ** 5) * 40 for w in cb_rel_w], marker='o', color='red')

plt.show()
