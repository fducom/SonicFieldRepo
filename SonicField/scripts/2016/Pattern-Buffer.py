#########
# Setup #
#########

#sf.SetSampleRate(60000)

import os

from Filters import byquad_filter
from organ.Generators import clean_noise
from Parallel_Helpers import mix,realise
from organ.Algorithms import do_formant,excite,create_vibrato
from organ.Voices import celest_flute 
import random
import math
import Signal_Generators

def makeNote():
    pass

def randWalk(value,size,uBound):
    value  = float(value)
    size   = float(size)
    uBound = float(uBound)
    r=(random.random()+random.random())/2.0
    r=math.floor(r*size)-math.floor((size/2.0))    
    value+=r
    if value<1:
        value=2
    elif value>uBound:
        value=uBound-2
    return value

def randWalk3(value,uBound):
    return randWalk(value,3,uBound)

def brittle(length,freq):
    sig=sf.WhiteNoise(length)
    for i in xrange(0,2):
        sig=byquad_filter(
            'low',
            sig,
            1,
            1
        )
    sig=sf.Pcnt25(sf.FixSize(sf.Power(sig,1.0)))
    sig=sf.DirectMix(1.0,sig)
    sig=sf.Multiply(
        sf.SineWave(length,freq),
        sig
    )
    #sig=sf.SineWave(length,freq)
    sig=sf.FixSize(sig)
    sig=sf.Power(sig,10)
    sig=sf.Finalise(sig)
    return sig

def ring(length, pitch):
    print "Ring: " + str(pitch) + "/" + str(length)
    sig1 = sf.SineWave(length,pitch*1.2)
    sig2 = sf.SineWave(length,pitch*1.2 + 1)
    env  = sf.ExponentialShape((0,-60),(125,0),(length,-30))
    
    sig1 = sf.Multiply(+env,sig1)
    sig1 = sf.Pcnt90(sf.DirectMix(1,sig1))
    sig3 = sf.PhaseModulatedSineWave(pitch,sig1)
    sig3 = sf.Multiply(+env,sig3)

    sig2 = sf.Multiply(+env,sig2)
    sig2 = sf.Pcnt90(sf.DirectMix(1,sig2))
    sig4 = sf.PhaseModulatedSineWave(pitch,sig2)
    sig4 = sf.Multiply(env,sig4)
    
    sig5 = sf.ExponentialVolume(sf.Mix(sig3,sig4),6)
    sig=sf.Saturate(sig5)
    sig=sf.ResonantFilter(sig,0.99,0.05,1000.0/pitch)
    return sf.Realise(sf.Normalise(sig))

@sf_parallel
def generate(
        voice,
        pPitch,
        pitch,
        a,
        d,
        s,
        r,
        v
    ):
    sig = voice(r,pitch)

    env = sf.LinearShape(
        (0,pitch*8),
        (a,pitch*4),
        ((a+d)*0.5,pitch*8),
        (d,pitch*4),
        (s,pitch*2),
        (r,pitch)
    )

    res = sf.LinearShape(
        (0,0),
        (a,0.75),
        ((a+d)*0.5,1.0),
        (d,0.85),
        (s,0.4),
        (r,0)
    )
    
    sig = sf.ShapedLadderLowPass(sig,env,res)

    env = sf.LinearShape(
        (0,0.1),
        (a,0.25),
        ((a+d)*0.5,1.0),
        (d,0.4*random.random()+0.1),
        (s,0.1*random.random()+0.05),
        (r,0)
    )
    sig = sf.Multiply(sig,env)
    
    # must be longer than the max delay
    sig=sf.Concatenate(sig,sf.Silence(200))
    
    dhz = 2.0
    dly = 1000.0/float(dhz);
    mod = sf.SineWave(sf.Length(+sig),0.25)
    mod = sf.LinearVolume(mod,dly/10)
    sig = sf.AnalogueChorus(sig,dly,mod,0.80,1.0)
    sgs = [ sf.FixSize(s) for s in sig ]
    
    return [ sf.LinearVolume(sf.FixSize(sig),v) for sig in sgs ]

def run(
        voice,
        pitch,
        beat,
        minutes,
        maxDenom=8,
        maxNume=8,
        octaves=2,
        verbose=False,
        vOver=1.0,
        atIn=0.0
    ):
    print voice, pitch, beat, octaves, vOver, atIn
    notesL=[]
    notesR=[]
    oPitch=float(pitch)
    pitchScaleDenom = 3.0
    pitchScaleNume  = 3.0
    lengthScale     = 4.0
    volumeScale     = 4.0
    oVolume         = 4.0
    octaves        /= 2.0
    at=atIn
    pPitch=float(pitch)

    while at/60000 < minutes:
        pitchScale = pitchScaleNume/pitchScaleDenom
        rvs        = 1.0/volumeScale
        volume     = rvs*oVolume
        pitch      = pitchScale*oPitch
        length     = lengthScale*beat


        # Create a consistent envelope
        rlen       = length * 0.75 + random.random() * length
        a          = rlen * (0.10 + random.random() * 0.1) 
        d          = rlen * (0.30 + random.random() * 0.1)
        s          = rlen * (0.70 + random.random() * 0.1)
        r          = rlen
               
        velocity_correction = 1/pitchScale
        
        # Do not over correct very & v high low frequencies 
        # or very quiet notes. This aim it to stop loud highs
        # dominating (psycho-acoustics)
        if rvs<0.2:
            if velocity_correction<1:
                velocity_correction=1
        
        if velocity_correction>4:
            velocity_correction=4
                                  
            if verbose:
                print
                at,
                "PitchNume: ",  pitchScaleNume,
                "PitchDenom: ", pitchScaleDenom,
                "Volume: ",     volumeScale,
                "Pitch: ",      pitch,
                "Length: ",     length,
                "Env:",         (a,d,s,r),
                "Rvs: ",        rvs,
                "VCorr: ",      velocity_correction

        signals = generate(
            voice,
            pPitch,
            pitch,
            a,
            d,
            s,
            r,
            volume * velocity_correction
        )

        lr=random.random()
        rl=1.0-lr
    
        notesL.append((signals,lr,at+30*rl))
        notesR.append((signals,rl,at+30*lr))
        
        at+=length

        # Get a new pitch but within the allowed octave
        # range
        count = 1
        ratio = pitchScaleNume/pitchScaleDenom
        while True:
            pitchScaleDenom = randWalk3(pitchScaleDenom,maxDenom)
            pitchScaleNume  = randWalk3(pitchScaleNume,maxNume)
            t = pitchScaleNume/pitchScaleDenom
            if t == ratio:
                continue
            t = abs(math.log(t,2))
            if t <= octaves:
                break
            count += 1
            if count > 100:
                print 'Waringing, over iteration getting pitch'

        lengthScale = randWalk3(lengthScale,8)
        volumeScale = randWalk3(volumeScale,8)
        pPitch      = pitch

    @sf_parallel
    def post(notes,i):
        r = []
        for s,v,a in notes:
            r += [(sf.LinearVolume(s.get()[i],v),a*2.0)]
        return r
    
    return (
        sf.Finalise(sf.LinearVolume(sf.MixAt(post(notesL,0)),vOver)),
        sf.Finalise(sf.LinearVolume(sf.MixAt(post(notesR,1)),vOver))
    )

random.seed()
mins = 35.0
voce = [ring]*6
scnt = len(voce)
sped = 1024.0*4.0
sigs = [
    run(
        voce[x],
        32*pow(2,x),
        sped*(scnt-x),
        mins,
        vOver = 1.0/(x*4.0+1.0),
        atIn = x*sped+256
    )
    for x in range(0,scnt)
]

sigs = (
    sf.Finalise(sf.Mix([sig[0]  for sig in sigs])),
    sf.Finalise(sf.Mix([sig[1]  for sig in sigs]))
)

@sf_parallel
def spatialise(sig):
    dly = sped
    mod = Signal_Generators.LimitedTriangle(sf.Length(+sig),0.111,10)
    mod = sf.Finalise(mod)
    mod = sf.LinearVolume(mod,sped/10.0)
    sig = sf.AnalogueChorus(sig,dly,mod,0.65,0.8)
    return [ sf.FixSize(s) for s in sig ]

lr = spatialise(sigs[0])
rl = spatialise(sigs[1])
lr = lr.get()
rl = rl.get()
ll = sf.MixAt(
    (lr[0],0),
    (sf.Pcnt10(lr[1]),30)
)
rr = sf.MixAt(
    (rl[0],0),
    (sf.Pcnt10(rl[1]),30)
)
sigs = [
    sf.Finalise(
        sf.Multiply(
            sf.LinearShape(
                (0,0),
                (100,0),
                (125,1),
                (sf.Length(+sig),1)
            ),sig
        )
    ) for sig in (ll,rr)]
print sigs 
sf.WriteFile32(sigs,"temp/rand.wav")
