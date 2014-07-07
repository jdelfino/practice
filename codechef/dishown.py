import fileinput
import time

class Chef(object):
    def __init__(self, x, score, dishes):
        self.id = x
        self.score = score
        self.dishes = dishes

    def __str__(self):
        return "[Chef %d, s: %d, dishes: %s]" % (self.id, self.score, self.dishes)

def main():
    tic = time.time()
    fi = fileinput.input()

    ntests = int(fi.readline())

    for _ in range(ntests):
        nchefs = int(fi.readline())
        scores = [int(x) for x in fi.readline().strip().split(" ")]
        # dish -> c#, best dish, list of dishes
        chefs = [Chef(x, scores[x], [x]) for x in range(nchefs)]
        dish_to_chef = dict((x, chefs[x]) for x in range(nchefs))
        #chef_to_best_dish = dict((x,scores[x]) for x in range(nchefs))

        nq = int(fi.readline())
        for _ in range(nq):
            query = [int(x)-1 for x in fi.readline().strip().split(" ")]
            #print query
            if len(query) == 3:
                _, d1, d2 = query
                #print "Dish %s vs Dish %s" % (d1,d2)
                c1 = dish_to_chef[d1]
                c2 = dish_to_chef[d2]
                if c1.id == c2.id:
                    #print "Invalid query!"
                    continue

                if c1.score > c2.score:
                    #print "%s beat %s" % (c1, c2)
                    for x in c2.dishes:
                        dish_to_chef[x] = c1

                    c1.dishes.extend(c2.dishes)
                    c2.dishes = []

                elif c2.score > c1.score:
                    #print "%s beat %s" % (c2, c1)
                    for x in c1.dishes:
                        dish_to_chef[x] = c2

                    c2.dishes.extend(c1.dishes)
                    c1.dishes = []
                    dish_to_chef[d1] = c2

            elif len(query) == 2:
                _, dish = query
                #print "Dish %s belongs to:" % dish
                print dish_to_chef[dish].id+1


    print time.time() - tic

if __name__ == '__main__':
    main()