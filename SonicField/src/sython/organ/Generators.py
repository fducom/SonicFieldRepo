import random
from sython.utils.Parallel_Helpers import mix, realise
from sython.organ.Algorithms import pitch_move
from sython.utils.Algorithms import polish
from sython.concurrent import sf_parallel

@sf_parallel
def posaune_pulse(length,frequency):
    p1 =random.random()
    p2=1.0-p1
    if frequency>4000:
        raise "Too High for pasaune"
    elif frequency>1000:
        sig=mix(
            sf.PhasedSineWave(length,frequency,p1),
            sf.LinearVolume(sf.PhasedSineWave(length,frequency*2.0,p1),2.0),
            sf.LinearVolume(sf.PhasedSineWave(length,frequency*3.0,p1),2.0),
            sf.LinearVolume(sf.PhasedSineWave(length,frequency*4.0,p1),1.5),
            sf.LinearVolume(sf.PhasedSineWave(length,frequency*5.0,p1),1.3),
            sf.LinearVolume(sf.PhasedSineWave(length,frequency*6.0,p1),1.1),
            sf.LinearVolume(sf.PhasedSineWave(length,frequency*7.0,p1),0.8),
            sf.LinearVolume(sf.PhasedSineWave(length,frequency*8.0,p1),0.6),
            sf.LinearVolume(sf.PhasedSineWave(length,frequency*9.0,p1),0.4),
            sf.LinearVolume(sf.PhasedSineWave(length,frequency*10.0,p1),0.2)
        )
    else:
        sig=mix(
            sf.PhasedSineWave(length,frequency,p1),
            sf.LinearVolume(sf.PhasedSineWave(length,frequency*2.0,p1),2.0),
            sf.LinearVolume(sf.PhasedSineWave(length,frequency*3.0,p2),2.0),
            sf.LinearVolume(sf.PhasedSineWave(length,frequency*4.0,p1),1.8),
            sf.LinearVolume(sf.PhasedSineWave(length,frequency*5.0,p2),1.6),
            sf.LinearVolume(sf.PhasedSineWave(length,frequency*6.0,p1),1.4),
            sf.LinearVolume(sf.PhasedSineWave(length,frequency*7.0,p2),1.2),
            sf.LinearVolume(sf.PhasedSineWave(length,frequency*8.0,p1),1.0),
            sf.LinearVolume(sf.PhasedSineWave(length,frequency*9.0,p2),0.8),
            sf.LinearVolume(sf.PhasedSineWave(length,frequency*10.0,p1),0.6),
            sf.LinearVolume(sf.PhasedSineWave(length,frequency*11.0,p2),0.5),
            sf.LinearVolume(sf.PhasedSineWave(length,frequency*12.0,p1),0.4),
            sf.LinearVolume(sf.PhasedSineWave(length,frequency*13.0,p2),0.3),
            sf.LinearVolume(sf.PhasedSineWave(length,frequency*14.0,p1),0.2),
            sf.LinearVolume(sf.PhasedSineWave(length,frequency*15.0,p2),0.1),
            sf.LinearVolume(sf.PhasedSineWave(length,frequency*16.0,p1),0.05),
            sf.LinearVolume(sf.PhasedSineWave(length,frequency*16.0,p2),0.05),
            sf.LinearVolume(sf.PhasedSineWave(length,frequency*17.0,p1),0.05),
            sf.LinearVolume(sf.PhasedSineWave(length,frequency*18.0,p2),0.05),
            sf.LinearVolume(sf.PhasedSineWave(length,frequency*19.0,p1),0.01)
        )
    sig=sf.Multiply(
        sf.LinearShape((0,0),(32,1),(length,1)),
        sig
    )
    return sf.FixSize(sig)

@sf_parallel
def bombard_pulse(length,frequency):
    p =random.random()
    p2=1.0-p
    if frequency>4000:
        raise "Too high for bombard"
    else:
        sig=mix(
            sf.PhasedSineWave(length,frequency,p),
            sf.LinearVolume(sf.PhasedSineWave(length,frequency*2.0,p),2.0),
            sf.LinearVolume(sf.PhasedSineWave(length,frequency*3.0,p),1.5),
            sf.LinearVolume(sf.PhasedSineWave(length,frequency*4.0,p),1.3),
            sf.LinearVolume(sf.PhasedSineWave(length,frequency*5.0,p),1.2),
            sf.LinearVolume(sf.PhasedSineWave(length,frequency*6.0,p),1.0),
            sf.LinearVolume(sf.PhasedSineWave(length,frequency*7.0,p),0.8),
            sf.LinearVolume(sf.PhasedSineWave(length,frequency*8.0,p),0.6),
            sf.LinearVolume(sf.PhasedSineWave(length,frequency*9.0,p),0.4),
            sf.LinearVolume(sf.PhasedSineWave(length,frequency*10.0,p),0.2)
        )
    
    sig=sf.Multiply(
        sf.LinearShape((0,0),(32,1),(length,1)),
        sig
    )
    return sf.FixSize(sig)
    
@sf_parallel
def ophicleide_pulse(length,frequency):
    p=random.random()
    if frequency>4000:
        raise "Too high for ophicleide"        
    elif frequency>1000:
        sig=mix(
            sf.PhasedSineWave(length,frequency,p),
            sf.LinearVolume(sf.PhasedSineWave(length,frequency*2.0,p),1.5),
            sf.LinearVolume(sf.PhasedSineWave(length,frequency*3.0,p),2.0),
            sf.LinearVolume(sf.PhasedSineWave(length,frequency*4.0,p),2.0),
            sf.LinearVolume(sf.PhasedSineWave(length,frequency*5.0,p),1.5),
            sf.LinearVolume(sf.PhasedSineWave(length,frequency*6.0,p),1.0),
            sf.LinearVolume(sf.PhasedSineWave(length,frequency*7.0,p),0.9),
            sf.LinearVolume(sf.PhasedSineWave(length,frequency*8.0,p),0.8),
            sf.LinearVolume(sf.PhasedSineWave(length,frequency*9.0,p),0.6),
            sf.LinearVolume(sf.PhasedSineWave(length,frequency*10.0,p),0.4)
        )
    else:
        sig=mix(
            sf.PhasedSineWave(length,frequency,p),
            sf.LinearVolume(sf.PhasedSineWave(length,frequency*2.0,p),1.5),
            sf.LinearVolume(sf.PhasedSineWave(length,frequency*3.0,p),2.0),
            sf.LinearVolume(sf.PhasedSineWave(length,frequency*4.0,p),2.0),
            sf.LinearVolume(sf.PhasedSineWave(length,frequency*5.0,p),1.8),
            sf.LinearVolume(sf.PhasedSineWave(length,frequency*6.0,p),1.6),
            sf.LinearVolume(sf.PhasedSineWave(length,frequency*7.0,p),1.4),
            sf.LinearVolume(sf.PhasedSineWave(length,frequency*8.0,p),1.2),
            sf.LinearVolume(sf.PhasedSineWave(length,frequency*9.0,p),1.0),
            sf.LinearVolume(sf.PhasedSineWave(length,frequency*10.0,p),0.8),
            sf.LinearVolume(sf.PhasedSineWave(length,frequency*11.0,p),0.5),
            sf.LinearVolume(sf.PhasedSineWave(length,frequency*12.0,p),0.3),
            sf.LinearVolume(sf.PhasedSineWave(length,frequency*13.0,p),0.2),
            sf.LinearVolume(sf.PhasedSineWave(length,frequency*14.0,p),0.1)
       )   
    return sf.FixSize(sig)

@sf_parallel
def nice_pulse(length,frequency):
    p=random.random()
    if frequency>4000:
        sig=mix(
            sf.PhasedSineWave(length,frequency,p),
            sf.LinearVolume(sf.PhasedSineWave(length,frequency*2.0,p),1.0/1.5),
            sf.LinearVolume(sf.PhasedSineWave(length,frequency*3.0,p),1.0/1.0),
            sf.LinearVolume(sf.PhasedSineWave(length,frequency*4.0,p),1.0/1.0),
            sf.LinearVolume(sf.PhasedSineWave(length,frequency*5.0,p),1.0/1.5),
            sf.LinearVolume(sf.PhasedSineWave(length,frequency*6.0,p),1.0/2.0),
            sf.LinearVolume(sf.PhasedSineWave(length,frequency*7.0,p),1.0/3.0),
            sf.LinearVolume(sf.PhasedSineWave(length,frequency*8.0,p),1.0/4.0)
            )
    else:
        sig=mix(
            sf.PhasedSineWave(length,frequency,p),
            sf.LinearVolume(sf.PhasedSineWave(length,frequency*2.0,p),1.0/1.5),
            sf.LinearVolume(sf.PhasedSineWave(length,frequency*3.0,p),1.0/1.0),
            sf.LinearVolume(sf.PhasedSineWave(length,frequency*4.0,p),1.0/1.0),
            sf.LinearVolume(sf.PhasedSineWave(length,frequency*5.0,p),1.0/1.5),
            sf.LinearVolume(sf.PhasedSineWave(length,frequency*6.0,p),1.0/2.0),
            sf.LinearVolume(sf.PhasedSineWave(length,frequency*7.0,p),1.0/3.0),
            sf.LinearVolume(sf.PhasedSineWave(length,frequency*8.0,p),1.0/4.0),
            sf.LinearVolume(sf.PhasedSineWave(length,frequency*9.0,p),1.0/6.0),
            sf.LinearVolume(sf.PhasedSineWave(length,frequency*10.0,p),1.0/10.0)
        )
    return sf.FixSize(sig)

@sf_parallel
def make_simple_base(length,frequency,z):
    p=random.random()
    if frequency>4000:
        sig=mix(
            sf.PhasedSineWave(length,frequency,p),
            sf.LinearVolume(sf.PhasedSineWave(length,frequency*2.0,p),(1.0/2.0)**z),
            sf.LinearVolume(sf.PhasedSineWave(length,frequency*3.0,p),(1.0/3.0)**z),
            sf.LinearVolume(sf.PhasedSineWave(length,frequency*4.0,p),(1.0/4.0)**z),
            sf.LinearVolume(sf.PhasedSineWave(length,frequency*5.0,p),(1.0/5.0)**z),
            sf.LinearVolume(sf.PhasedSineWave(length,frequency*6.0,p),(1.0/6.0)**z),
            sf.LinearVolume(sf.PhasedSineWave(length,frequency*7.0,p),(1.0/7.0)**z),
            sf.LinearVolume(sf.PhasedSineWave(length,frequency*8.0,p),(1.0/8.0)**z)
            )
    else:
        sig=mix(
            sf.PhasedSineWave(length,frequency,p),
            sf.LinearVolume(sf.PhasedSineWave(length,frequency*2.0,p),(1.0/2.0)**z),
            sf.LinearVolume(sf.PhasedSineWave(length,frequency*3.0,p),(1.0/3.0)**z),
            sf.LinearVolume(sf.PhasedSineWave(length,frequency*4.0,p),(1.0/4.0)**z),
            sf.LinearVolume(sf.PhasedSineWave(length,frequency*5.0,p),(1.0/5.0)**z),
            sf.LinearVolume(sf.PhasedSineWave(length,frequency*6.0,p),(1.0/6.0)**z),
            sf.LinearVolume(sf.PhasedSineWave(length,frequency*7.0,p),(1.0/7.0)**z),
            sf.LinearVolume(sf.PhasedSineWave(length,frequency*8.0,p),(1.0/8.0)**z),
            sf.LinearVolume(sf.PhasedSineWave(length,frequency*9.0,p),(1.0/9.0)**z),
            sf.LinearVolume(sf.PhasedSineWave(length,frequency*10.0,p),(1.0/10.0)**z)
        )
    return sf.FixSize(sig)

@sf_parallel
def nice_saw(length,frequency):
    return make_simple_base(length,frequency,1.0)

@sf_parallel
def viola_base(length,frequency):
    return make_simple_base(length,frequency,0.5)

@sf_parallel
def sweet_flute_base(length,frequency):
    return make_simple_base(length,frequency,8.0)
    
@sf_parallel
def brightFluteBase(length,frequency):
    return make_simple_base(length,frequency,3.5)

@sf_parallel
def stopped_pulse(length,frequency):
    p=random.random()
    if frequency>3000:
        sig=mix(
            sf.PhasedSineWave(length,frequency,p),
            sf.LinearVolume(sf.PhasedSineWave(length,frequency*3.0,p),1.0/1.0),
            sf.LinearVolume(sf.PhasedSineWave(length,frequency*5.0,p),1.0/1.5),
            sf.LinearVolume(sf.PhasedSineWave(length,frequency*7.0,p),1.0/2.0)
            )
    else:
        sig=mix(
            sf.PhasedSineWave(length,frequency,p),
            sf.LinearVolume(sf.PhasedSineWave(length,frequency*3.0,p),1.0/1.0),
            sf.LinearVolume(sf.PhasedSineWave(length,frequency*5.0,p),1.0/1.5),
            sf.LinearVolume(sf.PhasedSineWave(length,frequency*7.0,p),1.0/2.0),
            sf.LinearVolume(sf.PhasedSineWave(length,frequency*9.0,p),1.0/4.0),
            sf.LinearVolume(sf.PhasedSineWave(length,frequency*11.0,p),1.0/8.0)
        )
    return sf.FixSize(sig)

@sf_parallel
def sing_base(length,freq,z=1.0):
    voxA=[]
    hc=1.0
    freq=float(freq)
    while hc*freq<18000:
        hf=hc*freq
        # at higher frequencies there is less need to
        # richen the sound so do only one pass of creating the 
        # waves, but double the volume of each one by two to 
        # avoid filtering effects
        if freq<5000:
            x=2
            y=1.0
        else:
            x=1
            y=2.0
        for c in range(0,x):
            vol = (1.0/hc)**z
            # cut of at -60 db 
            if vol>0.25e-06:
                vol*=y
                voxA.append(sf.LinearVolume(sf.PhasedTableSineWave(length,hf+random.random()*10.0,random.random()),vol))
                voxA.append(sf.LinearVolume(sf.PhasedTableSineWave(length,hf-random.random()*10.0,random.random()),vol))
                voxA.append(sf.LinearVolume(sf.PhasedTableSineWave(length,hf+random.random()*10.0,random.random()),vol))
                voxA.append(sf.LinearVolume(sf.PhasedTableSineWave(length,hf-random.random()*10.0,random.random()),vol))
        hc+=1

    vox=mix(voxA)       
    vox=sf.Clean(vox)
    vox=polish(sf.FixSize(vox),freq)
    return sf.FixSize(vox)

@sf_parallel
def trumpet_base(length,freq,z=1.0):
    voxA=[]
    hc=1.0
    freq=float(freq)
    while hc*freq<20000:
        hf=hc*freq
        voxA.append(sf.LinearVolume(sf.PhasedSineWave(length,hf,random.random()),(1.0/hc)**z))
        hc+=1
        
    vox=mix(voxA)
    vox=sf.Clean(vox)
    vox=polish(sf.FixSize(vox),freq)
    return sf.FixSize(vox)

@sf_parallel
def stretched_bass(length,freq,z=1.0,s=1.0,d=0.0,at=0):
    freq=float(freq)
    hf=freq
    hc=1.0
    if at==0:
        at=length*0.9
    vox=sf.Silence(length)
    while hf<20000:
        v=(1.0/hc)**z
        env=sf.LinearShape((0,v),(at,v-(d**hc-1.0)),(length,v-(d**hc-1.0)))
        vox=mix(
            sf.Multiply(
                sf.PhasedSineWave(length,hf,random.random()),
                env
            ),
            vox
        )
        hf+=freq*s
        hc+=1
        
    vox=sf.Clean(vox)
    vox=polish(sf.FixSize(vox),freq)
    return sf.FixSize(vox)
 
