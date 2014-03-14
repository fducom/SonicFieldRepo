/* For Copyright and License see LICENSE.txt and COPYING.txt in the root directory */
package com.nerdscentral.audio.combine;

import java.util.ArrayList;
import java.util.List;

import com.nerdscentral.audio.SFConstants;
import com.nerdscentral.audio.SFData;
import com.nerdscentral.audio.SFSignal;
import com.nerdscentral.sython.Caster;
import com.nerdscentral.sython.SFMaths;
import com.nerdscentral.sython.SFPL_Context;
import com.nerdscentral.sython.SFPL_Operator;
import com.nerdscentral.sython.SFPL_RuntimeException;

public class SF_Blockulate implements SFPL_Operator
{
    /**
     * 
     */
    private static final long serialVersionUID = 1L;

    @Override
    public Object Interpret(final Object input, final SFPL_Context context) throws SFPL_RuntimeException
    {
        List<Object> lin = Caster.makeBunch(input);
        try (SFSignal data = Caster.makeSFSignal(lin.get(0));)
        {
            int lenSamples = (int) (Caster.makeDouble(lin.get(1)) * SFConstants.SAMPLE_RATE_MS);
            int randSamples = lin.size() > 2 ? (int) (Caster.makeDouble(lin.get(2)) * SFConstants.SAMPLE_RATE_MS) : 0;
            lenSamples /= 2;
            List<Object> retOuter = new ArrayList<>();
            int len = data.getLength();
            int start = 0;
            while (true)
            {
                int rollOffSamplesOld = lenSamples;
                lenSamples += SFMaths.random() * randSamples;
                int k = lenSamples * 2;
                int end = start + k;
                if (end > len) break;
                try (SFSignal out = SFData.build(k);)
                {
                    Caster.prep4Ret(out);
                    for (int i = start; i < end; ++i)
                    {
                        int l = i - start;
                        out.setSample(l, data.getSample(i));
                    }
                    // add to retout,
                    List<Object> thisRet = new ArrayList<>(2);
                    thisRet.add(out);
                    thisRet.add(start / SFConstants.SAMPLE_RATE_MS);
                    retOuter.add(thisRet);
                    // move on by rolloutsamples
                    start += lenSamples;
                    lenSamples = rollOffSamplesOld;
                }
            }
            return retOuter;
        }
    }

    @Override
    public String Word()
    {
        return Messages.getString("SF_Blockulate.0"); //$NON-NLS-1$
    }

}