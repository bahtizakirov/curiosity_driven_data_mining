import pygame as pg
import time
import numpy
import os
from datetime import datetime
pg.mixer.init()
pg.init()
num_generations = 3
num_initial_members = 2
num_progeny_per_mating = 3
num_saved_progeny_per_generation = 2
note_subdivision = 8
num_loops = 2
tempo = 110
beat_length = (60/tempo)*(4 / note_subdivision)
mutation_rate = .1
print("beat_length: " + str(beat_length))
sounds = []
hi_hat = pg.mixer.Sound("/Users/ianborukhovich/Projects/curiosity_driven_data_mining/genetic_beats/boom.wav")
pg.mixer.set_num_channels(19)
sounds.append(pg.mixer.Sound(pg.mixer.Sound("/Users/ianborukhovich/Projects/curiosity_driven_data_mining/genetic_beats/kick.wav")))
sounds.append(pg.mixer.Sound(pg.mixer.Sound("/Users/ianborukhovich/Projects/curiosity_driven_data_mining/genetic_beats/snare.wav")))
sounds.append(pg.mixer.Sound(pg.mixer.Sound("/Users/ianborukhovich/Projects/curiosity_driven_data_mining/genetic_beats/hi_hat.wav")))
num_sounds = len(sounds)
sound_lengths = []
for sound in sounds:
    sound_lengths.append(sound.get_length())
print(sound_lengths)
sound_names  = ['K','S','H']

def array_of_random_integers(length, max_int):
    rand_int_array = []
    for i in range(0,length):
        random_binary = numpy.random.randint(0, max_int)
        rand_int_array.append(random_binary)
    return rand_int_array

def create_inital_generation(sounds):
    last_generation = []
    for j in range(0, num_initial_members):
        current_member = []
        for i in range(0, num_sounds):
            current_member = current_member + array_of_random_integers(note_subdivision, 2)
        last_generation.append(current_member)
    return last_generation

def create_next_generation(last_generation):
    next_generation = []
    for a in range(0, len(last_generation)):
        for b in range(a, len(last_generation)): 
            #mate current pair to generate progeny
            if a != b:
                next_generation = next_generation + mate_current_pair(last_generation[a], last_generation[b])
    return next_generation

def mate_current_pair(father,mother):
    current_generation_beats = []
    for x in range(0, num_progeny_per_mating):
        #choose member to donate each beat
        child_beat = []
        for y in range(0, len(father)):
            inhereted_beat = get_inherited_beat(father[y],mother[y])
            mutated_beat = inhereted_beat if numpy.random.randint(0,101) > mutation_rate*100 else 1 - inhereted_beat
            child_beat.append(mutated_beat)
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
        play_beat(beat, num_loops)
        fitness = input("score beat\n")
        next_generation_fitness.append(int(fitness))
    saved_progeny_indices = find_top_n_indices(next_generation_fitness, num_saved_progeny_per_generation)
    return [next_generation[i] for i in saved_progeny_indices]

def find_top_n_indices(list, n):
    top_n_indices = sorted(range(len(list)), key=lambda x: list[x])[-n-1:]
    return top_n_indices

def play_beat(beat, num_loops):
    stacked_beat = []
    try:
        for x in range(0, num_loops):
            beat_string = ""
            for i in range(0, note_subdivision):
                note_string = ""
                max_sound_length = 0
                #start_beat = datetime.now()
                #print("start beat " + str(start_beat))
                for j in range(0, num_sounds):
                    beat_index = i+ (note_subdivision - 1) * j
                    if beat[beat_index]:
                        sounds[j].play()
                        if(max_sound_length < sound_lengths[j]):
                            max_sound_length = sound_lengths[j]
                        note_string += "-" + sound_names[j]
                beat_string += note_string + " | "
                #print(str(max_sound_length) + " " + str(beat_length))
                time.sleep(beat_length)
                #end_beat = str(datetime.now()-start_beat)
                #print("end_beat " + end_beat)
            print(beat_string)
    except KeyboardInterrupt:
        print("interrupted")
#evolve num_generations
last_generation = create_inital_generation(sounds)

for x in range(0,num_generations):
    #mate pairs of members of current generation
    print("generation: " + str(x))
    next_generation = create_next_generation(last_generation)
    saved_progeny = identify_fit_progeny(next_generation)
    last_generation = saved_progeny

for beat in last_generation:
    play_beat(beat, 4)
