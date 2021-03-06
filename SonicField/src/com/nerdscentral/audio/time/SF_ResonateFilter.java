/* For Copyright and License see LICENSE.txt and COPYING.txt in the root directory */
package com.nerdscentral.audio.time;

import java.util.List;

import com.nerdscentral.audio.core.SFConstants;
import com.nerdscentral.audio.core.SFSignal;
import com.nerdscentral.sython.Caster;
import com.nerdscentral.sython.SFPL_Operator;
import com.nerdscentral.sython.SFPL_RuntimeException;

public class SF_ResonateFilter implements SFPL_Operator
{

    private static final long serialVersionUID = 1L;

    @Override
    public String Word()
    {
        return Messages.getString("SF_ResonateFilter.0"); //$NON-NLS-1$
    }

    @Override
    public Object Interpret(Object input) throws SFPL_RuntimeException
    {
        List<Object> lin = Caster.makeBunch(input);
        SFSignal in = Caster.makeSFSignal(lin.get(0));
        double vResonant = Caster.makeDouble(lin.get(1));
        double vOriginal = Caster.makeDouble(lin.get(2));
        double delay = Caster.makeDouble(lin.get(3));
        SFSignal out = in.replicate();
        double r = in.getLength();
        int delaySamples = (int) (delay * SFConstants.SAMPLE_RATE_MS);
        for (int n = 0; n < delaySamples; ++n)
        {
            out.setSample(n, out.getSample(n) * vOriginal);
        }
        for (int n = 0; n < r; ++n)
        {
            double q = out.getSample(n);
            int index = n + delaySamples;
            if (index < r)
            {
                out.setSample(index, out.getSample(index) * vOriginal + q * vResonant);
            }
        }
        return out;
    }
}
