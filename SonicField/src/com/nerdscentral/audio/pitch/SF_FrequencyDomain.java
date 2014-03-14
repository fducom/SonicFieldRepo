package com.nerdscentral.audio.pitch;

import com.nerdscentral.audio.SFData;
import com.nerdscentral.audio.SFSignal;
import com.nerdscentral.audio.pitch.algorithm.FFTbase;
import com.nerdscentral.sython.Caster;
import com.nerdscentral.sython.SFPL_Context;
import com.nerdscentral.sython.SFPL_Operator;
import com.nerdscentral.sython.SFPL_RuntimeException;

public class SF_FrequencyDomain implements SFPL_Operator
{

    private static final long serialVersionUID = 1L;

    @Override
    public String Word()
    {
        return Messages.getString("SF_PhaseSpace.1"); //$NON-NLS-1$
    }

    @Override
    public Object Interpret(Object input, SFPL_Context context) throws SFPL_RuntimeException
    {
        double[] re = null;
        double[] im = null;
        int NFFT = 0;
        try (SFSignal signal = Caster.makeSFSignal(input))
        {

            int Nx = signal.getLength();
            NFFT = (int) Math.pow(2.0, Math.ceil(Math.log(Nx) / Math.log(2.0)));
            re = new double[NFFT];
            im = new double[NFFT];
            // Store x as real/complex setting complex to zero
            // Java pre-sets the rest to zero for us
            for (int i = 0; i < Nx; ++i)
            {
                re[i] = signal.getSample(i);
            }

        }

        double[] d = FFTbase.fft(re, im, true);

        try (SFData ret = SFData.build(d, NFFT))
        {
            return Caster.prep4Ret(ret);
        }
    }
}