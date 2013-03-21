from postgres_config import PostgresConfig
import random
import copy
import shlex, subprocess


population_size=10
current_population = []

def generate_initial_population(the_population_size):
  newpopulation = []
  while the_population_size>=0:
    the_population_size = the_population_size-1
    p = PostgresConfig()
    p.set_random()
    newpopulation.append(p)

  return newpopulation

def run_test(g):
  """run the test 3 times, avg out the results """
  results=[]
  for x in range(1):
    output1 = subprocess.Popen(["./run_a_test.sh"], stdout=subprocess.PIPE).communicate()[0]
    results.append(int(output1))

  if (len(results)):
    g.result = sum(results) / float(len(results))
  else:
    g.result = 0

  print g.result


def test_population(the_test_population):
  for guy in the_test_population:
    run_test(guy)


def eliminate_weakests(the_test_population):
  """ order by score, remove half """
  the_test_population = sorted(the_test_population, key=lambda guy: guy.result)
  the_test_population = the_test_population[0:population_size/2]
  #remove ones with result equal 0
  for guy in the_test_population:
    if guy.result < 1:
      the_test_population.remove(guy)

  return the_test_population

def mutate_new_population(parent_population):
  """ take what's there, and mate them until you get at most population_size """
  new_population = []
  for x in parent_population:
    for y in parent_population:
      if (x == y):
        continue #need two different mates!
      newguy = copy.deepcopy(x)
      newguy.cross_over(y)
      newguy.mutate_random(5, 3)

      new_population.append(newguy)
      if len(new_population) == population_size:
        return new_population
  return new_population


def main():
  current_population = generate_initial_population(population_size)

  print 'foo1'

  for i in range(10):
    print 'foo %d' % len(current_population)

    test_population(current_population)
    living_population = eliminate_weakests(current_population)
    current_population = mutate_new_population(living_population)

  for guy in current_population:
   guy.print_out()

if __name__ == '__main__':
  main()

