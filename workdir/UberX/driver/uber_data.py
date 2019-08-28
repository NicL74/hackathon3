import numpy as np

# Data for uber sims

# Define map to be used
# Each element represents a block type
block_map_array = np.array([(5,4,4,4,6,5,4,6),   \
                   (8,6,5,6,8,2,4,10),  \
                   (5,7,3,3,5,7,5,10),  \
                   (8,4,10,3,3,5,10,3),  \
                   (5,6,3,12,2,2,10,3),  \
                   (3,12,11,7,3,3,12,10),  \
                   (3,3,5,4,2,2,7,3),  \
                   (8,11,11,4,7,8,4,7)])


# Defined as "name", x-loc, y-loc (in range of 1 to 8)
locations = np.array([("airport", 1,6),     \
                      ("boating lake", 7,1),    \
                      ("city hall", 2,1),   \
                      ("downtown", 5, 6),   \
                      ("emergency room", 2, 8), \
                      ("fast food diner", 3, 5),    \
                      ("garage", 6, 6), \
                      ("hospital", 4, 6),   \
                      ("ice-rink", 4, 7),   \
                      ("jailhouse", 2, 4)])

# Define list of passengers
# format: <name> <profile>
passengers = np.array([(1, "Angela", "budget"), \
                       (2, "Bill", "budget"),   \
                       (3, "Cathy", "leisure"),   \
                       (4, "David", "leisure"),   \
                       (5, "Eleanor", "leisure"),   \
                       (6, "Frank", "leisure"),   \
                       (7, "Gisella", "business"),   \
                       (8, "Harry", "business")])


