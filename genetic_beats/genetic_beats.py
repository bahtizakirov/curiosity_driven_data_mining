import pygame as pg
import time
import numpy

pg.mixer.init()
pg.init()
pg.mixer.set_num_channels(19)

num_notes = 8
num_saved_generations = 3
num_progeny = 5
sounds = []
sounds.append(pg.mixer.sounds("/Users/ianborukhovich/Music/Ableton/Factory Packs/Bomblastic/Samples/Drums/Hihat/ClosedHH\ Electrified\ 04\ 2.aif"))
sounds.append(pg.mixer.sounds("/Users/ianborukhovich/Music/Ableton/Factory Packs/Bomblastic/Samples/Drums/Kick/Kick\ Acoustified\ 01\ 1.aif"))
sounds.append(pg.mixer.sounds("/Users/ianborukhovich/Music/Ableton/Factory Packs/Bomblastic/Samples/Drums/Hihat/Snare\ Acoustified\ 01\ 1.aif"))
num_sounds = len(sounds)
last_generation = numpy.empty
last_generation.concatenate(numpy.randint(0,1, size=(1,num_sounds*num_notes)))
last_generation.concatenate(numpy.randint(0,1, size=(1,num_sounds*num_notes)))

def create_next_generation(last_generation):
    next_generation = []
    for a in range(0, len(last_generation)):
        for b in range(a, len(last_generation)): 
            #mate current pair to generate progeny
            next_generation.append(
                mate_current_pair(last_generation[a], last_generation[b])
                )
    return next_generation

def mate_current_pair(father,mother):
    current_generation_beats = []
    for x in range(0, num_progeny):
        #choose member to donate each beat
        for y in range(0, len(father)):
            inhereted_beat = get_inhereted_beat(father[y],mother[y])
            child_beat.append(father_or_mother[beat_number])
    return current_generation_beats

def get_inherited_beat(father_beat,mother_beat):
    random_1_0 = numpy.randint(0,1)
    if random_1_0 == 0:
        return father_beat
    else:
        return mother_beat

def identify_fit_progeny(next_generation):
    for beat in next_generation:
        #play beat to rate fitness
        play_beat(child_beat)
        fitness = raw_input("score beat")
        next_generation_fitness.append(fitness)
    saved_progeny_indices = find_top_n_indices(next_generation_fitness)
    return next_generation[saved_progeny_indices]

def play_beat(beat):
    stacked_beat = []
    for i in range(0, num_sounds*num_notes):
        stacked_beat_index = i%num_notes
        for sound in sounds
            if(note)

#evolve num_generations
for x in range(0,num_generations):
    #mate pairs of members of current generation
    next_generation = create_next_generation(last_generation)
    saved_progeny = identify_fit_progeny(next_generation)
    last_generation = saved_progeny
