package com.nerdscentral.audio.pitch;

import com.nerdscentral.audio.core.SFData;
import com.nerdscentral.audio.core.SFSignal;
import com.nerdscentral.audio.pitch.algorithm.OnHeapFFTBase;
import com.nerdscentral.sython.Caster;
import com.nerdscentral.sython.SFPL_Operator;
import com.nerdscentral.sython.SFPL_RuntimeException;

public class SF_OnHeapFrequencyDomain implements SFPL_Operator
{
    /* THIS CLASS IS HERE FOR PERFORMANCE COMPARISON USE AND SHOULD NOT BE USED NORMALLY.
     * SEE SF_FrequencyDomain FOR THE OPTIMISED VERSION.
     */
    private static final long serialVersionUID = 1L;

    @Override
    public String Word()
    {
        return Messages.getString("SF_OnHeapFrequencyDomain.0");  //$NON-NLS-1$
    }

    @Override
    public Object Interpret(Object input) throws SFPL_RuntimeException
    {
        SFSignal signal = Caster.makeSFSignal(input);
        int Nx = signal.getLength();
        int NFFT = (int) Math.pow(2.0, Math.ceil(Math.log(Nx) / Math.log(2.0)));
        double[] out = new double[NFFT << 1];
        double[] re = new double[NFFT];
        double[] im = new double[NFFT];
        for (int i = 0; i < Nx; ++i)
        {
            re[i] = signal.getSample(i);
        }
        OnHeapFFTBase.fft(re, im, out, true);
        SFSignal ret = SFData.build(out, NFFT);
        return ret;
    }
}
