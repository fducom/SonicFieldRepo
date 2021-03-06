import threading
from sython.utils.Reverberation import granular_reverberate,reverberate,convolve
from java.util.concurrent.atomic import AtomicLong
from sython.utils.Envelopes import linearEnv
from com.nerdscentral.audio.core import SFMemoryZone, SFConstants
from com.nerdscentral.audio.core import SFData
from sython.utils.Memory import writeSawppedCache, readSwappedCache
import random
import os.path

################################################################################
#  hint:     NN TN TT NT for trill and normal for the previous and next notes
#            a special hint value of E or S inticates end or start note
#            respectively
#  pitch:    the frequency of the note in Hz
#  v:        over all volume 0 to 1
#  vl:       volume left correction 0 to 1
#  vr:       volume right correction 0 to 1
#  voice:    voice function
#  velocity_correct: correct volume by this amount between 0 and 1
#  quick_factor:     'quick' scales initial attack. >1 makes
#                    slow/soft <1 make fast/hard
#  flat_env: true/false if true flatten all but attack and short release
#            (more like a tradition organ pipe)
#  pure:     true/false if true do not mix in several slight pitch shifts
#            otherwise do
#  raw_bass: true/false if true no post processing of bass
#  decay:    true/false if true causes steady decay of note throughout envelope.
#  bend:     true/false if true then let the pitch of the note rise very
#            slightly over the note
#  mellow:   Use filtering to mellow the note, required for sub_bass to work
#
# smooth:    Use convolution to smooth out notes individually.
################################################################################

def sing(
        hint,
        pitch,
        lengthIn,
        v,
        vl,
        vr,
        voice,
        velocity_correct_,
        quick_factor,
        sub_bass,
        flat_env,
        pure,
        raw_bass,
        decay,
        bend,
        mellow,
        smooth,
        slope,
    ):
    if pitch > 20000:
        raise ValueError('Pitch too great {0}'.format(pitch))
    with SFMemoryZone():
        velocity_correct=velocity_correct_
        length=lengthIn
        tp=0

        # minimum play time
        if length<192:
            length=192
            tp=0
        elif length<363:
            length+=128
            tp=1
        elif length<512:
            length+=256
            tp=2
        elif length<1024:
            length+=128
            tp=3
        else:
            tp=4

        sig=[]
        if pure:
            x=1
        else:
            if pitch<330:
                x=5
            elif pitch<880:
                x=6
            else:
                x=3
        for x in range(0,x):
            vc=voice(length,pitch*(1.0+random.random()*0.005))
            if quick_factor:
                vc=sf.Multiply(
                    linearEnv(
                        vc,
                        [
                            (0,0),
                            (24,1),
                            (sf.Length(vc)-24,1),
                            (sf.Length(vc),0)
                        ]
                    ),
                    vc
                )
                sig.append(
                    sf.LinearVolume(
                        sf.Concatenate(
                            sf.Silence(24*random.random()),
                            vc
                        )
                        ,random.random()+0.25
                    )
                )
            else:
                sig.append(sf.LinearVolume(vc, random.random()+0.25))

        sig = sf.FixSize(sf.Mix(sig))
        length=sf.Length(sig)

        if decay:
            # -60 db at 1 minute
            dbs=-60.0*float(length)/float(decay)
            env=sf.ExponentialShape((0,0),(length,dbs))
            sig=sf.Multiply(sig,env)

        pHint = hint[0]
        nHint = hint[1]
        shine = False
        env = None
        if quick_factor:
            if tp==0:
                if pHint=="T":
                    q=32
                else:
                    q=64
                if nHint=="T":
                    p=32
                else:
                    p=64
                q*=quick_factor
                env=linearEnv(sig,[(0,0),(q,1),(192-p,0.5),(length,0)])
                if hint=="TT":
                    velocity_correct*=0.8
                elif hint=="NN" and pitch>660:
                    shine=True
                    velocity_correct*=0.5
            elif tp==1 or flat_env:
                if pHint=="T":
                    q=48
                else:
                    q=96
                if nHint=="T":
                    p=64
                else:
                    p=128
                q*=quick_factor
                env=linearEnv(sig,[(0,0),(q,0.75),(length-p,1.0),(length,0)])
                if hint=="TT":
                    velocity_correct*=0.8
                if hint=="TT":
                    velocity_correct*=0.8
                elif hint=="NN" and pitch>880:
                    shine=True
                    velocity_correct*=0.6
            elif tp==2:
                env=linearEnv(sig,[(0,0),(96*quick_factor,0.75),(length-256,1.0),(length,0)])
            elif tp==3:
                if length<1280:
                    env=linearEnv(sig,[(0,0),(64*quick_factor,0.5),(256,1),(512,0.75),((length-512)/2.0+512,0.5),(length,0)])
                else:
                    env=linearEnv(sig,[(0,0),(64*quick_factor,0.5),(256,1),(512,0.75),(length-512,0.75),(length,0)])
            else:
                env=linearEnv(sig,[(0,0),(64*quick_factor,0.25),(512,1),(length/2,0.75),(length,0)])

        if bend:
            mod=sf.LinearShape((0,0.995),(length,1.005))
            if env:
                mod=sf.Mix(mod,sf.LinearVolume(+env,0.01))
            # if we have envelope extension then we don't do this as
            # it get really hard to get the lengths correct and make
            # sense of what we are trying to do. KISS
            if sf.Length(+sig)==sf.Length(+mod):
                sig=sf.FrequencyModulate(sig,mod)

        sig=sf.FixSize(sig)
        if mellow:
            if pitch<256:
                if sub_bass:
                    if pitch < 128:
                        sig=sf.Mix(
                            granular_reverberate(+sig,ratio=0.501 ,delay=256,density=32,length=256,stretch=1,vol=0.20),
                            granular_reverberate(+sig,ratio=0.2495,delay=256,density=32,length=256,stretch=1,vol=0.10),
                            sig
                        )
                    elif pitch < 192:
                        sig=sf.Mix(
                            granular_reverberate(+sig,ratio=0.501,delay=256,density=32,length=256,stretch=1,vol=0.25),
                            sig
                        )
                    else:
                        sig=sf.Mix(
                            granular_reverberate(+sig,ratio=0.501,delay=256,density=32,length=256,stretch=1,vol=0.15),
                            sig
                        )
                if raw_bass:
                    sig=sf.BesselLowPass(sig,pitch*8.0,1)
                else:
                    sig=sf.BesselLowPass(sig,pitch*8.0,2)
            if pitch<392:
                sig=sf.BesselLowPass(sig,pitch*6.0,2)
            elif pitch<512:
                sig=sf.Mix(
                    sf.BesselLowPass(+sig,pitch*6.0, 2),
                    sf.BesselLowPass( sig,pitch*3.0, 2)
                )
            elif pitch<640:
                sig=sf.BesselLowPass(sig,pitch*3.5, 2)
            elif pitch<1280:
                sig=sf.Mix(
                    sf.BesselLowPass(+sig,pitch*3.5, 2),
                    sf.BesselLowPass( sig,pitch*5.0, 2)
                )
            else:
                sig=sf.Mix(
                    sf.BesselLowPass(+sig,pitch*5, 2),
                    sf.BesselLowPass( sig,5000,    1)
                )

        if env:
            sig=sf.Multiply(sig,env)
        # Aggressively clean up an dc offset or other issue on the tail.
        sig = sf.RTrim(sig)
        length = sf.Length(sig)
        sig = sf.Multiply(
            sf.LinearShape(((0,1), (length - 10, 1), (length, 0))),
            sig
            )
        sig=sf.FixSize(sig)

        if smooth:
            cnv=sf.WhiteNoise(10240)
            cnv=sf.ButterworthHighPass(cnv,32,4)
            if shine:
                q=640
                print "Shine"
            else:
                q=256
            cnv=sf.Cut(5000,5000+q,cnv)
            cnv=sf.Multiply(cnv,sf.LinearShape((0,0),(32,1),(q,0)))
            sigr=convolve(+sig,cnv)
            length = sf.Length(sigr)
            env = None
            if length > 300:
                env = linearEnv(sigr,[(0,0),(256,1),( length - 20,1.5), (length, 0)])
            else:
                env = linearEnv(sigr,[(0,0),(length / 2.0, 1), (length, 0)])
            sigr=sf.Multiply(env, sigr)
            sig=sf.Mix(
                sf.Pcnt20(sigr),
                sf.Pcnt80(sig)
            )
            slopeEnv = sf.ExponentialShape(slope)
            velocity_correct *= sf.ValueAt(slopeEnv, pitch)
            print 'VCorrect: {0}'.format(velocity_correct)
        note  = sf.LinearVolume(sf.FixSize(sig), v)
        notel = sf.LinearVolume(note, vl*velocity_correct).keep()
        noter = sf.LinearVolume(note, vr*velocity_correct).keep()
        return notel, noter

################################################################################
# Play a list of notes representing a midi channel.
#
# midi:        the list of midi notes from a midi reader
# beat:         milliseconds per midi tick
# temperament:  the temperament function to convert note to pitch
# voice:        the voice creating function
# velocity_correct:     velocity correction between 0 and 1 to scale the volume
# pitch_shift:  the frequency moved from the midi frequency as a ratio i.e. 0.5
#               would be down one octave
# quick_factor: quickness - see sing
# sub_bass:     use sub bass enhancement - see sing
# flat_env:     use flat env - see sing
# pure:         use pure pitch - see sing
# pan:          pan left and right from 0 to 1. A special value of -1 (the
#               default) causes 'auto pan' where pitch is used to work out
#               the pan.
# raw_bass:     use raw bass - see sing
# pitch_add:    add this pitch in hz to every note - this can detune for example
#               to produce a celest effect
# decay:        use decay - see sing
# bend:         use bend - see sing
# mellow:       use mellow - see sing
# smooth:       use convolution to smooth out notes
# simple:       use simple midi mode (see below), default True
# controllers:  in complex midi mode use these functions as controllers#
#
# Notes
# =====
#
# midi channles are list of MidiEvent objects:
#
# See Midi.py for the defintion of MidiEvent objects.
#
# In this mode we have controllers and meta events. Sysex as currently ignored.
# The only meta event which is considered is temp.
#
# Controllers are named using the standard midi names all under control_change
# as type:
#
#  modewheel
#  breath
#  foot
#  portamento_time
#  volume
#  balance
#  pan
#  portamento
#  sostenuto
#  reset
#
#
################################################################################

# Restart is a global thing as we might have multiple passes through play.
RESTART_INFO = threading.local()
NOTE_CACHE = {}

def play(
        midi,
        beat,
        temperament,
        voice,
        velocity_correct    = 1.0,
        pitch_shift         = 1.0,
        quick_factor        = 1.0,
        sub_bass            = False,
        flat_env            = False,
        pure                = False,
        pan                 = -1,
        raw_bass            = False,
        pitch_add           = 0.0,
        decay               = False,
        bend                = False,
        mellow              = False,
        smooth              = True,
        controllers         = {},
        slope               = None
    ):
    RESTART_INFO.restartIndex = getattr(RESTART_INFO, 'restartIndex', 0)
    RESTART_INFO.replayIndex  = getattr(RESTART_INFO, 'replayIndex', 0)

    if not slope:
        slope = ((0, 0),  (20000, 0))
    notes=[]
    d_log("Stop: ",voice)
    d_log('Total notes:',len(midi))
    cacheMisses = 0
    # Stores up sing futures so they are executed in batches giving better parallelisation.
    toWrite=[]

    for index in range(0,len(midi)):
        if index>0:
            prev=midi[index-1]
        else:
            prev=None
        if index<len(midi)-1:
            next=midi[index+1]
        else:
            next=None
        current=midi[index]
        if current.isNote():
            tickOn   = current.tick
            tickOff  = current.tick_off
            key      = current.key
            velocity = current.velocity
        else:
            continue

        at=tickOn*beat
        length=(tickOff-tickOn)*beat
        if key==0:
            pitch=base
        else:
            key=float(key)
            pitch= temperament(key) * pitch_shift
        velocity=velocity/100
        velocity
        pitch+=pitch_add
        pl=pitch

        vCUse=velocity_correct

        # volume pitch correction to stop domination
        # of high notes - not quite the same as
        # loudness correction due to the high dominating
        # low perception issue.
        pCorrect=1
        if velocity_correct>0.25 and pitch > 660 :
            # shorter is less intense and gets lost easily so boost a bit
            if length <256:
                sCorrect=1.5
            else:
                sCorrect=1.0
            pCorrect=1.0
            if pitch>660:
                if pitch<2000:
                    pCorrect=float(2000-pitch)/1340.0
                    pCorrect=0.40*(1.0-pCorrect)+pCorrect
                elif pitch<4000:
                    pCorrect=float(8000-pitch)/4000.0
                    pCorrect=0.75*(1.0-pCorrect)+0.4*pCorrect
            pCorrect*=sCorrect
            if pCorrect>1:
                pCorrect=1
        vCUse*=pCorrect

        if pan==-1:
            if pl<300:
                # low to the right ish
                if pl <100:
                    pl=100
                pl=float(pl-100)/200.0
                pl=pl*0.5+0.4
                lr=pl
            elif pl <880:
                # middle across all
                pl=float(pl-300)/580.0
                pl=pl*0.8+0.1
                lr=pl
            else:
                # high off to the left
                pl=pl-880
                pl=float(pl-880)/880.0
                if pl>1:
                    pl=1
                pl=0.05+pl*0.3
                lr=pl
        else:
            lr=1.0-pan

        rl=1.0-lr

        # Compute hint
        # Two letters - first for previous note
        # second for next note
        # S=start
        # T=trill
        # N=normal
        # E=end
        hint=""
        if prev and prev.isNote():
            to,tf,n,k,v=prev.getNote()
            lp=(tf-to)*beat
            ep=tf*beat
            # quick close previous note
            if at-ep < 100 and lp<256:
                hint+="T"
            else:
                hint+="N"
        else:
            hint+="S"
        if next and next.isNote():
            to,tf,n,k,v=next.getNote()
            sn=to*beat
            # quick close previous note
            if sn-at < 100+length and length<256:
                hint+="T"
            else:
                hint+="N"
        else:
            hint+="E"

        d_log("H",hint,"P",pitch,"@",at,"L",length,"V",velocity,"VU",vCUse,"PC",pCorrect)
        args = (
            hint,
            pitch,
            length,
            velocity,
            lr,
            rl,
            voice,
            vCUse,
            quick_factor,
            sub_bass,
            flat_env,
            pure,
            raw_bass,
            decay,
            bend,
            mellow,
            smooth,
            slope)

        # Here is the restart logic. If this is a restart then it
        # should automatically skip generating notes it has already generated.
        # However, it will still cache them. Note, other caches in the signal generators
        # may not be populated so a restart might not generate exactly the same notes
        # as a complete run would.
        signals = None
        if args in NOTE_CACHE and (RESTART_INFO.restartIndex < RESTART_INFO.replayIndex or random.random() < 0.9):
            print 'Note Cache Hit! {0} -> {1}'.format(index, index - cacheMisses)
            signals = [readSwappedCache(s) for s in NOTE_CACHE[args]]
        else:
            path_l, signal_l = sf.MaybeReadSignal("left_{0}".format(RESTART_INFO.restartIndex))
            path_r, signal_r = sf.MaybeReadSignal("right_{0}".format(RESTART_INFO.restartIndex))
            signals = None
            if not (signal_l and signal_r):
                signals = sing(*args)
                toWrite += [(signals, path_l, path_r)]
                if len(toWrite) > 4:
                    for sPair, path_l, path_r in toWrite:                            
                        sf.WriteSignal(sPair[0], path_l)
                        sf.WriteSignal(sPair[1], path_r)
                    toWrite = []
            else:
                print 'Restart Hit!   {0}'.format(RESTART_INFO.restartIndex)
                signals = (signal_l, signal_r)
            # Note that the get code below will compute the value for these futures as some point.
            NOTE_CACHE[args] = [writeSawppedCache(s) for s in signals]
            cacheMisses += 1
        RESTART_INFO.restartIndex += 1
        dl=30 * rl + 1000
        dr=38 * lr + 1000
        print "Appending Node {} of {}".format(index, len(midi))
        notes.append((signals,at+dl,at+dr))

        #pickle.dump(noteCache, cacheFileName)
    return notes

