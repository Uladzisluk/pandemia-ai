import random
import csv

from person import Person
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

for x in [1, 2, 3, 4, 5]:

    # SIMULATION PARAMETERS
    n = 600  # number of individuals
    p_infected = 1  # percentage of infected people at the beginning of the simulation (0-100%)
    r_transmission = 2  # radius of transmission in pixels (0-100)
    p_transmission = x  # probability of transmission in percentage (0-100%)
    p_isolated = 40  # percentage of the people in quarantine (0-100%)
    t_recover = 100  # time taken to recover in number of frames (0-infinity)

    infected = 0
    individuals = []

    # creating all the individuals in random positions
    for i in range(n):
        p = Person(i, np.random.random() * 100, np.random.random() * 100,
                   np.random.random() * 100, np.random.random() * 100,
                   (np.random.random() + 0.5) * 100, t_recover, False)

        individuals.append(p)

    #  Infecting some of them
    to_infect = random.choices(individuals, k=int(p_infected * n / 100))
    for person in to_infect:
        person.infect(0)
        infected = infected + 1

    # Isolating some of them
    to_isolate = random.choices(individuals, k=int(p_isolated * n / 100))
    for person in to_isolate:
        person.fixed = True

    # this creates all the graphics
    fig = plt.figure(figsize=(18, 9))
    ax = fig.add_subplot(1, 2, 1)
    cx = fig.add_subplot(1, 2, 2)
    ax.axis('off')
    cx.axis([0, 1700, 0, n])
    scat = ax.scatter([p.pos_x for p in individuals],
                      [p.pos_y for p in individuals], c='blue', s=8)
    rect = plt.Rectangle((0, 0), 100, 100, fill=False)
    ax.add_patch(rect)
    sus, = cx.plot(n - infected, color="blue", label="Susceptible")
    cinf, = cx.plot(infected, color="red", label="Currently infected")
    rec, = cx.plot(infected, color="gray", label="Recovered")
    cx.legend(handles=[rec, sus, cinf])
    cx.set_xlabel("Time")
    cx.set_ylabel("People")

    susceptible_for_plot = [n - infected]
    infected_for_plot = [infected]
    recovered_for_plot = [0]
    time = [0]


    # generate csv file
    def generate_csv(frame):
        p_transmissions = np.full(frame, p_transmission)
        with open('data.csv', 'a') as f_object:
            writer_object = csv.writer(f_object)
            for i in range(0, frame):
                writer_object.writerow([p_transmissions[i], time[i], susceptible_for_plot[i], infected_for_plot[i],
                                        recovered_for_plot[i]])
            f_object.close()


    # function executed frame by frame
    def update(frame, rp, ip, sp, t):
        infected_cycle = 0
        recovered = 0
        colores = []
        sizes = [8 for _ in individuals]
        for individual in individuals:
            # check how much time the person has been sick
            individual.check_transmission(frame)
            # animate the movement of each person
            individual.update_pos(0, 0)
            if individual.retired:
                recovered += 1  # count the amount of recovered
            if individual.infected:
                infected_cycle = infected_cycle + 1  # count the amount of infected
                # check for people around the sick individual and infect the ones within the
                # transmission radius given the probability
                for per in individuals:
                    if per.index == individual.index or per.infected or per.retired:
                        pass
                    else:
                        d = individual.get_dist(per.pos_x, per.pos_y)
                        if d < r_transmission:
                            if np.random.random() < p_transmission / 100:
                                per.infect(frame)
                                sizes[per.index] = 80

            colores.append(individual.get_color())  # change dot color according to the person's status
        if frame == 1000:
            generate_csv(frame)

        # update the plotting data
        sp.append(n - infected_cycle - recovered)
        ip.append(infected_cycle)
        rp.append(recovered)
        t.append(frame)

        # transfer de data to the matplotlib graphics
        offsets = np.array([[p.pos_x for p in individuals],
                            [p.pos_y for p in individuals]])
        scat.set_offsets(np.ndarray.transpose(offsets))
        scat.set_color(colores)
        scat.set_sizes(sizes)
        cinf.set_data(t, ip)
        rec.set_data(t, rp)
        sus.set_data(t, sp)
        return scat, cinf, rec, sus


    # run the animation indefinitely
    animation = FuncAnimation(fig, update, interval=25, fargs=(recovered_for_plot, infected_for_plot, susceptible_for_plot,
                                                               time), blit=True)
    plt.show()
