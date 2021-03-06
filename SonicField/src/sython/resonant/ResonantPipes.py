import sython.organ.Player as Player
from com.nerdscentral.audio.core import SFData

import sython.utils.Midi as Midi
from com.nerdscentral.audio.core import SFMemoryZone

from sython.organ.Post   import \
    do_final_mix, \
    mix, \
    post_process, \
    post_process_echo, \
    post_process_tremolate

from sython.voices.ResonantVoices import \
    distant_wind, \
    make_addtive_resonance, \
    make_harpsichord_filter, \
    oboe_filter, \
    violin_filter, \
    harpsichord_filter, \
    oboe_harpsichord_filter, \
    goldberg_filter, \
    goldberg_filter_bright, \
    synthichord_filter, \
    femail_soprano_ah_filter, \
    tuned_wind

def distant(midi_in,beat,temperament,velocity):
    notes1=Player.play(
        midi_in,
        beat,
        temperament,
        voice=distant_wind,
        bend=True,
        mellow=False,
        velocity_correct=velocity*1.5,
        flat_env=True,
        quick_factor=1.5,
        pan = -1
    )
    return post_process(notes1)

def distant_bass(midi_in,beat,temperament,velocity, pan):
    l = 512
    plr = make_addtive_resonance(qCorrect=1.0, rollOff=2.0, saturate=0.5, power=1.1)
    notes1=Player.play(
        midi_in,
        beat,
        temperament,
        voice=plr,
        bend=False,
        mellow=False,
        velocity_correct=velocity,
        flat_env=True,
        quick_factor=1.5,
        pure=True,
        pan=pan
    )
    return post_process(notes1)

def distant_bass_accented(midi_in, beat, temperament, velocity, pan):
    l = 512
    plr = make_addtive_resonance(qCorrect=1.0, rollOff=2.0, saturate=0.5, power=1.1)
    notes1=Player.play(
        midi_in,
        beat,
        temperament,
        voice=plr,
        bend=False,
        mellow=False,
        velocity_correct=velocity,
        flat_env=True,
        quick_factor=1.5,
        pure=False,
        pan = pan
    )
    
    plr = make_addtive_resonance(qCorrect=2.0, rollOff=4.0, saturate=0.0, power=1.0)
    notes2=Player.play(
        midi_in,
        beat,
        temperament,
        voice=plr,
        bend=False,
        mellow=False,
        velocity_correct=velocity,
        flat_env=True,
        quick_factor=1.0,
        pure=True,
        pitch_shift=4.0,
        pan = pan
    )
    
    left1,right1 = post_process(notes1)
    left2,right2 = post_process(notes2)
    return mix(left1,left2),mix(right1,right2)

def distant_string(midi_in,beat,temperament,velocity):
    l = 512
    plr = make_addtive_resonance(qCorrect=2.0, rollOff=1.5, power=1.0, post=violin_filter)
    notes1=Player.play(
        midi_in,
        beat,
        temperament,
        voice=plr,
        bend=True,
        mellow=False,
        velocity_correct=velocity*1.5,
        flat_env=True,
        quick_factor=1.0,
        pan = -1
    )
    return post_process(notes1)

def distant_femail_soprano_ah(midi_in,beat,temperament,velocity, pan):
    plr = make_addtive_resonance(qCorrect=2.0, rollOff=1.5, saturate=0.1, power=1.4, post=oboe_filter)
    notes1=Player.play(
        midi_in,
        beat,
        temperament,
        voice=plr,
        bend=False,
        mellow=False,
        velocity_correct=velocity,
        flat_env=True,
        quick_factor=0.5,
        pure=True,
        pan=pan
    )
    return post_process_tremolate(notes1)

def distant_oboe(midi_in, beat, temperament, velocity, pan):
    plr = make_addtive_resonance(qCorrect=2.0, rollOff=1.5, saturate=0.1, power=1.4, post=oboe_filter)
    notes1=Player.play(
        midi_in,
        beat,
        temperament,
        voice=plr,
        bend=False,
        mellow=False,
        velocity_correct=velocity,
        flat_env=True,
        quick_factor=0.5,
        pure=True,
        pan=pan
    )
    return post_process_tremolate(notes1)

def distant_oboe2(midi_in, beat, temperament, velocity):
    midi=Midi.legato(midi_in,beat,200)
    plr = make_addtive_resonance(qCorrect=1.5, rollOff=1.5, saturate=0.1, power=1.4, post=oboe_filter)
    notes1=Player.play(
        midi,
        beat,
        temperament,
        voice=plr,
        bend=False,
        mellow=False,
        velocity_correct=velocity,
        flat_env=True,
        quick_factor=1.0,
        pure=True,
        pan = -1
    )
    return post_process(notes1)

def soft_harpsichord(midi_in, beat, temperament, velocity, pan):

    harmonics1 = [pow(x,1.01) for x in xrange(1,100)]
    plr1 = make_addtive_resonance(qCorrect=5.0, rollOff=2.5, saturate=0.1, power=1.0, 
                                 post=make_harpsichord_filter(power=1.00, soft=True),
                                 harmonics=harmonics1, seed = -40)
    notes1 = Player.play(
        midi_in,
        beat,
        temperament,
        voice=plr1,
        bend=False,
        mellow=False,
        velocity_correct=velocity,
        flat_env=True,
        quick_factor=0,
        pure=False,
        pan=pan,
        slope = ((0.0, 0), (100, 0) , (440, -5), (4000, -10), (20000, -30)) 
    )
    left1, right1 = post_process(notes1)

    harmonics2 = harmonics1[1:10]
    plr1 = make_addtive_resonance(qCorrect=4.5, rollOff=3.0, saturate=0.0, power=1.0, 
                                 post=make_harpsichord_filter(power=1.00, soft=True),
                                 harmonics=harmonics2, seed = -50)
    notes2 = Player.play(
        midi_in,
        beat,
        temperament,
        voice=plr1,
        bend=False,
        mellow=True,
        velocity_correct=velocity*0.25,
        flat_env=True,
        quick_factor=0,
        pure=True,
        pitch_shift=0.5,
        pan=pan
    )
    left2, right2 = post_process(notes2)
    
    return mix(left1, left2), mix(right1, right2)

def oboe_harpsichord(midi_in, beat, temperament, velocity):

    soft = False
    #brightNess = 1.1
    brightNess = 1.0
    harmonics1 = [pow(x,1.002) for x in xrange(1,100)]
    plr1 = None
    if soft:
        plr1 = make_addtive_resonance(qCorrect=4.0, rollOff=2.75 / brightNess, saturate=0.0, power=1.0, 
                                     post=oboe_harpsichord_filter,
                                 harmonics=harmonics1, seed = -50)
    else:
        plr1 = make_addtive_resonance(qCorrect=5.0, rollOff=2.5 / brightNess, saturate=0.1, power=1.0, 
                                     post=oboe_harpsichord_filter,
                                     harmonics=harmonics1, seed = -40)
    notes1 = Player.play(
        midi_in,
        beat,
        temperament,
        voice=plr1,
        bend=True,
        mellow=False,
        velocity_correct=velocity*1.0,
        flat_env=True,
        quick_factor=0,
        pure=False,
        pan = -1
    )
    return post_process(notes1)

def mephisto_harpsichord(midi_in, beat, temperament, velocity, pan):

    harmonics1 = [pow(x,1.005) for x in xrange(1,100)]

    plr1 = make_addtive_resonance(qCorrect=5.0, rollOff=2.0, saturate=0.20, power=1.1, 
                                 post=goldberg_filter_bright,
                                 harmonics=harmonics1, seed = -50)
    notes1 = Player.play(
        midi_in,
        beat,
        temperament,
        voice=plr1,
        bend=True,
        mellow=False,
        velocity_correct=velocity*1.0,
        flat_env=True,
        quick_factor=0.0,
        pure=False,
        pan=pan,
        slope = ((0.0, 0), (100, 0) , (440, -10), (4000, -30), (20000, -30))
    )
    return post_process(notes1)


def double_pure_harpsichord(midi_in, beat, temperament, velocity, pan):

    harmonics1 = [pow(x,1.001) for x in xrange(1,100)]

    plr1 = make_addtive_resonance(qCorrect=5.0, rollOff=2.0, saturate=0.10, power=1.0, 
                                 post=goldberg_filter_bright,
                                 harmonics=harmonics1, seed = -50)
    notes1 = Player.play(
        midi_in,
        beat,
        temperament,
        voice=plr1,
        bend=True,
        mellow=False,
        velocity_correct=velocity*1.0,
        flat_env=True,
        quick_factor=0.0,
        pure=False,
        pan = pan,
        slope = ((0.0, 0), (100, 0) , (440, -10), (4000, -40), (20000, -30)) 
    )
    
    left1, right1 = post_process_echo(notes1)
    
    harmonics2 = harmonics1[1:10]
    plr1 = make_addtive_resonance(qCorrect=4.5, rollOff=3.0, saturate=0.25, power=1.1, 
                                 post=goldberg_filter,
                                 harmonics=harmonics2, seed = -35)
    notes2 = Player.play(
        midi_in,
        beat,
        temperament,
        voice=plr1,
        bend=False,
        mellow=True,
        velocity_correct=velocity*0.5,
        flat_env=True,
        quick_factor=0,
        pure=True,
        pitch_shift=0.5,
        pan = pan,
        slope = ((0.0, 0), (50, 0) , (220, -10), (4000, -60), (20000, -90)) 
    )
    left2, right2 = post_process_tremolate(notes2)
    
    return mix(left1, left2), mix(right1, right2)

def _golberg_harpsichord(midi_in, beat, temperament, velocity, slope, pan):

    harmonics1 = [pow(x,1.002) for x in xrange(1,100)]

    plr1 = make_addtive_resonance(qCorrect=5.0, rollOff=2.5, saturate=0.1, power=1.0, 
                                 post=goldberg_filter,
                                 harmonics=harmonics1, seed = -30 if slope else -50)
    notes1 = Player.play(
        midi_in,
        beat,
        temperament,
        voice=plr1,
        bend=True if slope else False,
        mellow=False,
        velocity_correct=velocity*1.0,
        flat_env=True,
        quick_factor=0,
        pure=False,
        pan = pan,
        slope = slope
    )
    return post_process(notes1)

def golberg_harpsichord(midi_in, beat, temperament, velocity, pan):
    return _golberg_harpsichord(midi_in, beat, temperament, velocity, None, pan)

def sloped_golberg_harpsichord(midi_in, beat, temperament, velocity, pan):
    return _golberg_harpsichord(midi_in, beat, temperament, velocity, 
                         ((0.0, 0), (100, 0) , (440, -10), (4000, -30), (20000, -30)), pan)
    
def harpsichord(midi_in, beat, temperament, velocity):
    harmonics = [pow(x,1.01) for x in xrange(1,100)]
    plr = make_addtive_resonance(qCorrect=4.0, rollOff=0.5, saturate=0.1, power=1.0, 
                                 post=make_harpsichord_filter(power=1.05), harmonics=harmonics, seed = -40)
    notes1=Player.play(
        midi_in,
        beat,
        temperament,
        voice=plr,
        bend=True,
        mellow=False,
        velocity_correct=velocity*1.5,
        flat_env=True,
        quick_factor=0,
        pure=False,
        pan = -1
    )
    return post_process(notes1)  

def distant_accent(midi_in, beat, temperament, velocity, pan):
    plr = make_addtive_resonance(qCorrect=4.0, rollOff=4.0, saturate=0.0, power=1.0, seed = -40)
    notes1=Player.play(
        midi_in,
        beat,
        temperament,
        voice=plr,
        bend=False,
        mellow=False,
        velocity_correct=velocity,
        flat_env=False,
        quick_factor=0.25,
        pure=True,
        pitch_shift=2.0,
        pan = pan
    )
    return post_process_echo(notes1) 

def distant_soft_accent(midi_in, beat, temperament, velocity, pan):
    plr = make_addtive_resonance(qCorrect=4.0, rollOff=4.0, saturate=0.0, power=1.0, seed = -40)
    notes1=Player.play(
        midi_in,
        beat,
        temperament,
        voice=plr,
        bend=False,
        mellow=True,
        velocity_correct=velocity,
        flat_env=False,
        quick_factor=0.25,
        pure=True,
        pitch_shift=2.0,
        pan = pan
    )
    return post_process_tremolate(notes1, rate=3.75) 

def distant_string_pipe(midi_in, beat, temperament, velocity, pan):
    midi = Midi.legato(midi_in, beat, 128)
    plr = make_addtive_resonance(qCorrect=4.0, rollOff=4.5, saturate=0.05, power=1.02, seed = -40)
    #plr = make_addtive_resonance(qCorrect=4.0, rollOff=4.0, saturate=0.0, power=1.1, seed = -40)
    notes1=Player.play(
        midi_in,
        beat,
        temperament,
        voice=plr,
        bend=True,
        mellow=False,
        velocity_correct=velocity,
        flat_env=False,
        quick_factor=0.25,
        pure=False,
        pitch_shift=1.0,
        pan = pan
    )
    return post_process(notes1) 

def distant_string_pipe_bass(midi_in, beat, temperament, velocity, pan):
    midi = Midi.legato(midi_in, beat, 128)
    plr = make_addtive_resonance(qCorrect=4.0, rollOff=4.5, saturate=0.05, power=1.02, seed = -40)
    #plr = make_addtive_resonance(qCorrect=4.0, rollOff=4.0, saturate=0.0, power=1.1, seed = -40)
    notes1=Player.play(
        midi_in,
        beat,
        temperament,
        voice=plr,
        bend=True,
        mellow=False,
        velocity_correct=velocity,
        flat_env=False,
        quick_factor=1.0,
        pure=False,
        pitch_shift=0.5,
        pan = pan
    )
    return post_process(notes1)

def distant_flute_pipe(midi_in, beat, temperament, velocity, pan):
    harmonics = [pow(x,1.00) for x in xrange(1,16)]
    midi = Midi.legato(midi_in, beat, 128)
    plr = make_addtive_resonance(qCorrect=4.0, rollOff=4.5, saturate=0.00, power=1.001, seed = -30, harmonics=harmonics)
    notes1=Player.play(
        midi,
        beat,
        temperament,
        voice=plr,
        bend=False,
        mellow=False,
        velocity_correct=velocity,
        flat_env=False,
        quick_factor=0.5,
        pure=True,
        pitch_shift=1.0,
        pan = pan
    )

    return post_process(notes1) 

def bass_harpsichord(midi_in, beat, temperament, velocity):
    harmonics = [pow(x,1.01) for x in xrange(1,100)]
    plr1 = make_addtive_resonance(qCorrect=4.0, rollOff=0.5, saturate=0.1, power=1.0, 
                                 post=make_harpsichord_filter(power=1.05, resonance=0.9),
                                 harmonics=harmonics, seed = -40)
    notes1=Player.play(
        midi_in,
        beat,
        temperament,
        voice=plr1,
        bend=True,
        mellow=False,
        velocity_correct=velocity*0.75,
        flat_env=True,
        quick_factor=0,
        pure=False,
        pan = 0.1
    )

    plr2 = make_addtive_resonance(qCorrect=4.0, rollOff=1.0, saturate=0.0, power=1.0, 
                                 post=make_harpsichord_filter(power=0.95, resonance=0.2),
                                 harmonics=harmonics, seed = -50)
    notes2=Player.play(
        midi_in,
        beat,
        temperament,
        voice=plr2,
        bend=False,
        mellow=False,
        velocity_correct=velocity*1.0,
        flat_env=True,
        quick_factor=0,
        pure=True,
        pitch_shift=0.5,
        pan = 0.8
    )

    left1,right1 = post_process(notes1)
    left2,right2 = post_process(notes2)
    return mix(left1, left2),mix(right1, right2)

def harpsiPipe(midi_in, beat, temperament, velocity, pan):
    with SFMemoryZone():
        a = distant_flute_pipe(midi_in, beat, temperament, velocity, pan)
        b = sloped_golberg_harpsichord(midi_in, beat, temperament, velocity, pan)
        a=a.get()
        b=b.get()
        return (
            sf.FixSize(sf.Mix(sf.Pcnt60(a[0]), sf.Pcnt40(b[0]))).keep(),
            sf.FixSize(sf.Mix(sf.Pcnt60(a[1]), sf.Pcnt40(b[1]))).keep()
        )
