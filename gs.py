"""
Genetic server for postgresql configuration genetic thingie
Includes only performance related options - to keep it simple

(c) Greg Jaskiewicz 2013

Licenced under PostgreSQL BSD Licence

TODO:
* split generic stuff into separate agnostic class
* store results and so on in database maybe (sqllite would do)
* save/restore of state ?
* separate configuration file
* improve perhaps the way new generation is generated. Current one isn't perhaps the greatest - but still not bad
* we don't have a goal to reach here. It just keeps on going. So perhaps make that an option?
"""

from postgres_config import PostgresConfig
import copy
import subprocess
import os

# Bad, bad globals
population_size = 24
current_population = []
new_pg_config = "/tmp/new_pg_config.conf"


def generate_initial_population(the_population_size):
    newpopulation = []
    while the_population_size > 0:
        the_population_size = the_population_size - 1
        p = PostgresConfig()
        # maybe use some less random methods to generate different PostgreSQL configurations
        p.set_random()
        newpopulation.append(p)

    return newpopulation


def run_test(g):
    # g.result = 10.0
    # return 10.0

    g.print_out()
    """run the test 3 times, avg out the results """
    results = []
    for _ in range(3):
        output1 = subprocess.Popen(["./run_a_test.sh"], stdout=subprocess.PIPE).communicate()[0]
        if (len(output1)):
            results.append(int(output1))

    if (len(results)):
        g.result = sum(results) / float(len(results))
    else:
        g.result = 0

    print g.result


def test_population(the_test_population):
    for guy in the_test_population:
        reload_postgresql_for(guy)
        run_test(guy)


def reload_postgresql_for(guy):
    try:
        os.remove(new_pg_config)
    except:
        """foo"""
    finally:
        """dont care if didn't exist"""
    guy.print_out_to_file(new_pg_config)

    subprocess.call(["./reload_postgresql_with_new_config.sh", new_pg_config])


def eliminate_weakests(the_test_population):
    """ order by score, remove half """
    # remove ones with result equal 0
    for guy in the_test_population:
        if guy.result < 1:
            the_test_population.remove(guy)

    the_test_population = sorted(the_test_population, key=lambda guy: guy.result)
    the_test_population.reverse()
    for guy in the_test_population:
        print guy.result
    print '\n'
    """
       maybe use average as cut off point ?
       but then, what about new generation when there's not enough parents ?
       We could also use historical median/average as a cut off point. But this might be bit
       problematic
    """
    the_test_population = the_test_population[0:population_size / 2]

    return the_test_population


def mutate_new_population(parent_population):
    """
    take what's there, and mate them until you get at most population_size
    """
    new_population = []
    for x in range(len(parent_population)):
        for y in range(x):
            if (x == y):
                continue    # need two different mates!
            newguy = copy.deepcopy(parent_population[x])
            newguy.cross_over(parent_population[y])
            newguy.mutate_random(5, 3)
            newguy.result = 0
            new_population.append(newguy)
            if len(new_population) == population_size:
                return new_population
    return new_population


def dump_population(x, population):
    file_name = 'population_' + str(x) + '.ppldump'
    f = open(file_name, 'w')

    for guy in population:
        config = guy.get_config()
        print >> f, config
        print >> f, 'score = ' + str(guy.result)
        print >> f, '\n'

    f.close()


def main():
    current_population = generate_initial_population(population_size)

    print 'foo1'

    for i in range(1000):
        print '\n===============\nNew Population %d, %d members\n===============\n' % (i, len(current_population))

        """
        dump this population, before it is run, it will eventually get overriden with the one with results
        """
        dump_population(i, current_population)

        test_population(current_population)
        dump_population(i, current_population)

        living_population = eliminate_weakests(current_population)
        current_population = mutate_new_population(living_population)

    for guy in current_population:
        guy.print_out()

if __name__ == '__main__':
    main()
