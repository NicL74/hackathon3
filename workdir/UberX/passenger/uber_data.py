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
'''''
locations = np.array([("airport", 1,6),     \
                      ("boating lake", 7,1),    \
                      ("city hall", 2,1),   \
                      ("downtown", 5, 6),   \
                      ("emergency room", 2, 8), \
                      ("fast food diner", 3, 5),    \
                      ("garage", 2, 2), \
                      ("hospital", 4, 6),   \
                      ("ice-rink", 4, 7),   \
                      ("jailhouse", 2, 4)])
'''
# Defined as "name", x-loc, y-loc (in range of 1 to 54 (x) and 1 to 36 (y))
locations = np.array([("airport", 3, 28),     \
                      ("boating lake", 39, 17),    \
                      ("city hall", 12, 10),   \
                      ("downtown", 18, 18),   \
                      ("emergency room", 48, 25), \
                      ("fast food diner", 49, 6),    \
                      ("garage", 12, 28), \
                      ("hospital", 36, 13),   \
                      ("ice-rink", 30, 7),   \
                      ("jailhouse", 30, 5)])

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
                       
blue = 14
green = 13

b = 14
g = 13


manhattan = np.array([ \
                       (b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b), \
                       (b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1), \
                       (b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,1, 5, 4, 9, 4, 4, 4, 4, 4, 9, 4, 9, 4, 9, 4, 9, 4, 9, 4, 9, 4, 9, 4, 9, 4, 9, 4, 4, 9, 4, 4, 4, 4, 4), \
                       (b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b, 1, 5, 4, 10, 13, 3, 13, 13, 13, 13, 13, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 1, 3, 1, 1, 1, 1, 1),    \
                       (b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b, 1, 5, 4, 10, 1, 3, 13, 3, 13, 13, 13, 13, 13, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 1, 12, 4, 4, 4, 4, 4),  \
                       (b,b,b,b,b,b,b,b,b,b,b,b,b, 1, 1, 5, 4, 10, 1, 3, 1, 3, 13, 3, 13, 13, 13, 13, 13, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 5, 7, 13, 13, 13, 13, 13),  \
                       (b,b,b,b,b,b,b,b,b,b, 1, 1, 1, 5, 4, 2, 4, 2, 4, 2, 4, 2, 4, 2, 4, 9, 4, 9, 4, 2, 4, 2, 4, 2, 4, 2, 4, 2, 4, 2, 4, 2, 4, 2, 4, 2, 4, 7, g,g,g,g,g,g),  \
                       (b,b,b,b,b,b,b,b, 1, 1, 1, 5, 4, 10, 1, 3, 5, 10, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, g,g,g,g,g,g,g,g),  \
                       (b,b,b,b,b, 1, 1, 1, 1, 5, 4, 10, 1, 3, 1, 12, 7, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, g,g,g,g,g,g, 1, 1),  \
                       (b,b,b, 1, 1, 5, 4, 9, 4, 2, 4, 2, 4, 2, 4, 2, 4, 2, 4, 2, 4, 2, 4, 2, 4, 2, 4, 2, 4, 2, 4, 2, 4, 2, 4, 11, 4, 2, 4, 2, 4, 2, 4, 2, 4, 2, 4, 9, 4, 9, 4, 9, 4, 4),  \
                       (b,b, 1, 1, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 5, 10, 1, 3, 1, 3, 1, 3, 5, 10, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 1, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 1), \
                       (b, 1, g,g, 1, 3, 1, 3, 1, 3, 1, 3, 1, 12, 7, 3, 1, 3, 1, 3, 1, 12, 7, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 1, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 1), \
                       (b, 1, g,g, 4, 2, 4, 2, 4, 2, 4, 2, 4, 2, 4, 2, 4, 2, 4, 2, 9, 2, 4, 2, 4, 11, 4, 11, 4, 2, 4, 11, 4, 11, 4, 9, 4, 11, 4, 11, 4, 2, 4, 11, 4, 2, 4, 10, 1, 3, 1, 3, 1, 1),  \
                       (b, 1, g,g, 1, 3, 1, 3, 1, 3, 1, 3, 5, 10, 1, 3, 1, 3, 1, 12, 7, 3, 1, 3, g,g,g,g,g, 3,g,g,g,g,g, 3,g,g,g,g,g, 3,g,g,g, 3,g, 3, 1, 3, 1, 3, 1, 1), \
                       (b,b,g,g,g, 3, 1, 3, 1, 3, 1, 12, 7, 3, 1, 3, 1, 3, 5, 10, 1, 3, 1, 3, g,g,g,g,g, 3,g,b,b,g,g, 3,g,g,g,g,g, 3,g,g, 5, 7, g, 12, 4, 11, 4, 10, 1, 1), \
                       (b,b,b,b, 1, 8, 4, 2, 4, 2, 4, 2, 4, 2, 4, 2, 4, 2, 11, 2, 4, 2, 4, 2, 4, 4, 4, 4, 4, 2, 6, g,g,g,g, 3, g,b,b,g,g, 3, g,g, 3, g,g, 3, g,g,g, 3, 1, 1), \
                       (b,b,b,b,b, 1, 1, 3, 1, 3, g, 3, 1, 3, 1, 3, 5, 10, 1, 3, 1, 3, 1, 3, g,g,g,g,g, 3, 8, 4, 4, 4, 4, 2, 4, 4, 4, 4, 4, 2, 4, 4, 7, g,g, 3, g,g,g,3, 1, 1),  \
                       (b,b,b,b,b, 1, 1, 3, 1, 3, g, 3, 1, 3, 1, 12, 7, 3, 1, 3, 1, 3, 1, 3, g,g,g,g,g, 3, g,g,g,g,g, 3, g,g,g,g,g, 3, g,g,g,g,g, 3, g,g,g, 3, 1, 1),  \
                       (b,b,b,b,b,b, 1, 12, 4, 2, 4, 2, 4, 2, 4, 2, 4, 2, 4, 2, 4, 2, 4, 2, 4, 9, 4, 9, 4, 2, 4, 9, 4, 9, 4, 2, 4, 9, 4, 9, 4, 2, 4, 9, 4, 9, 4, 2, 4, 4, 4, 2, 4, 4),  \
                       (b,b,b,b,b,b, 1, 12, 6, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 1, 1, 3, 1, 1), \
                       (b,b,b,b,b,b,b, 3, 8, 10, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 1, 1, 3, 1, 1),  \
                       (b,b,b,b,b,b,b, 8, 9, 11, 9, 2, 4, 2, 4, 2, 4, 2, 4, 2, 4, 2, 4, 2, 4, 2, 4, 2, 4, 2, 4, 2, 4, 2, 4, 2, 4, 2, 4, 2, 4, 2, 4, 2, 4, 2, 4, 2, 4, 4, 4, 10, 1, 1),  \
                       (b,b,b,b,b,b,b, 1, 3, 1, 8, 10, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 1, 1, 3, 1, 1), \
                       (b,b,b,b,b,b,b,b, 8, 6, 1, 8, 6, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 1, 1, 3, 1, 1), \
                       (b,b, 1, 1, b,b,b,b, 1, 12, 4, 4, 11, 2, 4, 2, 4, 2, 4, 2, 4, 2, 4, 2, 4, 2, 4, 2, 4, 2, 4, 2, 4, 2, 4, 2, 4, 2, 4, 2, 4, 2, 4, 2, 4, 2, 4, 2, 4, 4, 4, 10, 1, 1), \
                       (1, 1, 1, 1, 1, b,b,b, 1, 12, 6, 1, 1, 12, 6, 3, 1, 3, 1, 3, g, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 1, 1, 3, 1, 1), \
                       (1, 1, 1, 1, 1, 1, b,b,b, 3, 8, 6, 1, 3, 8, 10, 1, 3, 1, 3, g, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 1, 1, 3, 1, 1), \
                       (1, 1, 4, 4, 4, 4, 4, 4, 4, 11, 4, 11, 9, 11, 4, 2, 4, 2, 4, 2, 4, 2, 4, 11, 4, 11, 4, 11, 4, 11, 4, 2, 4, 11, 4, 11, 4, 11, 4, 11, 4, 11, 4, 11, 4, 11, 4, 11, 4, 4, 4, 11, 4, 4), \
                       (1, 1, g,g, 1, 1, 1, b,b, 1, 1, 1, 3, 1, 1, 3, 1, 3, 1, 3, 1, 3, 1, 1, 1, 1, 1, b,b,b,b, 3, b,b,b,b,b, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1), \
                       (1, 1, g,g, 1, 1, 1, b,b,b, 1, 1, 8, 4, 4, 11, 4, 11, 4, 11, 4, 7, 1, 1, b,b,b,b,b,b,b, 3, b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b, 1, 1, 1, 1, 1, 1), \
                       (1, 1, 1, 1, 1, 1, 1, 1, b,b,b, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, b,b,b,b,b,b,b,b,b, 3, b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b), \
                       (1, 1, 1, 1, 1, 1, 1, 1, b,b,b,b, 1, 1, 1, 1, 1, 1, 1, b,b,b,b,b,b,b,b,b,b,b,b, 3, b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,), \
                       (1, 1, 1, 1, 1, 1, 1, 1, b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,), \
                       (1, 1, 1, 1, 1, 1, 1, 1, 1, b,b,b,b,b,b,b,b,b,b,b,b,b,b, 1, 1, 1, 1, 1, 1, 1, 1, 3, g,g, 1, 1, 1, 1, 1, 1, 1, 1, 1, b,b,b,b,b,b,b,b,b,b,b), \
                       (1, 1, 1, 1, 1, 1, 1, 1, 1, b,b,b,b,b,b,b,b,b,b,b,b, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, g,g, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, b,b,b,b,b,b), \
                       (1, 1, 1, 1, 1, 1, 1, 1, 1, b,b,b,b,b,b,b,b,b,b, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, b,b,b)])
                       
'''                       
    
manhattan = np.array([ \
                       (blue*np.ones((1,54))), \
                       (np.hstack((blue*np.ones((1,23)), np.ones((1,31)))))])
                       #(np.hstack((blue*np.ones((1,20)), np.array((1, 2, 3)))))])
                       
                       #

                       #(np.hstack((blue*np.ones((1,20)), ([1,2, 3]))))]) #[1, 5, 4, 9, 4, 4, 4, 4, 4, 9, 4, 9, 4, 9, 4, 9, 4, 9, 4, 9, 4, 9, 4, 9, 4, 9, 4, 4, 9, 4, 4, 4, 4, 4])))])
                       #, \
                       (blue*np.ones((1,18)), 1, 5, 4, 10, 13, 3, 13, 13, 13, 13, 13, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 1, 3, 1, 1, 1, 1, 1), \
                       (blue*np.ones((1,16)), 1, 5, 4, 10, 1, 3, 13, 3, 13, 13, 13, 13, 13, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 1, 12, 4, 4, 4, 4, 4), \
                       (blue*np.ones((1,13)), 1, 1, 5, 4, 10, 1, 3, 1, 3, 13, 3, 13, 13, 13, 13, 13, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 5, 7, 13, 13, 13, 13, 13), \
                       (blue*np.ones((1,10)), 1, 1, 1, 5, (np.kron((np.ones((1,5)),[4, 2]))), 4, 9, 4, 9, 4, (np.kron(np.ones((1,8)),[2, 4])), 2, 4, 7, green*np.ones((1,6))), \
                       (blue*np.ones((1,8)), 1, 1, 1, 5, 4, 10, 1, 3, 5, 10, (np.kron(np.ones((1,14)),[1, 3])), green*np.ones((1,8))), \
                       (blue*np.ones((1,5)), 1, 1, 1, 1, 5, 4, 10, 1, 3, 1, 12, 7, 3, (np.kron(np.ones((1,14)),[1, 3])), green*np.ones((1,6)), 1, 1), \
                       (blue*np.ones((1,3)), 1, 1, 5, 4, 9, np.kron(np.ones((1,13)),[4, 2]), 4, 11, 4, (np.kron(np.ones((1,5)),[2, 4])), 9, 4, 9, 4, 9, 4, 4), \
                       (blue*np.ones((1,2)), 1, 1, 1, np.kron(np.ones((1,4)),[3, 1]), 3, 5, 10, 1, 3, 1, 3, 1, 3, 5, 10, np.kron(np.ones((1,5)),[1, 3]), 1, 1, 1, np.kron(np.ones((1,8)),[3, 1]), 1), \
                       (blue, 1, green, green, np.kron(np.ones((1,4)),[1, 3]), 1, 12, 7, 3, 1, 3, 1, 3, 1, 12, 7, 3, np.kron(np.ones((1,5)),[1, 3]), 1, 1, 1, np.kron(np.ones((1,8)),[3, 1]), 1), \
                       (blue, 1, green, green, np.kron(np.ones((1,8)),[4, 2]), 9, 2, 4, 2, 4, 11, 4, 11, 4, 2, 4, 11, 4, 11, 4, 9, 4, 11, 4, 11, 4, 2, 4, 11, 4, 2, 4, 10, 1, 3, 1, 3, 1, 1), \
                       (blue, 1, green, green, np.kron(np.ones((1,4)),[1, 3]), 5, 10, 1, 3, 1, 3, 1, 12, 7, 3, 1, 3, np.kron(np.ones((1,3)),[green*np.ones((1,5)), 3]), green*np.ones((1,3)), 3, green, np.kron(np.ones((1,3)),[3, 1]), 1), \
                       (blue*np.ones((1,2)), green*np.ones((1,3)), np.kron(np.ones((1,3)),[3, 1]), 12, 7, 3, 1, 3, 1, 3, 5, 10, 1, 3, 1, 3, np.kron(np.ones((1,3)),[green*np.ones((1,5)), 3]), green, green, 5, 7, green, 12, 4, 11, 4, 10, 1, 1), \
                       (blue*np.ones((1,4)), 1, 8, np.kron(np.ones((1,6)),[4, 2]), 11, 2, 4, 2, 4, 2, 4*np.ones((1,5)), 2, 6, green*np.ones((1,4)), 3, green*np.ones((1,5)), 3, green, green, 3, green, green, 3, green, green, green, 3, 1, 1), \
                       (blue*np.ones((1,5)), 1, 1, 3, 1, 3, green, 3, 1, 3, 1, 3, 5, 10, 1, 3, 1, 3, 1, 3, green*np.ones((1,5)), 3, 8, 4, 4, 4, 4, 2, 4, 4, 4, 4, 4, 2, 4, 4, 7, green, green, 3, green, green, green, 3, 1, 1),  \
                       (blue*np.ones((1,5)), 1, 1, 3, 1, 3, green, 3, 1, 3, 1, 12, 7, 3, 1, 3, 1, 3, 1, 3, np.kron(np.ones((1,4)),[green*np.ones((1,5)), 3]), green*np.ones((1,3)), 3, 1, 1), \
                       (blue*np.ones((1,6)), 1, 12, 4, 2, 4, 2, 4, 2, 4, 2, 4, 2, 4, 2, 4, 2, 4, 2, np.kron(np.ones((1,4)),[4, 9, 4, 9, 4, 2]), 4, 4, 4, 2, 4, 4), \
                       (blue*np.ones((1,6)), 1, 12, 6, 3, np.kron(np.ones((1,19)),[1, 3]), 1, 1, 1, 3, 1, 1), \
                       (blue*np.ones((1,7)), 3, 8, 10, np.kron(np.ones((1,19)),[1, 3]), 1, 1, 1, 3, 1, 1), \
                       (blue*np.ones((1,7)), 8, 9, 11, 9, np.kron(np.ones((1,19)),[2, 4]), 4, 4, 10, 1, 1), \
                       (blue*np.ones((1,7)), 1, 3, 1, 8, 10, np.kron(np.ones((1,18)),[1, 3]), 1, 1, 1, 3, 1, 1), \
                       (blue*np.ones((1,8)), 8, 6, 1, 8, 6, np.kron(np.ones((1,17)),[3, 1]), 3, 1, 1, 1, 3, 1, 1), \
                       (blue*np.ones((1,2)), 1, 1, blue*np.ones((1,4)), 1, 12, 4, 4, 11, 2, np.kron(np.ones((1,17)),[4, 2]), 4, 4, 4, 10, 1, 1),
                       (np.ones((1,5)), blue*np.ones((1,3)), 1, 12, 6, 1, 1, 12, 6, 3, 1, 3, 1, 3, green, np.kron(np.ones((1,13)),[3, 1]), 3, 1, 1, 1, 3, 1, 1), \
                       (np.ones((1,6)), blue*np.ones((1,3)), 3, 8, 6, 1, 3, 8, 10, 1, 3, 1, 3, green, np.kron(np.ones((1,13)),[3, 1]), 3, 1, 1, 1, 3, 1, 1), \
                       (1, 1, 4*np.ones((1,7)), 11, 4, 11, 9, 11, 4, 2, 4, 2, 4, 2, 4, 2, np.kron(np.ones((1,4)),[4, 11]), 4, 2, np.kron(np.ones((1,8)),[4, 11]), 4, 4, 4, 11, 4, 4), \
                       (1, 1, green, green, 1, 1, 1, blue, blue, 1, 1, 1, 3, 1, 1, 3, 1, 3, 1, 3, 1, 3, 1, 1, 1, 1, 1, blue*np.ones((1,4)), 3, blue*np.ones((1,5)), np.ones((1,17))), \
                       (1, 1, green, green, 1, 1, 1, blue*np.ones((1,3)), 1, 1, 8, 4, 4, 11, 4, 11, 4, 11, 4, 7, 1, 1, blue*np.ones((1,7)), 3, blue*np.ones((1,16)), np.ones((1,6))), \
                       (np.ones((1,8)), blue*np.ones((1,3)), np.ones((1,11)), blue*np.ones((1,9)), 3, blue*np.ones((1,22))), \
                       (np.ones((1,8)), blue*np.ones((1,4)), np.ones((1,7)), blue*np.ones((1,12)), 3, blue*np.ones((1,22))), \
                       (np.ones((1,8)), blue*np.ones((1,18)), np.ones((1,5)), 3, np.ones((1,4)), blue*np.ones((1,18))), \
                       (np.ones((1,9)), blue*np.ones((1,14)), np.ones((1,8)), 3, green, green, np.ones((1,9)), blue*np.ones((1,11))), \
                       (np.ones((1,9)), blue*np.ones((1,12)), np.ones((1,10)), 3, green, green, np.ones((1,14)), blue*np.ones((1,6))), \
                       (np.ones((1,9)), blue*np.ones((1,10)), np.ones((1,32)), blue*np.ones((1,3)))])
'''
                       
#print(manhattan)
                       


