import pygame as pg
import time
import numpy
import os
pg.mixer.init()
pg.init()
num_generations = 2
num_notes = 8
num_saved_progeny = 2
num_progeny = 3
num_loops = 12

sounds = []
#hi_hat = pg.mixer.Sound("./boom.wav")
pg.mixer.set_num_channels(19)
#pg.mixer.Sound.play(hi_hat)
#sounds.append(pg.mixer.Sound("./ClosedHH Electrified 04 2.aif"))
#sounds.append(pg.mixer.Sound("./Kick Acoustified 01 1.aif"))
#sounds.append(pg.mixer.Sound("./Snare Acoustified 01 1.aif"))
sounds.append('hi hat')
sounds.append('snare')
sounds.append('kick')
num_sounds = len(sounds)

def array_of_random_integers(length, max_int):
    rand_int_array = []
    for i in range(0,length):
        rand_int_array.append(numpy.random.randint(0, max_int))
    return rand_int_array

def create_inital_generation(sounds):
    last_generation = []
    for j in range(0, num_generations):
        current_member = []
        for i in range(0, num_sounds):
            current_member = current_member + array_of_random_integers(num_notes,2)
        last_generation.append(current_member)
    return last_generation

def create_next_generation(last_generation):
    next_generation = []
    for a in range(0, len(last_generation)):
        for b in range(a, len(last_generation)): 
            #mate current pair to generate progeny
            next_generation = next_generation + mate_current_pair(last_generation[a], last_generation[b])
    return next_generation

def mate_current_pair(father,mother):
    current_generation_beats = []
    for x in range(0, num_progeny):
        #choose member to donate each beat
        child_beat = []
        for y in range(0, len(father)):
            inhereted_beat = get_inherited_beat(father[y],mother[y])
            child_beat.append(inhereted_beat)
        current_generation_beats.append(child_beat)
    return current_generation_beats

def get_inherited_beat(father_beat,mother_beat):
    random_1_0 = numpy.random.randint(0,2)
    if random_1_0 == 0:
        return father_beat
    else:
        return mother_beat

def identify_fit_progeny(next_generation):
    next_generation_fitness = []
    for beat in next_generation:
        #play beat to rate fitness
        #play_beat(beat)
        print("beat")
        fitness = input("score beat")
        next_generation_fitness.append(int(fitness))
    saved_progeny_indices = find_top_n_indices(next_generation_fitness, num_saved_progeny)
    return [next_generation[i] for i in saved_progeny_indices]

def find_top_n_indices(list, n):
    top_n_indices = sorted(range(len(list)), key=lambda x: list[x])[-n:]
    return top_n_indices
def play_beat(beat):
    print(beat)
    stacked_beat = []
    for x in range(0, num_loops):
        for i in range(0, num_sounds*num_notes):
            stacked_beat_index = i%num_notes
            sound_index = i//num_notes
            if beat[i]:
                sounds[sound_index].play

#evolve num_generations
last_generation = create_inital_generation(sounds)

for x in range(0,num_generations):
    #mate pairs of members of current generation
    next_generation = create_next_generation(last_generation)
    saved_progeny = identify_fit_progeny(next_generation)
    last_generation = saved_progeny

